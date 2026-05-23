# Tulio Hermes Customizations

This document catalogs all customizations made to the Hermes agent for the tulio-hermes-agent project. These customizations include local development tools, UI enhancements, uncle-dev workflow automation, and developer-focused features.

**Last Updated:** 2026-05-08 (rebased onto main)  
**Branch:** uncle-dev  
**Backup:** uncle-dev-backup-2026-05-08

---

## Overview

The tulio customizations represent a developer-friendly fork of Hermes with enhanced local development capabilities, automated task management, and uncle-dev workflow integration. The customizations are designed to:

- Streamline local development setup and environment management
- Automate actionable task selection from specifications
- Provide better visibility into development processes
- Enhance UI readability for development workflows
- Integrate knowledge capture and documentation

---

## 1. Local Development Infrastructure

### 1.1 LOCAL_DEV_RUN.md
**Location:** `/LOCAL_DEV_RUN.md`  
**Purpose:** Developer runbook for setting up and running Hermes locally

**Contents:**
- Prerequisites and installation instructions
- Quick start guide
- Make targets documentation
- Directory structure explanation
- Required first-time configuration
- Typical local developer workflow
- Troubleshooting guide
- Tool addition instructions

**Key Sections:**
- `make setup`: Creates virtual environment and editable install
- `make doctor`: Verification pass matching project test flow
- `make npm-install`: Installs Node dependencies
- Development file locations (~/.hermes/)
- Model provider configuration requirements

---

## 2. Build System & Development Targets

### 2.1 Makefile
**Location:** `/Makefile`  
**Purpose:** Central entry point for common development tasks

**Key Targets:**

#### Development Targets
- `make setup`: Initialize virtual environment
- `make doctor`: Run full verification suite
- `make npm-install`: Install Node dependencies
- `make clean`: Clean build artifacts
- `make format`: Code formatting
- `make test`: Run test suite
- `make lint`: Linting checks

#### Service Targets
- `make dashboard`: Start the Hermes dashboard
- `make dev`: Run Hermes in dev mode
- `make gateway`: Start the gateway service
- `make webui`: Start the web UI

#### Documentation Targets
- `make docs`: Generate documentation

**Features:**
- 123 lines of utility functions and targets
- Integrated with main project's test flow
- Convenient shortcuts for common operations
- Service startup without manual command construction

---

## 3. Web UI Customizations

### 3.1 Web UI Theme Updates

#### index.css
**Location:** `/web/src/index.css`  
**Changes:**
- **Global Typography Bump:** `--theme-base-size` changed from 15px to 18px
- Additional theme customizations (54 line changes)
- Integrates with main's new theme-token system

#### presets.ts
**Location:** `/web/src/themes/presets.ts`  
**Changes:**
- Theme preset updates (24 line additions/modifications)
- Enhanced color schemes
- Typography scale adjustments

**Rationale:**
- Improved readability in development dashboards
- Better visibility for extended development sessions
- Aligned with modern design tokens

---

## 4. Gateway & CLI Enhancements

### 4.1 Gateway Display Configuration
**Location:** `/hermes_cli/gateway.py`  
**Changes:**
- Gateway API URL now printed in `launchd_status` output
- Enhanced visibility into gateway service health
- Easier debugging and service monitoring

**Purpose:**
- Developers can quickly see the gateway endpoint
- Better integration with local service management
- Improved troubleshooting when gateway issues occur

---

## 5. Plugin & Developer Documentation

### 5.1 Plugin Authoring Guide
**Location:** `/website/docs/developer-guide/creating-a-plugin.md`  
**Purpose:** Comprehensive guide for creating custom Hermes plugins

**Contents:**
- 332 lines of documentation
- Plugin structure and anatomy
- Development workflow
- Testing and validation
- Distribution and sharing

**Target Audience:**
- Plugin developers
- Contributors extending Hermes
- Custom tool creators

---

## 6. Uncle-Dev Workflow System

### 6.1 Uncle-Dev Skills Framework
**Location:** `/plugins/uncle/`  
**Purpose:** Integrated workflow automation for structured development

#### 6.1.1 uncle-dev-next-task
**Location:** `/plugins/uncle/skills/uncle-dev-next-task/`  
**Purpose:** Determine the next actionable task from OpenSpec changes and scratchpads

**Components:**
- `SKILL.md` (281 lines): Skill documentation and usage
- `acknowledge-gate.md`: Gate management system
- `conflict-resolution.md`: Scratchpad vs task.md conflict handling
- `parallelism-and-locks.md`: Parallel execution algorithm
- `parsing-and-annotations.md`: Task grammar and annotations

**Features:**
- Analyzes OpenSpec changes
- Parses personal scratchpads
- Detects task dependencies and mutexes
- Resolves conflicts with user intervention
- Supports parallel task execution
- Lock file management

#### 6.1.2 uncle-dev-acknowledge
**Location:** `/plugins/uncle/skills/uncle-dev-acknowledge/`  
**Purpose:** Gate management for pending acknowledgements

**Components:**
- `SKILL.md` (110 lines): Workflow documentation
- `acknowledge-workflow.md`: Workflow description
- `inference-rules.md`: Acknowledgement detection rules
- `note-schema.yaml`: Schema for note management

**Features:**
- Track pending acknowledgements
- Non-bypassable check enforcement
- Workflow state management
- Integration with development gates

#### 6.1.3 uncle-dev-knowledge-capture
**Location:** `/plugins/uncle/skills/uncle-dev-knowledge-capture/`  
**Purpose:** Document recently solved problems while context is fresh

**Features:**
- Automated problem documentation
- `.uncle-dev/learns/` storage
- Context preservation
- Knowledge reuse support

