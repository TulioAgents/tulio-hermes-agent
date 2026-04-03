# Local Makefile Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a root `Makefile` that manages safe local source setup and daily development commands for Hermes Agent.

**Architecture:** Keep the `Makefile` thin and explicit. It should wrap the repository's existing setup commands and contributor workflow instead of replacing them with custom logic. User-home configuration should only be created through clearly named bootstrap targets and should avoid overwriting existing files.

**Tech Stack:** GNU Make, shell commands, `uv`, `npm`, Hermes CLI

---

### Task 1: Add a conservative root Makefile

**Files:**
- Create: `Makefile`
- Reference: `README.md`
- Reference: `CONTRIBUTING.md`
- Reference: `setup-hermes.sh`

- [ ] **Step 1: Define target surface**

Include targets for:
- `help`
- `venv`
- `install`
- `setup`
- `npm-install`
- `bootstrap-user-config`
- `doctor`
- `run`
- `chat`
- `setup-wizard`
- `test`
- `clean`

- [ ] **Step 2: Keep user config writes explicit and non-destructive**

`bootstrap-user-config` should:
- create `~/.hermes/{cron,sessions,logs,memories,skills}`
- copy `cli-config.yaml.example` to `~/.hermes/config.yaml` only if missing
- copy `.env.example` to `~/.hermes/.env` only if missing

- [ ] **Step 3: Keep repo-local setup simple**

`venv` should create `venv` with Python 3.11 using `uv`.

`install` should install Hermes in editable mode with:

```bash
uv pip install -e ".[all,dev]"
```

`setup` should depend on `venv` and `install`.

- [ ] **Step 4: Wrap daily commands**

Daily targets should run through the local venv binary where possible:
- `doctor`
- `run`
- `chat`
- `setup-wizard`
- `test`

- [ ] **Step 5: Add friendly help output**

The default target should print concise grouped commands so a developer can discover the workflow quickly.

### Task 2: Verify Makefile behavior

**Files:**
- Modify: `Makefile`

- [ ] **Step 1: Run help target**

Run:

```bash
make help
```

Expected: prints the available local development targets.

- [ ] **Step 2: Run a dry verification pass**

Run:

```bash
make -n setup
make -n bootstrap-user-config
```

Expected: shows the intended commands without mutating the machine.

- [ ] **Step 3: Fix any quoting or path issues**

Adjust Makefile variables or recipes until the dry-run output is clean and readable.
