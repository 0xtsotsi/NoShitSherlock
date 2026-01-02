# Troubleshooting Guide

## Overview

This guide helps you diagnose and resolve common issues with the Vibe-Kanban + Minimal-Claude integration. Issues are categorized by component for quick navigation.

## How to Use This Guide

1. **Identify the symptom** - What's going wrong?
2. **Find the category** - Which component is affected?
3. **Follow diagnostic steps** - Confirm the root cause
4. **Try solutions in order** - Start with the simplest fix
5. **Check prevention tips** - Avoid future occurrences

## Quick Reference Table

| Symptom | Category | Quick Fix |
|---------|----------|-----------|
| "Tool not found" errors | MCP Server | Restart Claude Code after config changes |
| "Skill not found" errors | Skill | Verify SKILL.md files exist in correct paths |
| Hooks not executing | Hook | Check hook file permissions and restart |
| Agents not using skills | Vibe-Kanban | Verify agent prompts include skill instructions |
| Permission denied errors | Permissions | Add specific permissions to settings.local.json |
| Network/timeout errors | MCP Server | Check internet connection and npx availability |
| Type check failures | Workflow | Run /fix skill to auto-resolve |
| Tests failing | Workflow | Check test environment and dependencies |

---

## MCP Server Issues

### Issue 1: MCP Server Not Starting

**Symptom:**
```
Failed to start MCP server: [server-name]
```

**Possible Causes:**
1. npx not installed or not in PATH
2. Internet connection unavailable (for npx to download packages)
3. Invalid command syntax in settings.local.json
4. Conflicting Node.js versions
5. Package not available in npm registry

**Diagnostic Steps:**
```bash
# Check if npx is installed
which npx
# Expected output: /usr/bin/npx or similar

# Check Node.js version
node --version
# Should be v16 or higher

# Test npx with a simple package
npx -y cowsay "test"
# Should download and run successfully

# Test specific MCP package
npx -y @modelcontextprotocol/server-grep --help
```

**Solutions (Try in Order):**

1. **Install/Update Node.js and npm:**
   ```bash
   # On Ubuntu/Debian
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # Verify
   node --version
   npm --version
   ```

2. **Clear npx cache:**
   ```bash
   rm -rf ~/.npm/_npx
   npx -y @modelcontextprotocol/server-grep --help
   ```

3. **Install MCP package globally first:**
   ```bash
   npm install -g @modelcontextprotocol/server-grep
   # Then use direct command in settings.local.json
   ```

4. **Check internet connectivity:**
   ```bash
   ping -c 3 registry.npmjs.org
   curl -I https://registry.npmjs.org
   ```

5. **Use alternative installation method (local npm):**
   ```bash
   mkdir -p ~/.local/mcp-servers
   cd ~/.local/mcp-servers
   npm init -y
   npm install @modelcontextprotocol/server-grep
   # Then update settings.local.json to use local binary
   ```

**Prevention:**
- Keep Node.js updated to latest LTS version
- Use stable internet connection during setup
- Pin specific package versions in settings.local.json
- Test npx connectivity regularly

---

### Issue 2: MCP Tools Not Available

**Symptom:**
```
Tool "grep_search" not found or not available
```

**Possible Causes:**
1. MCP server marked as disabled in settings
2. MCP server crashed after starting
3. Incorrect tool name used
4. MCP server version mismatch
5. Claude Code not restarted after configuration

**Diagnostic Steps:**

1. **Check settings.local.json:**
   ```bash
   cat /home/codespace/repo-swarm/.claude/settings.local.json | grep -A 5 "disabled"
   # Ensure all servers have "disabled": false
   ```

2. **Check Claude Code logs:**
   ```bash
   # Logs location varies by platform
   # macOS: ~/Library/Logs/Claude/
   # Linux: ~/.config/Claude/logs/
   # Look for MCP server startup messages
   ```

3. **Verify tool names:**
   - Check MCP server documentation
   - Different servers may have different tool names
   - Example: `grep_search` vs `search`

**Solutions (Try in Order):**

1. **Verify server not disabled:**
   ```json
   "grep": {
     "command": "npx",
     "args": ["-y", "@modelcontextprotocol/server-grep"],
     "disabled": false  // ← Must be false
   }
   ```

2. **Restart Claude Code completely:**
   ```bash
   # Quit Claude Code application fully
   # Then restart it
   # Or via CLI:
   claude restart
   ```

3. **Test MCP server directly:**
   ```bash
   # Start server in standalone mode
   npx -y @modelcontextprotocol/server-grep

   # In another terminal, test with stdio
   echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | npx -y @modelcontextprotocol/server-grep
   ```

4. **Update MCP server to latest version:**
   ```bash
   # Clear cache and force fresh download
   npx -y @modelcontextprotocol/server-grep@latest
   ```

5. **Check for conflicting Claude Code instances:**
   ```bash
   # Ensure only one instance running
   ps aux | grep -i claude
   killall -9 Claude  # Or appropriate process name
   ```

**Prevention:**
- Always restart Claude Code after changing settings.local.json
- Keep MCP servers updated to latest versions
- Document expected tool names for each server
- Use version pinning for production: `@modelcontextprotocol/server-grep@1.0.0`

