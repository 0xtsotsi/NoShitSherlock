# Using Your Claude Subscription with RepoSwarm

**TL;DR**: RepoSwarm can now use your existing Claude Max or Pro subscription instead of requiring separate API credits. One config change and you're set.

---

## The Problem

If you're paying $20-200/month for a Claude subscription, you've probably noticed something frustrating: that subscription only works on claude.ai and the official CLI. Want to build something with Claude? That's a separate API, with separate billing.

RepoSwarm originally required an Anthropic API key. This meant:
- Setting up API billing (separate from your subscription)
- Managing API credits
- Paying twice if you already have a Claude subscription

Not ideal for developers who just want to analyze their codebases.

## What We Found

A project called [subclaude](https://github.com/creativeprofit22/subclaude) showed a clever approach: instead of calling the API directly, pipe your prompts through the Claude CLI. The CLI is already authenticated with your subscription, so your requests use your existing quota.

The technique is simple:
1. Start the Claude CLI process
2. Send your prompt via stdin (standard input)
3. Capture the response from stdout

This bypasses the normal terminal detection that would block automated usage, making the CLI work just like an API endpoint.

## What Changed in RepoSwarm

We added a new option to toggle between API mode and CLI mode:

**Before (API mode only)**:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**Now (CLI mode available)**:
```
USE_CLAUDE_CLI=true
# No API key needed!
```

The core change was in our `ClaudeAnalyzer` class. When CLI mode is enabled, instead of:

```python
response = self.client.messages.create(
    model=model,
    messages=[{"role": "user", "content": prompt}]
)
```

We now run:

```python
proc = subprocess.run(
    ["claude", "--print", "--model", model, ...],
    input=prompt,
    capture_output=True
)
```

Same result, different path to get there.

## How to Use It

**Step 1**: Install the Claude CLI
```bash
npm install -g @anthropic-ai/claude-code
```

**Step 2**: Log in with your subscription
```bash
claude login
```

**Step 3**: Enable CLI mode in RepoSwarm
```bash
# In your .env.local
USE_CLAUDE_CLI=true
```

**Step 4**: Run as normal
```bash
mise investigate-one your-repo
```

That's it. RepoSwarm now uses your subscription instead of API credits.

## Quick Verification

```bash
export USE_CLAUDE_CLI=true
python -c "
from investigator.core.claude_analyzer import ClaudeAnalyzer
analyzer = ClaudeAnalyzer(logger=None)
print(f'Using CLI mode: {analyzer.use_cli}')
"
```

Should print: `Using CLI mode: True`

## Lessons Learned

1. **Sometimes the best integration is the simplest one.** subclaude is a Node.js library, and RepoSwarm is Python. Instead of adding Node.js as a dependency or calling subclaude via subprocess, we just replicated the core technique directly in Python. Five lines of subprocess code replaced what could have been a complex cross-language integration.

2. **The CLI is an API.** Command-line tools with structured input/output can work as programmatic interfaces. The Claude CLI accepts stdin and produces stdout - that's basically HTTP without the network overhead.

3. **Existing authentication is valuable.** The Claude CLI handles OAuth tokens, session management, and all the authentication complexity. By leveraging it, we got subscription billing "for free" without implementing any auth code.

## What's Next

- **Model-specific optimizations**: Different models may have different CLI flags worth exploring
- **Streaming support**: The CLI supports streaming output, which could improve UX for long analyses
- **Rate limit handling**: Subscription tiers have different quotas - we could add smarter retry logic

## Try It Out

The feature is available now in the main branch. If you have a Claude subscription, give CLI mode a try and let us know how it works for you.

```bash
git pull
export USE_CLAUDE_CLI=true
mise investigate-one hello-world
```

No API key setup. No separate billing. Just your existing subscription.

---

*Questions? Issues? Open a ticket on [GitHub](https://github.com/royosherove/repo-swarm/issues).*
