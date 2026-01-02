# Vibe-Kanban Integration with Claude Code Skills

## Overview

Vibe-Kanban is a multi-agent orchestration system that coordinates specialized AI agents to complete complex software development tasks. This integration with Claude Code skills enables Vibe-Kanban agents to leverage powerful capabilities like:
- Automated code fixing (`/fix`)
- Intelligent commits (`/commit`)
- Dependency updates (`/update-app`)
- Project setup automation

### Key Benefits

- **Parallel Execution**: Multiple agents work simultaneously on different aspects of a task
- **Specialized Capabilities**: Each agent has optimized model and tool configurations
- **Seamless Claude Code Integration**: Direct access to Claude Code skills through agent profiles
- **State Management**: Kanban-style task tracking with pending, in-progress, and completed states

## Prerequisites

### 1. Vibe-Kanban Installation

Vibe-Kanban should already be installed. Verify installation:

```bash
# Check if vibe-kanban is available
which vibe-kanban

# Or if installed via cargo
cargo list | grep vibe-kanban
```

### 2. Claude Code Skills

Ensure these Claude Code skills are available in your project:
- `/fix` - Run typechecking and linting, then spawn parallel agents to fix issues
- `/commit` - Run checks, commit with AI message, and push
- `/update-app` - Update dependencies, fix deprecations and warnings

Verify skills are configured:
```bash
cat .claude/settings.json | grep -A 5 "skills"
```

### 3. Project Structure

Your project should have:
```
repo-swarm/
├── .claude/
│   └── settings.json          # Claude Code configuration
├── src/                        # Source code
├── docs/
│   └── vibe-kanban-integration/
│       └── vibe-kanban-setup.md
└── vibe-kanban-config.json    # Vibe-Kanban configuration
```

## Configuration

### Creating the Configuration File

Create `vibe-kanban-config.json` in your project root:

```bash
touch /home/codespace/repo-swarm/vibe-kanban-config.json
```

### Basic Configuration Structure

```json
{
  "project": {
    "name": "repo-swarm",
    "description": "Multi-agent repository investigation system",
    "root": "/home/codespace/repo-swarm"
  },
  "agents": {
    "research": {
      "model": "claude-sonnet-4-5-20250929",
      "role": "Research and analysis specialist"
    },
    "implement": {
      "model": "claude-opus-4-5-20251101",
      "role": "Implementation specialist"
    },
    "cicd": {
      "model": "claude-sonnet-4-5-20250929",
      "role": "CI/CD and automation specialist"
    }
  },
  "workflows": []
}
```

## Agent Profiles

### 1. Research Agent

**Purpose**: Deep code analysis, investigation, and architectural research

**Model**: Claude Sonnet 4.5
- Optimized for complex reasoning
- Fast response times
- Large context window for codebase analysis

**Tools**:
- `Grep` - Search code patterns
- `Read` - Read file contents
- `LSP` - Language Server Protocol for code intelligence
- `mcp__zread__*` - GitHub repository reading tools
- `mcp__web_reader__webReader` - Web documentation fetching

**Claude Code Skills Integration**:
```json
{
  "agent_name": "research",
  "model": "claude-sonnet-4-5-20250929",
  "system_prompt": "You are a research specialist focused on codebase analysis, architectural investigation, and gathering information. Use Grep and Read tools extensively. Document findings clearly.",
  "tools": {
    "primary": ["Grep", "Read", "Glob", "LSP"],
    "secondary": ["mcp__zread__search_doc", "mcp__web_reader__webReader"]
  },
  "skills": {
    "enabled": ["minimal-claude:setup-claude-md"],
    "usage": "Use setup-claude-md to generate project documentation during research"
  },
  "capabilities": {
    "search_patterns": "Can search across large codebases using regex and glob patterns",
    "code_intelligence": "Uses LSP for symbol resolution and type information",
    "documentation_access": "Reads GitHub docs and web resources",
    "analysis": "Performs architectural analysis and code quality assessments"
  }
}
```

**Best For**:
- Investigating codebases
- Finding usage patterns
- Understanding architecture
- Researching dependencies
- Analyzing test coverage

