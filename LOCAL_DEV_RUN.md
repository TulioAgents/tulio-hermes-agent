# Local Hermes Development Runbook

This guide explains how to set up, configure, run, and customize Hermes Agent locally from this source checkout.

It assumes:

- you are already in the repository root
- you want Hermes to run from your local source code
- you want a repeatable workflow for day-to-day development

## What the local workflow does

The local development flow uses:

- a repo-local virtual environment in `./venv`
- an editable Python install, so source changes in this repo are picked up when you run `hermes`
- user configuration in `~/.hermes`
- the root [`Makefile`](/Users/javierhbr/agents/tulio-hermes-agent/Makefile) for common tasks

## Prerequisites

You need:

- `uv`
- Python 3.11 support through `uv`
- optionally `npm` if you want browser or WhatsApp-related tooling

If `uv` is not installed yet, see the contributor flow in [`CONTRIBUTING.md`](/Users/javierhbr/agents/tulio-hermes-agent/CONTRIBUTING.md).

## Quick start

From the repo root:

```bash
make setup
make bootstrap-user-config
make doctor
make run
```

That sequence:

1. creates `./venv`
2. installs Hermes in editable mode with development dependencies
3. creates `~/.hermes` config files if they do not exist yet
4. runs diagnostics
5. starts the local Hermes CLI

## Make targets

The root [`Makefile`](/Users/javierhbr/agents/tulio-hermes-agent/Makefile) is the main entry point for local development.

### `make setup`

Creates the local virtual environment and installs the project in editable mode:

```bash
uv venv venv --python 3.11
uv pip install -e ".[all,dev]"
```

Because the install is editable, changes you make in this repository are reflected the next time you run Hermes.

The `Makefile` tracks setup completion with a local stamp file in `venv/.installed`. After the first successful setup, `make doctor`, `make run`, `make chat`, `make setup-wizard`, and `make test` reuse the existing install instead of reinstalling every time.

### `make bootstrap-user-config`

Creates the standard Hermes home directories under `~/.hermes` and copies starter config files only if they do not already exist.

It creates:

- `~/.hermes/cron`
- `~/.hermes/sessions`
- `~/.hermes/logs`
- `~/.hermes/memories`
- `~/.hermes/skills`

It also creates, if missing:

- `~/.hermes/config.yaml` from [`cli-config.yaml.example`](/Users/javierhbr/agents/tulio-hermes-agent/cli-config.yaml.example)
- `~/.hermes/.env` from [`.env.example`](/Users/javierhbr/agents/tulio-hermes-agent/.env.example)

This target is intentionally conservative. It does not overwrite an existing config.

### `make doctor`

Runs Hermes diagnostics:

```bash
./venv/bin/hermes doctor
```

Use this after setup or when something is not working.

### `make run`

Starts the local Hermes CLI:

```bash
./venv/bin/hermes
```

This is the normal entry point for local interactive use.

### `make chat`

Runs a fast smoke test:

```bash
./venv/bin/hermes chat -q "Hello"
```

This is useful to confirm that the install and model setup are working.

### `make setup-wizard`

Runs the interactive Hermes setup flow:

```bash
./venv/bin/hermes setup
```

Use this if you want Hermes to walk you through model selection, terminal backend, tools, and messaging setup.

### `make test`

Runs the test suite:

```bash
./venv/bin/pytest tests/ -q
```

For a full contributor-style verification pass, this matches the documented project test flow in [`README.md`](/Users/javierhbr/agents/tulio-hermes-agent/README.md) and [`AGENTS.md`](/Users/javierhbr/agents/tulio-hermes-agent/AGENTS.md).

### `make npm-install`

Installs Node dependencies:

```bash
npm install
```

You usually only need this for browser-related tooling or parts of the messaging stack that rely on Node.

### `make clean`

Removes the repo-local virtual environment:

```bash
rm -rf venv
```

It does not touch `~/.hermes`.

## Manual workflow without Make

If you prefer to run the steps directly:

```bash
uv venv venv --python 3.11
source venv/bin/activate
uv pip install -e ".[all,dev]"
mkdir -p ~/.hermes/{cron,sessions,logs,memories,skills}
cp cli-config.yaml.example ~/.hermes/config.yaml
cp .env.example ~/.hermes/.env
```

After that:

```bash
source venv/bin/activate
hermes doctor
hermes setup
hermes
```

If `~/.hermes/config.yaml` or `~/.hermes/.env` already exist, do not overwrite them unless you mean to reset your local setup.

## Where Hermes stores local state

Hermes keeps runtime configuration outside the repo in `~/.hermes`.

Important paths:

- `~/.hermes/config.yaml`: user settings
- `~/.hermes/.env`: API keys and secrets
- `~/.hermes/auth.json`: OAuth credentials
- `~/.hermes/skills/`: active skills
- `~/.hermes/memories/`: persistent memory files
- `~/.hermes/state.db`: SQLite session database
- `~/.hermes/sessions/`: JSON session logs
- `~/.hermes/logs/`: runtime logs
- `~/.hermes/cron/`: scheduled job data

These locations are described in [`CONTRIBUTING.md`](/Users/javierhbr/agents/tulio-hermes-agent/CONTRIBUTING.md) and referenced throughout the codebase.

## Required first configuration

Hermes needs at least one usable model provider before normal chat will work.

The usual path is:

1. create `~/.hermes/.env`
2. add a provider key
3. run `hermes setup` or `hermes model`

A common minimum setup is an OpenRouter key in `~/.hermes/.env`:

```env
OPENROUTER_API_KEY=your-key-here
```

The example env file at [`.env.example`](/Users/javierhbr/agents/tulio-hermes-agent/.env.example) lists many supported providers and optional tool keys.

## Typical local developer loop

Once the repo is installed, a normal development cycle looks like this:

1. Edit source files in this repository.
2. Run `make test` for code changes.
3. Run `make doctor` if the environment looks wrong.
4. Run `make run` to use Hermes locally.
5. Repeat.

Because Hermes is installed in editable mode, you usually do not need to reinstall after code changes.

## Files you will most likely customize

If your goal is to change how Hermes behaves locally, these are the main files to start with:

- [`run_agent.py`](/Users/javierhbr/agents/tulio-hermes-agent/run_agent.py): core agent loop
- [`model_tools.py`](/Users/javierhbr/agents/tulio-hermes-agent/model_tools.py): tool discovery and dispatch
- [`toolsets.py`](/Users/javierhbr/agents/tulio-hermes-agent/toolsets.py): tool grouping and availability
- [`cli.py`](/Users/javierhbr/agents/tulio-hermes-agent/cli.py): interactive CLI orchestration
- [`hermes_cli/main.py`](/Users/javierhbr/agents/tulio-hermes-agent/hermes_cli/main.py): command entrypoint
- [`hermes_cli/setup.py`](/Users/javierhbr/agents/tulio-hermes-agent/hermes_cli/setup.py): setup wizard
- [`tools/`](/Users/javierhbr/agents/tulio-hermes-agent/tools): individual tool implementations

## Adding a new tool locally

The project guide says a new tool usually requires changes in three places:

1. add a new file in [`tools/`](/Users/javierhbr/agents/tulio-hermes-agent/tools)
2. import it in [`model_tools.py`](/Users/javierhbr/agents/tulio-hermes-agent/model_tools.py)
3. include it in [`toolsets.py`](/Users/javierhbr/agents/tulio-hermes-agent/toolsets.py)

That is the basic path if your customization involves extending Hermes with a new tool.

## Troubleshooting

### `make setup` fails

Check:

- `uv` is installed
- Python 3.11 is available through `uv`
- you are running from the repo root

### `make run` starts but chat does not work

Check:

- `~/.hermes/.env` contains a valid provider key
- `~/.hermes/config.yaml` points to a usable default model
- `make doctor` for diagnostics

### `make bootstrap-user-config` did not change anything

That usually means your `~/.hermes/config.yaml` and `~/.hermes/.env` already exist. The target is designed not to overwrite them.

### I changed code but Hermes still behaves the same

Check:

- you installed with editable mode through `make setup`
- you are running the local Hermes binary from `./venv/bin/hermes`
- your change is in the code path exercised by the command you are running

## Recommended first run

If you want the shortest safe path from this repo to a working local agent:

```bash
make setup
make bootstrap-user-config
make setup-wizard
make doctor
make run
```

That gives you a local editable install, initializes the standard Hermes home directory, walks you through provider setup, checks the environment, and starts the CLI.
