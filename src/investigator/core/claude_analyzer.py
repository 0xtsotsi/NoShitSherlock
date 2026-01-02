"""
Claude API integration for the Claude Investigator.

Supports two modes:
1. API mode (default): Uses Anthropic API with ANTHROPIC_API_KEY
2. CLI mode: Uses Claude CLI with subscription auth (subclaude technique)
"""

from anthropic import Anthropic

from .config import Config


class ClaudeCLIError(Exception):
    """Raised when Claude CLI invocation fails."""


class ClaudeAnalyzer:
    """Handles Claude API interactions for analysis."""

    def __init__(self, api_key: str | None = None, logger=None):
        """
        Initialize the Claude analyzer with either API or CLI mode.

        Args:
            api_key: Anthropic API key (required if USE_CLAUDE_CLI=false, ignored in CLI mode)
            logger: Logger instance for output
        """
        self.logger = logger
        self.use_cli = Config.USE_CLAUDE_CLI

        if self.use_cli:
            # CLI mode - import and use the CLI adapter
            from .claude_cli_adapter import ClaudeCLIClient

            self.client: ClaudeCLIClient | Anthropic = ClaudeCLIClient(logger)
            self.mode = "CLI"
            if logger:
                logger.warning("=" * 70)
                logger.warning("CLAUDE CLI MODE ACTIVE")
                logger.warning("Using Claude CLI binary instead of Anthropic API")
                logger.warning("=" * 70)
        else:
            # API mode - use the Anthropic SDK
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY required when USE_CLAUDE_CLI=false. "
                    "Set ANTHROPIC_API_KEY environment variable or set USE_CLAUDE_CLI=true to use subscription mode."
                )
            self.client = Anthropic(api_key=api_key)
            self.mode = "API"
            if logger:
                logger.info("Using Anthropic API for Claude requests")

        if logger:
            logger.info(f"Claude Analyzer initialized in {self.mode} mode")

    def clean_prompt(self, prompt_template: str) -> str:
        """
        Clean the prompt template by removing version lines and other metadata.

        Args:
            prompt_template: Raw prompt template that may contain version headers

        Returns:
            Cleaned prompt template ready for Claude
        """
        if not prompt_template:
            return prompt_template

        lines = prompt_template.split("\n")

        # Only clean if version line exists at the beginning
        if lines and lines[0].startswith("version"):
            lines = lines[1:]
            if self.logger:
                self.logger.debug("Removed version line from prompt")

            # Remove any leading empty lines after version removal
            while lines and lines[0].strip() == "":
                lines = lines[1:]

            cleaned_prompt = "\n".join(lines)
            if self.logger:
                self.logger.debug(f"Cleaned prompt ({len(cleaned_prompt)} characters)")

            return cleaned_prompt
        else:
            # No version line found, return as-is
            return prompt_template

    def analyze_with_context(
        self,
        prompt_template: str,
        repo_structure: str,
        previous_context: str | None = None,
        config_overrides: dict | None = None,
    ) -> str:
        """
        Analyze using Claude with optional context from previous analyses.

        Args:
            prompt_template: Prompt template to use
            repo_structure: Repository structure string
            previous_context: Previous analysis results to include as context
            config_overrides: Optional dict with claude_model, max_tokens overrides

        Returns:
            Analysis result from Claude
        """
        if config_overrides is None:
            config_overrides = {}

        # Clean the prompt template first (remove version lines, etc.)
        cleaned_template = self.clean_prompt(prompt_template)

        # Replace placeholders in the cleaned prompt
        prompt = cleaned_template.replace("{repo_structure}", repo_structure)

        # Add previous context if available
        if previous_context:
            context_section = f"\n\n## Previous Analysis Context\n\n{previous_context}\n\n"
            prompt = prompt.replace("{previous_context}", context_section)
        else:
            # Remove the placeholder if no context
            prompt = prompt.replace("{previous_context}", "")

        if self.logger:
            self.logger.debug(f"Prompt created ({len(prompt)} characters)")
            self.logger.debug(f"Prompt preview (first 1000 chars): {prompt[:1000]}...")

        try:
            # Use config overrides or defaults
            claude_model = config_overrides.get("claude_model") or Config.CLAUDE_MODEL
            max_tokens = config_overrides.get("max_tokens") or Config.MAX_TOKENS

            # Log the mode being used
            if self.logger:
                self.logger.info(
                    f"[{self.mode} MODE] Sending analysis request via Claude {'CLI' if self.use_cli else 'API'}"
                )
                self.logger.debug(f"Using model: {claude_model}, max_tokens: {max_tokens}")

            response = self.client.messages.create(
                model=claude_model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )

            # Type assertion: response.content is a list with at least one text block
            content_block = response.content[0]
            analysis_text: str = getattr(content_block, "text", str(content_block))

            if self.logger:
                self.logger.info(
                    f"[{self.mode} MODE] Received analysis from Claude {'CLI' if self.use_cli else 'API'} "
                    f"({len(analysis_text)} characters)"
                )
                self.logger.debug(f"Analysis preview (first 1000 chars): {analysis_text[:1000]}...")

            return analysis_text

        except Exception as e:
            error_prefix = f"[{self.mode} MODE] "
            if self.logger:
                self.logger.error(f"{error_prefix}Claude request failed: {e!s}")
            raise Exception(f"{error_prefix}Failed to get analysis from Claude: {e!s}") from e

    def analyze_structure(self, repo_structure: str, prompt_template: str) -> str:
        """
        Analyze repository structure using Claude.

        Args:
            repo_structure: Repository structure string
            prompt_template: Prompt template to use

        Returns:
            Analysis result from Claude
        """
        return self.analyze_with_context(prompt_template, repo_structure, None)
