"""
Claude CLI adapter for the Claude Investigator.

This module provides a CLI-based alternative to the Anthropic Python SDK,
allowing the investigator to use the official Claude CLI binary instead of API calls.
"""

import json
import os
import shutil
import subprocess


class ClaudeCLIAdapter:
    """Adapter for using Claude CLI instead of the Anthropic Python SDK."""

    def __init__(self, logger):
        """
        Initialize the Claude CLI adapter.

        Args:
            logger: Logger instance for output

        Raises:
            RuntimeError: If Claude CLI binary is not found or not executable
        """
        self.logger = logger
        self.cli_path = self._detect_cli_binary()

        # Verify the CLI works
        self._verify_cli()

        self.logger.info(f"Claude CLI adapter initialized using: {self.cli_path}")

    def _detect_cli_binary(self) -> str:
        """
        Detect the Claude CLI binary location.

        Returns:
            str: Path to the Claude CLI binary

        Raises:
            RuntimeError: If CLI binary is not found
        """
        # Try to find the claude CLI in PATH
        cli_path = shutil.which("claude")

        if not cli_path:
            error_msg = (
                "Claude CLI binary not found in PATH. "
                "Please install the Claude CLI:\n"
                "  npm install -g @anthropic/claude-cli\n"
                "Or ensure it's available in your PATH."
            )
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

        # Check if it's executable
        if not os.access(cli_path, os.X_OK):
            error_msg = (
                f"Claude CLI found at {cli_path} but it's not executable. "
                f"Please check file permissions."
            )
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)

        self.logger.debug(f"Detected Claude CLI at: {cli_path}")
        return cli_path

    def _verify_cli(self) -> None:
        """
        Verify that the Claude CLI is working correctly.

        Raises:
            RuntimeError: If CLI verification fails
        """
        try:
            result = subprocess.run(
                [self.cli_path, "--version"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode != 0:
                error_msg = (
                    f"Claude CLI verification failed (exit code {result.returncode}).\n"
                    f"Error: {result.stderr}"
                )
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)

            version_output = result.stdout.strip()
            self.logger.debug(f"Claude CLI version: {version_output}")

        except subprocess.TimeoutExpired as err:
            error_msg = "Claude CLI verification timed out after 10 seconds"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg) from err
        except Exception as e:
            error_msg = f"Failed to verify Claude CLI: {e!s}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg) from e

    def create_message(self, model: str, max_tokens: int, messages: list) -> dict:
        """
        Create a message using the Claude CLI.

        This method mimics the Anthropic SDK's messages.create() interface
        but uses the CLI under the hood.

        Args:
            model: The Claude model to use
            max_tokens: Maximum tokens in the response
            messages: List of message dicts with 'role' and 'content'

        Returns:
            dict: Response object with structure similar to Anthropic SDK

        Raises:
            Exception: If the CLI call fails
        """
        # Extract the user prompt (assuming single user message for simplicity)
        if not messages or len(messages) == 0:
            raise ValueError("No messages provided")

        user_message = messages[0]
        if user_message.get("role") != "user":
            raise ValueError("First message must be from user")

        prompt = user_message.get("content", "")

        self.logger.info("Sending request to Claude CLI")
        self.logger.debug(f"Model: {model}, max_tokens: {max_tokens}")
        self.logger.debug(f"Prompt length: {len(prompt)} characters")

        try:
            # Prepare the CLI command
            # The Claude CLI accepts prompts via stdin or as arguments
            # We'll use stdin for large prompts
            cmd = [
                self.cli_path,
                "prompt",
                "--model",
                model,
                "--max-tokens",
                str(max_tokens),
                "--format",
                "json",  # Request JSON output for easier parsing
            ]

            self.logger.debug(f"Running CLI command: {' '.join(cmd)}")

            # Execute the CLI with the prompt as stdin
            result = subprocess.run(
                cmd,
                check=False,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=900,  # 15 minutes timeout (same as activity timeout)
            )

            if result.returncode != 0:
                error_msg = (
                    f"Claude CLI failed with exit code {result.returncode}.\n"
                    f"Error: {result.stderr}\n"
                    f"Output: {result.stdout}"
                )
                self.logger.error(error_msg)
                raise Exception(error_msg)

            # Parse the CLI output
            # The CLI might return JSON or plain text depending on the format flag
            response_text = result.stdout.strip()

            # Try to parse as JSON first
            try:
                response_data = json.loads(response_text)
                # If it's a JSON response from the CLI, extract the text
                if isinstance(response_data, dict) and "response" in response_data:
                    response_text = response_data["response"]
            except json.JSONDecodeError:
                # Not JSON, use the raw text
                pass

            self.logger.info(f"Received response from Claude CLI ({len(response_text)} characters)")
            self.logger.debug(f"Response preview: {response_text[:200]}...")

            # Return a response object that mimics the Anthropic SDK structure
            return {
                "content": [{"type": "text", "text": response_text}],
                "model": model,
                "stop_reason": "end_turn",
                "usage": {
                    "input_tokens": 0,  # CLI doesn't provide this
                    "output_tokens": 0,  # CLI doesn't provide this
                },
            }

        except subprocess.TimeoutExpired as err:
            error_msg = "Claude CLI request timed out after 15 minutes"
            self.logger.error(error_msg)
            raise Exception(error_msg) from err
        except Exception as e:
            error_msg = f"Failed to execute Claude CLI: {e!s}"
            self.logger.error(error_msg)
            raise Exception(error_msg) from e


class ClaudeCLIClient:
    """
    Client wrapper that provides an interface compatible with the Anthropic SDK.

    This allows seamless switching between API and CLI modes.
    """

    def __init__(self, logger):
        """
        Initialize the CLI client.

        Args:
            logger: Logger instance
        """
        self.logger = logger
        self.adapter = ClaudeCLIAdapter(logger)
        self.messages = self  # Allow client.messages.create() syntax

    def create(self, model: str, max_tokens: int, messages: list) -> "ClaudeCLIResponse":
        """
        Create a message using the Claude CLI.

        Args:
            model: The Claude model to use
            max_tokens: Maximum tokens in the response
            messages: List of message dicts

        Returns:
            ClaudeCLIResponse: Response object with SDK-compatible interface
        """
        response_data = self.adapter.create_message(model, max_tokens, messages)
        return ClaudeCLIResponse(response_data)


class ClaudeCLIResponse:
    """Response wrapper that mimics the Anthropic SDK response structure."""

    def __init__(self, response_data: dict):
        """
        Initialize the response wrapper.

        Args:
            response_data: Raw response data from the CLI adapter
        """
        self._data = response_data
        self.content = [ClaudeCLIContent(item) for item in response_data.get("content", [])]
        self.model = response_data.get("model", "")
        self.stop_reason = response_data.get("stop_reason", "")
        self.usage = response_data.get("usage", {})


class ClaudeCLIContent:
    """Content wrapper that mimics the Anthropic SDK content structure."""

    def __init__(self, content_data: dict):
        """
        Initialize the content wrapper.

        Args:
            content_data: Content data dict
        """
        self.type = content_data.get("type", "text")
        self.text = content_data.get("text", "")
