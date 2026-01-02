# Vibe-Kanban Integration - Implementation Checklist

## Overview

This checklist provides a step-by-step guide to implement the complete Vibe-Kanban + Minimal-Claude integration. Each step includes exact commands, verification procedures, expected outputs, and troubleshooting tips.

**Estimated Time**: 45-60 minutes
**Difficulty**: Intermediate
**Prerequisites**: Claude Code installed, basic terminal knowledge

---

## Pre-Implementation Checklist

### Before You Start

- [ ] **Backup Current Configuration**
  ```bash
  cp ~/.claude/settings.local.json ~/.claude/settings.local.json.backup
  cp /home/codespace/repo-swarm/.claude/settings.local.json /home/codespace/repo-swarm/.claude/settings.local.json.backup
  ```
  **Why**: Safe rollback if something goes wrong

- [ ] **Verify Prerequisites**
  ```bash
  # Check Node.js and npm are installed (required for MCP servers)
  node --version  # Should be v18+ or v20+
  npm --version   # Should be v9+ or v10+

  # Check npx is available
  which npx

  # Check project structure
  ls -la /home/codespace/repo-swarm/.claude/
  ```
  **Expected Output**: Commands should return version numbers or show existing .claude directory

- [ ] **Verify Internet Connection**
  ```bash
  ping -c 3 google.com
  ```
  **Why**: Required to download MCP servers via npx

- [ ] **Check Available Disk Space**
  ```bash
  df -h /home/codespace
  ```
  **Expected**: At least 500MB free space for MCP server downloads

- [ ] **Read Documentation**
  - [ ] Read `README.md` - Overview and architecture
  - [ ] Read `mcp-setup.md` - MCP server details
  - [ ] Read `skills-guide.md` - Skills implementation details

**If any prerequisite fails**: Resolve before proceeding. See Troubleshooting section.

---

## Phase 1: MCP Setup

### Step 1.1: Create Directory Structure

```bash
# Create .claude directory if it doesn't exist
mkdir -p /home/codespace/repo-swarm/.claude
mkdir -p /home/codespace/repo-swarm/.claude/skills
mkdir -p /home/codespace/repo-swarm/.claude/hooks
mkdir -p /home/codespace/repo-swarm/.claude/commands
```

**Verification**:
```bash
ls -la /home/codespace/repo-swarm/.claude/
```
**Expected Output**: Should show skills/, hooks/, commands/ directories

**Common Issues**:
- If you get "Permission denied": Check directory ownership
- If directories already exist: That's fine, proceed to next step

---

### Step 1.2: Configure settings.local.json

Create or update `/home/codespace/repo-swarm/.claude/settings.local.json`:

```bash
cat > /home/codespace/repo-swarm/.claude/settings.local.json << 'EOF'
{
  "permissions": {
    "allow": [
      "Bash(ruff:*)",
      "Bash(pip install:*)",
      "Bash(mise:*)",
      "Bash(git:*)",
      "Bash(uv:*)",
      "Bash(temporal:*)",
      "Bash(mypy:*)",
      "Bash(black:*)",
      "Bash(pylint:*)",
      "Bash(pytest:*)",
      "Bash(python:*)",
      "Bash(docker:*)",
      "Bash(node:*)",
      "Bash(npx:*)",
      "Skill(fix)",
      "Skill(commit)",
      "Skill(update-app)",
      "Skill(research)",
      "Skill(implement)",
      "Skill(cicd)",
      "Skill(workflow-orchestrator)"
    ]
  },
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": [
        "-y",
        "exa-mcp-server",
        "api-key",
        "9b2f9ab7-c27c-4763-b0ef-2c743232dab9"
      ],
      "disabled": false
    },
    "grep": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-grep"],
      "disabled": false
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/codespace/repo-swarm"
      ],
      "disabled": false
    },
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "--repository",
        "/home/codespace/repo-swarm"
      ],
      "disabled": false
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"],
      "disabled": false
    }
  }
}
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/settings.local.json | python -m json.tool
```
**Expected Output**: Pretty-printed JSON with no syntax errors

**Common Issues**:
- JSON parse error: Check for missing commas or brackets
- File permission denied: Ensure you have write access to .claude directory

---

### Step 1.3: Test MCP Server Installation

Test each MCP server can be downloaded and started:

```bash
# Test Exa MCP (5-10 seconds)
echo "Testing Exa MCP..."
timeout 15 npx -y exa-mcp-server api-key 9b2f9ab7-c27c-4763-b0ef-2c743232dab9 --help 2>&1 | head -5

# Test Grep MCP (5-10 seconds)
echo "Testing Grep MCP..."
timeout 15 npx -y @modelcontextprotocol/server-grep --help 2>&1 | head -5

# Test Filesystem MCP (5-10 seconds)
echo "Testing Filesystem MCP..."
timeout 15 npx -y @modelcontextprotocol/server-filesystem --help 2>&1 | head -5

# Test Git MCP (5-10 seconds)
echo "Testing Git MCP..."
timeout 15 npx -y @modelcontextprotocol/server-git --help 2>&1 | head -5

# Test Playwright MCP (optional, 10-15 seconds)
echo "Testing Playwright MCP..."
timeout 20 npx -y @executeautomation/playwright-mcp-server --help 2>&1 | head -5
```

