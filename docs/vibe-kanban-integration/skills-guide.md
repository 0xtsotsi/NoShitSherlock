# Skills Implementation Guide

## Overview

This guide covers creating and configuring custom Claude Code skills for the Vibe-Kanban + Minimal-Claude integration.

## Skills to Create

1. **/research** - Research patterns using Grep + Exa MCP
2. **/implement** - Implement features based on research
3. **/cicd** - Handle CI/CD pipelines and infrastructure
4. **/workflow-orchestrator** - Orchestrate complete workflow

## Directory Structure

```
/home/codespace/repo-swarm/.claude/skills/
├── research/
│   └── SKILL.md
├── implement/
│   └── SKILL.md
├── cicd/
│   └── SKILL.md
└── workflow-orchestrator/
    └── SKILL.md
```

## Skill 1: /research

**Purpose**: Use Grep and Exa MCP to research before implementing

**File**: `/home/codespace/repo-swarm/.claude/skills/research/SKILL.md`

```markdown
---
name: research
description: Research code patterns using Exa and Grep MCP before implementation
---

# Research Phase Agent

You are a research specialist. Your goal is to gather comprehensive information BEFORE any code implementation begins.

## Step 1: Use Grep MCP - Search Existing Code

Use the Grep MCP server to find:
- Similar implementations in the codebase
- Test patterns for the feature type
- Configuration files and conventions
- Error handling patterns

Search for:
- Relevant function/class names
- Similar file names or patterns
- Import statements that might be needed
- Test files that test similar functionality

## Step 2: Use Exa MCP - Web Research

Use Exa to research:
- Best practices for the technology stack
- Common patterns and libraries
- Documentation examples
- Community solutions
- Potential pitfalls and issues

Search for:
- Technology-specific best practices
- Library/framework documentation
- StackOverflow discussions
- GitHub issues and PRs
- Blog posts and tutorials

## Step 3: Synthesize Findings

Create a comprehensive research brief that includes:

### From Grep MCP (Local Codebase):
- Relevant code snippets (show file paths and line numbers)
- Existing patterns to follow
- Test patterns to emulate
- Configuration files to update
- Dependencies to add

### From Exa MCP (External):
- Best practices from documentation
- Common library recommendations
- Community patterns
- Known issues to avoid
- Alternative approaches

### Recommendations:
- Suggested implementation approach
- Files to create/modify
- Tests to write
- Dependencies to add
- Potential risks and mitigations

## Step 4: Present Research Brief

Share the research brief in this format:

```markdown
# Research Brief: [Feature Name]

## Local Patterns Found (Grep MCP)
- Similar implementation: `file/path:line`
- Test pattern: `test/file:path`
- Configuration: `config/file:path`

## External Best Practices (Exa MCP)
- Best practice 1
- Best practice 2
- Library recommendation: X

## Implementation Plan
1. Create: `new_file.py`
2. Modify: `existing_file.py` (add function X)
3. Add tests: `test_new_file.py`

## Dependencies
- Add: `package-name` (version)
- Update: `existing-package`

## Risks & Mitigations
- Risk: Description → Mitigation: Solution
```

## Automation Mode (FULLY AUTOMATED)

- Do NOT wait for user approval
- After presenting brief, automatically proceed to /implement
- Brief is logged for visibility but doesn't block execution
- Continue only on critical errors (e.g., conflicting information)

## Error Handling
- If Grep MCP fails: Continue with Exa only, note limitation
- If Exa MCP fails: Continue with Grep only, note limitation
- If both fail: Report error and pause
```

**Create the skill file**:

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/research
cat > /home/codespace/repo-swarm/.claude/skills/research/SKILL.md << 'EOF'
[Paste the markdown content above]
EOF
```

## Skill 2: /implement

**Purpose**: Implement features based on research findings

**File**: `/home/codespace/repo-swarm/.claude/skills/implement/SKILL.md`

```markdown
---
name: implement
description: Implement features based on research findings
---