### 2. Implement Agent

**Purpose**: Code implementation, refactoring, and feature development

**Model**: Claude Opus 4.5
- Highest reasoning capability
- Best for complex implementation tasks
- Optimized for code generation

**Tools**:
- `Read`/`Write`/`Edit` - File manipulation
- `Bash` - Command execution
- `LSP` - Code intelligence
- `NotebookEdit` - Jupyter notebook support

**Claude Code Skills Integration**:
```json
{
  "agent_name": "implement",
  "model": "claude-opus-4-5-20251101",
  "system_prompt": "You are an implementation specialist. Write clean, maintainable code. Always read files before editing. Test your changes. Use the /fix skill to resolve issues.",
  "tools": {
    "primary": ["Read", "Write", "Edit", "Bash", "LSP"],
    "secondary": ["NotebookEdit"]
  },
  "skills": {
    "enabled": ["fix", "update-app"],
    "fix_usage": "Run /fix after making changes to resolve any linting or type errors",
    "update_usage": "Use /update-app when dependencies need upgrading or deprecation fixes"
  },
  "capabilities": {
    "code_generation": "Generates production-ready code with proper error handling",
    "refactoring": "Restructures code while maintaining functionality",
    "testing": "Creates and updates tests",
    "documentation": "Adds inline documentation and docstrings"
  }
}
```

**Best For**:
- Implementing new features
- Refactoring code
- Writing tests
- Fixing bugs
- Performance optimization

### 3. CI/CD Agent

**Purpose**: Automation, deployment, and repository maintenance

**Model**: Claude Sonnet 4.5
- Fast execution for repetitive tasks
- Good at following structured procedures
- Efficient for Git operations

**Tools**:
- `Bash` - Command execution
- `Git` operations via Bash
- `Read` - Configuration file reading

**Claude Code Skills Integration**:
```json
{
  "agent_name": "cicd",
  "model": "claude-sonnet-4-5-20250929",
  "system_prompt": "You are a CI/CD specialist. Handle Git operations, dependency updates, and automation. Use /commit for changes and /update-app for dependency maintenance.",
  "tools": {
    "primary": ["Bash", "Read"],
    "git_commands": ["git status", "git add", "git commit", "git push", "git pull"]
  },
  "skills": {
    "enabled": ["commit", "update-app"],
    "commit_usage": "Use /commit to stage, commit, and push changes with AI-generated messages",
    "update_usage": "Run /update-app regularly to maintain dependencies and fix deprecations",
    "workflow": "Always run /fix before /commit to ensure code quality"
  },
  "capabilities": {
    "git_management": "Handles branching, merging, and commit operations",
    "dependency_management": "Keeps dependencies updated and secure",
    "automation": "Creates and maintains CI/CD pipelines",
    "quality_gates": "Ensures tests and linting pass before commits"
  }
}
```

**Best For**:
- Git operations (commit, push, PR creation)
- Dependency updates
- Running CI/CD pipelines
- Code quality checks
- Automated maintenance tasks

## Task Workflow

### Vibe-Kanban Orchestration Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    TASK INITIATION                          │
│  User submits task → Vibe-Kanban parses requirements         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    TASK BREAKDOWN                           │
│  Vibe-Kanban analyzes task complexity and agent capabilities│
│  → Splits into subtasks if needed                            │
│  → Assigns appropriate agents                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  PARALLEL EXECUTION                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Research    │  │  Implement   │  │    CI/CD     │       │
│  │   Agent      │  │   Agent      │  │   Agent      │       │
│  │              │  │              │  │              │       │
│  │ - Grep code  │  │ - Write code │  │ - Git ops    │       │
│  │ - Read files │  │ - Edit files │  │ - /commit    │       │
│  │ - LSP query  │  │ - /fix       │  │ - /update-app│       │
│  └───────┬──────┘  └───────┬──────┘  └───────┬──────┘       │
│          │                 │                 │              │
│          └─────────────────┴─────────────────┘              │
│                            │                                │
│                            ▼                                │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    STATE UPDATE                             │
│  Vibe-Kanban updates task states:                           │
│  pending → in_progress → completed (or failed)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESULTS AGGREGATION                      │
│  Collect outputs from all agents                            │
│  → Combine results                                           │
│  → Resolve conflicts                                         │
│  → Final deliverable                                         │
└─────────────────────────────────────────────────────────────┘
```

### Task State Flow

```
┌──────────┐
│ PENDING  │ ← Task created, waiting for agent assignment
└────┬─────┘
     │
     ▼
