# Hooks Guide for Vibe-Kanban Integration

## Overview

**Hooks** are markdown files that the Claude Code agent reads and executes at specific points during the development workflow. They provide visibility into what's happening, validate prerequisites, and give you context about upcoming operations.

### When Hooks Trigger

- **Pre-task hooks**: Run before Claude starts any task
- **Post-task hooks**: Run after a task completes successfully
- **Pre-commit hooks**: Run before creating a git commit

### Hook Philosophy

- **Fast**: Pre-task hooks complete in < 5 seconds
- **Non-blocking**: Hooks warn and inform, never prevent operations
- **Contextual**: Explain what they're checking and why
- **Overridable**: You can always proceed regardless of hook output

---

## Hooks to Create

Create these three hook files in your `.claude/hooks/` directory:

1. **pre-task.md** - Validates environment before tasks
2. **post-task.md** - Shows task impact and next steps
3. **pre-commit.md** - Validates commit readiness

---

## Hook Details

### 1. Pre-Task Hook

**File**: `.claude/hooks/pre-task.md`

**Purpose**: Validate the development environment and provide context before starting any task.

**When it triggers**: Before Claude executes any task command.

**What it does**:
- Checks AWS credentials are configured
- Verifies Python virtual environment is active
- Validates DynamoDB table accessibility
- Shows current git branch and status
- Provides context about the task environment

**Full Hook Content**:

```markdown
# Pre-Task Environment Check

You are about to execute a task. Let me validate your environment first.

## Checking Prerequisites

### 1. AWS Credentials
_Ensuring you can access AWS services for DynamoDB operations_

```bash
aws sts get-caller-identity 2>&1 | head -1
```

### 2. Python Virtual Environment
_Verifying you're working in an isolated Python environment_

```bash
if [ -n "$VIRTUAL_ENV" ]; then
  echo "✓ Active: $(basename $VIRTUAL_ENV)"
else
  echo "⚠ Warning: No virtual environment detected"
  echo "  Run: python -m venv .venv && source .venv/bin/activate"
fi
```

### 3. DynamoDB Access
_Ensuring database connectivity_

```bash
aws dynamodb list-tables --region us-east-1 --query "TableNames" --output text 2>&1 | head -c 100
```

## Current Context

### Git Branch
```bash
git branch --show-current
```

### Git Status
```bash
git status --short
```

### Recent Activity
```bash
git log -1 --oneline
```

## Task Environment Summary

- **AWS Region**: us-east-1
- **DynamoDB Table**: investigation-results (if configured)
- **Python Version**: $(python --version)
- **Working Directory**: $(pwd)

---

## What This Means

✓ **All checks passed** - Your environment is ready for task execution
⚠ **Warnings present** - You can proceed, but some features may be limited
❌ **Errors detected** - You can still proceed, but operations may fail

---

**Remember**: This is a non-blocking check. You can proceed regardless of the results above.
If you see warnings, consider addressing them for optimal task execution.
```

**Creation Command**:

```bash
cat > .claude/hooks/pre-task.md << 'EOF'
# Pre-Task Environment Check

You are about to execute a task. Let me validate your environment first.

## Checking Prerequisites

### 1. AWS Credentials
_Ensuring you can access AWS services for DynamoDB operations_

```bash
aws sts get-caller-identity 2>&1 | head -1
```

### 2. Python Virtual Environment
_Verifying you're working in an isolated Python environment_

```bash
if [ -n "$VIRTUAL_ENV" ]; then
  echo "✓ Active: $(basename $VIRTUAL_ENV)"
else
  echo "⚠ Warning: No virtual environment detected"
  echo "  Run: python -m venv .venv && source .venv/bin/activate"
fi
```

### 3. DynamoDB Access
_Ensuring database connectivity_

```bash
aws dynamodb list-tables --region us-east-1 --query "TableNames" --output text 2>&1 | head -c 100
```

## Current Context

### Git Branch
```bash
git branch --show-current
```

### Git Status
```bash
git status --short
```

### Recent Activity
```bash
git log -1 --oneline
```

## Task Environment Summary

- **AWS Region**: us-east-1
- **DynamoDB Table**: investigation-results (if configured)
- **Python Version**: $(python --version)
- **Working Directory**: $(pwd)

---

## What This Means

✓ **All checks passed** - Your environment is ready for task execution
⚠ **Warnings present** - You can proceed, but some features may be limited
❌ **Errors detected** - You can still proceed, but operations may fail

---

**Remember**: This is a non-blocking check. You can proceed regardless of the results above.
If you see warnings, consider addressing them for optimal task execution.
EOF
```

