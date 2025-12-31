#!/usr/bin/env python3
"""
Test script to verify that USE_CLAUDE_CLI environment variable correctly switches
between CLI and API modes.

This script tests:
1. CLI binary detection and verification
2. Mode selection based on USE_CLAUDE_CLI environment variable
3. Logging output confirming the active mode
"""

import os
import sys
import logging

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from investigator.core.claude_analyzer import ClaudeAnalyzer


def setup_logging():
    """Set up logging to show all messages."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def test_api_mode():
    """Test API mode (USE_CLAUDE_CLI not set or false)."""
    logger = setup_logging()
    logger.info("\n" + "=" * 80)
    logger.info("TEST 1: API Mode (USE_CLAUDE_CLI not set)")
    logger.info("=" * 80)

    # Ensure USE_CLAUDE_CLI is not set
    os.environ.pop('USE_CLAUDE_CLI', None)

    try:
        # This will fail without a valid API key, but we should see the mode message
        analyzer = ClaudeAnalyzer(api_key="test-key", logger=logger)
        logger.info(f"Mode detected: {analyzer.mode}")
        assert analyzer.mode == "API", f"Expected API mode, got {analyzer.mode}"
        logger.info("✓ API mode correctly activated")
        return True
    except Exception as e:
        logger.error(f"✗ Test failed: {e}")
        return False


def test_cli_mode():
    """Test CLI mode (USE_CLAUDE_CLI=true)."""
    logger = setup_logging()
    logger.info("\n" + "=" * 80)
    logger.info("TEST 2: CLI Mode (USE_CLAUDE_CLI=true)")
    logger.info("=" * 80)

    # Set USE_CLAUDE_CLI
    os.environ['USE_CLAUDE_CLI'] = 'true'

    try:
        analyzer = ClaudeAnalyzer(api_key="dummy-key", logger=logger)
        logger.info(f"Mode detected: {analyzer.mode}")
        assert analyzer.mode == "CLI", f"Expected CLI mode, got {analyzer.mode}"
        logger.info("✓ CLI mode correctly activated")
        logger.info(f"✓ CLI binary found at: {analyzer.client.adapter.cli_path}")
        return True
    except RuntimeError as e:
        if "Claude CLI binary not found" in str(e):
            logger.warning("⚠ CLI mode requested but Claude CLI not installed")
            logger.warning("  This is expected if Claude CLI is not available")
            logger.info("✓ CLI mode switch works (but CLI not available)")
            return True
        else:
            logger.error(f"✗ Test failed with unexpected error: {e}")
            return False
    except Exception as e:
        logger.error(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_cli_mode_variations():
    """Test different variations of USE_CLAUDE_CLI values."""
    logger = setup_logging()
    logger.info("\n" + "=" * 80)
    logger.info("TEST 3: CLI Mode Value Variations")
    logger.info("=" * 80)

    test_values = [
        ('true', True, "lowercase true"),
        ('TRUE', True, "uppercase TRUE"),
        ('1', True, "numeric 1"),
        ('yes', True, "yes"),
        ('false', False, "false"),
        ('0', False, "numeric 0"),
        ('no', False, "no"),
        ('', False, "empty string"),
    ]

    all_passed = True
    for value, expected_cli, description in test_values:
        os.environ['USE_CLAUDE_CLI'] = value
        try:
            analyzer = ClaudeAnalyzer(api_key="test-key", logger=logger)
            expected_mode = "CLI" if expected_cli else "API"
            if analyzer.mode == expected_mode:
                logger.info(f"✓ '{value}' ({description}) -> {analyzer.mode} mode")
            else:
                logger.error(f"✗ '{value}' ({description}) -> expected {expected_mode}, got {analyzer.mode}")
                all_passed = False
        except RuntimeError as e:
            if expected_cli and "Claude CLI binary not found" in str(e):
                logger.info(f"✓ '{value}' ({description}) -> CLI mode (CLI not available)")
            else:
                logger.error(f"✗ '{value}' ({description}) -> unexpected error: {e}")
                all_passed = False
        except Exception as e:
            logger.error(f"✗ '{value}' ({description}) -> error: {e}")
            all_passed = False

    return all_passed


def test_no_fallback():
    """Test that CLI mode fails explicitly if CLI is not available."""
    logger = setup_logging()
    logger.info("\n" + "=" * 80)
    logger.info("TEST 4: No Silent Fallback to API")
    logger.info("=" * 80)

    # Set USE_CLAUDE_CLI but fake that CLI doesn't exist
    os.environ['USE_CLAUDE_CLI'] = 'true'

    # This test assumes we're checking if error is explicit
    logger.info("Testing that CLI mode errors are explicit...")

    try:
        analyzer = ClaudeAnalyzer(api_key="test-key", logger=logger)
        # If we get here, either CLI exists or there was a silent fallback
        if analyzer.mode == "CLI":
            logger.info("✓ CLI mode activated successfully")
            return True
        else:
            logger.error("✗ Silent fallback to API mode detected!")
            return False
    except RuntimeError as e:
        if "Claude CLI binary not found" in str(e):
            logger.info("✓ Explicit error when CLI not found (no silent fallback)")
            return True
        else:
            logger.error(f"✗ Unexpected error: {e}")
            return False


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("CLI MODE SWITCH VERIFICATION TESTS")
    print("=" * 80)

    results = []

    # Run all tests
    results.append(("API Mode", test_api_mode()))
    results.append(("CLI Mode", test_cli_mode()))
    results.append(("CLI Mode Variations", test_cli_mode_variations()))
    results.append(("No Silent Fallback", test_no_fallback()))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(passed for _, passed in results)

    print("=" * 80)
    if all_passed:
        print("ALL TESTS PASSED ✓")
        return 0
    else:
        print("SOME TESTS FAILED ✗")
        return 1


if __name__ == '__main__':
    sys.exit(main())
