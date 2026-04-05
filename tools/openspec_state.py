#!/usr/bin/env python3
"""
OpenSpec State Models

Data models for the OpenSpec multi-agent workflow:
- AgentRecord  : role agents and orchestrators (kanban swimlane actors)
- TaskRecord   : kanban cards -- one per workflow phase per change
- AgentEvent   : append-only structured event log for dashboard streaming

All records are stored in three new tables added to the existing
~/.hermes/state.db SQLite database (see hermes_state.py schema additions).
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


# ── Constants ──────────────────────────────────────────────────────────────────

VALID_PHASES = (
    "idea", "proposal", "plan", "design",
    "implementation", "verification", "release", "done", "blocked",
)

VALID_AGENT_STATUSES = ("running", "completed", "failed", "blocked")

VALID_TASK_STATUSES = ("pending", "in_progress", "completed", "blocked", "failed")

VALID_ROLES = (
    "orchestrator",
    "team-manager",
    "product-owner",
    "tech-lead",
    "fullstack-developer",
    "qa-engineer",
    "release-manager",
    "heartbeat",
)

# Structured event types emitted by agents and the event bus integration
VALID_EVENT_TYPES = (
    "agent_registered",
    "agent_completed",
    "agent_failed",
    "phase_started",
    "phase_completed",
    "phase_blocked",
    "task_created",
    "task_updated",
    "tool_call",
    "artifact_written",
    "decision_recorded",
    "mistake_recorded",
    "lesson_proposed",
    "handoff_written",
    "heartbeat_ok",
    "heartbeat_alert",
    "error",
    "status_change",
)


def _now_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    import datetime
    return datetime.datetime.utcnow().isoformat() + "Z"


def _new_id(prefix: str = "") -> str:
    return (prefix + uuid.uuid4().hex[:12]) if prefix else uuid.uuid4().hex[:12]


# ── Data Models ────────────────────────────────────────────────────────────────

@dataclass
class AgentRecord:
    """
    Represents a running or completed Hermes agent in the OpenSpec workflow.

    One record per agent invocation -- orchestrators, role agents, and
    heartbeat agents each get their own record with a stable agent_id.
    """
    agent_id: str
    session_id: str                  # links to hermes_state.sessions.id
    project_code: str
    change_id: str
    role: str                        # one of VALID_ROLES
    status: str                      # one of VALID_AGENT_STATUSES
    started_at: str                  # ISO 8601
    ended_at: Optional[str] = None
    parent_agent_id: Optional[str] = None   # orchestrator that spawned this
    summary: Optional[str] = None           # final output summary

    @classmethod
    def create(
        cls,
        session_id: str,
        project_code: str,
        change_id: str,
        role: str,
        parent_agent_id: Optional[str] = None,
    ) -> "AgentRecord":
        return cls(
            agent_id=_new_id("ag-"),
            session_id=session_id,
            project_code=project_code,
            change_id=change_id,
            role=role,
            status="running",
            started_at=_now_iso(),
            parent_agent_id=parent_agent_id,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_row(cls, row) -> "AgentRecord":
        return cls(**{k: row[k] for k in row.keys()})


@dataclass
class TaskRecord:
    """
    A kanban card representing one unit of work within a change.

    The orchestrator creates one TaskRecord per phase it dispatches.
    Role agents update the status as they progress.
    """
    task_id: str
    project_code: str
    change_id: str
    phase: str                       # one of VALID_PHASES
    title: str
    description: str
    assigned_role: str
    status: str                      # one of VALID_TASK_STATUSES
    created_at: str
    updated_at: str
    assigned_agent_id: Optional[str] = None
    completed_at: Optional[str] = None

    @classmethod
    def create(
        cls,
        project_code: str,
        change_id: str,
        phase: str,
        title: str,
        description: str,
        assigned_role: str,
    ) -> "TaskRecord":
        now = _now_iso()
        return cls(
            task_id=_new_id("tk-"),
            project_code=project_code,
            change_id=change_id,
            phase=phase,
            title=title,
            description=description,
            assigned_role=assigned_role,
            status="pending",
            created_at=now,
            updated_at=now,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_row(cls, row) -> "TaskRecord":
        return cls(**{k: row[k] for k in row.keys()})


@dataclass
class AgentEvent:
    """
    A single structured event emitted by an agent or the event bus integration.

    This is the append-only audit trail that feeds both the SQLite event log
    and the real-time WebSocket broadcast to dashboard clients.
    """
    event_id: str
    timestamp: str                   # ISO 8601
    project_code: str
    change_id: str
    agent_id: str
    event_type: str                  # one of VALID_EVENT_TYPES
    payload: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        project_code: str,
        change_id: str,
        agent_id: str,
        event_type: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> "AgentEvent":
        return cls(
            event_id=_new_id("ev-"),
            timestamp=_now_iso(),
            project_code=project_code,
            change_id=change_id,
            agent_id=agent_id,
            event_type=event_type,
            payload=payload or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Ensure payload is a JSON string for SQLite storage
        return d

    def to_wire(self) -> Dict[str, Any]:
        """WebSocket-ready representation."""
        d = self.to_dict()
        # payload is already a dict here -- serialize for JSON transport
        return {"type": "event", "data": d}

    @classmethod
    def from_row(cls, row) -> "AgentEvent":
        data = {k: row[k] for k in row.keys()}
        if isinstance(data.get("payload"), str):
            try:
                data["payload"] = json.loads(data["payload"])
            except (json.JSONDecodeError, TypeError):
                data["payload"] = {}
        return cls(**data)


# ── OpenSpec SQLite Schema Extension ──────────────────────────────────────────
#
# These SQL statements are appended to hermes_state.py's SCHEMA_SQL during
# SessionDB._init_schema().  They use CREATE TABLE IF NOT EXISTS so they're
# safe to run on an existing database.

OPENSPEC_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS openspec_agents (
    agent_id        TEXT PRIMARY KEY,
    session_id      TEXT NOT NULL,
    project_code    TEXT NOT NULL,
    change_id       TEXT NOT NULL,
    role            TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'running',
    started_at      TEXT NOT NULL,
    ended_at        TEXT,
    parent_agent_id TEXT,
    summary         TEXT
);

CREATE TABLE IF NOT EXISTS openspec_tasks (
    task_id             TEXT PRIMARY KEY,
    project_code        TEXT NOT NULL,
    change_id           TEXT NOT NULL,
    phase               TEXT NOT NULL,
    title               TEXT NOT NULL,
    description         TEXT,
    assigned_role       TEXT NOT NULL,
    assigned_agent_id   TEXT,
    status              TEXT NOT NULL DEFAULT 'pending',
    created_at          TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    completed_at        TEXT
);

CREATE TABLE IF NOT EXISTS openspec_events (
    event_id        TEXT PRIMARY KEY,
    timestamp       TEXT NOT NULL,
    project_code    TEXT NOT NULL,
    change_id       TEXT NOT NULL,
    agent_id        TEXT NOT NULL,
    event_type      TEXT NOT NULL,
    payload         TEXT NOT NULL DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_os_agents_project  ON openspec_agents(project_code, change_id);
CREATE INDEX IF NOT EXISTS idx_os_agents_status   ON openspec_agents(status);
CREATE INDEX IF NOT EXISTS idx_os_tasks_project   ON openspec_tasks(project_code, change_id);
CREATE INDEX IF NOT EXISTS idx_os_tasks_status    ON openspec_tasks(status);
CREATE INDEX IF NOT EXISTS idx_os_events_project  ON openspec_events(project_code, change_id);
CREATE INDEX IF NOT EXISTS idx_os_events_agent    ON openspec_events(agent_id);
CREATE INDEX IF NOT EXISTS idx_os_events_time     ON openspec_events(timestamp DESC);
"""
