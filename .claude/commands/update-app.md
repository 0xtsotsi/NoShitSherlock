---
name: update-app
description: Update dependencies, fix deprecations and warnings
---

# Dependency Update & Deprecation Fix

## Step 1: Check for Updates

```bash
uv pip list --outdated
```

## Step 2: Update Dependencies

```bash
uv sync --upgrade
```

## Step 3: Check for Deprecations & Warnings

Run installation and check output:
```bash
uv sync
```

Read ALL output carefully. Look for:
- Deprecation warnings
- Security vulnerabilities
- Dependency conflicts
- Breaking changes

## Step 4: Fix Issues

For each warning/deprecation:
1. Research the recommended replacement or fix
2. Update code/dependencies accordingly
3. Re-run `uv sync`
4. Verify no warnings remain

## Step 5: Run Quality Checks

```bash
ruff check src/ && mypy src/ && black --check src/
```

Fix all errors before completing.

## Step 6: Verify Clean Install

Ensure a fresh install works:
```bash
rm -rf .venv uv.lock
uv sync
```

Verify ZERO warnings/errors and all dependencies resolve correctly.
