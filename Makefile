.DEFAULT_GOAL := help

SHELL := /bin/bash
PYTHON_VERSION := 3.11
VENV_DIR := venv
UV := uv
VENV_BIN := $(CURDIR)/$(VENV_DIR)/bin
HERMES := $(VENV_BIN)/hermes
PYTEST := $(VENV_BIN)/pytest
INSTALL_STAMP := $(VENV_DIR)/.installed
HERMES_HOME ?= $(HOME)/.hermes
HERMES_CONFIG := $(HERMES_HOME)/config.yaml
HERMES_ENV := $(HERMES_HOME)/.env

API_SERVER_KEY ?= hermes-local-key
WEBUI_PORT ?= 8080

.PHONY: help setup npm-install bootstrap-user-config doctor run chat setup-wizard test clean \
        gateway-setup gateway-start gateway-stop gateway-restart gateway-status gateway-install gateway-uninstall \
        webui-install webui

help:
	@printf "\nHermes local development\n\n"
	@printf "  make setup                 Create venv and install editable deps\n"
	@printf "  make npm-install           Install Node dependencies\n"
	@printf "  make bootstrap-user-config Create ~/.hermes files if missing\n"
	@printf "  make doctor                Run Hermes diagnostics\n"
	@printf "  make run                   Start Hermes CLI\n"
	@printf "  make chat                  Quick Hermes smoke test\n"
	@printf "  make setup-wizard          Run Hermes interactive setup\n"
	@printf "  make test                  Run pytest suite\n"
	@printf "  make clean                 Remove repo-local venv\n"
	@printf "\nGateway / daemon (UI access via http://127.0.0.1:8642)\n\n"
	@printf "  make gateway-setup         Configure gateway platforms (run once)\n"
	@printf "  make gateway-start         Start gateway as background daemon\n"
	@printf "  make gateway-stop          Stop background daemon\n"
	@printf "  make gateway-restart       Restart background daemon\n"
	@printf "  make gateway-status        Show daemon status\n"
	@printf "  make gateway-install       Register daemon with OS service manager\n"
	@printf "  make gateway-uninstall     Remove daemon from OS service manager\n"
	@printf "\nWeb UI (Open WebUI at http://localhost:8080)\n\n"
	@printf "  make webui-install         Install Open WebUI via pip\n"
	@printf "  make webui                 Start Open WebUI (connects to gateway on port 8642)\n\n"

$(VENV_BIN)/python:
	$(UV) venv $(VENV_DIR) --python $(PYTHON_VERSION)

$(INSTALL_STAMP): $(VENV_BIN)/python pyproject.toml uv.lock
	VIRTUAL_ENV="$(CURDIR)/$(VENV_DIR)" $(UV) pip install -e ".[all,dev]"
	touch $(INSTALL_STAMP)

install: $(INSTALL_STAMP)

setup: install

npm-install:
	npm install

bootstrap-user-config:
	mkdir -p "$(HERMES_HOME)/cron" "$(HERMES_HOME)/sessions" "$(HERMES_HOME)/logs" "$(HERMES_HOME)/memories" "$(HERMES_HOME)/skills"
	if [ ! -f "$(HERMES_CONFIG)" ]; then cp cli-config.yaml.example "$(HERMES_CONFIG)"; fi
	if [ ! -f "$(HERMES_ENV)" ]; then cp .env.example "$(HERMES_ENV)"; fi

doctor: install
	$(HERMES) doctor

run: install
	$(HERMES)

chat: install
	$(HERMES) chat -q "Hello"

setup-wizard: install
	$(HERMES) setup

test: install
	$(PYTEST) tests/ -q

clean:
	rm -rf "$(VENV_DIR)"

gateway-setup: install
	$(HERMES) gateway setup

gateway-start: install
	$(HERMES) gateway start

gateway-stop: install
	$(HERMES) gateway stop

gateway-restart: install
	$(HERMES) gateway restart

gateway-status: install
	$(HERMES) gateway status

gateway-install: install
	$(HERMES) gateway install

gateway-uninstall: install
	$(HERMES) gateway uninstall

webui-install:
	VIRTUAL_ENV="$(CURDIR)/$(VENV_DIR)" $(UV) pip install open-webui

webui: webui-install
	OPENAI_API_BASE_URL=http://localhost:8642/v1 \
	OPENAI_API_KEY=$(API_SERVER_KEY) \
	$(VENV_BIN)/open-webui serve --port $(WEBUI_PORT)