**Expected Output**: Each command should show help text or version info (not error messages)

**Verification Commands**:
```bash
# All should complete within timeout
# No "command not found" errors
# No "404 Not Found" errors
# No "EACCES" permission errors
```

**Common Issues**:
- **"npx: command not found"**: Install Node.js from https://nodejs.org
- **"404 Not Found"**: Check package name spelling, internet connection
- **"EACCES"**: Try `npm cache clean` or use `sudo` (not recommended)
- **Timeouts**: Slow internet, packages still downloading (retry)

---

### Step 1.4: Verify MCP Servers Are Loaded

Restart Claude Code to load the new configuration:

**If using Claude Code CLI**:
```bash
claude restart
```

**If using Claude Code Desktop**:
1. Quit the application completely
2. Reopen the application
3. Open the project: `/home/codespace/repo-swarm`

**Verification**:
In Claude Code, ask: "What MCP servers are available?"

**Expected Output**:
Should list: exa, grep, filesystem, git, playwright

**Common Issues**:
- MCP servers not showing: Check settings.local.json path is correct
- Some servers missing: Check for typos in server names
- "disabled": true in config: Change to false

---

## Phase 2: Skills Creation

### Step 2.1: Create /research Skill

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/research
cat > /home/codespace/repo-swarm/.claude/skills/research/SKILL.md << 'EOF'
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
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/skills/research/SKILL.md | head -20
```
**Expected Output**: Should show the skill markdown with frontmatter

**Common Issues**:
- File creation fails: Check directory permissions
- Empty file: Check command completed successfully

---

### Step 2.2: Create /implement Skill

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/implement
cat > /home/codespace/repo-swarm/.claude/skills/implement/SKILL.md << 'EOF'
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
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/skills/implement/SKILL.md | head -20
```
**Expected Output**: Should show the skill markdown with frontmatter

---

### Step 2.3: Create /cicd Skill

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/cicd
cat > /home/codespace/repo-swarm/.claude/skills/cicd/SKILL.md << 'EOF'
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
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/skills/cicd/SKILL.md | head -20
```
**Expected Output**: Should show the skill markdown with frontmatter

---

### Step 2.4: Create /workflow-orchestrator Skill

```bash
mkdir -p /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator
cat > /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator/SKILL.md << 'EOF'
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
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator/SKILL.md | head -20
```
**Expected Output**: Should show the skill markdown with frontmatter

---

### Step 2.5: Verify All Skills Created

```bash
# List all skill directories
ls -la /home/codespace/repo-swarm/.claude/skills/

# Verify each SKILL.md file exists
for skill in research implement cicd workflow-orchestrator; do
  echo "Checking $skill skill..."
  if [ -f "/home/codespace/repo-swarm/.claude/skills/$skill/SKILL.md" ]; then
    echo "✓ $skill/SKILL.md exists"
  else
    echo "✗ $skill/SKILL.md missing"
  fi
done
```

**Expected Output**:
```
drwxr-xr-x ... research
drwxr-xr-x ... implement
drwxr-xr-x ... cicd
drwxr-xr-x ... workflow-orchestrator
Checking research skill...
✓ research/SKILL.md exists
Checking implement skill...
✓ implement/SKILL.md exists
Checking cicd skill...
✓ cicd/SKILL.md exists
Checking workflow-orchestrator skill...
✓ workflow-orchestrator/SKILL.md exists
```

---

### Step 2.6: Restart Claude Code and Test Skills

**Restart Claude Code**:
```bash
claude restart
```

Or restart the Claude Code desktop application.

**Test Each Skill in Claude Code**:

1. **Test /research skill**:
   - Ask: "Run /research to find examples of Temporal workflow patterns"
   - Expected: Skill executes, uses Grep and Exa MCP

2. **Test /implement skill**:
   - Ask: "Run /implement to create a simple test function"
   - Expected: Skill creates code, runs /fix automatically

3. **Test /cicd skill**:
   - Ask: "Run /cicd to validate current state"
   - Expected: Skill runs tests, validates configuration

4. **Test /workflow-orchestrator**:
   - Ask: "Run /workflow-orchestrator to add a simple logging function"
   - Expected: Full workflow executes end-to-end

**Common Issues**:
- **"Skill not found"**: Restart Claude Code, check file paths
- **"MCP tool not available"**: Verify MCP servers loaded (Phase 1)
- **Skill hangs**: Check MCP server is running, check internet connection

---

## Phase 3: Hooks Setup

### Step 3.1: Create pre-task Hook

```bash
cat > /home/codespace/repo-swarm/.claude/hooks/pre-task.md << 'EOF'
# Pre-Task Hook

This hook runs before any task begins.

## Purpose
- Log task start
- Check git status
- Verify environment
- Document starting state

## Actions