---

### 2. Post-Task Hook

**File**: `.claude/hooks/post-task.md`

**Purpose**: Show what changed during the task and provide guidance on next steps.

**When it triggers**: After a task completes successfully.

**What it does**:
- Shows modified and new files
- Displays git diff summary
- Provides commit guidance
- Suggests next actions
- Shows task completion context

**Full Hook Content**:

```markdown
# Post-Task Summary

The task has completed. Here's what changed and what to do next.

## Files Modified

```bash
git status --short
```

## Changes Summary

### Git Diff Overview
```bash
git diff --stat
```

### Detailed Changes (Last 5 files)
```bash
git diff --name-only | head -5
```

## Impact Analysis

### Files Added
```bash
git status --short | grep "^??" | wc -l
```
_new files created_

### Files Modified
```bash
git status --short | grep "^.M" | wc -l
```
_existing files changed_

### Files Staged
```bash
git status --short | grep "^[MAD]" | wc -l
```
_files ready for commit_

## Next Steps

### 1. Review Changes
```bash
git diff
```
_Review what actually changed_

### 2. Stage Your Changes
```bash
git add .
```
_or selectively: git add <file>_

### 3. Commit
```bash
git commit -m "your commit message"
```
_The pre-commit hook will validate your commit readiness_

### 4. Push (When Ready)
```bash
git push
```

## Task Completion Checklist

- [ ] Changes reviewed
- [ ] Tests passing (if applicable)
- [ ] Documentation updated (if needed)
- [ ] No sensitive data included
- [ ] Commit message follows project conventions

---

## Task Context

**Branch**: $(git branch --show-current)
**Completion Time**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Working Directory**: $(pwd)

---

**Good to go?** Use the commit command when ready. The pre-commit hook will help you validate everything before committing.
```

**Creation Command**:

```bash
cat > .claude/hooks/post-task.md << 'EOF'
# Post-Task Summary

The task has completed. Here's what changed and what to do next.

## Files Modified

```bash
git status --short
```

## Changes Summary

### Git Diff Overview
```bash
git diff --stat
```

### Detailed Changes (Last 5 files)
```bash
git diff --name-only | head -5
```

## Impact Analysis

### Files Added
```bash
git status --short | grep "^??" | wc -l
```
_new files created_

### Files Modified
```bash
git status --short | grep "^.M" | wc -l
```
_existing files changed_

### Files Staged
```bash
git status --short | grep "^[MAD]" | wc -l
```
_files ready for commit_

## Next Steps

### 1. Review Changes
```bash
git diff
```
_Review what actually changed_

### 2. Stage Your Changes
```bash
git add .
```
_or selectively: git add <file>_

### 3. Commit
```bash
git commit -m "your commit message"
```
_The pre-commit hook will validate your commit readiness_

### 4. Push (When Ready)
```bash
git push
```

## Task Completion Checklist

- [ ] Changes reviewed
- [ ] Tests passing (if applicable)
- [ ] Documentation updated (if needed)
- [ ] No sensitive data included
- [ ] Commit message follows project conventions

---

## Task Context

**Branch**: $(git branch --show-current)
**Completion Time**: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
**Working Directory**: $(pwd)

---

**Good to go?** Use the commit command when ready. The pre-commit hook will help you validate everything before committing.
EOF
```

---

### 3. Pre-Commit Hook

**File**: `.claude/hooks/pre-commit.md`

**Purpose**: Validate commit readiness and provide guidance for creating good commits.

**When it triggers**: Before creating a git commit.

**What it does**:
- Shows staged files
- Checks for common commit mistakes
- Validates commit message quality
- Provides commit message suggestions
- Shows what will be committed

**Full Hook Content**:

```markdown
# Pre-Commit Validation

You're about to create a commit. Let me validate everything is ready.

## What Will Be Committed

### Staged Files
```bash
git diff --cached --name-only
```

### Staged Changes Summary
```bash
git diff --cached --stat
```

## Commit Readiness Checks

### 1. File Content Checks

#### Check for Secrets/Sensitive Data
```bash
git diff --cached | grep -i "password\|secret\|api_key\|token\|credential" | head -3 || echo "✓ No obvious sensitive data detected"
```

#### Check for Debug/TODO Statements
```bash
git diff --cached | grep -i "TODO\|FIXME\|XXX\|HACK\|debugger\|pdb" | head -3 || echo "✓ No debug markers found"
```

#### Check for Large Files
```bash
git diff --cached --name-only | xargs ls -lh 2>/dev/null | awk '$5 > "1M" {print $9, $5}' || echo "✓ No large files detected"
```

### 2. Branch Check
```bash
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
  echo "⚠ Warning: Committing directly to $CURRENT_BRANCH"