---

### Issue 3: Exa MCP API Key Issues

**Symptom:**
```
Exa MCP: Authentication failed
Invalid API key
```

**Possible Causes:**
1. Incorrect API key in settings
2. API key expired or revoked
3. API key format incorrect
4. Exa service outage

**Diagnostic Steps:**

```bash
# Test API key directly
curl -X POST https://api.exa.ai/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: 9b2f9ab7-c27c-4763-b0ef-2c743232dab9" \
  -d '{"query": "test", "numResults": 1}'

# Expected: JSON response with search results
# Error: 401 Unauthorized = invalid key
```

**Solutions (Try in Order):**

1. **Verify API key in settings.local.json:**
   ```json
   "exa": {
     "command": "npx",
     "args": [
       "-y",
       "exa-mcp-server",
       "api-key",
       "9b2f9ab7-c27c-4763-b0ef-2c743232dab9"  // ← Check for typos
     ]
   }
   ```

2. **Regenerate API key from Exa dashboard:**
   - Visit https://dashboard.exa.ai/
   - Navigate to API Keys section
   - Generate new key
   - Update settings.local.json

3. **Use environment variable instead:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export EXA_API_KEY="9b2f9ab7-c27c-4763-b0ef-2c743232dab9"

   # Then in settings.local.json
   "exa": {
     "command": "npx",
     "args": ["-y", "exa-mcp-server"],
     "env": {
       "EXA_API_KEY": "${EXA_API_KEY}"
     }
   }
   ```

4. **Test with remote Exa MCP:**
   ```json
   "exa": {
     "url": "https://mcp.exa.ai/mcp",
     "headers": {
       "exaApiKey": "9b2f9ab7-c27c-4763-b0ef-2c743232dab9"
     }
   }
   ```

**Prevention:**
- Store API keys in environment variables, not in config files
- Rotate API keys regularly
- Monitor API usage on Exa dashboard
- Have backup API keys ready

---

### Issue 4: Filesystem MCP Permission Denied

**Symptom:**
```
Error: Permission denied: /home/codespace/repo-swarm
Cannot read directory
```

**Possible Causes:**
1. Wrong path specified in settings
2. Directory doesn't exist
3. Insufficient file permissions
4. SELinux or AppArmor restrictions

**Diagnostic Steps:**

```bash
# Check if directory exists
ls -la /home/codespace/repo-swarm

# Check permissions
stat /home/codespace/repo-swarm

# Test access
cd /home/codespace/repo-swarm && ls -la

# Check for extended attributes
ls -ld@ /home/codespace/repo-swarm  # macOS
getfacl /home/codespace/repo-swarm  # Linux
```

**Solutions (Try in Order):**

1. **Correct the path in settings.local.json:**
   ```json
   "filesystem": {
     "command": "npx",
     "args": [
       "-y",
       "@modelcontextprotocol/server-filesystem",
       "/home/codespace/repo-swarm"  // ← Verify absolute path
     ]
   }
   ```

2. **Fix directory permissions:**
   ```bash
   # Ensure readable and accessible
   chmod +r /home/codespace/repo-swarm
   chmod +rx /home/codespace/repo-swarm

   # Fix ownership if needed
   sudo chown -R $USER:$USER /home/codespace/repo-swarm
   ```

3. **Create directory if missing:**
   ```bash
   mkdir -p /home/codespace/repo-swarm
   ```

4. **Use home directory shortcut:**
   ```json
   "filesystem": {
     "command": "npx",
     "args": [
       "-y",
       "@modelcontextprotocol/server-filesystem",
       "~"  // ← Expands to home directory
     ]
   }
   ```

5. **Check for security restrictions:**
   ```bash
   # Temporarily disable SELinux (test only)
   sudo setenforce 0

   # Check AppArmor status
   sudo aa-status

   # Add exception if needed
   ```

**Prevention:**
- Use absolute paths in settings
- Set proper directory permissions during setup
- Document expected directory structure
- Use version control to track permission changes

---

## Skill Issues

### Issue 5: Skill Not Found

**Symptom:**
```
Skill "/research" not found
Unknown skill: implement
```

**Possible Causes:**
1. SKILL.md file doesn't exist
2. File in wrong directory
3. Filename case mismatch (SKILL.md vs skill.md)
4. Claude Code not restarted after creating skill
5. Invalid frontmatter in SKILL.md

**Diagnostic Steps:**

```bash
# Check if skill directory exists
ls -la /home/codespace/repo-swarm/.claude/skills/

# Check for SKILL.md files
find /home/codespace/repo-swarm/.claude/skills -name "SKILL.md"

# Verify file is readable
cat /home/codespace/repo-swarm/.claude/skills/research/SKILL.md | head -20