1. Log current timestamp and task description
2. Check git status: `git status --short`
3. Verify MCP servers are available
4. Check for uncommitted changes
5. Document current branch

## Non-Blocking
This hook provides visibility but should NOT block task execution.
Continue even if checks fail, but log warnings.

## Output Format

```markdown
## Pre-Task Check
- Time: [timestamp]
- Task: [task description]
- Branch: [current branch]
- Git Status: [clean/dirty]
- MCP Servers: [available/unavailable]
- Uncommitted Changes: [yes/no]
```
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/hooks/pre-task.md
```
**Expected Output**: Should show the hook markdown content

---

### Step 3.2: Create post-task Hook

```bash
cat > /home/codespace/repo-swarm/.claude/hooks/post-task.md << 'EOF'
# Post-Task Hook

This hook runs after any task completes.

## Purpose
- Log task completion
- Show git diff summary
- List files changed
- Suggest next actions

## Actions

1. Log completion timestamp
2. Show git diff: `git diff --stat`
3. List modified files
4. Check if tests pass
5. Suggest /commit if changes made

## Non-Blocking
This hook provides visibility but should NOT block.
Report status but don't require action.

## Output Format

```markdown
## Post-Task Summary
- Time: [timestamp]
- Duration: [time elapsed]
- Files Modified: [count]
- Lines Added: [count]
- Lines Removed: [count]
- Test Status: [pass/fail/not run]
- Suggested Next Step: [commit/research/implement/etc]
```
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/hooks/post-task.md
```
**Expected Output**: Should show the hook markdown content

---

### Step 3.3: Create pre-commit Hook

```bash
cat > /home/codespace/repo-swarm/.claude/hooks/pre-commit.md << 'EOF'
# Pre-Commit Hook

This hook runs before committing changes.

## Purpose
- Verify code quality
- Run quick checks
- Ensure tests pass
- Document commit contents

## Actions

1. Check for TODO/FIXME comments
2. Verify no console.log or debug prints
3. Check file sizes (warn if > 500 lines added)
4. Verify tests pass: `mise test-units`
5. Check type safety: `mypy src/`

## Non-Blocking
This hook provides visibility but should NOT block commits.
Report issues but allow commit to proceed.

## Warnings to Report

```markdown
## Pre-Commit Check
- Tests: [passing/failing/skipped]
- Type Check: [passing/failing]
- Lint Check: [passing/failing]
- Debug Code Found: [yes/no]
- Large Files: [yes/no]
- TODOs Added: [count]

⚠️  Warnings (if any):
- [List warnings]

✓ Ready to commit
```
EOF
```

**Verification**:
```bash
cat /home/codespace/repo-swarm/.claude/hooks/pre-commit.md
```
**Expected Output**: Should show the hook markdown content

---

### Step 3.4: Verify All Hooks Created

```bash
# List all hooks
ls -la /home/codespace/repo-swarm/.claude/hooks/

# Verify each hook file exists
for hook in pre-task post-task pre-commit; do
  echo "Checking $hook hook..."
  if [ -f "/home/codespace/repo-swarm/.claude/hooks/$hook.md" ]; then
    echo "✓ $hook.md exists"
  else
    echo "✗ $hook.md missing"
  fi
done
```

**Expected Output**:
```
-rw-r--r-- ... pre-task.md
-rw-r--r-- ... post-task.md
-rw-r--r-- ... pre-commit.md
Checking pre-task hook...
✓ pre-task.md exists
Checking post-task hook...
✓ post-task.md exists
Checking pre-commit hook...
✓ pre-commit.md exists
```

**Common Issues**:
- Hooks not executing: Restart Claude Code
- Hooks blocking execution: Verify "Non-Blocking" section in hook files
- Hook output not showing: Check Claude Code logs

---

## Phase 4: Vibe-Kanban Configuration

### Step 4.1: Verify Vibe-Kanban Installation

```bash
# Check if Vibe-Kanban is installed
which vibe-kanban

# Or check if it's available as a module
python -c "import vibe_kanban; print(vibe_kanban.__version__)" 2>/dev/null || echo "Not installed as Python module"

# Check for Vibe-Kanban configuration files
find /home/codespace -name "*vibe*kanban*" -o -name "*kanban*.json" 2>/dev/null | head -10
```

**Expected Output**:
- If installed: Shows path to vibe-kanban executable or version info
- If not installed: Install instructions will be provided

**If Vibe-Kanban is not installed**:
1. Visit Vibe-Kanban installation guide (documentation link)
2. Install Vibe-Kanban following official instructions
3. Return to this checklist

---

### Step 4.2: Create Agent Profiles

Create Vibe-Kanban agent configurations for each agent type:

```bash
# Create Vibe-Kanban config directory
mkdir -p /home/codespace/repo-swarm/.vibe-kanban/agents

