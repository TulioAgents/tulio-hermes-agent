# Tulio Hermes Customizations Documentation Index

Welcome to the comprehensive documentation of all customizations made to the Hermes agent for the tulio-hermes-agent project. This index helps you navigate the documentation and find what you need.

**📍 You are here:** `.devLocal/INDEX.md`

---

## 📚 Documentation Overview

This `.devLocal/` directory contains complete documentation of tulio customizations:

### Core Documents (in reading order)

1. **INDEX.md** (this file)  
   Overview and navigation guide

2. **CUSTOMIZATIONS.md** (Complete Reference)  
   - Comprehensive breakdown of all changes
   - Organized by category (13 sections)
   - Best for understanding the full scope
   - ~3000 lines of detailed information
   - **Read this first** for complete picture

3. **QUICK_REFERENCE.md** (Fast Lookup)  
   - Common tasks and quick answers
   - Organized by use case
   - Fast lookup table for files
   - Integration points
   - Common workflows
   - **Read this** when you need a quick answer

4. **FILE_LOCATIONS.md** (Detailed Map)  
   - Every file and directory
   - Specific line counts
   - Purpose and usage
   - Search guide by topic
   - **Use this** to find specific files

---

## 🎯 Quick Start: Choose Your Path

### 👤 "I'm new and setting up for the first time"
```
1. Read: QUICK_REFERENCE.md → "Installation Quick Start"
2. Run: make setup && make doctor
3. Reference: LOCAL_DEV_RUN.md for detailed setup
```

### 🛠️ "I want to add a tool or feature"
```
1. Read: CUSTOMIZATIONS.md → Section 5 (Plugin Documentation)
2. Reference: website/docs/developer-guide/creating-a-plugin.md
3. Reference: LOCAL_DEV_RUN.md → "Adding a new tool locally"
```

### 📋 "I want to understand task management"
```
1. Read: QUICK_REFERENCE.md → "Using Task Management"
2. Deep dive: docs/development-process.md
3. Reference: /uncle-dev-next-task/SKILL.md
```

### 🎨 "I want to understand UI customizations"
```
1. Read: CUSTOMIZATIONS.md → Section 3 (Web UI Customizations)
2. Files: web/src/index.css and web/src/themes/presets.ts
```

### 🔧 "I want to understand everything"
```
1. Read: CUSTOMIZATIONS.md (complete overview)
2. Reference: FILE_LOCATIONS.md (detailed map)
3. Explore: Individual files as needed
```

---

## 📖 Document Descriptions

### CUSTOMIZATIONS.md
**Size:** ~3000 lines  
**Complexity:** Medium-High  
**Audience:** Everyone (reference material)

**Contents:**
- 13 major sections covering all customizations
- Local development infrastructure
- Build system & development targets
- Web UI customizations
- Gateway & CLI enhancements
- Plugin & developer documentation
- Uncle-dev workflow system
- Git configuration
- Dropped customizations (important!)
- File structure summary
- Integration points
- Usage examples
- Maintenance & updates
- Complete appendix

**When to read:**
- First-time understanding of customizations
- Deep research on a topic
- Reference during implementation
- Comparing customizations with main branch

**Best for:**
- Getting the big picture
- Understanding rationale
- Learning integration points
- Catching edge cases

---

### QUICK_REFERENCE.md
**Size:** ~500 lines  
**Complexity:** Low  
**Audience:** Active developers (fast reference)

**Contents:**
- Fast lookup by task
- File location reference table
- Installation quick start
- Key features at a glance
- Customization highlights
- Integration points summary
- Environment variables
- Common workflows
- Need help guide
- Document navigation

**When to read:**
- You have a specific task
- You need a quick reminder
- You're looking for a command
- You want to know "what does this do?"

**Best for:**
- Daily reference
- Quick answers
- Command cheatsheet
- Workflow examples

---

### FILE_LOCATIONS.md
**Size:** ~1500 lines  
**Complexity:** Medium  
**Audience:** Developers exploring the codebase

**Contents:**
- Root level changes (Makefile, LOCAL_DEV_RUN.md, etc.)
- CLI & gateway changes
- Web UI customizations (CSS, themes)
- Documentation (guides, process docs)
- Uncle-dev skills & plugins (detailed)
- Complete directory tree structure
- Search guide by topic
- File statistics

**When to read:**
- You need to find a specific file
- You want to understand file structure
- You're exploring the codebase
- You need exact line numbers/sizes