┌──────────────┐
│ IN_PROGRESS  │ ← Agent working on task
└──────┬───────┘
       │
       ├─────────────────┐
       │                 │
       ▼                 ▼
┌──────────┐      ┌──────────┐
│ COMPLETED│      │  FAILED  │
└──────────┘      └──────────┘
```

### Parallel Execution Patterns

#### Pattern 1: Independent Subtasks
```
Task: "Add authentication and update dependencies"

Research Agent          Implement Agent         CI/CD Agent
    │                       │                       │
    ├─ Analyze auth         ├─ Implement auth       ├─ Update deps
    └─ Review existing      └─ Write tests          └─ Run tests
      authentication                               │
                                                    │
                         All complete ──────────────┘
                                   │
                                   ▼
                            Combine results
```

#### Pattern 2: Sequential Dependencies
```
Task: "Refactor module and add tests"

Phase 1: Research
    Research Agent
        │
        └─ Analyze module structure
        └─ Identify refactoring opportunities
        └─ Document dependencies

Phase 2: Implementation (waits for Research)
    Implement Agent
        │
        ├─ Refactor code
        ├─ Run /fix
        └─ Add tests

Phase 3: CI/CD (waits for Implementation)
    CI/CD Agent
        │
        ├─ Run /commit
        └─ Create PR
```

#### Pattern 3: Collaborative Parallel
```
Task: "Implement feature with database changes"

Research Agent          Implement Agent
    │                       │
    ├─ Schema design        ├─ Backend code
    ├─ Query optimization   ├─ API endpoints
    └─ Documentation        └─ Unit tests