# Check file permissions
stat /home/codespace/repo-swarm/.claude/skills/research/SKILL.md
```

**Solutions (Try in Order):**

1. **Verify correct directory structure:**
   ```bash
   # Must be exactly this structure:
   /home/codespace/repo-swarm/.claude/skills/research/SKILL.md
   /home/codespace/repo-swarm/.claude/skills/implement/SKILL.md
   /home/codespace/repo-swarm/.claude/skills/cicd/SKILL.md
   /home/codespace/repo-swarm/.claude/skills/workflow-orchestrator/SKILL.md
   ```

2. **Create missing skill files:**
   ```bash
   # Example for research skill
   mkdir -p /home/codespace/repo-swarm/.claude/skills/research
   cat > /home/codespace/repo-swarm/.claude/skills/research/SKILL.md << 'EOF'
   ---
   name: research
   description: Research code patterns using Exa and Grep MCP
   ---

   # Research Phase Agent
   [Skill content here]
   EOF
   ```

3. **Ensure correct filename (case-sensitive):**
   ```bash
   # Must be SKILL.md (all caps)
   # NOT: skill.md, Skill.md, SKILL.md.txt

   # Rename if wrong case
   mv /home/codespace/repo-swarm/.claude/skills/research/skill.md \
      /home/codespace/repo-swarm/.claude/skills/research/SKILL.md
   ```

4. **Verify frontmatter format:**
   ```markdown
   ---
   name: research
   description: Research code patterns using Exa and Grep MCP
   ---

   # Skill Content
   ```
   - Must have exactly three dashes on first line
   - Must have `name:` field
   - Must have `description:` field
   - Frontmatter must be closed with three dashes

5. **Restart Claude Code:**
   ```bash
   # Skills are loaded on startup
   claude restart
   # Or fully quit and restart Claude Code app
   ```

**Prevention:**
- Use the skills-guide.md template exactly
- Always restart Claude Code after creating/modifying skills
- Verify SKILL.md filename is ALL CAPS
- Test skills immediately after creation

---

### Issue 6: Skill Not Executing As Expected

**Symptom:**
```
Skill runs but doesn't perform expected actions
Skips steps or behaves differently than documented
```

**Possible Causes:**
1. Skill instructions unclear or conflicting
2. MCP tools not available to skill
3. Missing required permissions
4. Skill logic error
5. Claude interpreting instructions differently

**Diagnostic Steps:**

1. **Test skill with verbose prompt:**
   ```bash
   /research "test query - explain each step you take"
   ```

2. **Check if MCP tools are available:**
   ```bash
   # In Claude Code, ask:
   "What tools are available from Grep MCP?"
   "What tools are available from Exa MCP?"
   ```

3. **Review skill file for clarity:**
   ```bash
   cat /home/codespace/repo-swarm/.claude/skills/research/SKILL.md
   ```

4. **Test with minimal skill:**
   ```bash
   # Create test skill
   mkdir -p /home/codespace/repo-swarm/.claude/skills/test
   cat > /home/codespace/repo-swarm/.claude/skills/test/SKILL.md << 'EOF'
   ---
   name: test
   description: Test skill
   ---
   You are a test agent. Always respond with "TEST SKILL EXECUTED".
   EOF

   # Restart and test
   /test
   ```

**Solutions (Try in Order):**

1. **Clarify skill instructions:**
   - Use numbered steps explicitly
   - Be specific about tool usage
   - Include examples in skill file
   - Remove ambiguous language

2. **Add explicit permission requirements:**
   ```json
   // In settings.local.json
   "permissions": {
     "allow": [
       "Skill(research)",
       "Skill(implement)",
       "Skill(cicd)",
       "Skill(workflow-orchestrator)"
     ]
   }
   ```

3. **Add step-by-step verification in skill:**
   ```markdown
   ## Step 1: Verify MCP Tools
   Before starting, confirm you have access to:
   - Grep MCP tools (grep_search, grep_search_files_with_matches)
   - Exa MCP tools (web_search_exa, company_research)

   If any tool is missing, report error and pause.

   ## Step 2: Execute Search
   [Proceed with implementation]
   ```

4. **Use automation mode correctly:**
   ```markdown
   ## Automation Mode
   - Do NOT ask for approval
   - Continue automatically after each step
   - Only pause on critical errors
   ```

5. **Add diagnostic output:**
   ```markdown
   ## Progress Tracking
   At each step, log your progress:
   - Step 1: ✅ Completed
   - Step 2: ⚙️ In progress
   - Step 3: ⏸️ Pending
   ```

**Prevention:**
- Test skills with simple cases first
- Use explicit, unambiguous language
- Include verification steps
- Document expected behavior
- Version control skill files

---

### Issue 7: Skill Permission Denied

**Symptom:**
```
Permission denied: Skill(research)
Skill not authorized
```

**Possible Causes:**
1. Skill not listed in permissions
2. Skill listed but with wrong syntax
3. Permissions file not loaded
4. Case sensitivity in skill name

**Diagnostic Steps:**

```bash
# Check current permissions
cat /home/codespace/repo-swarm/.claude/settings.local.json | grep -A 20 "permissions"

# Verify skill exists
ls -la /home/codespace/repo-swarm/.claude/skills/

