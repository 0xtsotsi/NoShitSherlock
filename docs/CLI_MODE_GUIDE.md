# Claude CLI Mode Guide

## Overview

The RepoSwarm investigation system supports two modes for communicating with Claude:

1. **API Mode** (default): Uses the Anthropic Python SDK to make API calls
2. **CLI Mode**: Uses the official Claude CLI binary instead of API calls

This guide explains how the CLI mode switch works, how to enable it, and how to verify it's working correctly.

## Why Use CLI Mode?

- **Cost Management**: The Claude CLI may use different billing or token limits
- **Local Development**: Test investigations without consuming API credits
- **Integration Testing**: Verify system behavior with both API and CLI
- **Debugging**: CLI mode can provide different output formats for debugging

## Environment Variable: USE_CLAUDE_CLI

The mode is controlled by the `USE_CLAUDE_CLI` environment variable.

### Accepted Values

**CLI Mode Enabled (uses Claude CLI binary):**
- `true`
- `TRUE`
- `1`
- `yes`

**API Mode Enabled (uses Anthropic API - default):**
- `false`
- `FALSE`
- `0`
- `no`
- `` (empty/not set)

## Prerequisites for CLI Mode

To use CLI mode, you must have the Claude CLI binary installed and available in your PATH.

### Installing Claude CLI

```bash
# Install via npm
npm install -g @anthropic/claude-cli

# Verify installation
claude --version
```

Expected output:
```
2.0.75 (Claude Code)
```

## Enabling CLI Mode

### Method 1: Environment File

Add to your `.env.local` file:

```bash
USE_CLAUDE_CLI=true
```

### Method 2: Export in Shell

```bash
export USE_CLAUDE_CLI=true
```

### Method 3: Inline with Command

```bash
USE_CLAUDE_CLI=true python src/investigator/example.py
```

## How It Works

### Code Path Trace

1. **Environment Variable Read** (`src/investigator/core/claude_analyzer.py:23`)
   ```python
   self.use_cli = os.getenv('USE_CLAUDE_CLI', '').lower() in ('true', '1', 'yes')
   ```

2. **Mode Selection** (`src/investigator/core/claude_analyzer.py:25-40`)
   - If `USE_CLAUDE_CLI=true`: Imports and uses `ClaudeCLIClient`
   - Otherwise: Uses standard `Anthropic` SDK client

3. **CLI Binary Detection** (`src/investigator/core/claude_cli_adapter.py:33-49`)
   - Searches for `claude` binary in PATH
   - Verifies binary is executable
   - Raises explicit error if not found

4. **CLI Verification** (`src/investigator/core/claude_cli_adapter.py:51-73`)
   - Runs `claude --version` to verify CLI works
   - Fails with actionable error message if verification fails

5. **Message Creation** (`src/investigator/core/claude_cli_adapter.py:75-138`)
   - Calls CLI with: `claude prompt --model <model> --max-tokens <tokens> --format json`
   - Passes prompt via stdin
   - Parses response and returns SDK-compatible structure

### No Silent Fallback

**CRITICAL**: The system does NOT silently fall back to API mode if CLI mode is requested but unavailable.

If `USE_CLAUDE_CLI=true` is set but the CLI binary is not found:
- **Error is raised immediately** during ClaudeAnalyzer initialization
- **Error message is actionable** with instructions to install CLI
- **Investigation does not proceed** with wrong mode

Example error:
```
RuntimeError: Claude CLI binary not found in PATH. Please install the Claude CLI:
  npm install -g @anthropic/claude-cli
Or ensure it's available in your PATH.
```

## Logging Output

### API Mode Logging

When using API mode (default):

```
INFO - Using Anthropic API for Claude requests
INFO - Claude Analyzer initialized in API mode
INFO - [API MODE] Sending analysis request to Claude API
INFO - [API MODE] Received analysis from Claude API (1234 characters)
```

### CLI Mode Logging

When using CLI mode (`USE_CLAUDE_CLI=true`):

```
WARNING - ======================================================================
WARNING - CLAUDE CLI MODE ACTIVE
WARNING - Using Claude CLI binary instead of Anthropic API
WARNING - ======================================================================
INFO - Claude Analyzer initialized in CLI mode
INFO - [CLI MODE] Sending analysis request via Claude CLI
INFO - [CLI MODE] Received analysis from Claude CLI (1234 characters)
```

**Note**: CLI mode uses WARNING level for the banner to ensure visibility.

## Verification

### Automated Test Script

Run the verification test suite:

```bash
python scripts/test_cli_mode.py
```

This script tests:
1. API mode activation (when USE_CLAUDE_CLI is not set)
2. CLI mode activation (when USE_CLAUDE_CLI=true)
3. All environment variable value variations
4. Explicit error handling (no silent fallback)

