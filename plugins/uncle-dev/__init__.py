"""Uncle Dev plugin for Hermes Agent — registers all bundled skills."""

from pathlib import Path

_PLUGIN_DIR = Path(__file__).parent
_SKILLS_DIR = _PLUGIN_DIR / "skills"

# All skill directory names bundled in this plugin
_SKILLS = [
    "uncle-dev-acknowledge",
    "uncle-dev-api-and-interface-design",
    "uncle-dev-browser-testing-with-devtools",
    "uncle-dev-ci-cd-and-automation",
    "uncle-dev-code-context",
    "uncle-dev-code-review-and-quality",
    "uncle-dev-context-engineering",
    "uncle-dev-debug-error",
    "uncle-dev-deprecation-and-migration",
    "uncle-dev-dev-code-simplification",
    "uncle-dev-documentation-and-adrs",
    "uncle-dev-feature-map",
    "uncle-dev-frontend-ui-engineering",
    "uncle-dev-git-workflow-and-versioning",
    "uncle-dev-graphify-aware-analysis",
    "uncle-dev-idea-refine",
    "uncle-dev-incremental-implementation",
    "uncle-dev-knowledge-capture",
    "uncle-dev-knowledge-maintenance",
    "uncle-dev-next-task",
    "uncle-dev-performance-optimization",
    "uncle-dev-planning-and-task-breakdown",
    "uncle-dev-research",
    "uncle-dev-security-and-hardening",
    "uncle-dev-shipping-and-launch",
    "uncle-dev-source-driven-development",
    "uncle-dev-spec-driven-development",
    "uncle-dev-test-driven-development",
    "uncle-dev-using-agent-skills",]


def register(ctx):
    """Register all uncle-dev skills with Hermes."""
    for skill_name in _SKILLS:
        skill_md = _SKILLS_DIR / skill_name / "SKILL.md"
        if skill_md.exists():
            ctx.register_skill(skill_name, skill_md)
