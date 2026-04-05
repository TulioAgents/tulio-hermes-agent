#!/usr/bin/env python3
"""
OpenSpec Tool

Agent-callable tools for the OpenSpec multi-agent workflow system.
Role agents use these tools to:
- Register themselves in the tracking system on bootstrap
- Update kanban task status as work progresses
- Create new tasks (orchestrator only)
- Emit structured events for dashboard visibility
- Query current change status and active agents

All state is persisted to SQLite (openspec_agents, openspec_tasks,
openspec_events tables) and broadcast in real-time via the event bus
WebSocket endpoint.

Available tools (all registered in the "openspec" toolset):
- openspec_register_agent   : self-register on bootstrap, receive agent_id
- openspec_update_task      : update a task's kanban status
- openspec_create_task      : create a new kanban task (orchestrator use)
- openspec_emit_event       : emit a custom structured event
- openspec_get_change_status: query current state of a change
- openspec_list_active_agents: list running agents (all or per project)
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


# ── Availability check ─────────────────────────────────────────────────────────

def check_openspec_requirements() -> bool:
    """OpenSpec tools are always available."""
    return True


# ── Tool implementations ───────────────────────────────────────────────────────

def openspec_register_agent(
    project_code: str,
    change_id: str,
    role: str,
    session_id: Optional[str] = None,
    parent_agent_id: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Register this agent in the OpenSpec tracking system.

    Call this at the start of every role skill (immediately after bootstrap).
    Returns the assigned agent_id which should be used in subsequent tool calls.
    """
    try:
        from tools.openspec_state import AgentRecord, AgentEvent
        from tools.openspec_events import get_event_bus

        record = AgentRecord.create(
            session_id=session_id or kwargs.get("task_id", "unknown"),
            project_code=project_code,
            change_id=change_id,
            role=role,
            parent_agent_id=parent_agent_id,
        )

        db = _get_db()
        if db:
            db.openspec_upsert_agent(record)

        event = AgentEvent.create(
            project_code=project_code,
            change_id=change_id,
            agent_id=record.agent_id,
            event_type="agent_registered",
            payload={"role": role, "session_id": record.session_id},
        )
        get_event_bus().emit_sync(event)

        return json.dumps({
            "agent_id": record.agent_id,
            "project_code": project_code,
            "change_id": change_id,
            "role": role,
            "status": "registered",
        })

    except Exception as exc:
        logger.error("openspec_register_agent failed: %s", exc)
        return json.dumps({"error": str(exc)})