Both agents work on different aspects
but share information through Vibe-Kanban
```

## Configuration File

### Complete Example: vibe-kanban-config.json

```json
{
  "version": "1.0.0",
  "project": {
    "name": "repo-swarm",
    "description": "Multi-agent repository investigation system with Temporal workflows",
    "root": "/home/codespace/repo-swarm",
    "repository": "https://github.com/your-org/repo-swarm"
  },
  "agents": {
    "research": {
      "profile": "research",
      "model": "claude-sonnet-4-5-20250929",
      "temperature": 0.3,
      "max_tokens": 8192,
      "system_prompt": "You are a research specialist focused on codebase analysis, architectural investigation, and gathering information. Use Grep and Read tools extensively. Document findings clearly with code examples and file paths.",
      "capabilities": {
        "search": ["Grep", "Glob", "Read"],
        "analysis": ["LSP"],
        "external": ["mcp__zread__search_doc", "mcp__web_reader__webReader"]
      },
      "skills": {
        "minimal-claude:setup-claude-md": {
          "enabled": true,
          "trigger": "auto",
          "description": "Generate CLAUDE.md when researching new codebases"
        }
      },
      "preferences": {
        "max_iterations": 10,
        "timeout_seconds": 300,
        "parallel_searches": true
      }
    },
    "implement": {
      "profile": "implement",
      "model": "claude-opus-4-5-20251101",
      "temperature": 0.2,
      "max_tokens": 16384,
      "system_prompt": "You are an implementation specialist. Write clean, maintainable code following project conventions. Always read files before editing. Test your changes. Run /fix after making changes to resolve any issues.",
      "capabilities": {
        "filesystem": ["Read", "Write", "Edit"],
        "execution": ["Bash"],
        "code_intelligence": ["LSP"],
        "notebooks": ["NotebookEdit"]
      },
      "skills": {
        "fix": {
          "enabled": true,
          "trigger": "after_changes",
          "description": "Run typechecking and linting after code changes"
        },
        "update-app": {
          "enabled": true,
          "trigger": "manual",
          "description": "Update dependencies when needed"
        }
      },
      "preferences": {
        "max_iterations": 15,
        "timeout_seconds": 600,
        "auto_fix": true,
        "test_after_write": true
      },
      "code_style": {
        "language": "python",
        "formatter": "black",
        "linter": "ruff",
        "type_checker": "mypy"
      }
    },
    "cicd": {
      "profile": "cicd",
      "model": "claude-sonnet-4-5-20250929",
      "temperature": 0.1,
      "max_tokens": 4096,
      "system_prompt": "You are a CI/CD specialist. Handle Git operations, dependency updates, and automation. Use /commit for changes and /update-app for dependency maintenance. Always ensure quality gates pass before proceeding.",
      "capabilities": {
        "git": ["Bash"],
        "file_reading": ["Read"],
        "commands": ["git status", "git add", "git commit", "git push", "git pull", "gh pr create"]
      },
      "skills": {
        "commit": {
          "enabled": true,
          "trigger": "manual",
          "description": "Commit changes with AI-generated messages",
          "options": {
            "run_checks": true,
            "push": true
          }
        },
        "update-app": {
          "enabled": true,
          "trigger": "scheduled",
          "schedule": "weekly",
          "description": "Update dependencies weekly"
        }
      },
      "preferences": {
        "max_iterations": 5,
        "timeout_seconds": 180,
        "require_tests_pass": true,
        "require_lint_pass": true
      },
      "git_workflow": {
        "branch_strategy": "feature-branches",
        "commit_style": "conventional",
        "pr_required": true
      }
    }
  },
  "workflows": [
    {
      "name": "investigate-and-implement",
      "description": "Research codebase and implement changes",
      "steps": [
        {
          "agent": "research",
          "task": "Analyze current implementation and dependencies",
          "output": "research_findings.json"
        },
        {
          "agent": "implement",
          "task": "Implement required changes based on research",
          "depends_on": ["research_findings.json"],
          "skills": ["fix"]
        },
        {
          "agent": "cicd",
          "task": "Commit and push changes",
          "depends_on": ["implement"],
          "skills": ["commit"]
        }
      ]
    },
    {
      "name": "maintenance-cycle",
      "description": "Weekly dependency and quality maintenance",
      "steps": [
        {
          "agent": "implement",
          "task": "Update dependencies and fix deprecations",
          "skills": ["update-app"]
        },
        {
          "agent": "implement",
          "task": "Run /fix to resolve any issues",
          "depends_on": ["update-app"],
          "skills": ["fix"]
        },
        {
          "agent": "cicd",
          "task": "Commit and create PR if changes needed",
          "depends_on": ["fix"],
          "skills": ["commit"]
        }
      ]
    },
    {
      "name": "feature-development",
      "description": "Full feature development workflow",
      "steps": [
        {
          "agent": "research",
          "task": "Research feature requirements and existing patterns",
          "output": "feature_design.json"
        },
        {
          "agent": "implement",
          "task": "Implement feature with tests",
          "depends_on": ["feature_design.json"],
          "skills": ["fix"]
        },
        {
          "agent": "cicd",
          "task": "Run tests and commit changes",
          "depends_on": ["implement"],
          "skills": ["commit"]
        }
      ]
    }
  ],
  "integration": {
    "claude_code": {
      "skills_path": ".claude/settings.json",
      "auto_discover": true,
      "skill_mappings": {
        "fix": {
          "agents": ["implement"],
          "trigger": "after_code_changes"
        },
        "commit": {
          "agents": ["cicd"],
          "trigger": "manual"
        },
        "update-app": {
          "agents": ["implement", "cicd"],
          "trigger": "manual_or_scheduled"
        }
      }
    },
    "temporal": {
      "enabled": true,
      "namespace": "default",
      "task_queue": "vibe-kanban-tasks",
      "workflow_timeout": "3600s"
    }
  },
  "monitoring": {
    "log_level": "info",
    "metrics": {
      "enabled": true,
      "export": "prometheus"
    },
    "task_history": {
      "retention_days": 30,
      "max_entries": 1000
    }
  },
  "security": {
    "allowed_operations": [
      "read",
      "write",
      "bash",
      "git"
    ],
    "blocked_paths": [
      "/etc/",
      "~/.ssh/",
      "~/.gnupg/"
    ],
    "max_file_size": 10485760,
    "require_confirmation": [
      "git push",
      "git push --force",
      "rm -rf"
    ]
  }
}
```

## Integration Points

### How Agents Use Claude Code Skills

#### 1. Research Agent + setup-claude-md Skill

**Flow**:
```
Research Task Initiated
        │
        ▼