else
  echo "✓ Branch: $CURRENT_BRANCH"
fi
```

### 3. Commit Message Preview
```bash
# Claude will provide the commit message
# This section shows where it will appear
```

## Commit Message Guidelines

A good commit message should:

1. **Start with a verb** (imperative mood)
   - ✓ "Add new feature for X"
   - ✓ "Fix bug in Y component"
   - ✗ "Added new feature" (past tense)
   - ✗ "Adding feature" (continuous)

2. **Be specific but concise**
   - ✓ "Add DynamoDB cache for investigation results"
   - ✗ "Add some stuff"

3. **Reference issues if applicable**
   - ✓ "Fix #123: Handle empty repository list"
   - ✓ "Implement #45: Add retry logic"

4. **Explain why, not just what**
   - ✓ "Add timeout to prevent hanging on large repos"
   - ✗ "Add timeout"

### Commit Message Template

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Example**:
```
feat(investigator): Add caching layer for API results

- Implement DynamoDB-based cache
- Add cache invalidation logic
- Reduce API calls by 60%

Closes #123
```

## Pre-Commit Checklist

Before committing, verify:

- [ ] Changes are staged correctly (use `git add` to stage)
- [ ] Commit message is clear and follows guidelines
- [ ] No sensitive data included (API keys, passwords)
- [ ] No debug code left behind (print statements, breakpoints)
- [ ] Changes are minimal and focused (one logical change)
- [ ] Tests pass (if applicable)
- [ ] Documentation updated (if needed)

## Staging vs. Not Staging

### Stage Specific Files
```bash
git add path/to/file.py
git add path/to/another/file.py
```

### Stage All Changes
```bash
git add .
```

### Unstage Files
```bash
git reset path/to/file.py
```

### View Staged vs. Unstaged
```bash
git diff          # unstaged changes
git diff --cached # staged changes
```

---

## Commit Decision

Based on the checks above:

✓ **Ready to commit** - All validations passed
⚠ **Warnings present** - Review the warnings above, but you can still commit
❌ **Issues detected** - Please address the issues before committing

---

**Remember**: This is a non-blocking validation. You can proceed with the commit regardless of the warnings above.
However, addressing any issues now will prevent problems later.
```

**Creation Command**:

```bash
cat > .claude/hooks/pre-commit.md << 'EOF'
# Pre-Commit Validation

You're about to create a commit. Let me validate everything is ready.

## What Will Be Committed

### Staged Files
```bash
git diff --cached --name-only
```

### Staged Changes Summary
```bash
git diff --cached --stat
```

## Commit Readiness Checks

### 1. File Content Checks

#### Check for Secrets/Sensitive Data
```bash
git diff --cached | grep -i "password\|secret\|api_key\|token\|credential" | head -3 || echo "✓ No obvious sensitive data detected"
```

#### Check for Debug/TODO Statements
```bash
git diff --cached | grep -i "TODO\|FIXME\|XXX\|HACK\|debugger\|pdb" | head -3 || echo "✓ No debug markers found"
```

#### Check for Large Files
```bash
git diff --cached --name-only | xargs ls -lh 2>/dev/null | awk '$5 > "1M" {print $9, $5}' || echo "✓ No large files detected"
```

### 2. Branch Check
```bash
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
  echo "⚠ Warning: Committing directly to $CURRENT_BRANCH"
else
  echo "✓ Branch: $CURRENT_BRANCH"
fi
```

### 3. Commit Message Preview
```bash
# Claude will provide the commit message
# This section shows where it will appear
```

## Commit Message Guidelines

A good commit message should:

1. **Start with a verb** (imperative mood)
   - ✓ "Add new feature for X"
   - ✓ "Fix bug in Y component"
   - ✗ "Added new feature" (past tense)
   - ✗ "Adding feature" (continuous)

2. **Be specific but concise**
   - ✓ "Add DynamoDB cache for investigation results"
   - ✗ "Add some stuff"

3. **Reference issues if applicable**
   - ✓ "Fix #123: Handle empty repository list"
   - ✓ "Implement #45: Add retry logic"

4. **Explain why, not just what**
   - ✓ "Add timeout to prevent hanging on large repos"
   - ✗ "Add timeout"

### Commit Message Template

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore

**Example**:
```
feat(investigator): Add caching layer for API results

