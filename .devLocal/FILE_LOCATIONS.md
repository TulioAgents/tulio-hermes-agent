# Tulio Customizations: File Location Map

This document provides a detailed map of every customized file, its purpose, and what was changed.

---

## Root Level Changes

### Makefile
**Location:** `/Makefile`  
**Size:** ~123 lines  
**Status:** Added (new file)  
**Purpose:** Central build and development automation

**Key Targets:**
- `setup` - Initialize environment
- `doctor` - Verification pass
- `dashboard` - Start dashboard
- `dev` - Development mode
- `gateway` - Gateway service
- `webui` - Web UI
- `clean` - Cleanup
- `format` - Code formatting
- `test` - Run tests
- `lint` - Linting

**Usage:**
```bash
make <target>
```

**Dependencies:** Python 3.11+, npm (optional)

---

### LOCAL_DEV_RUN.md
**Location:** `/LOCAL_DEV_RUN.md`  
**Size:** ~291 lines  
**Status:** Added (new file)  
**Purpose:** Developer setup and workflow documentation

**Sections:**
1. Prerequisites
2. Quick start
3. Make targets reference
4. Directory structure
5. Required first configuration
6. Typical dev workflow
7. Main files to modify
8. Adding new tools
9. Troubleshooting

**Audience:** New developers, contributors

**How to Use:**
- Start with "Quick start" for setup
- Reference "Make targets" for commands
- See "Troubleshooting" for issues

---

### .gitignore
**Location:** `/.gitignore`  
**Size:** +9 lines  
**Status:** Modified  
**Original Size:** Unknown  
**Changes:**

```diff
+ graphify-out/           # Generated knowledge graph
+ .claude/                # Per-developer settings
+ .codex/                 # Per-developer settings
+ .opencode/              # Per-developer settings
+ CLAUDE.md               # Local overrides
```

**Purpose:** Prevent local artifacts and configs from polluting repo

**Rationale:**
- Each developer has own configs
- Generated files shouldn't be tracked
- Keep repo clean and personal setups separate

---

### .webui_secret_key
**Location:** `/.webui_secret_key`  
**Size:** 16 bytes  
**Status:** Added (new file)  
**Purpose:** Local development secret key

**Content:** 16-byte placeholder (not for production)

**Usage:** Web UI authentication in local development

**Security:** Never commit actual secrets; this is a template

---

## CLI & Gateway Changes

### hermes_cli/gateway.py
**Location:** `/hermes_cli/gateway.py`  
**Size:** +7 lines  
**Status:** Modified  
**Changes:** Added gateway API URL printing in `launchd_status` output

**What Changed:**
- Gateway endpoint now visible in service status
- Helps developers quickly identify gateway URL
- Better debugging and monitoring

**Function:** `launchd_status()`  
**New Output:** Gateway API URL displayed alongside service status

**Purpose:** 
- Improved visibility into gateway operation
- Easier local testing and debugging
- Quick access to gateway endpoint

---

## Web UI Customizations

### web/src/index.css
**Location:** `/web/src/index.css`  
**Size:** +54 lines (modified)  
**Status:** Modified  
**Key Change:** `--theme-base-size: 15px` → `--theme-base-size: 18px`

**Details:**
- Global typography bump for better readability
- Cascades to all text elements via CSS variables
- Integrates with main's new theme-token system
- 54 lines of additional styling

**Purpose:**
- Improved readability in development dashboards
- Better visibility during extended work sessions
- More comfortable for development workflows

**Scope:**
- Global change affecting entire dashboard
- Backward compatible with existing styles
- Uses CSS variables for easy adjustment

---

### web/src/themes/presets.ts
**Location:** `/web/src/themes/presets.ts`  
**Size:** +24 lines (modified)  
**Status:** Modified  
**Changes:**
- Updated theme preset definitions
- Enhanced color schemes
- Typography scale adjustments

**Details:**
- TypeScript/React configuration
- Integrates with Tailwind CSS system
- Syncs with CSS variable changes

**Purpose:**
- Consistent theme across development
- Improved visual hierarchy
- Better dark/light mode support

---

## Documentation

### website/docs/developer-guide/creating-a-plugin.md
**Location:** `/website/docs/developer-guide/creating-a-plugin.md`  
**Size:** 332 lines  
**Status:** Added (new file)  
**Purpose:** Comprehensive plugin development guide

**Sections:**
1. Overview and architecture
2. Plugin structure anatomy
3. Development workflow
4. Tool registration
5. Testing practices
6. Validation and safety
7. Distribution methods
8. Troubleshooting

