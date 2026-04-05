---
name: openspec-bootstrap
description: Bootstrap the OpenSpec workflow state for any role. Resolves project location from project-map.yaml, loads shared memory and OpenSpec artifacts, registers the agent in the tracking system, and produces a concise structured state summary.
version: 1.0.0
metadata:
  hermes:
    tags: [openspec, workflow, bootstrap, multi-agent]
    related_skills: [openspec-orchestrator, openspec-team-manager]
---

# OpenSpec Bootstrap

Use this skill at the start of every OpenSpec role session — before any planning, coding, verification, or deployment work.

## Purpose

Establish a reliable shared state before acting. Agents that skip bootstrap will produce incorrect or conflicting artifacts.

## Bootstrap Sequence

Execute these steps **in order**. Do not skip any step.

### 1. Resolve project location

Read `~/coding-projects/project-map.yaml`.

Find the entry matching the `projectCode` you were given (or the active one in `current-focus.md`). Extract the absolute path. If the project is not found or status is `closed`, stop and report the issue.

Example project-map.yaml format:
```yaml
projects:
  - name: myproject
    path: ~/coding-projects/myproject
    status: active
```

### 2. Change into the project directory

All subsequent file reads use this as the base path.

### 3. Load shared memory (progressive — report missing, don't fail)

Read each file that exists. For each missing file, add a `[MISSING]` note to your state summary.

- `.ai/shared-memory/project-context.md` — product purpose, global constraints
- `.ai/shared-memory/current-focus.md` — active changes, owners, statuses, blockers, branch/worktree mapping
- `.ai/shared-memory/decision-log.md` — architecture and process decisions
- `.ai/shared-memory/mistake-log.md` — past failures and conditions that caused them
- `.ai/shared-memory/lessons-learned.md` — durable guidance to prevent repeat mistakes
- `.ai/shared-memory/handoff-index.md` — index of active handoffs and freshness
- `.ai/shared-memory/project-risks.md` — active technical and delivery risks

**Fail closed** only if `current-focus.md` is missing AND a change is claimed as `in-progress`. For a brand-new project with no shared memory, proceed with warnings.

### 4. Load OpenSpec specs and changes

- List `openspec/specs/` if it exists
- List `openspec/changes/` — find all active change directories
- For the active change, read `openspec/changes/<change-id>/status.yaml`
- Read `openspec/changes/<change-id>/handoff.md` if it exists

### 5. Confirm branch and worktree

Run: `git branch --show-current`

If the current branch does not match the expected branch in `current-focus.md` or the change assignment, flag it as a warning. Do not proceed with implementation if on the wrong branch.

### 6. Register in tracking system

Call `openspec_register_agent` with:
- `project_code`: resolved project code
- `change_id`: active change ID
- `role`: your role (orchestrator, team-manager, product-owner, tech-lead, fullstack-developer, qa-engineer, release-manager)
- `parent_agent_id`: the orchestrator's agent_id if you were delegated (omit if you are the orchestrator)

Save the returned `agent_id` — you will use it in subsequent `openspec_emit_event` and `openspec_update_task` calls.

### 7. Produce state summary

Output a structured state summary:

```
## Bootstrap State Summary

- **Project**: <name> at <absolute-path>
- **Agent ID**: <agent_id from step 6>
- **Role**: <your role>
- **Active change**: <change-id> (phase: <current-phase>)
- **Branch**: <current-branch>
- **Worktree**: <worktree-path or "main">
- **Owner**: <assigned owner from current-focus.md>

### Blockers
<list blockers or "None">

### Missing files
<list missing shared-memory files or "None">

### Warnings
<list warnings (wrong branch, stale handoff, etc.) or "None">

### Required next artifact
<the artifact this role must produce or update>
```

## Failure modes

- **Project code not found in project-map.yaml** → Stop. Report which code was looked up and what entries exist.
- **Wrong branch** → Report branch mismatch. Stop if this is an implementation role.
- **Active change has no handoff.md** → Continue with warning if phase is `idea` or `proposal`. Stop if phase is `implementation` or later.
- **`current-focus.md` missing for in-progress change** → Stop. The state cannot be trusted.

## Important rules

- Never assume project context — always resolve from files.
- Never read from chat history to infer state — read files only.
- Never skip this sequence because you think you already know the state.
- If bootstrap reveals blockers, report them before doing any role work.