#### 6.1.4 uncle-dev-spec
**Location:** `/plugins/uncle/skills/uncle-dev-spec-driven-development/`  
**Purpose:** Spec-driven development workflow

**Features:**
- Define OpenSpec changes before coding
- API-first specification approach
- Test-driven specification

### 6.2 Development Process Documentation
**Location:** `/docs/development-process.md`  
**Purpose:** Comprehensive guide to the uncle-dev workflow system

**Contents:** (1269 lines)
- Development process overview
- Ready set algorithm
- Lock file management
- Conflict resolution procedures
- Parallelism strategies
- Acknowledgement gates
- Integration patterns

---

## 7. Git Configuration & Ignores

### 7.1 .gitignore Updates
**Location:** `/.gitignore`  
**Additions:**

```
graphify-out/          # Generated knowledge graph artifacts (~1.8M lines)
.claude/               # Per-developer Claude Code settings
.codex/                # Per-developer Codex settings
.opencode/             # Per-developer OpenCode settings
CLAUDE.md              # Local CLAUDE.md overrides
```

**Rationale:**
- Prevents local artifacts from polluting repository
- Each developer maintains local configurations
- Generated files don't affect version control
- Enables customized local workflows

### 7.2 Local Dev Secret Key
**Location:** `/.webui_secret_key`  
**Purpose:** 16-byte placeholder secret for local development

**Usage:**
- Web UI authentication in local dev
- Not used in production
- Regenerated per developer setup

---

## 8. Dropped Customizations

The following customizations from prior uncle-dev versions were dropped during the rebase because they conflicted with main's architecture:

### 8.1 UI Component Layout Tweaks
**Files:** `App.tsx`, `ConfigPage.tsx`, `StatusPage.tsx`  
**Reason:** Main rewrote the UI; original anchor selectors no longer exist  
**Status:** StatusPage.tsx was removed upstream entirely

### 8.2 Typography Sweep
**Scope:** 13 files with `text-[0.65rem]` → `text-xs`  
**Reason:** Stylistic preference not aligned with main's deliberate sizing choices  
**Status:** Replaced with consolidated theme-token changes in index.css

### 8.3 Graphify Artifacts
**Location:** `graphify-out/` (~1.8M lines)  
**Reason:** Generated artifacts now properly gitignored  
**Status:** Added to .gitignore instead of tracking

---

## 9. File Structure Summary

```
tulio-hermes-agent/
├── Makefile                                    # Build & dev targets
├── LOCAL_DEV_RUN.md                           # Dev runbook
├── .webui_secret_key                          # Local dev secret
├── .gitignore                                 # Updated ignores
├── .devLocal/
│   └── CUSTOMIZATIONS.md                      # This file
├── .claude/                                   # Per-developer settings
├── hermes_cli/
│   └── gateway.py                             # Gateway URL printing
├── web/src/
│   ├── index.css                              # Theme customizations
│   └── themes/presets.ts                      # Theme presets
├── website/docs/developer-guide/
│   └── creating-a-plugin.md                   # Plugin guide
├── plugins/uncle/
│   ├── __init__.py
│   └── skills/
│       ├── uncle-dev-next-task/               # Task selection
│       ├── uncle-dev-acknowledge/             # Gate management
│       ├── uncle-dev-knowledge-capture/       # Problem docs
│       └── uncle-dev-spec.../                 # Spec-driven dev
└── docs/
    └── development-process.md                 # Process documentation
```

---

## 10. Integration Points

### 10.1 With Claude Code
- `.claude/settings.json`: Claude Code configuration hooks
- Skills framework compatible with Claude Code agents
- Task management integrates with Claude Code workflows

### 10.2 With Main Hermes
- Minimal merge conflicts due to surgical changes
- Theme system integrated with main's token approach
- Plugin system backward compatible
- Gateway changes additive only

### 10.3 With Development Workflows
- Makes local development significantly easier
- Automation reduces manual task selection
- Knowledge capture prevents context loss
- Gate system ensures code quality gates

---

## 11. Usage Examples

### 11.1 Setting Up Local Environment
```bash
# Initial setup
make setup

# Verification
make doctor

# Install web dependencies
make npm-install
```

### 11.2 Running Services
```bash
# Start development environment
make dev

# Start dashboard
make dashboard

# Start gateway
make gateway

# Start web UI
make webui
```

### 11.3 Using Uncle-Dev Tasks
```bash
# Find next actionable task
/uncle-dev-next-task

# Acknowledge pending items
/uncle-dev-acknowledge

# Document solved problem
/uncle-dev-knowledge-capture
```

---

## 12. Maintenance & Updates

### 12.1 Rebasing Strategy
- Rebased to main on 2026-05-08
- Preserves functionality while staying synchronized
- Backup created at tag `uncle-dev-backup-2026-05-08`

### 12.2 Conflict Handling
- UI conflicts resolved by adopting main's theme token system
- Dropped conflicting customizations documented above
- Kept only non-conflicting improvements

### 12.3 Future Updates
- Watch for main's theme system changes
- Plugin system remains stable
- Makefile targets easily extensible
- Documentation should stay synchronized

---

## 13. Contact & Questions

For questions about these customizations:
- See LOCAL_DEV_RUN.md for setup issues
- Check docs/development-process.md for workflow questions
- Review plugin documentation for extending functionality
- File issues on GitHub for bugs

---

## Appendix: Complete Change Summary

**Total Changes in Latest Rebase (15b8a836):**
- 7 files added/modified
- 764 total insertions
- 1 deletion
- ~200 lines per file average

**Key Commits:**
- `15b8a836`: Uncle-dev rebase customizations
- `756321d8`: Uncle-dev-next-task skill addition

**Contributors:**
- TulioAgent
- Claude Sonnet 4.6