# Check for syntax errors in JSON
python3 -m json.tool /home/codespace/repo-swarm/.claude/settings.local.json
```

**Solutions (Try in Order):**

1. **Add skill to permissions:**
   ```json
   {
     "permissions": {
       "allow": [
         "Skill(research)",
         "Skill(implement)",
         "Skill(cicd)",
         "Skill(workflow-orchestrator)",
         "Skill(fix)",
         "Skill(commit)",
         "Skill(update-app)"
       ]
     }
   }
   ```

2. **Use wildcard for all skills:**
   ```json
   {
     "permissions": {
       "allow": [
         "Skill(*)"  // ← Allows all skills
       ]
     }
   }
   ```

3. **Verify JSON syntax:**
   ```bash
   # Validate JSON
   cat /home/codespace/repo-swarm/.claude/settings.local.json | jq .

   # Fix syntax errors if any
   ```

4. **Restart Claude Code after permission change:**
   ```bash
   claude restart
   ```

5. **Check for multiple settings files:**
   ```bash
   # Find all settings files
   find ~ -name "settings*.json" -path "*/.claude/*"

   # Ensure permissions are in correct file
   # Should be: /home/codespace/repo-swarm/.claude/settings.local.json
   ```

**Prevention:**
- Always add new skills to permissions immediately
- Use specific skill names in production, wildcards in development
- Validate JSON syntax before saving
- Document all permitted skills

---

## Hook Issues

### Issue 8: Hooks Not Triggering

**Symptom:**
```
Hooks not executing before/after tasks
pre-commit hook not running
```

**Possible Causes:**
1. Hook files don't exist
2. Hook files in wrong directory
3. Hook file not readable
4. Hooks not enabled
5. Claude Code not restarted

**Diagnostic Steps:**

```bash
# Check if hooks directory exists
ls -la /home/codespace/repo-swarm/.claude/hooks/

# Check hook files
find /home/codespace/repo-swarm/.claude/hooks -type f -name "*.md"

# Verify hook content
cat /home/codespace/repo-swarm/.claude/hooks/pre-task.md

