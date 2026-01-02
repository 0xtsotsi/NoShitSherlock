#!/usr/bin/env python3
"""
Test script for Claude API integration.
Tests both API mode and CLI mode.
"""

import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from investigator.core.claude_analyzer import ClaudeAnalyzer
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_api_mode():
    """Test Claude API mode (requires ANTHROPIC_API_KEY)."""
    print("\n" + "=" * 70)
    print("TESTING CLAUDE API MODE")
    print("=" * 70)

    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        print("\n❌ ANTHROPIC_API_KEY not set!")
        print("\nTo test API mode, set your API key:")
        print("  export ANTHROPIC_API_KEY='sk-ant-your-key-here'")
        print("\nGet your API key from: https://console.anthropic.com/")
        return False

    print(f"\n✓ API key found: {api_key[:10]}...{api_key[-4:]}")
    print("\nInitializing ClaudeAnalyzer in API mode...")

    # Force API mode
    os.environ['USE_CLAUDE_CLI'] = 'false'

    try:
        # Import fresh Config to pick up env var
        from investigator.core.config import Config
        print(f"Config.USE_CLAUDE_CLI = {Config.USE_CLAUDE_CLI}")

        analyzer = ClaudeAnalyzer(api_key=api_key, logger=logger)

        print("\n✓ ClaudeAnalyzer initialized successfully!")
        print(f"  Mode: {analyzer.mode}")

        # Test with a simple prompt
        print("\n" + "-" * 70)
        print("Sending test prompt to Claude...")
        print("-" * 70)

        test_prompt = "Say 'Hello from Claude API!' in a creative way."
        result = analyzer.analyze_with_context(
            prompt_template=test_prompt,
            repo_structure="",
            previous_context=None
        )

        print("\n" + "-" * 70)
        print("RESPONSE FROM CLAUDE:")
        print("-" * 70)
        print(result)
        print("-" * 70)

        print("\n✅ API MODE TEST PASSED!")
        return True

    except Exception as e:
        print(f"\n❌ API MODE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_mode():
    """Test Claude CLI mode (requires Claude CLI installed)."""
    print("\n" + "=" * 70)
    print("TESTING CLAUDE CLI MODE")
    print("=" * 70)

    # Check if CLI is available
    import shutil
    claude_path = shutil.which('claude')

    if not claude_path:
        print("\n❌ Claude CLI not found!")
        print("\nTo test CLI mode, install the Claude CLI:")
        print("  npm install -g @anthropic-ai/claude-code")
        print("  claude login")
        return False

    print(f"\n✓ Claude CLI found at: {claude_path}")
    print("\nInitializing ClaudeAnalyzer in CLI mode...")

    # Force CLI mode
    os.environ['USE_CLAUDE_CLI'] = 'true'

    try:
        # Import fresh Config to pick up env var
        from investigator.core.config import Config
        print(f"Config.USE_CLAUDE_CLI = {Config.USE_CLAUDE_CLI}")

        # CLI mode doesn't need API key
        analyzer = ClaudeAnalyzer(api_key=None, logger=logger)

        print("\n✓ ClaudeAnalyzer initialized successfully!")
        print(f"  Mode: {analyzer.mode}")

        # Test with a simple prompt
        print("\n" + "-" * 70)
        print("Sending test prompt to Claude via CLI...")
        print("-" * 70)

        test_prompt = "Say 'Hello from Claude CLI!' in a creative way."
        result = analyzer.analyze_with_context(
            prompt_template=test_prompt,
            repo_structure="",
            previous_context=None
        )

        print("\n" + "-" * 70)
        print("RESPONSE FROM CLAUDE:")
        print("-" * 70)
        print(result)
        print("-" * 70)

        print("\n✅ CLI MODE TEST PASSED!")
        return True

    except Exception as e:
        print(f"\n❌ CLI MODE TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run tests based on environment configuration."""
    print("\n" + "=" * 70)
    print("CLAUDE API/CLI INTEGRATION TEST")
    print("=" * 70)

    # Check current mode
    current_mode = os.getenv('USE_CLAUDE_CLI', 'false').lower() == 'true'
    print(f"\nCurrent USE_CLAUDE_CLI setting: {current_mode}")

    # Run appropriate test
    if current_mode:
        success = test_cli_mode()
    else:
        success = test_api_mode()

    # Summary
    print("\n" + "=" * 70)
    if success:
        print("✅ TEST COMPLETED SUCCESSFULLY")
        print("=" * 70)
        sys.exit(0)
    else:
        print("❌ TEST FAILED")
        print("=" * 70)
        sys.exit(1)

if __name__ == "__main__":
    main()