- Implement DynamoDB-based cache
- Add cache invalidation logic
- Reduce API calls by 60%

Closes #123
```

## Pre-Commit Checklist

Before committing, verify:

- [ ] Changes are staged correctly (use `git add` to stage)
- [ ] Commit message is clear and follows guidelines
- [ ] No sensitive data included (API keys, passwords)
- [ ] No debug code left behind (print statements, breakpoints)
- [ ] Changes are minimal and focused (one logical change)
- [ ] Tests pass (if applicable)
- [ ] Documentation updated (if needed)

## Staging vs. Not Staging

### Stage Specific Files
```bash
git add path/to/file.py
git add path/to/another/file.py
```

### Stage All Changes
```bash
git add .
```

### Unstage Files
```bash
git reset path/to/file.py
```

### View Staged vs. Unstaged
```bash
git diff          # unstaged changes
git diff --cached # staged changes
```

---

## Commit Decision

Based on the checks above:

✓ **Ready to commit** - All validations passed
⚠ **Warnings present** - Review the warnings above, but you can still commit
❌ **Issues detected** - Please address the issues before committing

---

**Remember**: This is a non-blocking validation. You can proceed with the commit regardless of the warnings above.
However, addressing any issues now will prevent problems later.
EOF
```

---

## Directory Structure

After creating all hooks, your `.claude` directory should look like this:

```
.claude/
├── hooks/
│   ├── pre-task.md
│   ├── post-task.md
│   └── pre-commit.md
├── CLAUDE.md
└── other config files...
```

**Verification Command**:
```bash
ls -la .claude/hooks/
```

Expected output:
```
pre-task.md
post-task.md
pre-commit.md
```

---

## Non-Blocking Design

### Philosophy

Hooks are designed to **inform and guide**, not **block and prevent**. This is intentional because:

1. **Automation Efficiency**: In fully automated mode, you don't want tasks to stop for warnings
2. **Developer Autonomy**: You know your context better than the hooks do
3. **Fast Iteration**: Don't let perfect be the enemy of good

### How Non-Blocking Works

Each hook follows this pattern:

```
1. Check something
2. Report the result
3. Provide guidance if there's an issue
4. Explicitly state you can proceed regardless
```

Example:
```
⚠ Warning: No virtual environment detected
  Run: python -m venv .venv && source .venv/bin/activate

[Continue with task anyway...]
```

### Override Example

If a hook warns you but you want to proceed anyway:

**User**: "Create a new user module"
**Hook**: "⚠ Warning: No virtual environment detected"
**User**: "Proceed anyway"
**Claude**: "Continuing with task..."

The hook provided visibility, but didn't prevent the task.

---

## Verification

### Test All Hooks

#### 1. Test Pre-Task Hook

```bash
# Trigger the pre-task hook by asking Claude to do any task
echo "Triggering pre-task hook check..."
```

Then ask Claude: "Create a simple test file"

**Expected Output**:
- AWS credentials check
- Virtual environment status
- DynamoDB accessibility
- Git branch and status
- Task environment summary

#### 2. Test Post-Task Hook

After a task completes, you should see:
- Modified files list
- Git diff summary
- Impact analysis (files added/modified)
- Next steps guidance
- Completion checklist

#### 3. Test Pre-Commit Hook

```bash
# Make a small change
echo "# Test" > test-hook.txt

# Stage it
git add test-hook.txt

# Trigger pre-commit by asking Claude to commit
echo "Ready to test pre-commit hook"
```

Then ask Claude: "Commit the changes with message 'Test hooks'"

**Expected Output**:
- Staged files list
- Changes summary
- Content checks (secrets, debug statements, large files)
- Branch validation
- Commit message guidelines
- Pre-commit checklist

### Verify Hook Files

```bash
# Check all hooks exist
ls -1 .claude/hooks/
```

Expected:
```
pre-commit.md
post-task.md
pre-task.md
```

```bash
# Verify hook content
echo "=== Pre-Task Hook ==="
head -20 .claude/hooks/pre-task.md

echo -e "\n=== Post-Task Hook ==="
head -20 .claude/hooks/post-task.md

echo -e "\n=== Pre-Commit Hook ==="
head -20 .claude/hooks/pre-commit.md
```

### Integration Test

