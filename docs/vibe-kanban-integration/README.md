# Vibe-Kanban + Minimal-Claude Integration Guide

## Overview

This integration creates a fully automated development workflow that combines:
- **Vibe-Kanban** - Agent orchestration and task tracking
- **Minimal-Claude** - Code quality commands (/fix, /commit, /update-app)
- **Custom Skills** - /research, /implement, /cicd, /workflow-orchestrator
- **MCP Servers** - Exa (web research), Grep (code search), Git, Filesystem, Playwright
- **Automated Hooks** - pre-task, post-task, pre-commit (non-blocking)

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   VIBE-KANBAN UI                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Research │  │Implement │  │  CI/CD   │  │  Review  ││
│  │  Agent   │  │  Agent   │  │  Agent   │  │  Agent   ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘│
└───────┼────────────┼────────────┼────────────┼────────┘
        │            │            │            │
        └────────────┴────────────┴────────────┘
                             │
                    ┌────────▼────────┐
                    │  CLAUDE CODE    │
                    │  (Orchestrator) │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼────────┐  ┌───────▼────────┐  ┌───────▼────────┐
│   MCP SERVERS  │  │    SKILLS      │  │     HOOKS      │
│                │  │                │  │                │
│ • Exa          │  │ • /research    │  │ • pre-task     │
│ • Grep         │  │ • /implement   │  │ • post-task    │
│ • Filesystem   │  │ • /cicd        │  │ • pre-commit   │
│ • Git          │  │ • /orchestrate │  │                │
│ • Playwright   │  │ • /fix         │  │                │
└────────────────┘  └────────────────┘  └────────────────┘
```

## Automation Mode

**FULLY AUTOMATED** - No approval checkpoints:
- /research flows directly to /implement
- /implement auto-invokes /fix
- /cicd runs all validations automatically
- /commit auto-pushes without confirmation
- Hooks provide visibility but don't block execution
- Pause only on critical failures

## Quick Start

1. **Configure MCP Servers**: See `mcp-setup.md`
2. **Create Skills**: See `skills-guide.md`
3. **Setup Hooks**: See `hooks-guide.md`
4. **Configure Vibe-Kanban**: See `vibe-kanban-setup.md`
5. **Test Workflow**: Run `/workflow-orchestrator` to test full pipeline

## File Structure

```
repo-swarm/
├── .claude/
│   ├── settings.local.json          # MCP server configuration
│   ├── skills/                      # Custom skills
│   │   ├── research/SKILL.md
│   │   ├── implement/SKILL.md
│   │   ├── cicd/SKILL.md
│   │   └── workflow-orchestrator/SKILL.md
│   ├── hooks/                       # Automation hooks
│   │   ├── pre-task.md
│   │   ├── post-task.md
│   │   └── pre-commit.md
│   └── commands/                    # Enhanced minimal-claude commands
│       ├── fix.md
│       └── commit.md
├── docs/vibe-kanban-integration/    # This documentation
└── CLAUDE.md                         # Updated project guidelines
```

## Documentation Files

1. **README.md** (this file) - Overview and quick start
2. **mcp-setup.md** - MCP server configuration guide
3. **skills-guide.md** - Skills implementation guide
4. **hooks-guide.md** - Hooks setup guide
5. **vibe-kanban-setup.md** - Vibe-Kanban configuration
6. **implementation-checklist.md** - Step-by-step implementation
7. **troubleshooting.md** - Common issues and solutions

## Workflow Examples

### Example 1: New Feature
```bash
# User creates task in Vibe-Kanban
Task: "Add monorepo support"

# Vibe-Kanban spawns Research Agent
/research
  → Grep MCP: Searches codebase for repo patterns
  → Exa MCP: Researches monorepo best practices
  → Creates research brief
  → Automatically proceeds to /implement

# Vibe-Kanban spawns Implementation Agent
/implement
  → Creates monorepo_analyzer.py
  → Updates models
  → Adds tests
  → Auto-invokes /fix

# /fix runs automatically
  → mypy, ruff, black checks
  → Fixes all issues
  → All checks pass

# /cicd runs automatically
  → Validates workflows
  → Runs mise test-all
  → Checks Docker build

# /commit runs automatically
  → Git MCP: Analyzes changes
  → Exa MCP: Researches commit best practices
  → Generates: "feat: add monorepo analysis support"
  → Pushes to feature branch

# Vibe-Kanban updates task to Done
```

### Example 2: Bug Fix
```bash
Task: "Fix type error in investigator.py"

# Research phase (skips if simple fix)
/research
  → Grep MCP: Finds similar type errors
  → Brief: "Use Optional[str] for nullable fields"

# Implementation phase
/implement
  → Updates type hints
  → Adds validation

# Auto-fix
/fix
  → Runs mypy: 0 errors
  → Runs ruff: 0 warnings

# Commit
/commit
  → Generates: "fix: resolve type errors in investigator"
  → Pushes changes

# Task marked Done
```

## Next Steps

1. Read `implementation-checklist.md` for step-by-step setup
2. Configure MCP servers following `mcp-setup.md`
3. Create skills following `skills-guide.md`
4. Setup hooks following `hooks-guide.md`
5. Configure Vibe-Kanban following `vibe-kanban-setup.md`
6. Test with `/workflow-orchestrator`

## Support

If you encounter issues:
1. Check `troubleshooting.md` for common problems
2. Review plan file at `/home/codespace/.claude/plans/merry-crunching-fountain.md`
3. Verify all MCP servers are running: Check settings.local.json
4. Check Vibe-Kanban agent configuration

## Status

- [ ] MCP servers configured
- [ ] Skills created
- [ ] Hooks configured
- [ ] Vibe-Kanban agents setup
- [ ] Workflow tested
- [ ] Documentation complete

---

**Last Updated**: 2025-12-31
**Plan Location**: `/home/codespace/.claude/plans/merry-crunching-fountain.md`
