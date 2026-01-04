"""
Abstract base classes for PromptContext and PromptContextManager.

These base classes define the interface for managing analysis data references,
allowing different implementations (DynamoDB, file-based, etc.) for different environments.
"""

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PromptContextBase(ABC):
    """
    Abstract base class for managing prompt, repository structure, context, and results.

    Subclasses must implement the storage-specific methods.
    """

    repo_name: str
    step_name: str | None = None
    data_reference_key: str | None = None
    context_reference_keys: list[str] = field(default_factory=list)
    result_reference_key: str | None = None
    prompt_version: str = "1"

    @classmethod
    def create_for_step(
        cls, repo_name: str, step_name: str, prompt_version: str = "1"
    ) -> "PromptContextBase":
        """
        Create a new PromptContext for a specific analysis step.

        Args:
            repo_name: Name of the repository being analyzed
            step_name: Name of the analysis step
            prompt_version: Version of the prompt (default "1")

        Returns:
            New PromptContext instance
        """
        return cls(repo_name=repo_name, step_name=step_name, prompt_version=prompt_version)

    @abstractmethod
    def save_prompt_data(
        self, prompt_content: str, repo_structure: str, ttl_minutes: int = 60
    ) -> str:
        """
        Save prompt and repository structure to storage.

        Args:
            prompt_content: The prompt template content
            repo_structure: Repository structure string
            ttl_minutes: TTL for the data in minutes (may be ignored by some implementations)

        Returns:
            Reference key for the saved data
        """

    @abstractmethod
    def get_prompt_and_context(self) -> dict[str, Any]:
        """
        Retrieve prompt data and context from storage.

        Returns:
            Dictionary containing prompt_content, repo_structure, and context
        """

    @abstractmethod
    def get_result(self) -> str | None:
        """
        Retrieve the analysis result from storage.

        Returns:
            The result content or None if not found
        """

    @abstractmethod
    def cleanup(self):
        """
        Clean up all temporary data associated with this context.
        """

    def add_context_reference(self, reference_key: str):
        """
        Add a context reference key from a previous step.

        Args:
            reference_key: Reference key of a previous step's result
        """
        if reference_key and reference_key not in self.context_reference_keys:
            self.context_reference_keys.append(reference_key)
            logger.debug("Added context reference: %s", reference_key)

    def add_context_from_steps(self, step_names: list[str], step_results: dict[str, str]):
        """
        Add context references from specific previous steps.

        Args:
            step_names: List of step names to include as context
            step_results: Dictionary mapping step names to their result reference keys
        """
        for step_name in step_names:
            if step_name in step_results:
                self.add_context_reference(step_results[step_name])
            else:
                logger.warning("Step %s not found in results for context", step_name)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to dictionary for serialization (e.g., passing between activities).

        Returns:
            Dictionary representation of the context
        """
        return {
            "repo_name": self.repo_name,
            "step_name": self.step_name,
            "data_reference_key": self.data_reference_key,
            "context_reference_keys": self.context_reference_keys,
            "result_reference_key": self.result_reference_key,
            "prompt_version": self.prompt_version,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PromptContextBase":
        """
        Create PromptContext from dictionary (e.g., from activity parameters).

        Args:
            data: Dictionary containing context data

        Returns:
            PromptContext instance
        """
        repo_name = data.get("repo_name")
        if repo_name is None:
            raise ValueError("repo_name is required")

        return cls(
            repo_name=repo_name,
            step_name=data.get("step_name"),
            data_reference_key=data.get("data_reference_key"),
            context_reference_keys=data.get("context_reference_keys", []),
            result_reference_key=data.get("result_reference_key"),
            prompt_version=data.get("prompt_version", "1"),
        )

    def to_json(self) -> str:
        """
        Convert to JSON string for serialization.

        Returns:
            JSON string representation
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> "PromptContextBase":
        """
        Create PromptContext from JSON string.

        Args:
            json_str: JSON string containing context data

        Returns:
            PromptContext instance
        """
        return cls.from_dict(json.loads(json_str))

    def __repr__(self) -> str:
        """String representation for debugging."""
        return (
            f"{self.__class__.__name__}(repo={self.repo_name}, step={self.step_name}, "
            f"data_key={self.data_reference_key[:20] if self.data_reference_key else None}..., "
            f"context_keys={len(self.context_reference_keys)}, "
            f"result_key={self.result_reference_key[:20] if self.result_reference_key else None}...)"
        )


class PromptContextManagerBase(ABC):
    """
    Abstract base class for managing multiple PromptContexts across analysis steps.
    """

    def __init__(self, repo_name: str):
        """
        Initialize the manager for a repository.

        Args:
            repo_name: Name of the repository being analyzed
        """
        self.repo_name = repo_name
        self.contexts: dict[str, PromptContextBase] = {}
        self.step_results: dict[str, str] = {}  # Maps step names to result keys
        logger.info("Initialized %s for %s", self.__class__.__name__, repo_name)

    @abstractmethod
    def create_context_for_step(
        self, step_name: str, context_config: list | None = None
    ) -> PromptContextBase:
        """
        Create a new context for an analysis step with proper context references.

        Args:
            step_name: Name of the analysis step
            context_config: Configuration for which previous steps to include as context

        Returns:
            New PromptContext instance
        """

    @abstractmethod
    def retrieve_all_results(self) -> dict[str, str]:
        """
        Retrieve all results from storage.

        Returns:
            Dictionary mapping step names to their result content
        """

    def register_result(self, step_name: str, result_key: str):
        """
        Register a step's result key for use as context in later steps.

        Args:
            step_name: Name of the completed step
            result_key: Reference key of the step's result
        """
        self.step_results[step_name] = result_key
        logger.info("Registered result for %s: %s", result_key, step_name)

    def get_all_result_keys(self) -> list[str]:
        """
        Get all result reference keys.

        Returns:
            List of all result reference keys
        """
        return list(self.step_results.values())

    def cleanup_all(self):
        """Clean up all contexts and their associated data."""
        for context in self.contexts.values():
            context.cleanup()
        logger.info("Cleaned up %s contexts for %s", len(self.contexts), self.repo_name)
