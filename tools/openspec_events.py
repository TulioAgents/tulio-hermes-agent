#!/usr/bin/env python3
"""
OpenSpec Event Bus

A singleton in-process pub/sub bus that:
1. Accepts structured AgentEvent objects from agents and integration hooks
2. Writes them to the SQLite openspec_events table (via SessionDB)
3. Pushes them asynchronously to all registered WebSocket subscribers

This bus is the bridge between:
- Hermes agent callbacks (tool_start_callback, gateway hooks, delegate_tool)
- The SQLite persistent event log
- The real-time WebSocket endpoint at /ws/events

Usage (from agent tools):
    from tools.openspec_events import get_event_bus
    bus = get_event_bus()
    bus.emit_sync(AgentEvent.create(...))

Usage (from async gateway code):
    bus = get_event_bus()
    await bus.emit(event)

Usage (WebSocket handler):
    bus = get_event_bus()
    queue = asyncio.Queue()
    bus.subscribe(queue)
    try:
        while True:
            event = await queue.get()
            await ws.send_json(event.to_wire())
    finally:
        bus.unsubscribe(queue)
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# Module-level singleton
_bus_instance: Optional["OpenSpecEventBus"] = None
_bus_lock = threading.Lock()


def get_event_bus() -> "OpenSpecEventBus":
    """Return the process-global OpenSpecEventBus instance (lazy init)."""
    global _bus_instance
    if _bus_instance is None:
        with _bus_lock:
            if _bus_instance is None:
                _bus_instance = OpenSpecEventBus()
    return _bus_instance


def set_event_bus(bus: "OpenSpecEventBus") -> None:
    """Replace the global bus (for testing)."""
    global _bus_instance
    with _bus_lock:
        _bus_instance = bus


class OpenSpecEventBus:
    """
    Process-global event bus for OpenSpec workflow observability.

    Thread-safe: emit_sync() can be called from any thread.
    Async-safe: emit() is an async method for gateway/aiohttp code.

    Subscribers are asyncio.Queue instances -- WebSocket handlers pull from
    their own queue. This decouples the bus from specific WebSocket frameworks.
    """

    def __init__(self, db: Any = None):
        """
        Args:
            db: Optional SessionDB instance. If None, the bus will attempt
                lazy import when the first event is emitted. Pass explicitly
                in tests to use an in-memory database.
        """
        self._db = db
        self._subscribers: List[asyncio.Queue] = []
        self._lock = threading.Lock()
        # Optional asyncio event loop for thread-safe cross-thread emit
        self._loop: Optional[asyncio.AbstractEventLoop] = None

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        """Register the gateway's asyncio event loop for thread-safe emit."""
        self._loop = loop

    def subscribe(self, queue: asyncio.Queue) -> None:
        """Register an asyncio.Queue to receive all future events."""
        with self._lock:
            if queue not in self._subscribers:
                self._subscribers.append(queue)

    def unsubscribe(self, queue: asyncio.Queue) -> None:
        """Remove a queue from the subscriber list."""
        with self._lock:
            try:
                self._subscribers.remove(queue)
            except ValueError:
                pass

    def subscribe_project(self, queue: asyncio.Queue, project_code: str, change_id: Optional[str] = None) -> None:
        """
        Filtered subscription -- queue only receives events matching
        project_code (and optionally change_id).

        Implemented by wrapping the queue in a FilteredQueue adapter.
        """
        adapter = _FilteredQueue(queue, project_code=project_code, change_id=change_id)
        self.subscribe(adapter)

    def _get_db(self):
        """Lazy-import SessionDB to avoid circular imports."""
        if self._db is None:
            try:
                from hermes_state import SessionDB
                self._db = SessionDB()
            except Exception as exc:
                logger.warning("OpenSpecEventBus: could not open SessionDB: %s", exc)
        return self._db

    def _persist(self, event) -> None:
        """Write event to SQLite. Swallows errors to never block callers."""
        try:
            db = self._get_db()
            if db is None:
                return
            if hasattr(db, "openspec_add_event"):
                db.openspec_add_event(event)
        except Exception as exc:
            logger.debug("OpenSpecEventBus: persist failed: %s", exc)

    def _broadcast(self, event) -> None:
        """Push event to all subscriber queues (non-blocking)."""
        wire = event.to_wire()
        with self._lock:
            subscribers = list(self._subscribers)
        for q in subscribers:
            try:
                q.put_nowait(wire)
            except asyncio.QueueFull:
                logger.debug("OpenSpecEventBus: subscriber queue full, dropping event")
            except Exception as exc:
                logger.debug("OpenSpecEventBus: broadcast to subscriber failed: %s", exc)

    def emit_sync(self, event) -> None:
        """
        Synchronous emit -- safe to call from any thread, including non-async
        agent tool handlers.

        Persists to SQLite immediately. Schedules the broadcast on the
        registered asyncio loop if available; otherwise does a direct
        put_nowait for each subscriber (works for non-async contexts).
        """
        self._persist(event)

        if self._loop is not None and self._loop.is_running():
            # Thread-safe schedule on the gateway event loop
            self._loop.call_soon_threadsafe(self._broadcast, event)
        else:
            # No event loop -- do a direct put (works in CLI / tests)
            self._broadcast(event)

    async def emit(self, event) -> None:
        """
        Async emit -- for use in gateway/aiohttp coroutines.
        Persist is done in a thread executor to avoid blocking the event loop.
        """
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._persist, event)
        self._broadcast(event)

    def emit_from_hook(self, event_type: str, context: Dict[str, Any]) -> None:
        """
        Convenience method for gateway hooks integration.

        Converts a gateway hook context dict into an AgentEvent and emits it.
        Called from gateway/hooks.py for agent:start, agent:step, agent:end.
        """
        from tools.openspec_state import AgentEvent

        project_code = context.get("openspec_project_code", "")
        change_id = context.get("openspec_change_id", "")
        agent_id = context.get("openspec_agent_id", "")

        # Only emit if the session has been registered with OpenSpec
        if not (project_code and agent_id):
            return

        payload = {k: v for k, v in context.items()
                   if k not in ("openspec_project_code", "openspec_change_id", "openspec_agent_id")
                   and isinstance(v, (str, int, float, bool, type(None)))}

        event = AgentEvent.create(
            project_code=project_code,
            change_id=change_id,
            agent_id=agent_id,
            event_type=event_type,
            payload=payload,
        )
        self.emit_sync(event)


class _FilteredQueue:
    """
    Wraps an asyncio.Queue and only forwards events matching a filter.
    Quacks like asyncio.Queue for the bus's put_nowait interface.
    """

    def __init__(self, queue: asyncio.Queue, project_code: str, change_id: Optional[str] = None):
        self._queue = queue
        self._project_code = project_code
        self._change_id = change_id

    def put_nowait(self, item: Dict[str, Any]) -> None:
        data = item.get("data", {})
        if data.get("project_code") != self._project_code:
            return
        if self._change_id and data.get("change_id") != self._change_id:
            return
        self._queue.put_nowait(item)