**Best for:**
- Navigation
- Finding files
- Understanding organization
- Locating related files

---

## 🗂️ Files in This Directory

```
.devLocal/
├── INDEX.md                    ← You are here
├── CUSTOMIZATIONS.md           ← Complete reference
├── QUICK_REFERENCE.md          ← Fast lookup
├── FILE_LOCATIONS.md           ← Detailed map
└── (Additional docs as needed)
```

All files are written in Markdown for easy viewing in any editor or browser.

---

## 🔍 How to Find Information

### By Task
Use **QUICK_REFERENCE.md** → "Fast Lookup by Task" section

### By File
Use **FILE_LOCATIONS.md** → "Search Guide" section or directory tree

### By Topic
Use **CUSTOMIZATIONS.md** → Section headers (13 major sections)

### By Complexity
- **Beginner:** QUICK_REFERENCE.md
- **Intermediate:** CUSTOMIZATIONS.md
- **Advanced:** Individual files in project root

### By Need
- **Setup:** LOCAL_DEV_RUN.md + Makefile
- **Development:** docs/development-process.md
- **Plugins:** creating-a-plugin.md
- **Workflow:** QUICK_REFERENCE.md → "Common Workflows"

---

## 📋 Customization Categories

Here's what was customized and where to learn about it:

| Category | Main Doc | Quick Ref | File Ref | Files |
|----------|----------|-----------|----------|-------|
| **Local Dev** | CUSTOMIZATIONS.md #1 | QR: Setup | FL: Root | Makefile, LOCAL_DEV_RUN.md |
| **Build System** | CUSTOMIZATIONS.md #2 | QR: Tasks | FL: Root | Makefile |
| **Web UI** | CUSTOMIZATIONS.md #3 | QR: UI | FL: web/src/ | index.css, presets.ts |
| **Gateway** | CUSTOMIZATIONS.md #4 | QR: Gateway | FL: hermes_cli/ | gateway.py |
| **Docs** | CUSTOMIZATIONS.md #5 | QR: Guide | FL: website/ | creating-a-plugin.md |
| **Task Management** | CUSTOMIZATIONS.md #6 | QR: Tasks | FL: plugins/uncle/ | uncle-dev-next-task/ |
| **Acknowledgements** | CUSTOMIZATIONS.md #6.1.2 | QR: Gates | FL: plugins/uncle/ | uncle-dev-acknowledge/ |
| **Knowledge Capture** | CUSTOMIZATIONS.md #6.1.3 | QR: Docs | FL: plugins/uncle/ | uncle-dev-knowledge-capture/ |
| **Git Config** | CUSTOMIZATIONS.md #7 | QR: Git | FL: Root | .gitignore, .webui_secret_key |

---

## 🚀 Common Workflows

### Setting Up a Fresh Machine
1. Read: QUICK_REFERENCE.md → "Installation Quick Start"
2. Run: `make setup && make doctor`
3. Configure: `~/.hermes/config.yaml` (see LOCAL_DEV_RUN.md)

### Daily Development
1. Run: `make dev`
2. Use: `/uncle-dev-next-task` for next task
3. Reference: QUICK_REFERENCE.md → "Common Workflows"

### Adding a New Feature
1. Create spec: `/uncle-dev-spec`
2. Get task: `/uncle-dev-next-task`
3. Implement feature
4. Document: `/uncle-dev-knowledge-capture`

### Creating a Plugin
1. Read: CUSTOMIZATIONS.md #5 or creating-a-plugin.md
2. Create: New file in `plugins/` or `tools/`
3. Reference: Structure examples
4. Test: Include in test suite

---

## 🔗 Related Files (Not in .devLocal)

### Must-Read Before Contributing
- **LOCAL_DEV_RUN.md** - Developer setup guide
- **README.md** - Project overview
- **CONTRIBUTING.md** - Contribution guidelines

### Process & Workflow
- **docs/development-process.md** - Complete task system
- **website/docs/developer-guide/creating-a-plugin.md** - Plugin guide

### Configuration
- **Makefile** - Build targets
- **web/src/index.css** - UI styling
- **.gitignore** - Version control rules