Agent scans new codebase
        │
        ▼
Calls minimal-claude:setup-claude-md
        │
        ▼
Skill generates CLAUDE.md with:
  - Project structure
  - Architecture overview
  - Key patterns
        │
        ▼
Agent uses CLAUDE.md for context
in subsequent research tasks
```

**Example Usage**:
```bash
# Vibe-Kanban triggers skill
vibe-kanban execute --task "research-auth-system" --agent research

# Agent internally calls:
/Skill skill: "minimal-claude:setup-claude-md"

# Result: CLAUDE.md created with auth system documentation
```

#### 2. Implement Agent + fix Skill

**Flow**:
```
Implement Agent makes code changes
        │
        ▼
Writes/Edits files
        │
        ▼
Vibe-Kanban triggers /fix skill
        │
        ├─ Run typechecker (mypy)
        ├─ Run linter (ruff)
        │
        ▼
Issues found? ──No──▶ Task complete
       │
      Yes
       │
       ▼
Spawn parallel fix agents
       │
       ├─ Fix agent 1: Type errors
       ├─ Fix agent 2: Linting issues
       └─ Fix agent N: Other issues
       │
       ▼
All fixes applied
       │
       ▼
Verify fixes pass
       │
       ▼
Task complete
```

**Example Usage**:
```json
{
  "task": "Add user authentication",
  "agent": "implement",
  "workflow": [
    {
      "step": "Implement auth module",
      "action": "Write auth.py with login/logout"
    },
    {
      "step": "Auto-fix",
      "action": "Call /fix skill",
      "expect": "All type and lint errors resolved"
    }
  ]
}
```

#### 3. CI/CD Agent + commit Skill

**Flow**:
```
Changes ready to commit
        │
        ▼
CI/CD Agent calls /commit
        │
        ├─ Run pre-commit checks
        │  ├─ Typecheck (mypy)
        │  ├─ Lint (ruff)
        │  └─ Tests (pytest)
        │
        ▼
Checks pass? ──No──▶ Fail with error
       │
      Yes
       │
       ▼
Stage changes (git add)
        │
        ▼
Generate commit message with AI
        │
        ├─ Analyze changes (git diff)
        │  └─ Check recent commit history
        │
        ▼
Create conventional commit
        │
        ▼
Commit and push
        │
        ▼
Task complete
```

**Example Usage**:
```bash
# Agent commits changes
vibe-kanban execute --task "commit-auth-feature" --agent cicd

# Agent internally calls:
/Skill skill: "commit"

# Generated commit:
# "feat(auth): add user authentication with JWT tokens
#
# - Implement login/logout endpoints
# - Add JWT token validation
# - Create authentication middleware
#
# 🤖 Generated with Claude Code
# Co-Authored-By: Claude Sonnet 4.5"
```

#### 4. CI/CD Agent + update-app Skill

**Flow**:
```
Dependency update triggered
        │
        ▼
Call /update-app skill
        │
        ├─ Check for outdated packages
        ├─ Update requirements.txt/pyproject.toml
        │
        ▼
Run tests with new versions
        │
        ▼
Failures? ──Yes──▶ Fix deprecations
       │           │
       │           ▼
       │      Implement fixes
       │           │
       │           └─────────────┐
       │                         │
      No                        │
       │                        │
       ▼                        │
Commit updates ◀────────────────┘
        │
        ▼
Create PR if needed
```

**Example Usage**:
```bash
# Scheduled weekly update
vibe-kanban execute --task "weekly-deps-update" --agent cicd --schedule weekly

# Agent internally calls:
/Skill skill: "update-app"