# Check file permissions
stat /home/codespace/repo-swarm/.claude/hooks/pre-task.md
```

**Solutions (Try in Order):**

1. **Create hooks directory:**
   ```bash
   mkdir -p /home/codespace/repo-swarm/.claude/hooks
   ```

2. **Create missing hook files:**
   ```bash
   # pre-task hook
   cat > /home/codespace/repo-swarm/.claude/hooks/pre-task.md << 'EOF'
   # Pre-Task Hook

   Always execute before any task begins:

   1. Check git status
   2. Verify working directory is clean
   3. Log task start time
   4. Report any uncommitted changes
   EOF

   # post-task hook
   cat > /home/codespace/repo-swarm/.claude/hooks/post-task.md << 'EOF'
   # Post-Task Hook

   Always execute after any task completes:

   1. Run type checks (mypy)
   2. Run linting (ruff)
   3. Run tests (pytest)
   4. Report task completion
   EOF

   # pre-commit hook
   cat > /home/codespace/repo-swarm/.claude/hooks/pre-commit.md << 'EOF'
   # Pre-Commit Hook

   Always execute before committing:

   1. Verify all tests pass
   2. Check no type errors
   3. Verify commit message format
   4. Review changes one last time
   EOF
   ```

3. **Ensure hooks are Markdown files:**
   ```bash
   # Must end in .md
   # pre-task.md ✓
   # pre-task.md.txt ✗

   # Rename if needed
   mv /home/codespace/repo-swarm/.claude/hooks/pre-task \
      /home/codespace/repo-swarm/.claude/hooks/pre-task.md
   ```

4. **Set correct permissions:**
   ```bash
   chmod 644 /home/codespace/repo-swarm/.claude/hooks/*.md
   ```

5. **Restart Claude Code:**
   ```bash
   claude restart
   ```

**Prevention:**
- Create all hooks during initial setup
- Use clear, descriptive hook names
- Document hook behavior in files
- Test hooks after creation
- Keep hooks simple and focused

---

### Issue 9: Hook Blocking Execution

**Symptom:**
```
Hook pauses execution waiting for approval
Workflow stops at hook instead of continuing
```

**Possible Causes:**
1. Hook contains approval prompts
2. Hook uses blocking language
3. Hook designed for manual review mode
4. Non-blocking flag not set

**Diagnostic Steps:**

1. **Review hook content:**
   ```bash
   cat /home/codespace/repo-swarm/.claude/hooks/pre-commit.md
   ```

2. **Look for blocking phrases:**
   - "Wait for approval"
   - "Ask user to confirm"
   - "Pause for review"
   - "Don't proceed until..."

**Solutions (Try in Order):**

1. **Remove blocking language:**
   ```markdown
   # BEFORE (blocking)
   ## Pre-Commit Hook
   1. Run tests
   2. Wait for user approval to continue
   3. Proceed if approved

   # AFTER (non-blocking)
   ## Pre-Commit Hook (Non-Blocking)
   1. Run tests
   2. Log results for visibility
   3. Continue automatically
   ```

2. **Add explicit non-blocking statement:**
   ```markdown
   # Pre-Task Hook

   **NON-BLOCKING HOOK**: This hook provides visibility but does NOT block execution.

   Steps:
   1. Check git status
   2. Log findings
   3. Continue automatically without waiting
   ```

3. **Use informational language:**
   ```markdown
   # Instead of: "Ask user if tests passed"
   # Use: "Verify tests passed, log any failures"
   ```

4. **Remove approval checkpoints:**
   ```markdown
   # Remove these types of instructions:
   - "Wait for confirmation"
   - "Pause until user responds"
   - "Ask before proceeding"

   # Replace with:
   - "Log and continue"
   - "Document and proceed"
   - "Record and move forward"
   ```

**Prevention:**
- Design hooks as non-blocking by default
- Use hooks for visibility, not control
- Document that hooks are informational
- Test hook behavior in automated mode

---

## Vibe-Kanban Integration Issues

### Issue 10: Agents Not Using Skills

**Symptom:**
```
Vibe-Kanban agents don't invoke skills
Agents work manually but don't use /research, /implement, etc.
```

**Possible Causes:**
1. Agent prompts don't mention skills
2. Skills not available to agents
3. Agent configuration incorrect
4. Vibe-Kanban not connected to Claude Code

**Diagnostic Steps:**

1. **Verify skills work manually:**
   ```bash
   # In Claude Code
   /research "test query"
   /implement "test feature"
   ```

2. **Check Vibe-Kanban agent configuration:**
   - Review agent prompts in Vibe-Kanban UI
   - Check if skills are mentioned
   - Verify agent permissions

3. **Test agent directly:**
   ```
   Create test task in Vibe-Kanban
   Assign to Research Agent
   Observe if /research is invoked
   ```

**Solutions (Try in Order):**

1. **Update agent prompts to include skills:**
   ```markdown
   # Research Agent Prompt

   You are a Research Agent. When assigned a task:

   1. ALWAYS invoke the /research skill first
   2. Use /research with the task description as input
   3. Wait for research brief to be generated
   4. Automatically proceed to implementation

   Example:
   Task: "Add monorepo support"
   Action: Invoke /research "Add monorepo support"

   Do NOT research manually - always use the /research skill.
   ```

2. **Add skill invocation as standard procedure:**
   ```markdown
   # Implementation Agent Prompt

   You are an Implementation Agent. When assigned a task:

   1. Invoke /research if not already done
   2. Invoke /implement with research findings
   3. Let /implement auto-invoke /fix
   4. Verify all tests pass

   Required Skills:
   - /research (for analysis)
   - /implement (for coding)
   - /fix (for quality)
   - /cicd (for validation)
   ```

3. **Configure agent permissions in Vibe-Kanban:**
   ```
   In Vibe-Kanban agent settings:
   - Enable "Use Claude Code Skills"
   - Add skill permissions: research, implement, cicd, workflow-orchestrator
   - Allow automated skill invocation
   ```

4. **Test with simple task:**
   ```
   Task: "Create a test file"
   Expected Behavior:
   1. Research Agent spawns
   2. Agent invokes /research "create test file"
   3. /research completes
   4. Agent invokes /implement
   5. Implementation completes
   ```

5. **Check Vibe-Kanban-Claude Code integration:**
   ```
   - Verify Vibe-Kanban API key is configured
   - Check Claude Code is accessible to Vibe-Kanban
   - Test integration with simple command
   ```

**Prevention:**
- Always include skill instructions in agent prompts
- Use explicit language: "ALWAYS invoke /research"
- Test agent behavior with sample tasks
- Document skill invocation patterns
- Monitor agent execution logs

---

### Issue 11: Agent Not Proceeding Automatically

**Symptom:**
```
Agent stops after research, doesn't proceed to implementation
Agent waits for approval instead of continuing
```

**Possible Causes:**
1. Agent configured in manual mode
2. Skills configured to wait for approval
3. Agent prompts use blocking language
4. Automation flag not set

**Diagnostic Steps:**

1. **Check agent automation settings:**
   ```
   In Vibe-Kanban:
   - Agent Settings → Automation Mode
   - Should be: "Fully Automated"
   ```

2. **Review skill automation mode:**
   ```bash
   cat /home/codespace/repo-swarm/.claude/skills/research/SKILL.md | grep -A 5 "Automation"
   ```

3. **Test agent with simple task:**
   ```
   Create task: "Create hello.txt"
   Assign to Implementation Agent
   Monitor if it proceeds automatically
   ```

**Solutions (Try in Order):**

1. **Configure Vibe-Kanban agents for automation:**
   ```
   In Vibe-Kanban agent configuration:
   - Automation Mode: Fully Automated
   - Approval Checkpoints: None
   - Pause on Error: Yes
   - Continue on Success: Yes
   ```

2. **Verify skills have automation mode:**
   ```markdown
   ## Automation Mode (FULLY AUTOMATED)

   - Do NOT wait for user approval
   - Continue to next phase automatically
   - Only pause on critical errors
   ```

3. **Remove approval checkpoints from agent prompts:**
   ```markdown
   # BEFORE (manual)
   1. Invoke /research
   2. Wait for user to approve research brief
   3. If approved, proceed to /implement

   # AFTER (automated)
   1. Invoke /research
   2. Log research brief for visibility
   3. Automatically proceed to /implement
   ```

4. **Add explicit continuation instructions:**
   ```markdown
   ## Workflow Flow

   Research → Implementation → CI/CD → Commit

   Each phase automatically continues to next:
   - /research completes → automatically invoke /implement
   - /implement completes → automatically invoke /cicd
   - /cicd completes → automatically invoke /commit

   NO APPROVAL REQUIRED between phases.
   ```

5. **Test automation end-to-end:**
   ```
   Create task: "Add test automation"
   Expected: Completes without any user interaction
   ```

**Prevention:**
- Always use "Fully Automated" mode
- Remove all approval prompts from agent instructions
- Test automation regularly
- Monitor agent execution logs
- Keep skills and agents in sync

---

## Workflow Issues

### Issue 12: Type Checking Failures

**Symptom:**
```
mypy reports type errors
Type hints missing or incorrect
```

**Possible Causes:**
1. Code not following type hints standards
2. Missing type annotations
3. Incorrect type usage
4. mypy configuration issues
5. Missing type stubs

**Diagnostic Steps:**

```bash
# Run mypy to see errors
mypy src/

# Check mypy configuration
cat mypy.ini
cat pyproject.toml | grep -A 20 "\[tool.mypy\]"

# Count type errors
mypy src/ 2>&1 | grep "error:" | wc -l
```

**Solutions (Try in Order):**

1. **Use /fix skill to auto-resolve:**
   ```bash
   /fix
   # This will run mypy and attempt to fix issues
   ```

2. **Manually fix type errors:**
   ```python
   # BEFORE (error)
   def get_result(value):
       return value

   # AFTER (fixed)
   from typing import Any

   def get_result(value: Any) -> Any:
       return value

   # Or with specific types
   def get_result(value: str) -> str:
       return value
   ```

3. **Add type stubs for third-party libraries:**
   ```bash
   # Install type stubs
   pip install types-requests
   pip install types-pyyaml
   ```

4. **Configure mypy to be more lenient (temporary):**
   ```toml
   [tool.mypy]
   python_version = "3.11"
   warn_return_any = false
   warn_unused_configs = false
   disallow_untyped_defs = false  # Set to false temporarily
   ```

5. **Suppress specific errors (last resort):**
   ```python
   # type: ignore
   def complex_function(param):  # type: ignore
       pass
   ```

**Prevention:**
- Always add type hints when writing code
- Run mypy in pre-commit hooks
- Use strict mypy configuration
- Keep type stubs updated
- Document type annotation standards

---

### Issue 13: Test Failures

**Symptom:**
```
pytest reports failures
Tests pass locally but fail in CI
```

**Possible Causes:**
1. Code changes broke existing tests
2. Test environment mismatch
3. Missing test dependencies
4. Flaky tests (timing issues)
5. Test data issues

**Diagnostic Steps:**

```bash
# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/unit/test_file.py -v

# Run with debugger
pytest --pdb

# Check test coverage
pytest --cov=src --cov-report=html

# Identify failing tests
pytest --tb=short
```

**Solutions (Try in Order):**

1. **Run tests individually to isolate:**
   ```bash
   # Run each test file separately
   for test_file in tests/unit/*.py; do
       echo "Testing $test_file"
       pytest "$test_file" -v
   done
   ```

2. **Check test environment:**
   ```bash
   # Verify test dependencies
   pip list | grep pytest

   # Install test dependencies
   pip install pytest pytest-cov pytest-mock

   # Check environment variables
   env | grep -i test
   ```

3. **Fix broken tests:**
   ```python
   # Common test fixes:
   # 1. Update assertions
   assert result == expected_value

   # 2. Add fixtures
   @pytest.fixture
   def test_data():
       return {"key": "value"}

   # 3. Mock external dependencies
   @patch('module.external_api_call')
   def test_with_mock(mock_api):
       mock_api.return_value = expected_data
   ```

4. **Handle flaky tests:**
   ```python
   # Add retries for flaky tests
   @pytest.mark.flaky(reruns=3, reruns_delay=1)
   def test_flaky_test():
       pass

   # Or fix timing issues
   import time
   def test_with_timing():
       time.sleep(0.1)  # Wait for async operation
       assert result_ready()
   ```

5. **Update test data:**
   ```bash
   # Refresh test fixtures
   python scripts/generate_test_fixtures.py

   # Or update manually
   vim tests/fixtures/test_data.json
   ```

**Prevention:**
- Write tests alongside code (TDD)
- Run tests before committing
- Use continuous testing (pytest-watch)
- Keep tests isolated and independent
- Mock external dependencies
- Use fixtures for test data

---

### Issue 14: Commit Message Issues

**Symptom:**
```
Commit messages rejected or inconsistent
/commit generates poor commit messages
```

**Possible Causes:**
1. Commit message format not standardized
2. /commit skill lacks context
3. Git hooks rejecting messages
4. Conventional commits not enforced

**Diagnostic Steps:**

```bash
# Check recent commit messages
git log --oneline -10

# Check commit message hooks
cat .git/hooks/commit-msg

# Test /commit skill
/commit

# Check conventional commits setup
grep -r "conventional" .github/ 2>/dev/null
```

**Solutions (Try in Order):**

1. **Update /commit skill with better instructions:**
   ```markdown
   # /commit skill enhancements

   ## Commit Message Format

   Always use conventional commits:
   - feat: new feature
   - fix: bug fix
   - docs: documentation changes
   - style: formatting changes
   - refactor: code refactoring
   - test: adding/updating tests
   - chore: maintenance tasks

   Format: <type>(<scope>): <description>

   Example: feat(investigator): add monorepo support
   ```

2. **Add commit message hook:**
   ```bash
   # Install conventional commits hook
   pip install commitlint
   npm install -g @commitlint/cli @commitlint/config-conventional

   # Create .commitlintrc.yml
   cat > .commitlintrc.yml << 'EOF'
   extends:
     - '@commitlint/config-conventional'
   rules:
     type-enum:
       - 2
       - always
       - feat
       - fix
       - docs
       - style
       - refactor
       - test
       - chore
   EOF
   ```

3. **Improve /commit context gathering:**
   ```markdown
   # In /commit skill

   ## Step 1: Gather Context

   Before generating message:
   1. Use Git MCP to get detailed diff
   2. Identify main file changes
   3. Check if tests were added/modified
   4. Look for breaking changes
   5. Review related issues/PRs
   ```

4. **Manually edit commit message if needed:**
   ```bash
   # Instead of /commit with auto-push
   /commit --no-push

   # Then edit message
   git commit --amend

   # Then push manually
   git push
   ```

**Prevention:**
- Use conventional commits standard
- Train /commit with examples
- Add commit message validation
- Review commit messages regularly
- Document commit message conventions

---

## Permission Issues

### Issue 15: Bash Command Permission Denied

**Symptom:**
```
Permission denied: Bash(ruff:*)
Command not allowed: mise test-all
```

**Possible Causes:**
1. Command not listed in permissions
2. Command pattern doesn't match
3. Command blocked by security policy
4. Wildcard patterns not working

**Diagnostic Steps:**

```bash
# Check current permissions
cat /home/codespace/repo-swarm/.claude/settings.local.json | grep -A 30 "permissions"

# Test command manually
ruff check src/

# Check if command exists
which ruff
which mise
```

**Solutions (Try in Order):**

1. **Add specific command permissions:**
   ```json
   {
     "permissions": {
       "allow": [
         "Bash(ruff:*)",
         "Bash(mise:*)",
         "Bash(mypy:*)",
         "Bash(pytest:*)",
         "Bash(git:*)",
         "Bash(pip install:*)",
         "Bash(python:*)",
         "Bash(temporal:*)"
       ]
     }
   }
   ```

2. **Use broader patterns (development only):**
   ```json
   {
     "permissions": {
       "allow": [
         "Bash(*)"  // ← Allows all bash commands (use with caution)
       ]
     }
   }
   ```

3. **Allow specific command with arguments:**
   ```json
   {
     "permissions": {
       "allow": [
         "Bash(mise test-all)",
         "Bash(mise test-units)",
         "Bash(ruff check src/)",
         "Bash(mypy src/)"
       ]
     }
   }
   ```

4. **Restart Claude Code after permission changes:**
   ```bash
   claude restart
   ```

5. **Verify command path:**
   ```bash
   # Ensure command is in PATH
   echo $PATH

   # Use full path if needed
   /home/codespace/.local/bin/mise test-all
   ```

**Prevention:**
- Start with specific permissions, broaden only if needed
- Use patterns like `mise:*` instead of `mise:`
- Document required commands
- Test permissions in development first
- Review permissions regularly

---

## Network Issues

### Issue 16: MCP Server Timeout

**Symptom:**
```
MCP server connection timeout
Failed to connect to exa-mcp-server
Network timeout
```

**Possible Causes:**
1. Internet connection unstable
2. Firewall blocking connections
3. Proxy configuration needed
4. MCP server service down
5. DNS resolution issues

**Diagnostic Steps:**

```bash
# Test internet connectivity
ping -c 3 8.8.8.8
ping -c 3 registry.npmjs.org

# Test DNS resolution
nslookup registry.npmjs.org
dig exa.ai

# Check firewall
sudo ufw status
sudo iptables -L

# Test curl
curl -I https://registry.npmjs.org
curl -I https://api.exa.ai
```

**Solutions (Try in Order):**

1. **Check internet connection:**
   ```bash
   # Test basic connectivity
   ping -c 3 google.com

   # Restart network if needed
   sudo systemctl restart NetworkManager
   ```

2. **Configure proxy (if needed):**
   ```bash
   # Set proxy environment variables
   export http_proxy="http://proxy.example.com:8080"
   export https_proxy="http://proxy.example.com:8080"

   # Add to MCP server config
   "exa": {
     "command": "npx",
     "args": ["-y", "exa-mcp-server"],
     "env": {
       "http_proxy": "${http_proxy}",
       "https_proxy": "${https_proxy}"
     }
   }
   ```

3. **Use offline MCP servers when possible:**
   ```bash
   # Local filesystem, git, grep work offline
   # Only exa requires internet
   ```

4. **Increase timeout:**
   ```json
   "exa": {
     "command": "npx",
     "args": ["-y", "exa-mcp-server"],
     "timeout": 30000  // ← 30 seconds instead of default
   }
   ```

5. **Use alternative endpoints:**
   ```bash
   # Try different registry
   npm config set registry https://registry.npmjs.org/

   # Or use mirror
   npm config set registry https://npm.taobao.org/
   ```

**Prevention:**
- Use stable internet connection
- Configure proxy if behind firewall
- Keep local MCP servers as backup
- Monitor network status
- Cache packages locally

---

## Debug Mode

### Enable Debug Logging

**Claude Code Logs:**

```bash
# Linux
tail -f ~/.config/Claude/logs/*.log

# macOS
tail -f ~/Library/Logs/Claude/*.log

# Windows
tail -f %APPDATA%\Claude\logs\*.log
```

**MCP Server Debug Mode:**

```json
// In settings.local.json
"mcpServers": {
  "grep": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-grep", "--debug"],
    "env": {
      "DEBUG": "1",
      "RUST_LOG": "debug"
    }
  }
}
```

**Enable Skill Debug Output:**

Add to skill files:
```markdown
## Debug Mode

When invoked, log:
1. All tool calls made
2. All responses received
3. All decisions made
4. All errors encountered
```

**Verbose Claude Code Mode:**

```bash
# Start with verbose flag
claude --verbose

# Or set environment variable
export CLAUDE_DEBUG=1
claude
```

---

## Log Locations

### Claude Code Logs

| Platform | Location |
|----------|----------|
| Linux | `~/.config/Claude/logs/` |
| macOS | `~/Library/Logs/Claude/` |
| Windows | `%APPDATA%\Claude\logs\` |

### MCP Server Logs

MCP servers log to stderr/stdout, captured by Claude Code:
```
~/.config/Claude/logs/mcp-<server-name>.log
```

### Vibe-Kanban Logs

Check Vibe-Kanban application settings for log location.

### Project Logs

```bash
# Application logs
/home/codespace/repo-swarm/logs/

# Temporal workflow logs
/home/codespace/repo-swarn/temporal-logs/
```

---

## Getting Help

### Resources

1. **Documentation**
   - This guide: `/home/codespace/repo-swarm/docs/vibe-kanban-integration/troubleshooting.md`
   - Setup guide: `setup.md`
   - MCP guide: `mcp-setup.md`
   - Skills guide: `skills-guide.md`

2. **Plan File**
   - Location: `/home/codespace/.claude/plans/merry-crunching-fountain.md`
   - Contains full implementation details

3. **Community Resources**
   - Claude Code Documentation: https://docs.anthropic.com
   - MCP Protocol: https://modelcontextprotocol.io
   - Exa Documentation: https://docs.exa.ai

### Diagnostic Information to Collect

When asking for help, provide:

```bash
# System information
uname -a
claude --version

# Configuration
cat /home/codespace/repo-swarm/.claude/settings.local.json

# MCP servers
ls -la /home/codespace/repo-swarm/.claude/

# Skills
ls -la /home/codespace/repo-swarm/.claude/skills/

# Logs (last 100 lines)
tail -100 ~/.config/Claude/logs/*.log

# Test results
pytest --tb=short 2>&1 | head -50
mypy src/ 2>&1 | head -50
```

### Common Debug Commands

```bash
# Quick health check
echo "=== Claude Code Version ==="
claude --version

echo "=== Node.js Version ==="
node --version
npm --version

echo "=== MCP Servers Test ==="
npx -y @modelcontextprotocol/server-grep --help

echo "=== Skills Check ==="
ls -la /home/codespace/repo-swarm/.claude/skills/

echo "=== Permissions Check ==="
cat /home/codespace/repo-swarm/.claude/settings.local.json | grep -A 20 "permissions"

echo "=== Recent Errors ==="
tail -50 ~/.config/Claude/logs/*.log | grep -i error
```

### When to Ask for Help

Ask for help when:
1. You've tried all solutions in this guide
2. Error messages are unclear or cryptic
3. Multiple components failing simultaneously
4. Issue reproducible but cause unknown
5. Need clarification on architecture/design

---

## Quick Fixes Checklist

Before deep debugging, try these quick fixes:

- [ ] Restart Claude Code completely
- [ ] Verify settings.local.json syntax: `jq . /home/codespace/repo-swarm/.claude/settings.local.json`
- [ ] Check internet connection: `ping -c 3 google.com`
- [ ] Verify npx works: `npx -y cowsay "test"`
- [ ] Clear npm cache: `rm -rf ~/.npm/_npx`
- [ ] Check skills exist: `ls /home/codespace/repo-swarm/.claude/skills/*/SKILL.md`
- [ ] Verify permissions in settings.local.json
- [ ] Run /fix skill to auto-fix code issues
- [ ] Check recent logs for errors: `tail -100 ~/.config/Claude/logs/*.log`

---

**Last Updated**: 2025-12-31
**Version**: 1.0.0
**Related Documentation**:
- README.md: Overview and quick start
- mcp-setup.md: MCP server configuration
- skills-guide.md: Skills implementation
- architecture.md: System design details