# Implementation Phase Agent

You are an implementation specialist. Your goal is to write clean, tested code following existing patterns.

## Prerequisites
- /research must have been completed
- Research brief should be available

## Step 1: Plan Implementation

Based on research brief:
1. Identify files to modify/create
2. Define implementation order
3. Plan test strategy
4. Check for potential conflicts

## Step 2: Execute Implementation

Follow these rules:
- **Follow existing patterns** from codebase (found by /research)
- **Use mise.toml tasks** when available
- **Maintain consistency** with repo conventions
- **Write tests first** when possible (TDD approach)
- **Document changes** in code comments when complex

## Implementation Checklist:
- [ ] Create new files as planned
- [ ] Modify existing files
- [ ] Add/update imports
- [ ] Follow code style (ruff, black formatting)
- [ ] Add type hints
- [ ] Write docstrings
- [ ] Create/update tests
- [ ] Update configuration files if needed

## Step 3: Auto-Invoke /Fix Skill

After implementation, automatically invoke /fix:
- Runs type checking (mypy)
- Runs linting (ruff)
- Auto-fixes all issues
- Re-checks until clean

## Step 4: Create Tests

Add comprehensive tests:
- Unit tests for new modules
- Integration tests for workflows
- Update existing tests if needed
- Ensure all tests pass

## Step 5: Verification

Run test suite:
```bash
mise test-units
```

Only proceed if:
- All tests pass
- No type errors
- No lint warnings
- Code follows project conventions

## Automation Mode (FULLY AUTOMATED)

