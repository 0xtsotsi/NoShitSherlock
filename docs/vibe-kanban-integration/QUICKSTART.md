# Quick Start Guide - Vibe-Kanban + Minimal-Claude Integration

## 🎯 What You'll Get

A fully automated development workflow:
- ✅ **Intelligent Research** (Grep + Exa MCP) before implementing
- ✅ **Pattern-Based Implementation** following existing conventions
- ✅ **Automatic Quality Gates** (/fix runs on every change)
- ✅ **Comprehensive Testing** via /cicd skill
- ✅ **Smart Commits** with research-backed messages
- ✅ **Full Orchestration** via Vibe-Kanban agents

## 📁 Documentation Files

All documentation is in: `/home/codespace/repo-swarm/docs/vibe-kanban-integration/`

| File | Purpose | When to Read |
|------|---------|--------------|
| **README.md** | Overview and architecture | Start here |
| **QUICKSTART.md** | This file - Quick reference | Implementation time |
| **mcp-setup.md** | MCP server configuration | First step |
| **skills-guide.md** | Skills implementation | Second step |
| **hooks-guide.md** | Hooks setup | Third step |
| **vibe-kanban-setup.md** | Vibe-Kanban configuration | Fourth step |
| **implementation-checklist.md** | Step-by-step checklist | During implementation |
| **troubleshooting.md** | Problem solving | When issues occur |

## ⚡ Quick Start (5 Steps)

### Step 1: MCP Server Setup (10 min)
```bash
# Edit configuration
nano /home/codespace/repo-swarm/.claude/settings.local.json

# Add MCP servers (see mcp-setup.md for full config)
# Required: exa, grep, filesystem, git
# Optional: playwright

# Restart Claude Code
claude restart
```

**Verify**: Test MCP tools are available
**Guide**: `mcp-setup.md`

### Step 2: Create Skills (20 min)
```bash
# Create skill directories
mkdir -p /home/codespace/repo-swarm/.claude/skills/{research,implement,cicd,workflow-orchestrator}

# Create SKILL.md files (content in skills-guide.md)
# - research/SKILL.md
# - implement/SKILL.md
# - cicd/SKILL.md
# - workflow-orchestrator/SKILL.md
```

**Verify**: Test `/research`, `/implement`, `/cicd`, `/workflow-orchestrator`
**Guide**: `skills-guide.md`

### Step 3: Setup Hooks (15 min)
```bash
# Create hooks directory
mkdir -p /home/codespace/repo-swarm/.claude/hooks

# Create hook files (content in hooks-guide.md)
# - pre-task.md
# - post-task.md
# - pre-commit.md
```

**Verify**: Hooks trigger on task/commit actions
**Guide**: `hooks-guide.md`

### Step 4: Configure Vibe-Kanban (10 min)
```bash
# Edit Vibe-Kanban config
nano ~/.config/vibe-kanban/config.json

# Add agent profiles (see vibe-kanban-setup.md)
# - research agent (Sonnet + Grep/Exa)
# - implement agent (Opus + Filesystem/Git)
# - cicd agent (Sonnet + Git/Filesystem)
```

**Verify**: Create test task in Vibe-Kanban
**Guide**: `vibe-kanban-setup.md`

### Step 5: Test Workflow (10 min)
```bash
# Create test task in Vibe-Kanban
Task: "Test automated workflow"

# Or run directly
/workflow-orchestrator "Test the complete automated workflow"
```

**Expected Flow**:
1. Research (Grep + Exa) → Brief created
2. Implement (auto-invokes /fix) → Code written
3. CI/CD (tests + validation) → All checks pass
4. Commit (smart message) → Changes pushed

**Guide**: `implementation-checklist.md`

## 🔧 Configuration Files

### Files to Create/Modify

```
/home/codespace/repo-swarm/
├── .claude/
│   ├── settings.local.json          # ✏️ EDIT: Add MCP servers
│   ├── skills/                      # ✏️ CREATE: 4 skills
│   │   ├── research/SKILL.md
│   │   ├── implement/SKILL.md
│   │   ├── cicd/SKILL.md
│   │   └── workflow-orchestrator/SKILL.md
│   ├── hooks/                       # ✏️ CREATE: 3 hooks
│   │   ├── pre-task.md
│   │   ├── post-task.md
│   │   └── pre-commit.md
│   └── commands/                    # ✅ EXISTS: Already from minimal-claude
│       ├── fix.md
│       └── commit.md
├── CLAUDE.md                         # ✏️ UPDATE: Add workflow docs
└── docs/vibe-kanban-integration/     # ✅ CREATED: This documentation
```

## 📋 Implementation Checklist

Use `implementation-checklist.md` for detailed step-by-step tracking.

**Quick Checklist**:
- [ ] Backup existing configuration
- [ ] Configure MCP servers (Exa, Grep, Filesystem, Git)
- [ ] Create /research skill
- [ ] Create /implement skill
- [ ] Create /cicd skill
- [ ] Create /workflow-orchestrator skill
- [ ] Create pre-task hook
- [ ] Create post-task hook
- [ ] Create pre-commit hook
- [ ] Configure Vibe-Kanban agents
- [ ] Test complete workflow
- [ ] Update CLAUDE.md

