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

.PHONY: help setup npm-install bootstrap-user-config doctor run chat setup-wizard test clean

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
	@printf "  make clean                 Remove repo-local venv\n\n"

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
