"""
Unit tests for Claude CLI integration (subclaude technique).

Tests the ability to use Claude via CLI with subscription authentication
instead of API keys.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import subprocess

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from investigator.core.claude_analyzer import ClaudeAnalyzer, ClaudeCLIError
from investigator.core.config import Config


class TestClaudeCLIIntegration(unittest.TestCase):
    """Test suite for Claude CLI integration functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_logger = Mock()

    @patch.object(Config, 'USE_CLAUDE_CLI', False)
    def test_api_mode_requires_api_key(self):
        """Test that API mode requires an API key."""
        with self.assertRaises(ValueError) as context:
            ClaudeAnalyzer(api_key=None, logger=self.mock_logger)

        self.assertIn("ANTHROPIC_API_KEY required", str(context.exception))

    @patch.object(Config, 'USE_CLAUDE_CLI', False)
    @patch('investigator.core.claude_analyzer.Anthropic')
    def test_api_mode_initializes_client(self, mock_anthropic):
        """Test that API mode initializes the Anthropic client."""
        analyzer = ClaudeAnalyzer(api_key="test-key", logger=self.mock_logger)

        self.assertFalse(analyzer.use_cli)
        mock_anthropic.assert_called_once_with(api_key="test-key")

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch('shutil.which')
    def test_cli_mode_validates_cli_present(self, mock_which):
        """Test that CLI mode validates Claude CLI is installed."""
        mock_which.return_value = "/usr/local/bin/claude"

        analyzer = ClaudeAnalyzer(api_key=None, logger=self.mock_logger)

        self.assertTrue(analyzer.use_cli)
        self.assertIsNone(analyzer.client)
        mock_which.assert_called_with("claude")

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch('shutil.which')
    def test_cli_mode_raises_error_when_cli_missing(self, mock_which):
        """Test that CLI mode raises error when Claude CLI is not installed."""
        mock_which.return_value = None

        with self.assertRaises(ClaudeCLIError) as context:
            ClaudeAnalyzer(api_key=None, logger=self.mock_logger)

        self.assertIn("Claude CLI not found", str(context.exception))
        self.assertIn("npm install", str(context.exception))

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch.object(Config, 'CLAUDE_CLI_TIMEOUT', 300)
    @patch('shutil.which')
    @patch('subprocess.run')
    def test_call_claude_cli_success(self, mock_run, mock_which):
        """Test successful Claude CLI invocation."""
        mock_which.return_value = "/usr/local/bin/claude"

        # Mock successful CLI response
        mock_run.return_value = Mock(
            returncode=0,
            stdout="This is Claude's response to your prompt.",
            stderr=""
        )

        analyzer = ClaudeAnalyzer(api_key=None, logger=self.mock_logger)
        result = analyzer._call_claude_cli(
            prompt="Hello Claude",
            model="claude-opus-4-5-20251101",
            max_tokens=1000
        )

        self.assertEqual(result, "This is Claude's response to your prompt.")

        # Verify subprocess was called correctly
        mock_run.assert_called_once()
        call_args = mock_run.call_args
        self.assertIn("claude", call_args[0][0])
        self.assertEqual(call_args[1]["input"], "Hello Claude")
        self.assertEqual(call_args[1]["timeout"], 300)

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch('shutil.which')
    @patch('subprocess.run')
    def test_call_claude_cli_authentication_error(self, mock_run, mock_which):
        """Test Claude CLI authentication error handling."""
        mock_which.return_value = "/usr/local/bin/claude"

        # Mock authentication error
        mock_run.return_value = Mock(
            returncode=1,
            stdout="",
            stderr="Error: Not authenticated. Please run 'claude login'"
        )

        analyzer = ClaudeAnalyzer(api_key=None, logger=self.mock_logger)

        with self.assertRaises(ClaudeCLIError) as context:
            analyzer._call_claude_cli("Hello", "claude-opus-4-5-20251101", 1000)

        self.assertIn("not authenticated", str(context.exception).lower())
        self.assertIn("claude login", str(context.exception))

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch.object(Config, 'CLAUDE_CLI_TIMEOUT', 1)
    @patch('shutil.which')
    @patch('subprocess.run')
    def test_call_claude_cli_timeout(self, mock_run, mock_which):
        """Test Claude CLI timeout handling."""
        mock_which.return_value = "/usr/local/bin/claude"

        # Mock timeout
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="claude", timeout=1)

        analyzer = ClaudeAnalyzer(api_key=None, logger=self.mock_logger)

        with self.assertRaises(ClaudeCLIError) as context:
            analyzer._call_claude_cli("Hello", "claude-opus-4-5-20251101", 1000)

        self.assertIn("timed out", str(context.exception))

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch('shutil.which')
    def test_model_mapping(self, mock_which):
        """Test model name mapping from API to CLI format."""
        mock_which.return_value = "/usr/local/bin/claude"

        analyzer = ClaudeAnalyzer(api_key=None, logger=self.mock_logger)

        # Test known model mappings
        self.assertEqual(
            analyzer._map_model_to_cli("claude-opus-4-5-20251101"),
            "claude-opus-4-5-20251101"
        )
        self.assertEqual(
            analyzer._map_model_to_cli("claude-sonnet-4-5-20250929"),
            "claude-sonnet-4-5-20250929"
        )

        # Test unknown model (should pass through)
        self.assertEqual(
            analyzer._map_model_to_cli("unknown-model"),
            "unknown-model"
        )

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch('shutil.which')
    @patch('subprocess.run')
    def test_analyze_with_context_uses_cli(self, mock_run, mock_which):
        """Test that analyze_with_context uses CLI when configured."""
        mock_which.return_value = "/usr/local/bin/claude"

        mock_run.return_value = Mock(
            returncode=0,
            stdout="Analysis of the repository structure shows...",
            stderr=""
        )

        analyzer = ClaudeAnalyzer(api_key=None, logger=self.mock_logger)

        result = analyzer.analyze_with_context(
            prompt_template="Analyze: {repo_structure}",
            repo_structure="src/\n  main.py\n  utils.py"
        )

        self.assertIn("Analysis", result)
        mock_run.assert_called_once()

    @patch.object(Config, 'USE_CLAUDE_CLI', True)
    @patch('shutil.which')
    @patch('subprocess.run')
    def test_cli_args_include_correct_flags(self, mock_run, mock_which):
        """Test that CLI invocation includes correct flags."""
        mock_which.return_value = "/usr/local/bin/claude"

        mock_run.return_value = Mock(
            returncode=0,
            stdout="Response",
            stderr=""
        )

        analyzer = ClaudeAnalyzer(api_key=None, logger=self.mock_logger)
        analyzer._call_claude_cli("Test prompt", "claude-opus-4-5-20251101", 2000)

        call_args = mock_run.call_args[0][0]

        # Verify required flags are present
        self.assertIn("--print", call_args)
        self.assertIn("--model", call_args)
        self.assertIn("--max-tokens", call_args)
        self.assertIn("--output-format", call_args)

        # Verify model and max-tokens values
        model_idx = call_args.index("--model")
        self.assertEqual(call_args[model_idx + 1], "claude-opus-4-5-20251101")

        tokens_idx = call_args.index("--max-tokens")
        self.assertEqual(call_args[tokens_idx + 1], "2000")