def openspec_update_task(
    task_id: str,
    status: str,
    agent_id: Optional[str] = None,
    summary: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Update the status of a kanban task.

    Valid statuses: pending, in_progress, completed, blocked, failed
    """
    from tools.openspec_state import VALID_TASK_STATUSES, AgentEvent, _now_iso
    from tools.openspec_events import get_event_bus

    if status not in VALID_TASK_STATUSES:
        return json.dumps({"error": f"Invalid status '{status}'. Valid: {VALID_TASK_STATUSES}"})

    try:
        db = _get_db()
        if db:
            db.openspec_update_task_status(
                task_id=task_id,
                status=status,
                agent_id=agent_id,
                summary=summary,
            )

        # Fetch task for event context
        task = db.openspec_get_task(task_id) if db else None
        project_code = task.project_code if task else ""
        change_id = task.change_id if task else ""
        aid = agent_id or "unknown"

        event = AgentEvent.create(
            project_code=project_code,
            change_id=change_id,
            agent_id=aid,
            event_type="task_updated",
            payload={"task_id": task_id, "status": status, "summary": summary},
        )
        get_event_bus().emit_sync(event)

        return json.dumps({"task_id": task_id, "status": status, "updated": True})

    except Exception as exc:
        logger.error("openspec_update_task failed: %s", exc)
        return json.dumps({"error": str(exc)})


def openspec_create_task(
    project_code: str,
    change_id: str,
    phase: str,
    title: str,
    description: str,
    assigned_role: str,
    agent_id: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Create a new kanban task for a given phase.

    Typically called by the orchestrator at each phase transition.
    Returns the new task_id.
    """
    from tools.openspec_state import TaskRecord, AgentEvent, VALID_PHASES
    from tools.openspec_events import get_event_bus

    if phase not in VALID_PHASES:
        return json.dumps({"error": f"Invalid phase '{phase}'. Valid: {VALID_PHASES}"})

    try:
        task = TaskRecord.create(
            project_code=project_code,
            change_id=change_id,
            phase=phase,
            title=title,
            description=description,
            assigned_role=assigned_role,
        )

        db = _get_db()
        if db:
            db.openspec_insert_task(task)

        aid = agent_id or "unknown"
        event = AgentEvent.create(
            project_code=project_code,
            change_id=change_id,
            agent_id=aid,
            event_type="task_created",
            payload={"task_id": task.task_id, "phase": phase, "title": title, "assigned_role": assigned_role},
        )
        get_event_bus().emit_sync(event)

        return json.dumps({
            "task_id": task.task_id,
            "phase": phase,
            "title": title,
            "assigned_role": assigned_role,
            "status": "pending",
        })

    except Exception as exc:
        logger.error("openspec_create_task failed: %s", exc)
        return json.dumps({"error": str(exc)})


def openspec_emit_event(
    project_code: str,
    change_id: str,
    agent_id: str,
    event_type: str,
    payload: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> str:
    """
    Emit a custom structured event for dashboard visibility.

    Use this to mark significant milestones:
    - artifact_written  : proposal.md, design.md, etc. created
    - decision_recorded : architecture decision added to decision-log
    - mistake_recorded  : mistake added to mistake-log
    - lesson_proposed   : lesson proposed for lessons-learned
    - handoff_written   : handoff.md updated for next role
    - phase_started     : role has begun work on a phase
    - phase_completed   : role has finished and written artifacts
    - phase_blocked     : role detected a blocker
    """
    from tools.openspec_state import AgentEvent, VALID_EVENT_TYPES
    from tools.openspec_events import get_event_bus

    if event_type not in VALID_EVENT_TYPES:
        return json.dumps({
            "error": f"Invalid event_type '{event_type}'. Valid: {VALID_EVENT_TYPES}"
        })

    try:
        event = AgentEvent.create(
            project_code=project_code,
            change_id=change_id,
            agent_id=agent_id,
            event_type=event_type,
            payload=payload or {},
        )
        get_event_bus().emit_sync(event)

        return json.dumps({
            "event_id": event.event_id,
            "event_type": event_type,
            "emitted": True,
        })

    except Exception as exc:
        logger.error("openspec_emit_event failed: %s", exc)
        return json.dumps({"error": str(exc)})


def openspec_get_change_status(
    project_code: str,
    change_id: str,
    **kwargs,
) -> str:
    """
    Query the current state of a change: active agents, task statuses, recent events.

    Used by the orchestrator and heartbeat to determine current phase and next action.
    """
    try:
        db = _get_db()
        if not db:
            return json.dumps({"error": "State database not available"})

        agents = db.openspec_list_agents(project_code=project_code, change_id=change_id)
        tasks = db.openspec_list_tasks(project_code=project_code, change_id=change_id)
        events = db.openspec_list_events(
            project_code=project_code, change_id=change_id, limit=20
        )

        # Summarize task statuses by phase
        phase_status: Dict[str, str] = {}
        for t in tasks:
            phase_status[t.phase] = t.status

        # Find running agents
        running = [a for a in agents if a.status == "running"]
        completed = [a for a in agents if a.status == "completed"]

        return json.dumps({
            "project_code": project_code,
            "change_id": change_id,
            "phase_status": phase_status,
            "running_agents": [
                {"agent_id": a.agent_id, "role": a.role, "started_at": a.started_at}
                for a in running
            ],
            "completed_agents": len(completed),
            "total_tasks": len(tasks),
            "recent_events": [
                {"timestamp": e.timestamp, "event_type": e.event_type, "agent_id": e.agent_id}
                for e in events[:10]
            ],
        })

    except Exception as exc:
        logger.error("openspec_get_change_status failed: %s", exc)
        return json.dumps({"error": str(exc)})


def openspec_list_active_agents(
    project_code: Optional[str] = None,
    **kwargs,
) -> str:
    """
    List currently running agents, optionally filtered by project.

    Used by the team-manager and heartbeat to see who is doing what.
    """
    try:
        db = _get_db()
        if not db:
            return json.dumps({"error": "State database not available"})

        agents = db.openspec_list_agents(project_code=project_code, status="running")

        return json.dumps({
            "active_agents": [
                {
                    "agent_id": a.agent_id,
                    "project_code": a.project_code,
                    "change_id": a.change_id,
                    "role": a.role,
                    "started_at": a.started_at,
                    "parent_agent_id": a.parent_agent_id,
                }
                for a in agents
            ],
            "count": len(agents),
        })

    except Exception as exc:
        logger.error("openspec_list_active_agents failed: %s", exc)
        return json.dumps({"error": str(exc)})


# ── Helpers ────────────────────────────────────────────────────────────────────

_cached_db = None

def _get_db():
    global _cached_db
    if _cached_db is None:
        try:
            from hermes_state import SessionDB
            _cached_db = SessionDB()
        except Exception as exc:
            logger.warning("openspec_tool: could not open SessionDB: %s", exc)
    return _cached_db


# ── Tool registration ──────────────────────────────────────────────────────────

from tools.registry import registry

registry.register(
    name="openspec_register_agent",
    toolset="openspec",
    schema={
        "name": "openspec_register_agent",
        "description": (
            "Register this agent in the OpenSpec tracking system. "
            "Call this at the start of every role skill after bootstrap. "
            "Returns the agent_id to use in subsequent openspec tool calls."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "project_code": {
                    "type": "string",
                    "description": "Project code from project-map.yaml (e.g. 'myproject')",
                },
                "change_id": {
                    "type": "string",
                    "description": "Change identifier (e.g. 'feature-auth', 'fix-login-bug')",
                },
                "role": {
                    "type": "string",
                    "description": "Agent role: orchestrator, team-manager, product-owner, tech-lead, fullstack-developer, qa-engineer, release-manager, heartbeat",
                },
                "parent_agent_id": {
                    "type": "string",
                    "description": "agent_id of the orchestrator that spawned this agent (omit if this is the orchestrator)",
                },
            },
            "required": ["project_code", "change_id", "role"],
        },
    },
    handler=lambda args, **kw: openspec_register_agent(
        project_code=args["project_code"],
        change_id=args["change_id"],
        role=args["role"],
        session_id=kw.get("task_id"),
        parent_agent_id=args.get("parent_agent_id"),
    ),
    check_fn=check_openspec_requirements,
    emoji="🏷️",
)

registry.register(
    name="openspec_update_task",
    toolset="openspec",
    schema={
        "name": "openspec_update_task",
        "description": "Update the status of a kanban task as work progresses.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "Task ID returned by openspec_create_task",
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "completed", "blocked", "failed"],
                    "description": "New task status",
                },
                "agent_id": {
                    "type": "string",
                    "description": "Your agent_id (from openspec_register_agent)",
                },
                "summary": {
                    "type": "string",
                    "description": "Brief description of what was done (shown in dashboard)",
                },
            },
            "required": ["task_id", "status"],
        },
    },
    handler=lambda args, **kw: openspec_update_task(
        task_id=args["task_id"],
        status=args["status"],
        agent_id=args.get("agent_id"),
        summary=args.get("summary"),
    ),
    check_fn=check_openspec_requirements,
    emoji="📋",
)

