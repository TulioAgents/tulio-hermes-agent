# custom-tulio Branch Customizations

Documents all changes on the `custom-tulio` branch relative to `main`.

## Commits

| SHA | Summary |
|-----|---------|
| `967b5391` | Add Local Dev Runbook + root Makefile |
| `0243292d` | Add OpenSpec team-manager & tech-lead roles, event bus, state models |

---

## New Files (40 files, ~3,823 lines)

### Developer Experience

| File | Purpose |
|------|---------|
| `Makefile` | Root Makefile with `setup`, `run`, `test`, `doctor`, `clean`, `bootstrap-user-config`, `chat` targets |
| `LOCAL_DEV_RUN.md` | Full local development runbook (prereqs, Make targets, config paths, troubleshooting) |
| `docs/plans/2026-04-02-local-makefile-design.md` | Design doc for the Makefile approach |
| `.webui_secret_key` | Local secret key file (verify this is not committed to shared environments) |

### OpenSpec Core Infrastructure

| File | Lines | Purpose |
|------|-------|---------|
| `tools/openspec_tool.py` | 585 | Tool implementations: `openspec_register_agent`, `openspec_update_task`, `openspec_create_task`, `openspec_emit_event`, `openspec_get_change_status`, `openspec_list_active_agents` |
| `tools/openspec_state.py` | 289 | Data models: `AgentRecord`, `TaskRecord`, `AgentEvent` |
| `tools/openspec_events.py` | 229 | In-process pub/sub event bus with project/change-filtered subscriptions |
| `tools/delegate_tool.py` | 30 | Agent delegation tool |

### OpenSpec Skills (`skills/software-development/`)

| Skill Directory | Purpose |
|-----------------|---------|
| `openspec-bootstrap/` | Project bootstrapper + document templates (proposal, plan, design, tasks, handoff, verification, release, status, shared-memory) |
| `openspec-orchestrator/` | Orchestrator agent role skill |
| `openspec-product-owner/` | Product owner agent role skill |
| `openspec-fullstack-developer/` | Full-stack developer agent role skill |
| `openspec-qa-engineer/` | QA engineer agent role skill |
| `openspec-release-manager/` | Release manager agent role skill |
| `openspec-heartbeat/` | Heartbeat / health-check agent role skill |
| `openspec-team-manager/` | Team manager agent role skill |
| `openspec-tech-lead/` | Tech lead agent role skill |

#### Bootstrap Templates (`openspec-bootstrap/templates/`)

**OpenSpec change lifecycle docs:**
- `openspec-change-template/proposal.md`
- `openspec-change-template/plan.md`
- `openspec-change-template/design.md`
- `openspec-change-template/tasks.md`
- `openspec-change-template/handoff.md`
- `openspec-change-template/verification.md`
- `openspec-change-template/release.md`
- `openspec-change-template/status.yaml`

**Shared memory templates:**
- `shared-memory/current-focus.md`
- `shared-memory/decision-log.md`
- `shared-memory/handoff-index.md`
- `shared-memory/lessons-learned.md`
- `shared-memory/mistake-log.md`
- `shared-memory/project-context.md`
- `shared-memory/project-risks.md`

---

## Modified Files

### `hermes_state.py`

- Added `OPENSPEC_SCHEMA_SQL` constant with 3 new SQLite tables and indexes:
  - `openspec_agents` — running/completed agent registry
  - `openspec_tasks` — kanban task board per change
  - `openspec_events` — append-only event log
- `SessionDB.__init__` runs the new schema on startup (safe on existing DBs)
- Added ~198 lines of CRUD methods on `SessionDB`:
  - `openspec_upsert_agent`, `openspec_update_agent_status`, `openspec_list_agents`
  - `openspec_insert_task`, `openspec_update_task_status`, `openspec_get_task`, `openspec_list_tasks`
  - `openspec_add_event`, `openspec_list_events`

### `toolsets.py`

- Added `"openspec"` toolset entry exposing the 6 OpenSpec tools to the agent

### `model_tools.py`

- Registered `tools.openspec_tool` in the tool discovery list (`_discover_tools`)

### `gateway/hooks.py`

- Added `HookRegistry.register(event_type, handler)` — programmatic runtime hook registration to complement file-based `discover_and_load()`

### `gateway/run.py`

- On `GatewayRunner` startup: initializes the OpenSpec event bus, binds it to the asyncio event loop, and registers `agent:start`, `agent:step`, `agent:end` gateway hooks to forward lifecycle events into the bus

### `gateway/platforms/api_server.py`

- Added WebSocket endpoint `GET /ws/events?project=X&change=Y` — streams all OpenSpec events in real time, optionally filtered by project/change
- Added WebSocket endpoint `GET /ws/agent/{agent_id}/logs` — streams live events for a specific agent

### `cron/scheduler.py`

- After each cron job completes, emits an `agent_completed` or `agent_failed` OpenSpec event if the job carries `openspec_project_code` in its `origin` metadata

---

## Architecture Overview

The branch adds a complete **OpenSpec multi-agent workflow system** on top of Hermes:

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenSpec Layer                           │
│                                                             │
│  Skills (8 agent roles + bootstrap)                         │
│      ↓                                                      │
│  Tools (openspec_tool.py)  ←→  State DB (hermes_state.py)  │
│      ↓                                ↓                     │
│  Event Bus (openspec_events.py)       SQLite tables         │
│      ↓                                                      │
│  Gateway hooks (run.py / hooks.py)                          │
│      ↓                                                      │
│  WebSocket streams (api_server.py)                          │
│      ↓                                                      │
│  Cron integration (scheduler.py)                            │
└─────────────────────────────────────────────────────────────┘
```

- **Persistence**: SQLite tables for agents, tasks, and events
- **Event bus**: in-process pub/sub wired into gateway startup and cron scheduler
- **8 agent role skills** with bootstrap skill and full document template set
- **6 tools** for agents to register themselves, manage kanban tasks, and emit events
- **WebSocket streaming** for real-time event observation by external clients
- **Dev tooling**: `Makefile` + `LOCAL_DEV_RUN.md` for reproducible local setup