# Create Research Agent profile
cat > /home/codespace/repo-swarm/.vibe-kanban/agents/research-agent.json << 'EOF'
{
  "name": "Research Agent",
  "type": "research",
  "description": "Researches code patterns using Grep and Exa MCP",
  "skills": ["research"],
  "mcp_tools": ["grep_search", "web_search_exa"],
  "permissions": [
    "read_files",
    "search_code",
    "web_search"
  ],
  "automation": "full",
  "next_agent": "implement",
  "triggers": ["task_created", "feature_requested"]
}
EOF

# Create Implementation Agent profile
cat > /home/codespace/repo-swarm/.vibe-kanban/agents/implement-agent.json << 'EOF'
{
  "name": "Implementation Agent",
  "type": "implement",
  "description": "Implements features based on research findings",
  "skills": ["implement", "fix"],
  "mcp_tools": ["filesystem", "git"],
  "permissions": [
    "read_files",
    "write_files",
    "run_tests",
    "execute_commands"
  ],
  "automation": "full",
  "next_agent": "cicd",
  "triggers": ["research_complete"],
  "auto_fix": true
}
EOF

# Create CI/CD Agent profile
cat > /home/codespace/repo-swarm/.vibe-kanban/agents/cicd-agent.json << 'EOF'
{
  "name": "CI/CD Agent",
  "type": "cicd",
  "description": "Handles CI/CD pipelines and deployments",
  "skills": ["cicd"],
  "mcp_tools": ["git", "filesystem"],
  "permissions": [
    "read_files",
    "run_tests",
    "execute_commands",
    "deploy"
  ],
  "automation": "full",
  "next_agent": "commit",
  "triggers": ["implementation_complete"],
  "validations": [
    "all_tests_passing",
    "docker_build_success",
    "no_security_issues"
  ]
}
EOF

# Create Review Agent profile
cat > /home/codespace/repo-swarm/.vibe-kanban/agents/review-agent.json << 'EOF'
{
  "name": "Review Agent",
  "type": "review",
  "description": "Reviews changes and prepares for commit",
  "skills": ["commit"],
  "mcp_tools": ["git_diff", "git_log"],
  "permissions": [
    "read_files",
    "review_changes",
    "commit",
    "push"
  ],
  "automation": "full",
  "triggers": ["cicd_complete"],
  "auto_commit": true,
  "auto_push": true
}
EOF
```

**Verification**:
```bash
# Verify all agent profiles created
ls -la /home/codespace/repo-swarm/.vibe-kanban/agents/

# Validate JSON syntax
for agent in research-agent implement-agent cicd-agent review-agent; do
  echo "Validating $agent.json..."
  python -m json.tool /home/codespace/repo-swarm/.vibe-kanban/agents/$agent.json > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"
done
```

**Expected Output**:
```
-rw-r--r-- ... research-agent.json
-rw-r--r-- ... implement-agent.json
-rw-r--r-- ... cicd-agent.json
-rw-r--r-- ... review-agent.json
Validating research-agent.json...
✓ Valid JSON
Validating implement-agent.json...
✓ Valid JSON
Validating cicd-agent.json...
✓ Valid JSON
Validating review-agent.json...
✓ Valid JSON
```

---

### Step 4.3: Create Workflow Configuration

```bash
# Create Vibe-Kanban workflow config
cat > /home/codespace/repo-swarm/.vibe-kanban/workflows/default.json << 'EOF'
{
  "name": "Default Development Workflow",
  "version": "1.0",
  "description": "Fully automated development workflow from research to deployment",

  "agents": [
    {
      "order": 1,
      "agent": "research-agent",
      "name": "Research",
      "trigger": "task_start",
      "timeout": 300,
      "retry_on_failure": true,
      "max_retries": 2
    },
    {
      "order": 2,
      "agent": "implement-agent",
      "name": "Implement",
      "trigger": "research_complete",
      "timeout": 600,
      "retry_on_failure": true,
      "max_retries": 3,
      "dependencies": ["research_complete"]
    },
    {
      "order": 3,
      "agent": "cicd-agent",
      "name": "CI/CD",
      "trigger": "implementation_complete",
      "timeout": 400,
      "retry_on_failure": true,
      "max_retries": 2,
      "dependencies": ["implementation_complete", "tests_passing"]
    },
    {
      "order": 4,
      "agent": "review-agent",
      "name": "Review & Commit",
      "trigger": "cicd_complete",
      "timeout": 120,
      "retry_on_failure": false,
      "dependencies": ["cicd_complete", "all_checks_passing"]
    }
  ],

  "automation_settings": {
    "mode": "full_auto",
    "approval_checkpoints": [],
    "pause_on_critical_failure": true,
    "continue_on_warnings": true,
    "auto_fix_issues": true
  },

  "notifications": {
    "on_start": true,
    "on_complete": true,
    "on_failure": true,
    "on_phase_change": true
  }
}
EOF
```

**Verification**:
```bash
# Validate workflow JSON
python -m json.tool /home/codespace/repo-swarm/.vibe-kanban/workflows/default.json > /dev/null && echo "✓ Workflow config valid" || echo "✗ Invalid JSON"
```

**Expected Output**: `✓ Workflow config valid`

---

### Step 4.4: Test Vibe-Kanban Configuration

```bash
# If Vibe-Kanban has a test command
vibe-kanban test-config --path /home/codespace/repo-swarm/.vibe-kanban 2>/dev/null || echo "Test command not available or Vibe-Kanban not installed"