### Skills & Tools
- **plugins/uncle/skills/** - Uncle-dev skills
- **tools/** - Individual tool implementations
- **model_tools.py** - Tool registration

---

## 🎓 Learning Path

### For New Developers
1. **Day 1:** QUICK_REFERENCE.md + make setup
2. **Day 2:** LOCAL_DEV_RUN.md + make dev
3. **Day 3:** CUSTOMIZATIONS.md overview
4. **Day 4+:** Deep dive into specific areas

### For Contributors
1. **Setup:** QUICK_REFERENCE.md
2. **Contributing:** CONTRIBUTING.md
3. **Process:** docs/development-process.md
4. **Plugin Dev:** creating-a-plugin.md

### For Advanced Users
1. **Task Management:** docs/development-process.md
2. **Skills:** uncle-dev skills documentation
3. **Architecture:** CUSTOMIZATIONS.md integration points
4. **Workflow:** QUICK_REFERENCE.md common workflows

---

## ❓ FAQ

### Q: Where do I start?
**A:** If you're new, read QUICK_REFERENCE.md first, then LOCAL_DEV_RUN.md

### Q: How do I find a specific file?
**A:** Use FILE_LOCATIONS.md or search by filename

### Q: What's the difference between these docs?
**A:** 
- CUSTOMIZATIONS = Comprehensive reference (what was changed)
- QUICK_REFERENCE = Fast answers (how do I...)
- FILE_LOCATIONS = Navigation map (where is...)

### Q: What customizations are most important?
**A:** 
1. Makefile (saves time daily)
2. uncle-dev-next-task (automates work)
3. LOCAL_DEV_RUN.md (onboarding)
4. Theme updates (improved readability)

### Q: Can I modify these customizations?
**A:** Yes! They're designed to be extended. See QUICK_REFERENCE.md → "Adding Tools or Features"

### Q: How do I keep up with main branch?
**A:** See CUSTOMIZATIONS.md → Section 12 "Maintenance & Updates"

---

## 📞 Support & Questions

### Where to Look
| Question | Document | Section |
|----------|----------|---------|
| How do I set up? | LOCAL_DEV_RUN.md | Quick start |
| What is X? | CUSTOMIZATIONS.md | Specific section |
| Where is file Y? | FILE_LOCATIONS.md | Directory tree |
| How do I do task Z? | QUICK_REFERENCE.md | Fast Lookup |
| Show me an example | QUICK_REFERENCE.md | Common Workflows |

### Getting Help
1. Search the appropriate document above
2. Check QUICK_REFERENCE.md "Need Help" section
3. Review CUSTOMIZATIONS.md relevant section
4. Check LOCAL_DEV_RUN.md "Troubleshooting"

---

## 📊 Documentation Statistics

| Document | Size | Sections | Purpose |
|----------|------|----------|---------|
| CUSTOMIZATIONS.md | ~3000 | 13 | Complete reference |
| QUICK_REFERENCE.md | ~500 | 11 | Fast lookup |
| FILE_LOCATIONS.md | ~1500 | 9 | Navigation map |
| INDEX.md | ~800 | 11 | This guide |
| **Total** | **~5800** | **~44** | Full documentation |

---

## 🔄 Document Relationships

```
You Are Here (INDEX.md)
        ↓
    ┌───┴────────────────┐
    ↓                    ↓
CUSTOMIZATIONS.md   QUICK_REFERENCE.md
    ↓                    ↓
    └───┬────────────────┘
        ↓
   FILE_LOCATIONS.md
        ↓
   Actual Project Files
```

---

## 📝 Version & Updates

- **Created:** 2026-05-08 (Initial customizations rebase)
- **Updated:** 2026-05-22 (Skills and documentation added)
- **Documented:** 2026-05-22 (This index created)

## Related Git Commits

- `15b8a836` - Uncle-dev rebase customizations
- `756321d8` - Uncle-dev-next-task skill addition

---

## 🎯 Next Steps

**Choose based on your role:**

- 👨‍💻 **New Developer:** Read QUICK_REFERENCE.md then LOCAL_DEV_RUN.md
- 🔨 **Contributor:** Read CONTRIBUTING.md then CUSTOMIZATIONS.md
- 🎯 **Task Manager:** Read docs/development-process.md and QUICK_REFERENCE.md
- 🏗️ **Architect:** Read CUSTOMIZATIONS.md → Integration Points
- 🔍 **Explorer:** Start with CUSTOMIZATIONS.md, then dive into specific sections

---

**Happy developing! 🚀**

For questions, refer to the appropriate document above or check the "FAQ" section.

---

Last Updated: 2026-05-22  
Documentation Version: 1.0