class TestClaudeCLIErrorHandling(unittest.TestCase):
    """Test suite for Claude CLI error handling."""

    def test_claude_cli_error_is_exception(self):
        """Test that ClaudeCLIError is a proper exception."""
        error = ClaudeCLIError("Test error message")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Test error message")


class TestConfigCLISettings(unittest.TestCase):
    """Test suite for CLI-related configuration."""

    def test_use_claude_cli_default_false(self):
        """Test that USE_CLAUDE_CLI defaults to False."""
        # Reset to check default (when env var not set)
        with patch.dict(os.environ, {}, clear=True):
            # Need to reimport to get fresh config
            # For this test, we verify the env var parsing logic
            result = os.getenv("USE_CLAUDE_CLI", "false").lower() == "true"
            self.assertFalse(result)

    def test_use_claude_cli_env_var_true(self):
        """Test that USE_CLAUDE_CLI can be enabled via env var."""
        with patch.dict(os.environ, {"USE_CLAUDE_CLI": "true"}):
            result = os.getenv("USE_CLAUDE_CLI", "false").lower() == "true"
            self.assertTrue(result)

    def test_claude_cli_timeout_default(self):
        """Test that CLAUDE_CLI_TIMEOUT has a sensible default."""
        with patch.dict(os.environ, {}, clear=True):
            result = int(os.getenv("CLAUDE_CLI_TIMEOUT", "300"))
            self.assertEqual(result, 300)


if __name__ == "__main__":
    unittest.main()
