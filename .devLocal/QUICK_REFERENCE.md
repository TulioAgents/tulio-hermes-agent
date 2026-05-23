# Quick Reference: Tulio Customizations

## Fast Lookup by Task

### Setting Up Local Development
**File:** `LOCAL_DEV_RUN.md`  
**Start here:** Prerequisites → Quick start → Make targets

**Key Commands:**
```bash
make setup       # Initialize environment
make doctor      # Verify installation
make dev         # Start development server
```

---

### Adding Tools or Features
**File:** `LOCAL_DEV_RUN.md` → "Adding a new tool locally"  
**Steps:**
1. Create new file in `tools/`
2. Import in `model_tools.py`
3. Include in `toolsets.py`

---

### Creating a Plugin
**File:** `website/docs/developer-guide/creating-a-plugin.md`  
**Key Topics:**
- Plugin structure and anatomy
- Development workflow
- Testing and validation
- Distribution

---

### Using Task Management
**Skills Available:**
- `/uncle-dev-next-task` → Find next actionable task
- `/uncle-dev-acknowledge` → Manage acknowledgements
- `/uncle-dev-knowledge-capture` → Document solutions
- `/uncle-dev-spec` → Spec-driven development

**Documentation:** `docs/development-process.md`

---

### Troubleshooting
**File:** `LOCAL_DEV_RUN.md` → "Troubleshooting"  
**Common Issues:**
- Model provider configuration
- Virtual environment problems
- Service startup issues

---

## File Location Reference

| Component | File/Directory | Lines | Purpose |
|-----------|---|---|---|
| Dev Runbook | `LOCAL_DEV_RUN.md` | 291 | Setup guide & workflow |
| Build System | `Makefile` | 123 | Development targets |
| UI Styling | `web/src/index.css` | 54 | Theme customizations |
| Theme Config | `web/src/themes/presets.ts` | 24 | Theme presets |
| Gateway | `hermes_cli/gateway.py` | 7 | URL printing |
| Plugin Guide | `website/docs/developer-guide/creating-a-plugin.md` | 332 | Plugin authoring |
| Task Mgmt | `plugins/uncle/skills/uncle-dev-next-task/` | 281 | Task selection |
| Acknowledge | `plugins/uncle/skills/uncle-dev-acknowledge/` | 110 | Gate management |
| Dev Process | `docs/development-process.md` | 1269 | Complete workflow |
| Customizations | `.devLocal/CUSTOMIZATIONS.md` | — | This documentation |

---

## Installation Quick Start

```bash
# 1. Initial setup
make setup

# 2. Verify everything works
make doctor

# 3. Install web dependencies (if needed)
make npm-install

# 4. Configure model provider in ~/.hermes/config.yaml
# (See LOCAL_DEV_RUN.md for details)

# 5. Start development
make dev
```

---

## Key Features at a Glance

### ✅ Local Development
- Makefile targets for all common tasks
- One-command environment setup
- Automated verification

### ✅ Web UI
- Improved typography (+18px base size)
- Better readability for long sessions
- Theme token integration

### ✅ Task Management
- Automatic next-task selection
- OpenSpec integration
- Conflict detection
- Lock-based parallelism

### ✅ Knowledge Capture
- Document solutions while fresh
- Automatic organization
- Easy recall

### ✅ Quality Gates
- Acknowledgement system
- Non-bypassable checks
- Specification-driven development

---

## Customization Highlights

### Most Impactful
1. **Makefile** - Saves time on every dev session
2. **uncle-dev-next-task** - Automates task selection
3. **LOCAL_DEV_RUN.md** - Onboarding reference
4. **Theme Updates** - Improved UI readability

### Most Complex
1. **uncle-dev-next-task** - Advanced task parsing & locking
2. **docs/development-process.md** - Complete system documentation
3. **Plugin authoring guide** - Comprehensive developer guide

### Easiest to Use
1. **Makefile targets** - Simple one-line commands
2. **Knowledge capture** - Just invoke and fill form
3. **UI theme** - Automatic, no action needed

---

## Integration Points

**With Claude Code:**
- Skills register with `.claude/` configuration
- Task management integrates with agent workflows

**With Main Hermes:**
- Additive changes only
- No breaking modifications
- Compatible plugin system

**With Development Workflows:**
- Reduces boilerplate setup
- Automates routine tasks
- Captures knowledge for team

---

## Environment Variables & Configs

### Key Locations
- **Config:** `~/.hermes/config.yaml`
- **Environment:** `~/.hermes/.env`
- **Secrets:** `.webui_secret_key` (dev only)
- **Tasks:** `.devLocal/` or scratchpads

### Important Paths
- **Home:** `~/.hermes/`
- **Cache:** `~/.hermes/cache/`
- **Cron:** `~/.hermes/cron/`
- **Tasks:** `.uncle-dev/` (project-specific)

---

## Common Workflows

### Daily Development
```
make dev
→ /uncle-dev-next-task
→ Implement task
→ /uncle-dev-knowledge-capture (if solved problem)
```

### Adding a Feature
```
/uncle-dev-spec (define OpenSpec)
make dev
/uncle-dev-next-task (get implementation task)
→ Implement from spec
→ Test
```

### Setting Up New Dev Machine
```
make setup
make doctor
make npm-install
# Configure ~/.hermes/config.yaml
make dev
```

---

## Document Navigation

```
CUSTOMIZATIONS.md ← Complete reference (start here for overview)
QUICK_REFERENCE.md ← This file (fast lookup)
FILE_LOCATIONS.md ← Detailed file structure
DEVELOPER_GUIDE.md ← How to use customizations
```

---

## Need Help?

| Question | File | Section |
|----------|------|---------|
| "How do I set up locally?" | LOCAL_DEV_RUN.md | Quick start |
| "What can I do with tasks?" | docs/development-process.md | Overview |
| "How do I make a plugin?" | creating-a-plugin.md | Full guide |
| "What's changed?" | CUSTOMIZATIONS.md | Overview |
| "How do I...?" | This file | Common Workflows |

---

Last Updated: 2026-05-22