**Audience:** Plugin developers, tool creators, contributors

**How to Use:**
- Start with "Overview" to understand plugin concepts
- Follow "Development workflow" step-by-step
- Reference anatomy for file structure

**Relates to:**
- `tools/` directory
- `model_tools.py`
- `toolsets.py`

---

### docs/development-process.md
**Location:** `/docs/development-process.md`  
**Size:** 1269 lines  
**Status:** Added (new file)  
**Purpose:** Complete uncle-dev workflow system documentation

**Sections:**
1. Development process overview
2. OpenSpec integration
3. Ready set algorithm
4. Task parsing and annotations
5. Lock file management
6. Conflict resolution
7. Parallelism strategies
8. Acknowledgement gates
9. Workflow examples
10. Advanced topics

**Audience:** All developers, advanced workflow users

**Complexity:** Advanced (not for beginners)

**Key Concepts:**
- OpenSpec-driven development
- Ready sets for task selection
- Mutex and dependency management
- Conflict resolution procedures

---

## Uncle-Dev Skills & Plugins

### plugins/uncle/__init__.py
**Location:** `/plugins/uncle/__init__.py`  
**Size:** 2 lines  
**Status:** Modified  
**Purpose:** Uncle-dev plugin namespace initialization

---

### plugins/uncle/skills/uncle-dev-next-task/

#### SKILL.md
**Location:** `/plugins/uncle/skills/uncle-dev-next-task/SKILL.md`  
**Size:** 281 lines  
**Purpose:** Main skill documentation and usage guide

**Contents:**
- Skill overview
- How it works
- Input parameters
- Output format
- Example usage
- Integration points
- Troubleshooting

**Key Features:**
- Analyzes OpenSpec changes
- Parses personal scratchpads
- Detects dependencies
- Suggests next actionable task
- Shows ready/blocked status

---

#### acknowledge-gate.md
**Location:** `/plugins/uncle/skills/uncle-dev-next-task/acknowledge-gate.md`  
**Size:** 80 lines  
**Purpose:** Acknowledgement gate system documentation

**Topics:**
- Gate lifecycle
- Pending acknowledgements
- Non-bypassable checks
- Override procedures
- State management

---

#### conflict-resolution.md
**Location:** `/plugins/uncle/skills/uncle-dev-next-task/conflict-resolution.md`  
**Size:** 118 lines  
**Purpose:** Handle discrepancies between specs and scratchpads

**Topics:**
- Conflict detection
- Resolution strategies
- User intervention points
- Automated vs manual resolution
- Edge cases

---

#### parallelism-and-locks.md
**Location:** `/plugins/uncle/skills/uncle-dev-next-task/parallelism-and-locks.md`  
**Size:** 231 lines  
**Purpose:** Parallel task execution and locking algorithm

**Topics:**
- Ready set algorithm
- Lock file format
- Mutex definitions
- Dependency graphs
- Execution ordering
- Lock acquisition

---

#### parsing-and-annotations.md
**Location:** `/plugins/uncle/skills/uncle-dev-next-task/parsing-and-annotations.md`  
**Size:** 160 lines  
**Purpose:** Task grammar and annotation system

**Topics:**
- Task file syntax
- Annotation grammar
- Dependency syntax
- Mutex declarations
- Parsing rules
- Examples

---

### plugins/uncle/skills/uncle-dev-acknowledge/

#### SKILL.md
**Location:** `/plugins/uncle/skills/uncle-dev-acknowledge/SKILL.md`  
**Size:** 110 lines  
**Purpose:** Acknowledgement management skill documentation

**Features:**
- Track pending items
- Enforce gates
- Workflow automation
- Status tracking

---

#### acknowledge-workflow.md
**Location:** `/plugins/uncle/skills/uncle-dev-acknowledge/acknowledge-workflow.md`  
**Size:** 141 lines  
**Purpose:** Detailed workflow description

**Topics:**
- Workflow steps
- State transitions
- User interactions
- Automation points

---

#### inference-rules.md
**Location:** `/plugins/uncle/skills/uncle-dev-acknowledge/inference-rules.md`  
**Size:** 94 lines  
**Purpose:** Rules for detecting acknowledgement requirements

**Topics:**
- Detection rules
- Pattern matching
- Automatic triggers
- Manual overrides

---

#### note-schema.yaml
**Location:** `/plugins/uncle/skills/uncle-dev-acknowledge/note-schema.yaml`  
**Size:** 144 lines  
**Purpose:** Schema definition for acknowledgement notes