## 🚀 Testing Your Setup

### Test 1: MCP Servers
```bash
# In Claude Code, test each MCP:
mcp__grep__searchGitHub("import.*temporal", language=["Python"])
mcp__web_reader__webReader("https://docs.exa.ai")
```

### Test 2: Skills
```bash
/research "How are Temporal activities structured?"
/implement "Add new activity handler"
/cicd "Validate current setup"
```

### Test 3: Complete Workflow
```bash
/workflow-orchestrator "Add a new repository type detector"
```

Expected result: Automated execution from research → implementation → testing → commit.

## 🎨 Architecture Diagram

```
User Request
     ↓
Vibe-Kanban Task
     ↓
┌─────────────────────────────────────┐
│  /workflow-orchestrator (auto)      │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  /research                          │
│  • Grep MCP (local codebase)        │
│  • Exa MCP (web research)           │
│  • Create brief                     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  /implement                         │
│  • Write code following patterns     │
│  • Auto-invoke /fix                 │
│  • Run tests                        │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  /fix (auto-triggered)              │
│  • mypy, ruff, black                │
│  • Auto-resolve issues              │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  /cicd                              │
│  • Test all                         │
│  • Validate pipelines               │
│  • Docker build                     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│  /commit                            │
│  • Git MCP: Analyze changes         │
│  • Exa MCP: Best practices          │
│  • Smart message                    │
│  • Push                             │
└──────────────┬──────────────────────┘
               ↓
        Task Complete ✅
```

## 🔍 Key Decisions

### Why Skills + Hooks + MCP?

| Component | Role | Example |
|-----------|------|---------|
| **Skills** | What agents can do | /research, /implement, /cicd |
| **Hooks** | When automation triggers | pre-task, post-task, pre-commit |
| **MCP** | Tools and capabilities | Exa, Grep, Git, Filesystem |

### Why Fully Automated?

- ✅ No approval checkpoints = faster development
- ✅ Hooks provide visibility without blocking
- ✅ Only pause on critical failures
- ✅ Rollback procedures available if needed

## 🆘 Troubleshooting

### Issue: MCP servers not starting
**Solution**: See `troubleshooting.md` - "MCP Server Issues"

### Issue: Skills not found
**Solution**: Verify SKILL.md files exist in `.claude/skills/*/SKILL.md`

### Issue: Vibe-Kanban agents not using skills
**Solution**: Check agent profiles in `vibe-kanban-setup.md`

### Issue: Workflow pauses unexpectedly
**Solution**: Check for critical errors in logs, see `troubleshooting.md`

## 📚 Additional Resources

### Plan File
- Location: `/home/codespace/.claude/plans/merry-crunching-fountain.md`
- Contains: Complete implementation plan and architecture

### GitHub Repositories
- Minimal-Claude: https://github.com/KenKaiii/minimal-claude
- Vibe-Kanban: https://github.com/BloopAI/vibe-kanban
- Exa MCP: https://docs.exa.ai/reference/exa-mcp

### Documentation
- Claude Code Skills: https://code.claude.com/docs/en/skills
- MCP Protocol: https://modelcontextprotocol.io/
- Vibe-Kanban Docs: https://www.vibekanban.com/

## ⏱️ Time Estimates

| Phase | Time | Dependencies |
|-------|------|--------------|
| MCP Setup | 10 min | None |
| Skills Creation | 20 min | MCP configured |
| Hooks Setup | 15 min | None |
| Vibe-Kanban Config | 10 min | None |
| Testing | 10 min | All above |
| **Total** | **~65 min** | **Sequential** |

## ✅ Success Criteria

When implementation is complete, you should have:

1. ✅ All 5 MCP servers running (Exa, Grep, Filesystem, Git, Playwright)
2. ✅ All 4 skills functional (/research, /implement, /cicd, /workflow-orchestrator)
3. ✅ All 3 hooks active (pre-task, post-task, pre-commit)
4. ✅ Vibe-Kanban agents configured and tested
5. ✅ Complete workflow tested end-to-end
6. ✅ Documentation reviewed
7. ✅ Rollback procedures documented

## 🎯 Next Steps

1. **Read** `implementation-checklist.md` for detailed steps
2. **Configure** MCP servers following `mcp-setup.md`
3. **Create** skills following `skills-guide.md`
4. **Setup** hooks following `hooks-guide.md`
5. **Configure** Vibe-Kanban following `vibe-kanban-setup.md`
6. **Test** complete workflow
7. **Deploy** to your team

## 📝 Notes

- **Fully Automated Mode**: No approvals needed, hooks don't block
- **Exa API Key**: Already configured in settings.local.json
- **Vibe-Kanban**: Already installed per your setup
- **Minimal-Claude**: Already provides /fix and /commit commands
- **Backup**: Always backup before modifying configuration

---

**Ready to implement?** Start with `implementation-checklist.md` for step-by-step instructions.

**Need help?** Check `troubleshooting.md` for common issues and solutions.

**Status**: Documentation complete ✅
**Last Updated**: 2025-12-31
**Implementation Time**: ~65 minutes