Expected output:
```
================================================================================
TEST SUMMARY
================================================================================
API Mode: ✓ PASSED
CLI Mode: ✓ PASSED
CLI Mode Variations: ✓ PASSED
No Silent Fallback: ✓ PASSED
================================================================================
ALL TESTS PASSED ✓
```

### Manual Verification

#### Test 1: Verify API Mode (Default)

```bash
# Ensure USE_CLAUDE_CLI is not set
unset USE_CLAUDE_CLI

# Run an investigation
python src/investigator/example.py https://github.com/example/repo

# Check logs for:
# "Using Anthropic API for Claude requests"
# "[API MODE] Sending analysis request to Claude API"
```

#### Test 2: Verify CLI Mode

```bash
# Enable CLI mode
export USE_CLAUDE_CLI=true

# Run an investigation
python src/investigator/example.py https://github.com/example/repo

# Check logs for:
# "CLAUDE CLI MODE ACTIVE"
# "[CLI MODE] Sending analysis request via Claude CLI"
```

#### Test 3: Verify Explicit Error on Missing CLI

```bash
# Enable CLI mode
export USE_CLAUDE_CLI=true

# Temporarily rename the CLI to simulate it not being installed
# (Don't actually do this - just understand the behavior)

# Expected error:
# RuntimeError: Claude CLI binary not found in PATH...
```

## Implementation Files

### Core Implementation

- **`src/investigator/core/claude_analyzer.py`**
  - Main analyzer class
  - Mode selection logic (line 23)
  - Client initialization (lines 25-40)
  - Mode-specific logging (lines 115-133)

- **`src/investigator/core/claude_cli_adapter.py`**
  - CLI adapter implementation
  - Binary detection and verification
  - CLI invocation logic
  - SDK-compatible response wrapper

### Configuration

- **`.env.example`** - Environment template (lines 18-20)
- **`env.example`** - Environment template (lines 18-20)
- **`env.local.example`** - Local environment template (lines 18-20)

### Testing

- **`scripts/test_cli_mode.py`** - Automated verification test suite

## Troubleshooting

### Error: "Claude CLI binary not found in PATH"

**Cause**: CLI mode is enabled but the claude binary is not installed or not in PATH.

**Solution**:
1. Install Claude CLI: `npm install -g @anthropic/claude-cli`
2. Verify installation: `claude --version`
3. If installed but not found, check your PATH: `echo $PATH`

### Error: "Claude CLI verification failed"

**Cause**: The CLI binary exists but is not working correctly.

**Solution**:
1. Run `claude --version` manually to see the error
2. Reinstall the CLI: `npm uninstall -g @anthropic/claude-cli && npm install -g @anthropic/claude-cli`
3. Check permissions: `ls -la $(which claude)`

### Logs show API mode but USE_CLAUDE_CLI is set

**Cause**: The environment variable is not set in the same context as the running process.

**Solution**:
1. Verify the variable is exported: `echo $USE_CLAUDE_CLI`
2. Set it in the same shell session as the investigation
3. Or add it to `.env.local` and ensure it's loaded

### CLI mode works but responses are different

**Expected Behavior**: The CLI may format responses differently or use different system prompts.

**Solution**:
1. This is normal and expected
2. The adapter attempts to normalize responses
3. Check the CLI documentation for CLI-specific behavior

## Best Practices

1. **Default to API Mode**: Unless specifically testing CLI mode, use API mode for consistency
2. **Explicit Configuration**: Always set USE_CLAUDE_CLI explicitly in environment files
3. **Document Mode**: When reporting issues, always specify which mode was used
4. **Test Both Modes**: Before deploying changes, test with both API and CLI modes
5. **Check Logs**: Always verify the mode logs to confirm the expected mode is active

## Architecture Notes

### Why No Silent Fallback?

The implementation deliberately does NOT fall back to API mode if CLI mode is requested but unavailable. This design decision ensures:

1. **Predictability**: Developers know exactly which mode is being used
2. **Cost Control**: Prevents unexpected API usage when CLI was intended
3. **Debugging**: Errors surface immediately rather than silently changing behavior
4. **Testing**: Tests can verify mode selection works correctly

### Compatibility Layer

The CLI adapter implements a compatibility layer that mimics the Anthropic SDK interface:

- `ClaudeCLIClient.messages.create()` - Matches SDK interface
- `ClaudeCLIResponse` - Matches SDK response structure
- `ClaudeCLIContent` - Matches SDK content structure

This allows the rest of the codebase to work identically in both modes.

## Summary

The `USE_CLAUDE_CLI` environment variable provides a clean, explicit way to switch between API and CLI modes:

✅ **Explicit mode selection** via environment variable
✅ **No silent fallback** - errors are raised if CLI is unavailable
✅ **Clear logging** - mode is visible in all log output
✅ **Binary detection** - explicit check with actionable error messages
✅ **Automated testing** - verification script confirms correct operation

The implementation ensures developers always know which mode is active and receive clear feedback when configuration is incorrect.
