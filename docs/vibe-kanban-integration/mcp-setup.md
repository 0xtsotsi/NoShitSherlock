# MCP Server Configuration Guide

## Overview

This guide covers setting up all required MCP (Model Context Protocol) servers for the Vibe-Kanban + Minimal-Claude integration.

## Required MCP Servers

1. **Exa** - Web research and information gathering
2. **Grep** - Local code pattern search
3. **Filesystem** - File operations
4. **Git** - Version control operations
5. **Playwright** - Browser automation (optional)

## Configuration File

**Location**: `/home/codespace/repo-swarm/.claude/settings.local.json`

## Step-by-Step Setup

### Step 1: Backup Existing Configuration

```bash
cp ~/.claude/settings.local.json ~/.claude/settings.local.json.backup
```

### Step 2: Create/Update settings.local.json

Create or update `/home/codespace/repo-swarm/.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(ruff:*)",
      "Bash(pip install:*)",
      "Bash(mise:*)",
      "Bash(git:*)",
      "Bash(uv:*)",
      "Bash(temporal:*)",
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
```

### Step 3: Verify MCP Server Installation

Test each MCP server individually:

```bash
# Test Exa MCP
npx -y exa-mcp-server api-key 9b2f9ab7-c27c-4763-b0ef-2c743232dab9

# Test Grep MCP
npx -y @modelcontextprotocol/server-grep --help

# Test Filesystem MCP
npx -y @modelcontextprotocol/server-filesystem --help

# Test Git MCP
npx -y @modelcontextprotocol/server-git --help

# Test Playwright MCP (optional)
npx -y @executeautomation/playwright-mcp-server --help
```

### Step 4: Restart Claude Code

After updating the configuration, restart Claude Code to load the new MCP servers:

```bash
# If running via CLI
claude restart
```

Or restart the Claude Code application.

## MCP Server Details

### 1. Exa MCP Server

**Purpose**: Web research, finding best practices, documentation lookup

**API Key**: `9b2f9ab7-c27c-4763-b0ef-2c743232dab9`

**Available Tools**:
- `web_search_exa` - Real-time web search
- `deep_researcher_start` - Start comprehensive research
- `deep_researcher_check` - Check research progress
- `company_research` - Company information gathering
- `crawling` - Extract content from URLs
- `linkedin_search` - Professional networking search

**Usage in Skills**:
- /research uses Exa to find best practices
- /commit uses Exa to research commit message conventions
- /implement uses Exa for library and framework research

**Documentation**: https://docs.exa.ai/reference/exa-mcp

### 2. Grep MCP Server

**Purpose**: Search codebase for patterns, implementations, examples

**Available Tools**:
- `grep_search` - Search files using regex patterns
- `grep_search_files_with_matches` - Find files containing patterns
- `grep_search_count` - Count pattern occurrences

**Usage in Skills**:
- /research uses Grep to find existing patterns
- /fix uses Grep to find how similar issues were fixed
- /implement uses Grep to follow existing conventions

**Installation**: `npx -y @modelcontextprotocol/server-grep`

### 3. Filesystem MCP Server

**Purpose**: File operations, directory traversal, file reading

**Available Tools**:
- `read_file` - Read file contents
- `write_file` - Write to files
- `create_directory` - Create directories
- `list_directory` - List directory contents
- `search_files` - Search for files by pattern

**Usage in Skills**:
- All skills use Filesystem for file operations
- /implement uses it to create new files
- /cicd uses it to validate configuration files

**Installation**: `npx -y @modelcontextprotocol/server-filesystem /path/to/project`

### 4. Git MCP Server

**Purpose**: Git operations, history analysis, diff generation

**Available Tools**:
- `git_diff` - Get git diff
- `git_log` - View commit history
- `git_status` - Check repository status
- `git_add` - Stage files
- `git_commit` - Create commits
- `git_push` - Push to remote

**Usage in Skills**:
- /commit uses Git MCP to analyze changes
- /research uses Git MCP to understand project history
- All hooks use Git MCP for status checks

**Installation**: `npx -y @modelcontextprotocol/server-git --repository /path/to/project`

### 5. Playwright MCP Server

**Purpose**: Browser automation, web testing, UI interaction

**Available Tools**:
- `browser_navigate` - Navigate to URLs
- `browser_click` - Click elements
- `browser_type` - Type text
- `browser_snapshot` - Get page state
- `browser_evaluate` - Execute JavaScript

**Usage in Skills**:
- /cicd can use Playwright for end-to-end testing
- /research can use Playwright to scrape documentation

**Installation**: `npx -y @executeautomation/playwright-mcp-server`

**Note**: Optional, can be disabled if not needed

## Verification

After setup, verify MCP servers are working:

1. **Check Claude Code logs** for MCP server connection status
2. **Test tools directly** in Claude Code:
   - Try using Grep to search for a pattern
   - Try using Exa to search the web
   - Try using Git to get repository status

## Troubleshooting

### MCP Server Not Starting

**Problem**: MCP server fails to start

**Solutions**:
1. Check npx is installed: `which npx`
2. Verify internet connection (for npx to download packages)
3. Try installing globally first: `npm install -g <package>`
4. Check API key for Exa is correct
5. Review Claude Code logs for error messages

### Tools Not Available

**Problem**: MCP server connected but tools not available

**Solutions**:
1. Verify `"disabled": false` in settings.local.json
2. Restart Claude Code
3. Check MCP server is still running
4. Verify tool names in MCP server documentation

### Permission Denied

**Problem**: Operations fail with permission errors

**Solutions**:
1. Check permissions section in settings.local.json
2. Add specific permission: `"Bash(command:*)"`
3. Add Skill permission: `"Skill(skillname)"`
4. Restart Claude Code after updating permissions

## Advanced Configuration

### Remote Exa MCP Server

Instead of local npx, you can use remote Exa MCP:

```json
"exa": {
  "url": "https://mcp.exa.ai/mcp",
  "headers": {
    "exaApiKey": "9b2f9ab7-c27c-4763-b0ef-2c743232dab9"
  }
}
```

### Custom Filesystem Paths

Add multiple filesystem MCP servers for different paths:

```json
"filesystem-project": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/codespace/repo-swarm"]
},
"filesystem-home": {
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/codespace"]
}
```

### Environment Variables

Use environment variables for sensitive data:

```bash
export EXA_API_KEY="9b2f9ab7-c27c-4763-b0ef-2c743232dab9"
```

Then in settings.local.json:

```json
"exa": {
  "command": "npx",
  "args": ["-y", "exa-mcp-server"],
  "env": {
    "EXA_API_KEY": "${EXA_API_KEY}"
  }
}
```

## Next Steps

After MCP servers are configured:

1. → Create Skills (see `skills-guide.md`)
2. → Setup Hooks (see `hooks-guide.md`)
3. → Configure Vibe-Kanban (see `vibe-kanban-setup.md`)

## Checklist

- [ ] Backup existing settings.local.json
- [ ] Create/update settings.local.json with all MCP servers
- [ ] Test each MCP server individually
- [ ] Restart Claude Code
- [ ] Verify tools are available in Claude Code
- [ ] Test Grep search
- [ ] Test Exa web search
- [ ] Test Git operations
- [ ] Document any custom configurations

---

**Related Documentation**:
- Skills Guide: `skills-guide.md`
- Hooks Guide: `hooks-guide.md`
- Vibe-Kanban Setup: `vibe-kanban-setup.md`
- Troubleshooting: `troubleshooting.md`