- Do NOT wait for user approval
- Auto-invoke /fix after implementation
- Auto-run tests
- Only pause on critical failures (test failures that can't be auto-fixed)

## Error Handling
- If tests fail: Try to fix, retry up to 3 times
- If type errors persist: Pause and report
- If implementation conflicts: Pause and report
- If /fix can't resolve: Pause and report with details

## Quality Standards
- Zero type errors (mypy)
- Zero lint warnings (ruff)
- All tests passing (pytest)
- Code formatted (black)
- Type hints on all functions
- Docstrings on public functions
```

**Create the skill file**:

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/implement
cat > /home/codespace/repo-swarm/.claude/skills/implement/SKILL.md << 'EOF'
[Paste the markdown content above]
EOF
```

## Skill 3: /cicd

**Purpose**: Handle CI/CD pipelines, deployments, and infrastructure

**File**: `/home/codespace/repo-swarm/.claude/skills/cicd/SKILL.md`

```markdown
---
name: cicd
description: Handle CI/CD pipelines, deployments, and infrastructure
---

# CI/CD Phase Agent

You are a DevOps specialist. Your goal is to ensure all code is deployment-ready.

## Prerequisites
- Implementation complete
- All tests passing
- Code reviewed and approved

## Step 1: Pipeline Configuration

Check and update CI configuration:

### GitHub Actions (if using):
- Check: `.github/workflows/*.yml`
- Validate: YAML syntax
- Verify: Action versions are current
- Test: Workflow triggers correctly

### Temporal Workflows (for this project):
- Check: `src/workflows/*.py`
- Validate: Workflow definitions
- Verify: Activity implementations
- Test: Workflow execution

### Docker Configuration:
- Check: `Dockerfile`
- Check: `docker-compose.yml`
- Validate: Docker build succeeds
- Verify: Multi-stage builds if used

## Step 2: Infrastructure as Code

Validate and update infrastructure:

### Environment Configuration:
- Check: `.env.example`
- Verify: All required variables documented
- Check: Default values are safe
- Validate: No secrets in example file

### Dependencies:
- Check: `pyproject.toml` (Python)
- Verify: All dependencies pinned
- Check: No vulnerable dependencies
- Update: If security patches available

### Deployment Scripts:
- Check: Deployment scripts exist
- Validate: Scripts work in test environment
- Verify: Rollback procedures

## Step 3: Comprehensive Testing

Run complete test suite:

```bash
# Unit tests
mise test-units

# Integration tests
mise test-all

# Docker build test
mise docker-test-build

# Linting and type checking
mise verify-config
ruff check src/
mypy src/
```

All must pass before proceeding.

## Step 4: Deployment Preparation

Prepare for deployment:

### Version Management:
- Check: Version numbers (if applicable)
- Update: CHANGELOG or release notes
- Tag: Create git tag if releasing

### Documentation:
- Update: API documentation
- Update: User guides
- Update: CLAUDE.md with new patterns

### Pre-Deployment Checks:
- [ ] All tests pass
- [ ] Docker build succeeds
- [ ] No security vulnerabilities
- [ ] Documentation updated
- [ ] Environment variables documented
- [ ] Migration scripts prepared (if needed)

## Step 5: Invoke /Commit

After all validations pass, invoke /commit to:
- Generate smart commit message
- Commit all changes
- Push to repository
- Trigger CI/CD pipeline

## Automation Mode (FULLY AUTOMATED)

- Do NOT wait for user approval
- Auto-run all tests
- Auto-invoke /commit when all checks pass
- Only pause on critical failures (pipeline breaks, security issues)

## Error Handling
- If tests fail: Investigate and fix
- If Docker build fails: Fix Dockerfile
- If security issues: Update dependencies
- If pipeline broken: Fix workflow configuration

## Deployment Readiness Criteria
✅ All tests passing (unit + integration)
✅ Docker build successful
✅ No security vulnerabilities
✅ Documentation updated
✅ Environment variables documented
✅ CI/CD pipelines validated
✅ Rollback plan ready
```

**Create the skill file**:

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/cicd
cat > /home/codespace/repo-swarm/.claude/skills/cicd/SKILL.md << 'EOF'
[Paste the markdown content above]
EOF
```

## Skill 4: /workflow-orchestrator

**Purpose**: Orchestrate complete Research → Implement → CI/CD workflow

**File**: `/home/codespace/repo-swarm/.claude/skills/workflow-orchestrator/SKILL.md`

```markdown
---
name: workflow-orchestrator
description: Orchestrate complete Research → Implement → CI/CD workflow
---

# Complete Workflow Orchestrator

You are the workflow orchestrator. Your goal is to coordinate all phases of development automatically.

## Phase 1: Research

1. Invoke `/research` skill
2. Monitor research progress
3. Review research brief
4. **NO APPROVAL NEEDED** - Automatically proceed to Phase 2
5. Log research brief for visibility

### Error Handling:
- If research fails completely: Pause and report
- If partial research: Log warning, continue with available data
- Retry once on transient failures

## Phase 2: Implementation

1. Invoke `/implement` skill
2. Monitor implementation progress
3. Track files created/modified
4. Auto-invoke `/fix` when implementation done
5. Verify all tests pass

### Error Handling:
- If /fix finds issues: Let it auto-resolve
- If tests fail: Retry up to 3 times
- If type errors persist: Pause and report
- If implementation conflicts: Pause and report

## Phase 3: CI/CD

1. Invoke `/cicd` skill
2. Validate pipeline configuration
3. Run comprehensive tests
4. Verify Docker build
5. Check for security issues
6. Prepare for deployment

### Error Handling:
- If tests fail: Run again, if still fails, pause
- If Docker build fails: Fix and retry
- If security issues: Update dependencies
- If pipeline broken: Fix workflow

## Phase 4: Finalization

1. Invoke `/commit` skill
2. Generate smart commit message
3. Commit all changes
4. Push to repository
5. Create pull request if needed
6. Update documentation

## Automation Mode (FULLY AUTOMATED)

- No user approval required at any phase
- Auto-proceed from research to implementation
- Auto-fix issues without asking
- Auto-commit and push changes
- Only pause on critical failures

## Progress Tracking

Log progress at each phase:

```
✅ Phase 1: Research Complete
   - Grep MCP: Found X patterns
   - Exa MCP: Researched Y topics
   - Brief created

⚙️  Phase 2: Implementation In Progress
   - Files created: X
   - Files modified: Y
   - Tests written: Z

✅ Phase 2: Implementation Complete
   - /fix run: 0 errors
   - Tests: All passing

⚙️  Phase 3: CI/CD In Progress
   - Pipeline validation: Pass
   - Docker build: Pass
   - Security check: Pass

✅ Phase 3: CI/CD Complete
   - All checks passed

⚙️  Phase 4: Finalization
   - Commit message generated
   - Changes pushed

✅ Workflow Complete
```

## Error Recovery

### Transient Failures (Retry)
- Network timeouts
- MCP server temporary unavailability
- Test flakiness

Retry up to 3 times with exponential backoff.

### Auto-Fixable Issues (Auto-Resolve)
- Type errors (use /fix)
- Lint warnings (use /fix)
- Format issues (use /fix)
- Dependency conflicts (update dependencies)

### Critical Failures (Pause and Report)
- Implementation conflicts with existing code
- Fundamental design issues
- Security vulnerabilities that can't be auto-fixed
- Test failures after 3 retries
- MCP servers completely unavailable

When paused, provide:
- Clear error description
- Phase where error occurred
- Steps already taken
- Recommended resolution
- Option to continue or abort

## Caching

Cache research results to avoid re-search:
- Research brief saved for session
- Implementation patterns cached
- Test results cached

## Logging

Comprehensive logging throughout:
- Every phase start/end
- Every skill invocation
- All errors and resolutions
- Final summary

## Final Summary

After completion, provide:

```markdown
# Workflow Complete ✅

## Research
- Grep MCP: X patterns found
- Exa MCP: Y topics researched
- Brief: [link to brief]

## Implementation
- Files created: [list]
- Files modified: [list]
- Tests written: [count]
- Type errors: 0
- Lint warnings: 0

## CI/CD
- Tests: All passing
- Docker build: Success
- Security: No issues
- Pipelines: Validated

## Commit
- Message: [commit message]
- Branch: [branch name]
- Push: Success

## Summary
- Total files changed: X
- Lines added: Y
- Lines removed: Z
- Tests added: N
- Duration: [time]
```
```

**Create the skill file**:

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator
cat > /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator/SKILL.md << 'EOF'
[Paste the markdown content above]
EOF
```

## Verification

After creating all skills, verify they're available:

1. **Restart Claude Code**
2. **Test each skill**:
   ```bash
   # Test research skill
   /research "Find examples of Temporal workflow patterns"

   # Test implement skill
   /implement "Create new activity handler"

   # Test cicd skill
   /cicd "Validate and prepare deployment"

   # Test orchestrator
   /workflow-orchestrator "Add monorepo support"
   ```

## Next Steps

After skills are created:

1. → Setup Hooks (see `hooks-guide.md`)
2. → Configure Vibe-Kanban (see `vibe-kanban-setup.md`)
3. → Test complete workflow

## Checklist

- [ ] Create research skill directory and SKILL.md
- [ ] Create implement skill directory and SKILL.md
- [ ] Create cicd skill directory and SKILL.md
- [ ] Create workflow-orchestrator skill directory and SKILL.md
- [ ] Verify skills are in correct location
- [ ] Restart Claude Code
- [ ] Test /research skill
- [ ] Test /implement skill
- [ ] Test /cicd skill
- [ ] Test /workflow-orchestrator skill
- [ ] Verify all skills work in automated mode

---

**Related Documentation**:
- MCP Setup: `mcp-setup.md`
- Hooks Guide: `hooks-guide.md`
- Vibe-Kanban Setup: `vibe-kanban-setup.md`
- Implementation Checklist: `implementation-checklist.md`
