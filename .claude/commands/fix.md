---
name: fix
description: Run typechecking and linting, then spawn parallel agents to fix all issues
---

# Project Code Quality Check

This command runs all linting and typechecking tools for this Python project, collects errors, groups them by domain, and spawns parallel agents to fix them.

## Step 1: Run Linting and Typechecking

Run the appropriate commands for this project:

```bash
# Type checking with mypy
mypy src/ --ignore-missing-imports

# Linting with ruff (fast, comprehensive linter)
ruff check src/

# Code formatting check with black
black --check src/

# Additional linting with pylint
pylint src/ --recursive=y
```

## Step 2: Collect and Parse Errors

Parse the output from the linting and typechecking commands. Group errors by domain:
- **Type errors**: Issues from mypy (missing types, type mismatches, etc.)
- **Lint errors**: Issues from ruff and pylint (unused imports, undefined names, code style, complexity, etc.)
- **Format errors**: Issues from black (formatting inconsistencies)

Create a list of all files with issues and the specific problems in each file.

## Step 3: Spawn Parallel Agents

For each domain that has issues, spawn an agent in parallel using the Task tool.

**IMPORTANT**: Use a SINGLE response with MULTIPLE Task tool calls to run agents in parallel.

Example:
- Spawn a "type-fixer" agent for type errors
- Spawn a "lint-fixer" agent for lint errors
- Spawn a "format-fixer" agent for formatting errors

Each agent should:
1. Receive the list of files and specific errors in their domain
2. Fix all errors in their domain
3. Run the relevant check command to verify fixes
4. Report completion

For formatting errors, you can directly run:
```bash
black src/
```

For lint errors, you can use ruff's auto-fix:
```bash
ruff check --fix src/
```

For type errors and complex lint issues, agents should read each file, understand the context, and make appropriate fixes.

## Step 4: Verify All Fixes

After all agents complete, run the full check again to ensure all issues are resolved:

```bash
mypy src/ --ignore-missing-imports
ruff check src/
black --check src/
pylint src/ --recursive=y
```

Report a summary of:
- Total errors fixed
- Any remaining errors that require manual intervention
- Files that were modified