# Result:
# - Dependencies updated
# - Deprecation warnings fixed
# - Tests passing
# - Changes committed
```

### Agent Capability Mappings

| Agent | Primary Skills | Secondary Tools | Output |
|-------|---------------|-----------------|--------|
| **Research** | setup-claude-md | Grep, Read, LSP, GitHub, Web | Documentation, analysis reports |
| **Implement** | fix, update-app | Write, Edit, Bash, LSP | Code changes, tests |
| **CI/CD** | commit, update-app | Bash (Git), Read | Commits, PRs, dependency updates |

### Skill Triggers

| Skill | Trigger Condition | Auto-Run | Manual Run |
|-------|------------------|----------|------------|
| **setup-claude-md** | New codebase detected | Yes | Yes |
| **fix** | After code changes | Yes | Yes |
| **commit** | Changes staged | No | Yes |
| **update-app** | Scheduled or manual | Scheduled | Yes |

## Testing

### Testing the Integration

#### 1. Verify Agent Configuration

```bash
# Test Vibe-Kanban can load config
vibe-kanban validate-config --config vibe-kanban-config.json

# Expected output:
# ✓ Configuration valid
# ✓ 3 agents loaded
# ✓ 3 workflows defined
```

#### 2. Test Individual Agents

```bash
# Test research agent
vibe-kanban test-agent --agent research \
  --task "Analyze the authentication system"

# Expected output:
# [Research] Analyzing authentication system...
# [Research] Found 3 authentication modules
# [Research] Generated CLAUDE.md

# Test implement agent
vibe-kanban test-agent --agent implement \
  --task "Add a simple hello world function"

# Expected output:
# [Implement] Created hello_world() in src/utils.py
# [Fix] Running typecheck...
# [Fix] Running linter...
# [Implement] No issues found

# Test cicd agent
vibe-kanban test-agent --agent cicd \
  --task "Commit test changes"

# Expected output:
# [CI/CD] Running checks...
# [CI/CD] Staging changes...
# [CI/CD] Generated commit message
# [CI/CD] Committed and pushed
```

#### 3. Test Workflow Integration

```bash
# Test full workflow
vibe-kanban run \
  --workflow investigate-and-implement \
  --config vibe-kanban-config.json \
  --params '{"task": "Add logging to investigate_worker.py"}'

# Expected flow:
# [1/3] Research: Analyze current logging
# [2/3] Implement: Add logging functionality
# [3/3] CI/CD: Commit changes
```

#### 4. Test Skill Integration

```bash
# Test /fix skill
vibe-kanban run \
  --agent implement \
  --task "Intentionally add type error and run fix" \
  --auto-fix true

# Test /commit skill
vibe-kanban run \
  --agent cicd \
  --task "Create test commit" \
  --skill commit

# Test /update-app skill
vibe-kanban run \
  --agent cicd \
  --task "Check for dependency updates" \
  --skill update-app
```

### Integration Tests

Create test file at `/home/codespace/repo-swarm/tests/integration/test_vibe_kanban.py`:

```python
"""Integration tests for Vibe-Kanban with Claude Code skills"""

import pytest
import subprocess
import json
from pathlib import Path