# Alternative: Verify config files exist and are valid JSON
echo "Checking Vibe-Kanban configuration..."
find /home/codespace/repo-swarm/.vibe-kanban -name "*.json" -exec echo "Found: {}" \; | wc -l
echo "Configuration files found."
```

**Expected Output**:
```
Checking Vibe-Kanban configuration...
5
Configuration files found.
```

**Common Issues**:
- **"Vibe-Kanban not found"**: Install Vibe-Kanban first
- **"Invalid JSON"**: Check syntax in agent profiles
- **"Config not loading"**: Verify file paths are correct

---

## Phase 5: Testing

### Step 5.1: Quick MCP Server Test

Test each MCP server is responding:

**In Claude Code**, ask:

1. **Test Grep MCP**:
   ```
   Use Grep MCP to search for "def main" in the codebase
   ```
   **Expected**: Returns list of files containing "def main"

2. **Test Exa MCP**:
   ```
   Use Exa MCP to search for "Python Temporal workflow best practices"
   ```
   **Expected**: Returns search results with web links

3. **Test Git MCP**:
   ```
   Use Git MCP to show recent commit history
   ```
   **Expected**: Returns git log with recent commits

4. **Test Filesystem MCP**:
   ```
   Use Filesystem MCP to list files in src/
   ```
   **Expected**: Returns directory listing of src/

---

### Step 5.2: Test Individual Skills

**Test /research skill**:

```bash
# In Claude Code, run:
/research "Find examples of Python activity implementations in this codebase"
```

**Expected Output**:
- Uses Grep to find activity files
- Uses Exa to research best practices
- Presents research brief
- Proceeds to suggest next steps

**Verification Checklist**:
- [ ] Grep MCP was used
- [ ] Exa MCP was used
- [ ] Research brief was presented
- [ ] No blocking errors occurred

---

**Test /implement skill**:

First create a simple test scenario:

```bash
# In Claude Code, run:
/implement "Create a simple hello_world() function in src/test_hello.py that returns a greeting string"
```

**Expected Output**:
- Creates src/test_hello.py
- Implements hello_world() function
- Auto-invokes /fix
- Runs tests
- All checks pass

**Verification Checklist**:
- [ ] File created successfully
- [ ] Function implemented
- [ ] /fix was auto-invoked
- [ ] Type checking passed
- [ ] Linting passed
- [ ] Tests created and passing

---

**Test /cicd skill**:

```bash
# In Claude Code, run:
/cicd "Validate current project state for deployment"
```

**Expected Output**:
- Runs all tests
- Validates Docker build
- Checks security
- Reports deployment readiness

**Verification Checklist**:
- [ ] Tests executed
- [ ] Docker build tested
- [ ] Security checks run
- [ ] Deployment readiness reported

---

**Test /workflow-orchestrator**:

```bash
# In Claude Code, run:
/workflow-orchestrator "Add a simple logging function that logs to both console and file"
```

**Expected Output**:
- Phase 1: Research complete (Grep + Exa)
- Phase 2: Implementation complete (with /fix)
- Phase 3: CI/CD validation complete
- Phase 4: Commit complete
- Final summary presented

**Verification Checklist**:
- [ ] All 4 phases executed
- [ ] No manual approval required
- [ ] Research brief logged
- [ ] Code implemented
- [ ] Tests passing
- [ ] Changes committed
- [ ] Final summary provided

---

### Step 5.3: Test Hooks

Test that hooks are executing:

1. **Test pre-task hook**:
   - Start any task
   - Check for pre-task output
   - Should see: Time, task, branch, git status

2. **Test post-task hook**:
   - Complete any task that makes changes
   - Check for post-task output
   - Should see: Duration, files changed, suggestions

3. **Test pre-commit hook**:
   - Run /commit or make changes then commit
   - Check for pre-commit output
   - Should see: Tests, type check, warnings

**Verification Checklist**:
- [ ] pre-task hook executes before tasks
- [ ] post-task hook executes after tasks
- [ ] pre-commit hook executes before commits
- [ ] Hooks are non-blocking (don't stop execution)
- [ ] Hook output is visible in logs

---

### Step 5.4: End-to-End Workflow Test

Run a complete end-to-end test:

```bash
# In Claude Code, run:
/workflow-orchestrator "Add a new utility function to calculate file hash in src/utils/file_utils.py with tests"
```

**Expected Flow**:

1. **Research Phase** (2-3 minutes):
   - Grep finds similar utility functions
   - Exa researches Python file hashing best practices
   - Research brief presented
   - Auto-proceeds to implementation

2. **Implementation Phase** (3-5 minutes):
   - Creates/modifies src/utils/file_utils.py
   - Implements hash calculation function
   - Auto-invokes /fix
   - /fix runs mypy, ruff, black
   - Creates tests in tests/test_file_utils.py
   - Runs tests

3. **CI/CD Phase** (2-3 minutes):
   - Runs test suite
   - Validates configuration
   - Checks Docker build
   - Reports deployment ready

4. **Commit Phase** (1 minute):
   - Generates commit message
   - Commits changes
   - Pushes to repository

**Final Summary**:
```
✅ Workflow Complete
- Research: Completed
- Implementation: Completed
- CI/CD: All checks passing
- Commit: Pushed to main
- Duration: ~10 minutes
```

**Verification Checklist**:
- [ ] All phases executed automatically
- [ ] No manual approval needed
- [ ] All tests passing
- [ ] No type errors
- [ ] No lint warnings
- [ ] Changes committed and pushed
- [ ] Hooks executed at each stage

---

## Rollback Procedures

### If MCP Servers Fail to Start

**Symptoms**: MCP tools not available, errors in logs

**Rollback Steps**:

1. **Restore backup configuration**:
   ```bash
   cp ~/.claude/settings.local.json.backup ~/.claude/settings.local.json
   cp /home/codespace/repo-swarm/.claude/settings.local.json.backup /home/codespace/repo-swarm/.claude/settings.local.json
   ```

2. **Restart Claude Code**:
   ```bash
   claude restart
   ```

3. **Verify original state**:
   - Check MCP servers are restored to previous state
   - Test basic functionality

---

### If Skills Don't Work

**Symptoms**: "Skill not found" errors, skills don't execute

**Rollback Steps**:

1. **Remove custom skills**:
   ```bash
   rm -rf /home/codespace/repo-swarm/.claude/skills/research
   rm -rf /home/codespace/repo-swarm/.claude/skills/implement
   rm -rf /home/codespace/repo-swarm/.claude/skills/cicd
   rm -rf /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator
   ```

2. **Restart Claude Code**:
   ```bash
   claude restart
   ```

3. **Verify**: Only default skills (fix, commit, update-app) remain

---

### If Hooks Cause Issues

**Symptoms**: Tasks hang, hooks blocking execution

**Rollback Steps**:

1. **Disable hooks temporarily**:
   ```bash
   mv /home/codespace/repo-swarm/.claude/hooks/pre-task.md /home/codespace/repo-swarm/.claude/hooks/pre-task.md.disabled
   mv /home/codespace/repo-swarm/.claude/hooks/post-task.md /home/codespace/repo-swarm/.claude/hooks/post-task.md.disabled
   mv /home/codespace/repo-swarm/.claude/hooks/pre-commit.md /home/codespace/repo-swarm/.claude/hooks/pre-commit.md.disabled
   ```

2. **Restart Claude Code**:
   ```bash
   claude restart
   ```

3. **Test**: Tasks should work normally without hooks

---

### If Vibe-Kanban Integration Fails

**Symptoms**: Vibe-Kanban errors, agents not spawning

**Rollback Steps**:

1. **Remove Vibe-Kanban configuration**:
   ```bash
   mv /home/codespace/repo-swarm/.vibe-kanban /home/codespace/repo-swarm/.vibe-kanban.backup
   ```

2. **Continue using Claude Code directly**:
   - Skills will still work
   - MCP servers will still work
   - Just won't have Vibe-Kanban orchestration

3. **Partial Rollback (keep skills, remove Vibe-Kanban)**:
   - Skills and MCP servers work independently
   - Can invoke skills manually without Vibe-Kanban

---

### Complete Rollback

To completely undo all changes and return to original state:

```bash
# 1. Restore settings.local.json
cp ~/.claude/settings.local.json.backup ~/.claude/settings.local.json
cp /home/codespace/repo-swarm/.claude/settings.local.json.backup /home/codespace/repo-swarm/.claude/settings.local.json