**Format:** YAML  
**Contents:**
- Field definitions
- Data types
- Validation rules
- Examples

---

### plugins/uncle/skills/uncle-dev-knowledge-capture/

#### SKILL.md
**Location:** `/plugins/uncle/skills/uncle-dev-knowledge-capture/SKILL.md`  
**Size:** 24 lines (modified, +24)  
**Purpose:** Knowledge capture skill documentation

**Features:**
- Document solutions
- Store in `.uncle-dev/learns/`
- Preserve context
- Enable knowledge reuse

---

### plugins/uncle/skills/uncle-dev-documentation-and-adrs/

#### SKILL.md
**Location:** `/plugins/uncle/skills/uncle-dev-documentation-and-adrs/SKILL.md`  
**Size:** 13 lines  
**Purpose:** ADR and documentation skill

---

### plugins/uncle/skills/uncle-dev-spec-driven-development/

#### SKILL.md
**Location:** `/plugins/uncle/skills/uncle-dev-spec-driven-development/SKILL.md`  
**Size:** 10 lines  
**Purpose:** Spec-driven development workflow

**Features:**
- Define OpenSpec before coding
- API-first approach
- Test-driven specifications

---

## Directory Structure

```
tulio-hermes-agent/
│
├── ROOT LEVEL (Core Changes)
│   ├── Makefile                          [Build automation]
│   ├── LOCAL_DEV_RUN.md                  [Dev guide]
│   ├── .gitignore                        [Ignore rules]
│   └── .webui_secret_key                 [Dev secret]
│
├── .devLocal/                            [This documentation]
│   ├── CUSTOMIZATIONS.md                 [Complete reference]
│   ├── QUICK_REFERENCE.md                [Fast lookup]
│   └── FILE_LOCATIONS.md                 [This file]
│
├── hermes_cli/
│   └── gateway.py                        [Gateway URL printing]
│
├── web/src/
│   ├── index.css                         [Theme styling]
│   └── themes/presets.ts                 [Theme config]
│
├── website/docs/developer-guide/
│   └── creating-a-plugin.md              [Plugin guide]
│
├── docs/
│   └── development-process.md            [Process docs]
│
└── plugins/uncle/                        [Uncle-dev system]
    ├── __init__.py
    └── skills/
        ├── uncle-dev-next-task/
        │   ├── SKILL.md
        │   ├── acknowledge-gate.md
        │   ├── conflict-resolution.md
        │   ├── parallelism-and-locks.md
        │   └── parsing-and-annotations.md
        │
        ├── uncle-dev-acknowledge/
        │   ├── SKILL.md
        │   ├── acknowledge-workflow.md
        │   ├── inference-rules.md
        │   └── note-schema.yaml
        │
        ├── uncle-dev-knowledge-capture/
        │   └── SKILL.md
        │
        └── uncle-dev-spec-driven-development/
            └── SKILL.md
```

---

## Search Guide

### Finding Documentation by Topic

**Local Development Setup**
- Primary: `LOCAL_DEV_RUN.md` (start here)
- Reference: `Makefile`

**Task Management**
- Primary: `docs/development-process.md` (1269 lines, comprehensive)
- Quick: `/uncle-dev-next-task/SKILL.md`

**Plugin Development**
- Primary: `creating-a-plugin.md` (332 lines, step-by-step)
- Reference: `plugins/uncle/` (see examples)

**UI Customization**
- CSS: `web/src/index.css`
- Config: `web/src/themes/presets.ts`

**Acknowledgement System**
- Overview: `uncle-dev-acknowledge/SKILL.md`
- Workflow: `acknowledge-workflow.md`
- Rules: `inference-rules.md`

**Parallelism & Locks**
- Primary: `parallelism-and-locks.md` (231 lines)
- Reference: `parsing-and-annotations.md`

---

## File Statistics

| Category | Count | Total Lines |
|----------|-------|------------|
| Added Files | 12 | ~3000 |
| Modified Files | 7 | +~100 |
| Documentation | 7 | ~2000 |
| Skills/Plugins | 8 | ~1000 |
| Configuration | 3 | ~100 |

---

## Last Modified

**Latest Rebase:** 2026-05-08  
**Skills Added:** 2026-05-09  
**This Map:** 2026-05-22

---

## Navigation Tips

1. **Start with CUSTOMIZATIONS.md** for complete overview
2. **Use QUICK_REFERENCE.md** for fast lookups
3. **Browse FILE_LOCATIONS.md** to understand structure
4. **Reference specific files** for detailed information

---

Generated: 2026-05-22