class TestVibeKanbanIntegration:
    """Test Vibe-Kanban integration with Claude Code skills"""

    @pytest.fixture
    def config_path(self):
        return Path("/home/codespace/repo-swarm/vibe-kanban-config.json")

    def test_config_valid(self, config_path):
        """Test configuration file is valid"""
        result = subprocess.run(
            ["vibe-kanban", "validate-config", "--config", str(config_path)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert "valid" in result.stdout.lower()

    def test_research_agent(self, config_path):
        """Test research agent with setup-claude-md skill"""
        result = subprocess.run([
            "vibe-kanban", "test-agent",
            "--agent", "research",
            "--config", str(config_path),
            "--task", "Analyze project structure"
        ], capture_output=True, text=True, timeout=60)

        assert result.returncode == 0
        assert (Path("/home/codespace/repo-swarm/CLAUDE.md").exists() or
                "analysis" in result.stdout.lower())

    def test_implement_agent_with_fix(self, config_path, tmp_path):
        """Test implement agent with /fix skill"""
        # Create test file with intentional error
        test_file = tmp_path / "test_module.py"
        test_file.write_text("""
def add_numbers(a: int, b: int) -> int:
    return a + b

# Call with wrong type
result = add_numbers("1", 2)
""")

        result = subprocess.run([
            "vibe-kanban", "test-agent",
            "--agent", "implement",
            "--config", str(config_path),
            "--task", f"Fix type errors in {test_file}",
            "--auto-fix", "true"
        ], capture_output=True, text=True, timeout=120)

        # Should run /fix and resolve issues
        assert "fix" in result.stdout.lower()

    def test_cicd_agent_with_commit(self, config_path):
        """Test CI/CD agent with /commit skill"""
        result = subprocess.run([
            "vibe-kanban", "test-agent",
            "--agent", "cicd",
            "--config", str(config_path),
            "--task", "Validate commit skill availability",
            "--dry-run", "true"
        ], capture_output=True, text=True, timeout=30)

        assert result.returncode == 0
        assert "commit" in result.stdout.lower() or "skill" in result.stdout.lower()

    def test_workflow_execution(self, config_path):
        """Test complete workflow execution"""
        result = subprocess.run([
            "vibe-kanban", "run",
            "--workflow", "maintenance-cycle",
            "--config", str(config_path),
            "--dry-run", "true"
        ], capture_output=True, text=True, timeout=60)

        assert result.returncode == 0
        # Verify workflow steps are present
        assert any(word in result.stdout.lower() for word in
                  ["update", "fix", "commit", "step"])
```

Run tests:
```bash
# Run integration tests
python -m pytest tests/integration/test_vibe_kanban.py -v

# Run with coverage
python -m pytest tests/integration/test_vibe_kanban.py --cov=src --cov-report=html
```

## Best Practices

### 1. Agent Selection Guidelines

**Use Research Agent When**:
- Analyzing unfamiliar codebases
- Investigating bugs or issues
- Documenting architecture
- Searching for patterns
- Reviewing PRs

**Use Implement Agent When**:
- Writing new code
- Refactoring existing code
- Adding tests
- Fixing bugs
- Performance optimization

**Use CI/CD Agent When**:
- Committing changes
- Creating PRs
- Updating dependencies
- Running CI/CD pipelines
- Repository maintenance

### 2. Workflow Design

**Do**:
- Break complex tasks into smaller subtasks
- Define clear dependencies between steps
- Specify which skills to use at each step
- Set appropriate timeouts for each agent

**Don't**:
- Overload a single agent with unrelated tasks
- Create circular dependencies
- Forget to include error handling steps
- Skip quality checks (fix, tests)

### 3. Skill Usage

**/fix Best Practices**:
- Run after every code change
- Use in implement agent workflow
- Let it complete fully before committing
- Review auto-fixes for edge cases

**/commit Best Practices**:
- Always run /fix before /commit
- Use in CI/CD agent only
- Enable automatic push for automation
- Review generated commit messages in PRs

**/update-app Best Practices**:
- Schedule regularly (weekly/monthly)
- Test thoroughly after updates
- Create separate branch for updates
- Review breaking changes manually

### 4. Performance Optimization

**Parallel Execution**:
```json
{
  "workflow": "parallel-research",
  "steps": [
    {
      "agent": "research",
      "task": "Analyze frontend code",
      "parallel": true
    },
    {
      "agent": "research",
      "task": "Analyze backend code",
      "parallel": true
    }
  ]
}
```

**Caching Research Results**:
```json
{
  "agent": "research",
  "task": "Analyze module structure",
  "cache": {
    "enabled": true,
    "key": "module-structure",
    "ttl": 3600
  }
}
```

### 5. Error Handling

**Retry Logic**:
```json
{
  "agent": "implement",
  "task": "Fix failing tests",
  "retry": {
    "max_attempts": 3,
    "backoff": "exponential",
    "on_error": "run_fix_skill"
  }
}
```

**Fallback Strategies**:
```json
{
  "workflow": "safe-implementation",
  "steps": [
    {
      "agent": "implement",
      "task": "Implement feature",
      "on_failure": "rollback",
      "fallback": "use_previous_version"
    }
  ]
}
```

### 6. Monitoring and Debugging

**Enable Detailed Logging**:
```json
{
  "monitoring": {
    "log_level": "debug",
    "log_file": "logs/vibe-kanban.log",
    "include_agent_thoughts": true
  }
}
```

**Track Task Metrics**:
```json
{
  "monitoring": {
    "metrics": {
      "enabled": true,
      "track": [
        "task_duration",
        "agent_usage",
        "skill_invocations",
        "success_rate"
      ]
    }
  }
}
```

### 7. Security Considerations

**Restrict Dangerous Operations**:
```json
{
  "security": {
    "require_confirmation": [
      "git push --force",
      "rm -rf",
      "DROP TABLE",
      "DELETE FROM"
    ],
    "blocked_paths": [
      "/etc/",
      "~/.ssh/",
      "credentials.json"
    ]
  }
}
```

**Secrets Management**:
```bash
# Use environment variables for secrets
export ANTHROPIC_API_KEY="your-key"
export GITHUB_TOKEN="your-token"

# Reference in config
{
  "environment": {
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
    "GITHUB_TOKEN": "${GITHUB_TOKEN}"
  }
}
```

### 8. Team Collaboration

**Share Agent Profiles**:
```bash
# Export agent configuration
vibe-kanban export-agent --agent research --output research-agent.json

# Import to another project
vibe-kanban import-agent --input research-agent.json
```

**Version Control Config**:
```bash
# Commit the config
git add vibe-kanban-config.json
git commit -m "chore: update Vibe-Kanban configuration"

# Use different configs for environments
vibe-kanban-config.dev.json
vibe-kanban-config.prod.json
```

### 9. Common Patterns

**Pattern: Progressive Enhancement**:
```json
{
  "workflow": "progressive-feature",
  "steps": [
    {"agent": "research", "task": "MVP analysis"},
    {"agent": "implement", "task": "Implement MVP", "skills": ["fix"]},
    {"agent": "cicd", "task": "Commit MVP", "skills": ["commit"]},
    {"agent": "research", "task": "Enhancement analysis"},
    {"agent": "implement", "task": "Add enhancements", "skills": ["fix"]},
    {"agent": "cicd", "task": "Commit enhancements", "skills": ["commit"]}
  ]
}
```

**Pattern: Test-Driven Development**:
```json
{
  "workflow": "tdd-cycle",
  "steps": [
    {"agent": "implement", "task": "Write failing test"},
    {"agent": "implement", "task": "Implement minimal code to pass"},
    {"agent": "implement", "task": "Run tests", "skills": ["fix"]},
    {"agent": "cicd", "task": "Commit if tests pass", "skills": ["commit"]}
  ]
}
```

### 10. Troubleshooting

**Agent Not Responding**:
- Check model availability
- Verify API credentials
- Increase timeout value
- Check logs for errors

**Skill Not Working**:
- Verify skill is enabled in config
- Check `.claude/settings.json`
- Test skill manually first
- Review skill output logs

**Workflow Stuck**:
- Check for circular dependencies
- Verify agent availability
- Review task state in logs
- Consider breaking into smaller workflows

## Quick Start Commands

```bash
# Initialize Vibe-Kanban for the first time
vibe-kanban init --config vibe-kanban-config.json

# Run a simple research task
vibe-kanban execute --agent research --task "Analyze the codebase structure"

# Run a full workflow
vibe-kanban run --workflow investigate-and-implement --params '{"feature": "user-auth"}'

# Monitor running tasks
vibe-kanban status --watch

# View task history
vibe-kanban history --last 10

# Get agent recommendations
vibe-kanban recommend --task "Add database migration"
```

## Additional Resources

- [Vibe-Kanban Documentation](https://github.com/vibe-kanban/vibe-kanban)
- [Claude Code Skills Reference](../claude-skills-reference.md)
- [Temporal Workflow Integration](../temporal-integration.md)
- [Project Documentation](../README.md)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in `logs/vibe-kanban.log`
3. Open an issue on GitHub
4. Contact the development team

---

**Last Updated**: 2025-12-31
**Version**: 1.0.0
**Maintainer**: repo-swarm team