```bash
# Complete workflow test
echo "Starting hooks integration test..."

# 1. Pre-task check (happens automatically)
echo "Step 1: Pre-task validation"

# 2. Make a change
echo "## Test Change" >> README.md

# 3. Stage the change
git add README.md

# 4. Pre-commit check (happens automatically)
echo "Step 2: Pre-commit validation"

# 5. Commit (this triggers pre-commit hook)
# Ask Claude: "Commit with message 'Test hooks integration'"

# 6. Post-task check (happens automatically after commit)
echo "Step 3: Post-task summary"

echo "Hooks integration test complete!"
```

---

## Troubleshooting

### Common Hook Issues

#### Issue 1: Hooks Not Executing

**Symptom**: You don't see hook output when you expect it.

**Diagnosis**:
```bash
# Check if hooks directory exists
ls -la .claude/hooks/

# Check if hook files exist
ls -1 .claude/hooks/

# Verify hook files have content
wc -l .claude/hooks/*.md
```

**Solutions**:
1. Ensure `.claude/hooks/` directory exists
2. Ensure hook files are named correctly (lowercase, hyphenated)
3. Ensure hook files have markdown content
4. Restart Claude Code session after creating hooks

#### Issue 2: Hook Commands Failing

**Symptom**: Hook shows error messages for bash commands.

**Diagnosis**:
```bash
# Test individual commands from the hook
aws sts get-caller-identity
git status --short
```

**Solutions**:
1. **AWS credentials not configured**:
   ```bash
   aws configure
   ```
   Or set environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID="your-key"
   export AWS_SECRET_ACCESS_KEY="your-secret"
   ```

2. **Git not initialized**:
   ```bash
   git init
   ```

3. **Not in a git repository**:
   ```bash
   # Initialize git repo first
   git init
   git add .
   git commit -m "Initial commit"
   ```

#### Issue 3: Hooks Too Slow

**Symptom**: Pre-task hook takes more than 5 seconds.

**Diagnosis**:
```bash
# Time each command in the hook
time aws sts get-caller-identity
time git status
time aws dynamodb list-tables --region us-east-1
```

**Solutions**:
1. **Slow AWS calls**: Cache credentials or reduce API calls
2. **Slow git status**: Large repo with many files - consider git ignore optimizations
3. **Network issues**: Check your internet connection for AWS API calls

#### Issue 4: Hook Output Not Clear

**Symptom**: Hook runs but output is confusing or incomplete.

**Diagnosis**:
```bash
# Review hook content
cat .claude/hooks/pre-task.md
```

**Solutions**:
1. Add more context to explain what each check does
2. Add headers and sections for better organization
3. Use emoji or symbols for visual clarity (✓ ⚠ ❌)
4. Add "What This Means" section to interpret results

#### Issue 5: Hooks Blocking Execution

**Symptom**: Claude stops and asks for confirmation after hook output.

**Diagnosis**: This is actually **correct behavior** in interactive mode.

**Solutions**:
1. **Understanding**: This is normal - hooks provide visibility, you decide to proceed
2. **Automated mode**: Use command-line flags for non-interactive operation
3. **Review hooks**: Ensure hooks say "you can proceed" not "you must stop"

### Hook Performance Optimization

If hooks are slow, optimize them:

#### Remove Unnecessary Checks

```markdown
## Original (slow)
```bash
# Check all AWS regions
for region in us-east-1 us-west-2 eu-west-1; do
  aws dynamodb list-tables --region $region
done
```

## Optimized (fast)
```bash
# Check only configured region
aws dynamodb list-tables --region us-east-1 --query "TableNames[0]" --output text
```
```

#### Add Timeouts

```bash
# Add timeout to prevent hanging
timeout 5 aws sts get-caller-identity || echo "⚠ AWS check timed out"
```

#### Cache Results

```bash
# Use a cache file to avoid repeated checks
CACHE_FILE=".claude/.cache/aws-check"
if [ -f "$CACHE_FILE" ] && [ $(find "$CACHE_FILE" -mmin -5) ]; then
  cat "$CACHE_FILE"
else
  aws sts get-caller-identity > "$CACHE_FILE" 2>&1
  cat "$CACHE_FILE"