registry.register(
    name="openspec_create_task",
    toolset="openspec",
    schema={
        "name": "openspec_create_task",
        "description": (
            "Create a new kanban task for a workflow phase. "
            "Typically called by the orchestrator at each phase transition."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "project_code": {"type": "string"},
                "change_id": {"type": "string"},
                "phase": {
                    "type": "string",
                    "enum": ["idea", "proposal", "plan", "design", "implementation", "verification", "release", "done", "blocked"],
                },
                "title": {"type": "string", "description": "Short task title for kanban card"},
                "description": {"type": "string", "description": "Full task description"},
                "assigned_role": {
                    "type": "string",
                    "description": "Role responsible for this task",
                },
                "agent_id": {
                    "type": "string",
                    "description": "Orchestrator agent_id creating this task",
                },
            },
            "required": ["project_code", "change_id", "phase", "title", "description", "assigned_role"],
        },
    },
    handler=lambda args, **kw: openspec_create_task(
        project_code=args["project_code"],
        change_id=args["change_id"],
        phase=args["phase"],
        title=args["title"],
        description=args["description"],
        assigned_role=args["assigned_role"],
        agent_id=args.get("agent_id"),
    ),
    check_fn=check_openspec_requirements,
    emoji="➕",
)

registry.register(
    name="openspec_emit_event",
    toolset="openspec",
    schema={
        "name": "openspec_emit_event",
        "description": (
            "Emit a structured event for dashboard visibility. "
            "Use to mark milestones: artifact_written, decision_recorded, "
            "mistake_recorded, lesson_proposed, handoff_written, "
            "phase_started, phase_completed, phase_blocked."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "project_code": {"type": "string"},
                "change_id": {"type": "string"},
                "agent_id": {"type": "string", "description": "Your agent_id"},
                "event_type": {
                    "type": "string",
                    "enum": [
                        "agent_registered", "agent_completed", "agent_failed",
                        "phase_started", "phase_completed", "phase_blocked",
                        "task_created", "task_updated",
                        "tool_call", "artifact_written", "decision_recorded",
                        "mistake_recorded", "lesson_proposed", "handoff_written",
                        "heartbeat_ok", "heartbeat_alert", "error", "status_change",
                    ],
                },
                "payload": {
                    "type": "object",
                    "description": "Event-specific data (file path, decision summary, etc.)",
                },
            },
            "required": ["project_code", "change_id", "agent_id", "event_type"],
        },
    },
    handler=lambda args, **kw: openspec_emit_event(
        project_code=args["project_code"],
        change_id=args["change_id"],
        agent_id=args["agent_id"],
        event_type=args["event_type"],
        payload=args.get("payload"),
    ),
    check_fn=check_openspec_requirements,
    emoji="📡",
)

registry.register(
    name="openspec_get_change_status",
    toolset="openspec",
    schema={
        "name": "openspec_get_change_status",
        "description": (
            "Query the current state of a change: active agents, task statuses, "
            "recent events. Used by orchestrator and heartbeat."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "project_code": {"type": "string"},
                "change_id": {"type": "string"},
            },
            "required": ["project_code", "change_id"],
        },
    },
    handler=lambda args, **kw: openspec_get_change_status(
        project_code=args["project_code"],
        change_id=args["change_id"],
    ),
    check_fn=check_openspec_requirements,
    emoji="🔍",
)

registry.register(
    name="openspec_list_active_agents",
    toolset="openspec",
    schema={
        "name": "openspec_list_active_agents",
        "description": "List currently running agents, optionally filtered by project.",
        "parameters": {
            "type": "object",
            "properties": {
                "project_code": {
                    "type": "string",
                    "description": "Filter by project code (omit for all projects)",
                },
            },
            "required": [],
        },
    },
    handler=lambda args, **kw: openspec_list_active_agents(
        project_code=args.get("project_code"),
    ),
    check_fn=check_openspec_requirements,
    emoji="👥",
)