# 2. Remove custom skills
rm -rf /home/codespace/repo-swarm/.claude/skills/research
rm -rf /home/codespace/repo-swarm/.claude/skills/implement
rm -rf /home/codespace/repo-swarm/.claude/skills/cicd
rm -rf /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator

# 3. Remove hooks
rm -rf /home/codespace/repo-swarm/.claude/hooks/*.md

# 4. Remove Vibe-Kanban config
rm -rf /home/codespace/repo-swarm/.vibe-kanban

# 5. Restart Claude Code
claude restart

# 6. Verify
echo "Rollback complete. Original state restored."
```

---

## Verification

### Phase 1 Verification: MCP Setup

- [ ] settings.local.json created with all 5 MCP servers
- [ ] JSON syntax is valid (no parse errors)
- [ ] Each MCP server can be downloaded via npx
- [ ] Claude Code restart completed
- [ ] MCP tools are available in Claude Code
- [ ] Grep MCP can search codebase
- [ ] Exa MCP can search web
- [ ] Git MCP can show repository status
- [ ] Filesystem MCP can list directories
- [ ] Playwright MCP available (optional)

**Test Command**:
```bash
cat /home/codespace/repo-swarm/.claude/settings.local.json | python -m json.tool > /dev/null && echo "✓ MCP config valid"
```

---

### Phase 2 Verification: Skills Creation

- [ ] research/SKILL.md created
- [ ] implement/SKILL.md created
- [ ] cicd/SKILL.md created
- [ ] workflow-orchestrator/SKILL.md created
- [ ] All skills have valid frontmatter (name, description)
- [ ] Claude Code restarted after skill creation
- [ ] /research skill executes successfully
- [ ] /implement skill executes successfully
- [ ] /cicd skill executes successfully
- [ ] /workflow-orchestrator executes successfully

**Test Command**:
```bash
for skill in research implement cicd workflow-orchestrator; do
  [ -f "/home/codespace/repo-swarm/.claude/skills/$skill/SKILL.md" ] && echo "✓ $skill skill exists" || echo "✗ $skill skill missing"
done
```

---

### Phase 3 Verification: Hooks Setup

- [ ] pre-task.md hook created
- [ ] post-task.md hook created
- [ ] pre-commit.md hook created
- [ ] Hooks are non-blocking (documented)
- [ ] Hooks execute at appropriate times
- [ ] Hook output is visible
- [ ] Hooks don't block workflow execution

**Test Command**:
```bash
for hook in pre-task post-task pre-commit; do
  [ -f "/home/codespace/repo-swarm/.claude/hooks/$hook.md" ] && echo "✓ $hook hook exists" || echo "✗ $hook hook missing"
done
```

---

### Phase 4 Verification: Vibe-Kanban Configuration

- [ ] .vibe-kanban directory created
- [ ] research-agent.json profile created
- [ ] implement-agent.json profile created
- [ ] cicd-agent.json profile created
- [ ] review-agent.json profile created
- [ ] default.json workflow created
- [ ] All agent profiles have valid JSON
- [ ] Workflow configuration has valid JSON
- [ ] Vibe-Kanban recognizes configuration (if installed)

**Test Command**:
```bash
find /home/codespace/repo-swarm/.vibe-kanban -name "*.json" -exec python -m json.tool {} \; > /dev/null 2>&1 && echo "✓ All Vibe-Kanban configs valid" || echo "✗ Some configs invalid"
```

---

### Phase 5 Verification: Testing

- [ ] All MCP servers respond to test queries
- [ ] /research skill works with MCP tools
- [ ] /implement skill creates code and auto-invokes /fix
- [ ] /cicd skill runs all validations
- [ ] /workflow-orchestrator completes full workflow
- [ ] Hooks execute at appropriate times
- [ ] End-to-end workflow test succeeds
- [ ] All tests passing
- [ ] No type errors
- [ ] No lint warnings
- [ ] Changes commit and push successfully

**Final Test Command**:
```bash
# Run this in Claude Code to verify everything
/workflow-orchestrator "Create a simple test function to verify integration"
```

**Expected Result**: Full workflow completes without manual intervention

---

## Completion Checklist

### Pre-Implementation
- [ ] Backed up existing configuration
- [ ] Verified all prerequisites (Node.js, npm, npx)
- [ ] Checked internet connection
- [ ] Read all documentation

### Phase 1: MCP Setup
- [ ] Created .claude directory structure
- [ ] Configured settings.local.json with all MCP servers
- [ ] Tested each MCP server individually
- [ ] Verified MCP servers are loaded in Claude Code

### Phase 2: Skills Creation
- [ ] Created /research skill
- [ ] Created /implement skill
- [ ] Created /cicd skill
- [ ] Created /workflow-orchestrator skill
- [ ] Tested all skills individually

### Phase 3: Hooks Setup
- [ ] Created pre-task hook
- [ ] Created post-task hook
- [ ] Created pre-commit hook
- [ ] Verified hooks execute

### Phase 4: Vibe-Kanban Configuration
- [ ] Created research agent profile
- [ ] Created implement agent profile
- [ ] Created cicd agent profile
- [ ] Created review agent profile
- [ ] Created default workflow configuration
- [ ] Validated all configurations

### Phase 5: Testing
- [ ] Tested all MCP servers
- [ ] Tested all skills individually
- [ ] Tested hooks
- [ ] Completed end-to-end workflow test

### Final Verification
- [ ] All components working together
- [ ] Full automation mode functional
- [ ] Rollback procedures documented
- [ ] Documentation complete

---

## Success Criteria

You have successfully completed the implementation when:

1. **MCP Servers**: All 5 MCP servers are loaded and responsive
2. **Skills**: All 4 custom skills execute without errors
3. **Hooks**: All 3 hooks provide visibility without blocking
4. **Vibe-Kanban**: Agent profiles and workflow configured (if using Vibe-Kanban)
5. **End-to-End**: `/workflow-orchestrator` completes full workflow automatically
6. **Quality**: All tests pass, no type errors, no lint warnings
7. **Automation**: No manual approval required from start to commit

**Test Success**:
```bash
# In Claude Code, run this final test:
/workflow-orchestrator "Add a simple greeting function with tests and documentation"

# Should complete in 10-15 minutes with:
# ✅ All phases complete
# ✅ All tests passing
# ✅ Changes committed and pushed
# ✅ No manual intervention required
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: MCP servers not loading

**Symptoms**: MCP tools not available in Claude Code

**Solutions**:
1. Check settings.local.json path is correct
2. Verify JSON syntax is valid
3. Restart Claude Code completely
4. Check npx can download packages
5. Verify internet connection

#### Issue: Skills not found

**Symptoms**: "Skill not found" error when invoking skills

**Solutions**:
1. Verify skills are in correct directory: `/home/codespace/repo-swarm/.claude/skills/`
2. Check SKILL.md files exist for each skill
3. Restart Claude Code
4. Verify skill frontmatter is valid

#### Issue: Hooks blocking execution

**Symptoms**: Workflow hangs, tasks don't complete

**Solutions**:
1. Check hooks don't have blocking logic
2. Verify hooks have "Non-Blocking" section
3. Temporarily disable hooks to test
4. Check hook output for errors

#### Issue: Workflow not fully automated

**Symptoms**: Workflow pauses for approval

**Solutions**:
1. Check skills have "Automation Mode (FULLY AUTOMATED)" section
2. Verify no approval checkpoints in Vibe-Kanban config
3. Check for user prompts in skill definitions
4. Verify "automation": "full" in agent profiles

#### Issue: Tests failing

**Symptoms**: Test failures during implementation

**Solutions**:
1. Check if tests exist for the feature
2. Verify test dependencies are installed
3. Run tests manually to see full error output
4. Check /fix skill is being invoked
5. Review implementation for bugs

---

## Additional Resources

### Documentation

- **MCP Protocol**: https://modelcontextprotocol.io
- **Exa MCP**: https://docs.exa.ai/reference/exa-mcp
- **Claude Code**: https://docs.anthropic.com/claude-code
- **Vibe-Kanban**: Check project documentation

### Configuration Files Reference

- **MCP Config**: `/home/codespace/repo-swarm/.claude/settings.local.json`
- **Skills**: `/home/codespace/repo-swarm/.claude/skills/*/SKILL.md`
- **Hooks**: `/home/codespace/repo-swarm/.claude/hooks/*.md`
- **Commands**: `/home/codespace/repo-swarm/.claude/commands/*.md`
- **Vibe-Kanban**: `/home/codespace/repo-swarm/.vibe-kanban/`

### Support

If you encounter issues not covered in this checklist:

1. Check the main documentation files in `/home/codespace/repo-swarm/docs/vibe-kanban-integration/`
2. Review the plan file at `/home/codespace/.claude/plans/merry-crunching-fountain.md`
3. Use rollback procedures to restore previous state
4. Check Claude Code logs for detailed error messages

---

## Quick Reference Commands

### Verify Everything is Working

```bash
# Check MCP config
cat /home/codespace/repo-swarm/.claude/settings.local.json | python -m json.tool

# List all skills
ls -la /home/codespace/repo-swarm/.claude/skills/

# List all hooks
ls -la /home/codespace/repo-swarm/.claude/hooks/

# List Vibe-Kanban configs
find /home/codespace/repo-swarm/.vibe-kanban -name "*.json"

# Test MCP servers
npx -y @modelcontextprotocol/server-grep --help
npx -y exa-mcp-server api-key 9b2f9ab7-c27c-4763-b0ef-2c743232dab9 --help

# Restart Claude Code
claude restart
```

### Common Tasks

```bash
# Add a new skill
mkdir -p /home/codespace/repo-swarm/.claude/skills/new-skill
# Create SKILL.md file
claude restart

# Modify an existing skill
# Edit the SKILL.md file
claude restart

# Add a new hook
cat > /home/codespace/repo-swarm/.claude/hooks/new-hook.md << 'EOF'
# Hook content
EOF

# Test the full workflow
# In Claude Code:
/workflow-orchestrator "Test task description"
```

---

## Implementation Time Estimate

- **Phase 1 (MCP Setup)**: 10-15 minutes
- **Phase 2 (Skills Creation)**: 15-20 minutes
- **Phase 3 (Hooks Setup)**: 5-10 minutes
- **Phase 4 (Vibe-Kanban Config)**: 10-15 minutes
- **Phase 5 (Testing)**: 10-15 minutes

**Total**: 50-75 minutes for first-time setup
**Subsequent setups**: 20-30 minutes (once familiar with process)

---

## Next Steps After Implementation

After completing this checklist:

1. **Monitor First Few Workflows**: Watch the first few automated workflows to ensure smooth operation
2. **Customize Skills**: Adjust skill instructions based on your project's specific needs
3. **Add More MCP Servers**: Integrate additional MCP servers as needed
4. **Create Additional Hooks**: Add hooks for specific project requirements
5. **Fine-Tune Vibe-Kanban**: Adjust agent profiles and workflows based on usage
6. **Document Customizations**: Keep track of any customizations you make

---

**Implementation Checklist Version**: 1.0
**Last Updated**: 2025-12-31
**Maintained In**: `/home/codespace/repo-swarm/docs/vibe-kanban-integration/`

---

**Status**: Ready to implement ✅

**Check off each item as you complete it to track your progress!**