fi
```

### Debug Mode

To debug hooks, add verbose output:

```markdown
## Debug Information
```bash
set -x  # Enable debug mode
echo "Hook: pre-task"
echo "Working directory: $(pwd)"
echo "Git status:"
git status --short
set +x  # Disable debug mode
```
```

### Getting Help

If hooks still don't work:

1. **Check Claude Code version**:
   ```bash
   claude --version
   ```

2. **Review documentation**:
   - Claude Code README
   - `.claude/CLAUDE.md` if it exists

3. **Test with minimal hook**:
   ```bash
   echo "# Test Hook" > .claude/hooks/pre-task.md
   ```

4. **Enable verbose logging** (if available):
   ```bash
   claude --verbose
   ```

5. **Check for conflicting tools**:
   - Traditional git hooks in `.git/hooks/`
   - Other AI assistant tools
   - Pre-commit frameworks

---

## Best Practices

### 1. Keep Hooks Fast

- Pre-task: < 5 seconds
- Post-task: < 10 seconds
- Pre-commit: < 5 seconds

### 2. Provide Context

Don't just run commands - explain what you're checking and why.

```markdown
### AWS Credentials Check
_Verifying you can access AWS services for DynamoDB operations_

```bash
aws sts get-caller-identity
```
```

### 3. Use Non-Blocking Language

✓ Good: "⚠ Warning: No virtual environment detected"
✓ Good: "You can proceed, but some features may be limited"

❌ Bad: "ERROR: Must activate virtual environment"
❌ Bad: "Cannot continue without AWS credentials"

### 4. Provide Actionable Guidance

Don't just report problems - show how to fix them.

```markdown
⚠ Warning: No virtual environment detected
  Run: python -m venv .venv && source .venv/bin/activate
```

### 5. Test Hooks Regularly

```bash
# Quick test after changes
echo "test" > test.txt
git add test.txt
# Ask Claude to commit - triggers pre-commit hook
git reset test.txt
rm test.txt
```

### 6. Version Control Your Hooks

Hooks are part of your development environment:

```bash
# Add hooks to git
git add .claude/hooks/
git commit -m "docs: add comprehensive hooks for validation"
```

### 7. Customize for Your Project

Adapt these hooks to your specific needs:

- **AWS projects**: Keep AWS checks
- **Python projects**: Add venv and pip checks
- **Node.js projects**: Add npm/node version checks
- **Documentation projects**: Add spelling/grammar checks

---

## Advanced Usage

### Conditional Hooks

Make hooks smarter by checking context:

```markdown
# Only run certain checks on specific branches
```bash
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
  echo "⚠ Warning: About to commit to main branch"
  echo "  Consider creating a feature branch instead"
fi
```
```

### Hook Chaining

Have hooks call other scripts:

```markdown
## Run External Validation
```bash
if [ -f "scripts/pre-commit-check.sh" ]; then
  bash scripts/pre-commit-check.sh
fi
```
```

### Environment-Specific Hooks

Different behavior for development vs. production:

```markdown
## Environment Check
```bash
if [ "$ENVIRONMENT" = "production" ]; then
  echo "⚠ PRODUCTION MODE - Extra validation enabled"
  # Run additional checks
fi
```
```

---

## Summary

### What You Created

1. **pre-task.md**: Validates environment before tasks start
2. **post-task.md**: Shows impact and next steps after tasks complete
3. **pre-commit.md**: Validates commit readiness before creating commits

### Key Benefits

- **Visibility**: See what's happening before/during/after operations
- **Guidance**: Get context and actionable recommendations
- **Safety**: Catch common mistakes before they cause problems
- **Efficiency**: Fast, non-blocking checks that don't slow you down

### Next Steps

1. Create all three hook files using the provided commands
2. Test each hook by triggering it (see Verification section)
3. Customize hooks for your specific project needs
4. Add hooks to version control
5. Share with your team for consistent workflow

---

## Appendix: Quick Reference

### Hook File Locations

```
.claude/hooks/pre-task.md      # Before any task
.claude/hooks/post-task.md     # After task completion
.claude/hooks/pre-commit.md    # Before git commit
```

### Trigger Commands

```bash
# Pre-task: Automatic when you ask Claude to do something
# Post-task: Automatic after task completes
# Pre-commit: Automatic when you commit
```

### Verification Commands

```bash
# List all hooks
ls -1 .claude/hooks/

# View hook content
cat .claude/hooks/pre-task.md
cat .claude/hooks/post-task.md
cat .claude/hooks/pre-commit.md

# Test hooks
# (See Verification section above)
```

### Common Modifications

- Add project-specific checks
- Change AWS region
- Modify commit message guidelines
- Add team-specific conventions
- Integrate with existing tools

---

**End of Hooks Guide**

For questions or issues, refer to the Troubleshooting section or check the main project documentation.
