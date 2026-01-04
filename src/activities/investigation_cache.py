"""
Investigation cache management for repository analysis.

This module provides a class to handle the caching logic for repository
investigations, determining when a repository needs re-investigation and
managing the storage of investigation metadata.
"""

import logging
from datetime import UTC, datetime
from typing import Any

# Import models from the centralized models package
from models.investigation import (
    InvestigationDecision,
    InvestigationMetadata,
    PromptMetadata,
    RepositoryState,
)

# Import the key name creator for consistent key generation
from utils.storage_keys import KeyNameCreator

logger = logging.getLogger(__name__)


class InvestigationCache:
    """
    Manages investigation caching logic for repositories.

    This class encapsulates the logic for determining when a repository
    needs to be investigated based on its current state and previous
    investigation history. It also provides prompt-level caching to avoid
    re-running the same prompts for unchanged commits.
    """

    def __init__(self, storage_client: Any):
        """
        Initialize the investigation cache.

        Args:
            storage_client: Client for storing/retrieving investigation metadata
                          (e.g., DynamoDBClient)
        """
        self.storage_client = storage_client
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def _get_raw_investigation_data(self, investigation: Any) -> Any:
        """Get raw investigation data for backward compatibility with tests."""
        return getattr(investigation, "_raw_data", investigation)

    def check_needs_investigation(
        self,
        repo_name: str,
        current_state: RepositoryState,
        current_prompt_versions: dict[str, str] | None = None,
    ) -> InvestigationDecision:
        """
        Check if a repository needs investigation based on its current state,
        previous investigation history, and prompt versions.

        Args:
            repo_name: Name of the repository
            current_state: Current state of the repository
            current_prompt_versions: Optional dict of prompt names to versions

        Returns:
            InvestigationDecision with details about whether investigation is needed
        """
        # Log initial state
        self._log_initial_state(repo_name, current_state, current_prompt_versions)

        # Fetch last investigation from storage
        last_investigation = self._fetch_last_investigation(repo_name, current_state)
        if isinstance(last_investigation, InvestigationDecision):
            return last_investigation  # Early return for errors or no previous investigation

        # Extract and log last investigation data
        last_investigation_data = self._extract_last_investigation_data(last_investigation)

        # Run checks in order - each can return early if investigation is needed
        decision = self._check_commit_changes(
            current_state, last_investigation_data, last_investigation
        )
        if decision:
            return decision

        decision = self._check_branch_changes(
            current_state, last_investigation_data, last_investigation
        )
        if decision:
            return decision

        decision = self._check_prompt_version_changes(
            current_state, current_prompt_versions, last_investigation
        )
        if decision:
            return decision

        # No changes detected - return no investigation needed
        return self._create_no_investigation_decision(
            repo_name, current_state, last_investigation_data, last_investigation
        )

    def _log_initial_state(
        self,
        repo_name: str,
        current_state: RepositoryState,
        current_prompt_versions: dict[str, str] | None,
    ) -> None:
        """Log the initial state and prompt versions for the investigation check."""
        self.logger.info("🔍 CACHE CHECK: Starting investigation check for %s", repo_name)
        self.logger.info(
            "📊 CURRENT STATE: Branch: %s, Commit: %s",
            current_state.branch_name,
            current_state.commit_sha[:8],
        )

        if current_prompt_versions:
            self.logger.info(
                "📝 CURRENT PROMPTS: %s prompts - %s",
                len(current_prompt_versions),
                list(current_prompt_versions.keys()),
            )
            for name, version in current_prompt_versions.items():
                self.logger.debug("   - %s: v%s", version, name)
        else:
            self.logger.warning("⚠️  NO PROMPT VERSIONS provided - version checking disabled")

    def _fetch_last_investigation(self, repo_name: str, current_state: RepositoryState) -> Any:
        """
        Fetch the last investigation from storage.

        Returns:
            Either the InvestigationMetadata, or an InvestigationDecision if
            there's an error or no previous investigation found.
        """
        self.logger.info("🗃️  STORAGE: Looking up previous investigation for %s", repo_name)
        try:
            raw_data = self.storage_client.get_latest_investigation(repo_name)
            if raw_data:
                self.logger.info("✅ STORAGE: Found previous investigation")
                # Parse raw data into Pydantic model for validation
                try:
                    # Handle prompt_metadata conversion
                    if raw_data.get("prompt_metadata"):
                        prompt_meta_data = raw_data["prompt_metadata"]
                        raw_data["prompt_metadata"] = PromptMetadata(**prompt_meta_data)

                    last_investigation = InvestigationMetadata(**raw_data)
                    # Store both the parsed model and raw data for backward compatibility
                    last_investigation._raw_data = raw_data
                    return last_investigation
                except Exception as parse_error:
                    self.logger.warning(
                        "⚠️  Failed to parse investigation metadata: %s", parse_error
                    )
                    self.logger.warning("   Raw data: %s", raw_data)
                    # Continue with raw data for backward compatibility
                    return raw_data
            else:
                self.logger.info("❌ STORAGE: No previous investigation found")
                self.logger.info(
                    "🆕 DECISION: No previous investigation found for %s - NEEDS INVESTIGATION",
                    repo_name,
                )
                return InvestigationDecision(
                    needs_investigation=True,
                    reason="No previous investigation found",
                    latest_commit=current_state.commit_sha,
                    branch_name=current_state.branch_name,
                    last_investigation=None,
                )
        except Exception as e:
            self.logger.error(
                "💥 STORAGE ERROR: Failed to check storage for previous investigation: %s", e
            )
            return InvestigationDecision(
                needs_investigation=True,
                reason=f"Unable to check previous investigations (storage error: {e!s})",
                latest_commit=current_state.commit_sha,
                branch_name=current_state.branch_name,
                last_investigation=None,
            )

    def _extract_last_investigation_data(self, last_investigation: Any) -> dict[str, Any]:
        """Extract and log data from the last investigation."""
        # Handle both Pydantic model and raw dict for backward compatibility
        if isinstance(last_investigation, InvestigationMetadata):
            last_commit = last_investigation.latest_commit or ""
            last_branch = last_investigation.branch_name
            last_timestamp = last_investigation.analysis_timestamp
            last_prompt_metadata = last_investigation.prompt_metadata
        else:
            # Fallback to dict access for backward compatibility
            last_commit = last_investigation.get("latest_commit", "")
            last_branch = last_investigation.get("branch_name", "")
            last_timestamp = last_investigation.get("analysis_timestamp", 0)
            last_prompt_metadata = last_investigation.get("prompt_metadata", {})

        # Convert timestamp to datetime for logging
        last_investigation_date = datetime.fromtimestamp(last_timestamp, tz=UTC)

        self.logger.info("📜 LAST INVESTIGATION DETAILS:")
        self.logger.info("   Date: %s", last_investigation_date.isoformat())
        self.logger.info("   Branch: %s", last_branch)
        self.logger.info("   Commit: %s", last_commit[:8] if last_commit else "unknown")

        # Log prompt metadata from last investigation
        if last_prompt_metadata:
            if isinstance(last_prompt_metadata, PromptMetadata):
                last_prompt_versions = last_prompt_metadata.versions
                last_prompt_count = last_prompt_metadata.count
            else:
                # Fallback to dict access
                last_prompt_versions = last_prompt_metadata.get("versions", {})
                last_prompt_count = last_prompt_metadata.get("count", 0)

            self.logger.info("   Prompts: %s prompts in last investigation", last_prompt_count)
            for name, version in last_prompt_versions.items():
                self.logger.debug("      - %s: v%s", version, name)
        else:
            self.logger.warning("   No prompt metadata found in last investigation")

        return {
            "commit": last_commit,
            "branch": last_branch,
            "timestamp": last_timestamp,
            "date": last_investigation_date,
            "prompt_metadata": last_prompt_metadata,
        }

    def _check_commit_changes(
        self,
        current_state: RepositoryState,
        last_investigation_data: dict[str, Any],
        last_investigation: Any,
    ) -> InvestigationDecision | None:
        """Check if the commit has changed since the last investigation."""
        last_investigated_commit = last_investigation_data["commit"]

        self.logger.info("🔄 CHECKING: Commit changes...")
        self.logger.info("   Current: %s", current_state.commit_sha[:8])
        self.logger.info(
            "   Last:    %s",
            last_investigated_commit[:8] if last_investigated_commit else "unknown",
        )

        if current_state.commit_sha != last_investigated_commit:
            self.logger.info(
                "✅ DECISION: Repository has new commits since last investigation - NEEDS INVESTIGATION"
            )
            return InvestigationDecision(
                needs_investigation=True,
                reason=f"New commits detected (current: {current_state.commit_sha[:8]}, "
                f"last: {last_investigated_commit[:8] if last_investigated_commit else 'unknown'})",
                latest_commit=current_state.commit_sha,
                branch_name=current_state.branch_name,
                last_investigation=self._get_raw_investigation_data(last_investigation),
            )
        else:
            self.logger.info("✅ CHECK: Commit unchanged")
            return None

    def _check_branch_changes(
        self,
        current_state: RepositoryState,
        last_investigation_data: dict[str, Any],
        last_investigation: Any,
    ) -> InvestigationDecision | None:
        """Check if the branch has changed since the last investigation."""
        last_branch = last_investigation_data["branch"]

        self.logger.info("🔄 CHECKING: Branch changes...")
        self.logger.info("   Current: %s", current_state.branch_name)
        self.logger.info("   Last:    %s", last_branch)

        if current_state.branch_name != last_branch:
            self.logger.info(
                "✅ DECISION: Repository branch has changed since last investigation - NEEDS INVESTIGATION"
            )
            return InvestigationDecision(
                needs_investigation=True,
                reason=f"Branch changed (current: {current_state.branch_name}, last: {last_branch})",
                latest_commit=current_state.commit_sha,
                branch_name=current_state.branch_name,
                last_investigation=self._get_raw_investigation_data(last_investigation),
            )
        else:
            self.logger.info("✅ CHECK: Branch unchanged")
            return None

    def _check_prompt_version_changes(
        self,
        current_state: RepositoryState,
        current_prompt_versions: dict[str, str] | None,
        last_investigation: Any,
    ) -> InvestigationDecision | None:
        """Check if prompt versions have changed since the last investigation."""
        self.logger.info("🔄 CHECKING: Prompt versions...")

        if not current_prompt_versions:
            self.logger.warning(
                "⚠️  SKIPPING prompt version checks - no current prompt versions provided"
            )
            return None

        # Handle both Pydantic model and raw dict
        if isinstance(last_investigation, InvestigationMetadata):
            last_prompt_metadata = last_investigation.prompt_metadata
            if last_prompt_metadata:
                last_prompt_versions = last_prompt_metadata.versions
                last_prompt_count = last_prompt_metadata.count
            else:
                last_prompt_versions = {}
                last_prompt_count = 0
        else:
            # Fallback to dict access
            last_prompt_metadata = last_investigation.get("prompt_metadata", {})
            last_prompt_versions = (
                last_prompt_metadata.get("versions", {}) if last_prompt_metadata else {}
            )
            last_prompt_count = last_prompt_metadata.get("count", 0) if last_prompt_metadata else 0

        # Check if there's no prompt metadata from last investigation
        decision = self._check_missing_prompt_metadata(
            current_state, current_prompt_versions, last_prompt_metadata, last_investigation
        )
        if decision:
            return decision

            # Only check prompt count and versions if we have previous metadata to compare against
        has_previous_versions = False
        if isinstance(last_prompt_metadata, PromptMetadata):
            has_previous_versions = bool(last_prompt_metadata.versions)
        elif last_prompt_metadata:
            has_previous_versions = bool(last_prompt_metadata.get("versions", {}))

        if last_prompt_metadata and has_previous_versions:
            # Check prompt count changes
            decision = self._check_prompt_count_changes(
                current_state, current_prompt_versions, last_prompt_count, last_investigation
            )
            if decision:
                return decision

            # Check individual prompt version changes
            decision = self._check_individual_prompt_versions(
                current_state, current_prompt_versions, last_prompt_versions, last_investigation
            )
            if decision:
                return decision

            # Check for removed prompts
            decision = self._check_removed_prompts(
                current_state, current_prompt_versions, last_prompt_versions, last_investigation
            )
            if decision:
                return decision

        return None

    def _check_missing_prompt_metadata(
        self,
        current_state: RepositoryState,
        current_prompt_versions: dict[str, str],
        last_prompt_metadata: Any,
        last_investigation: Any,
    ) -> InvestigationDecision | None:
        """Check if prompts have been updated when no previous metadata exists."""
        # Handle both Pydantic model and raw dict
        has_versions = False
        if isinstance(last_prompt_metadata, PromptMetadata):
            has_versions = bool(last_prompt_metadata.versions)
        elif last_prompt_metadata:
            has_versions = bool(last_prompt_metadata.get("versions", {}))

        if not last_prompt_metadata or not has_versions:
            # Check if any current prompt has version > 1
            for prompt_name, current_version in current_prompt_versions.items():
                if current_version != "1":
                    self.logger.info(
                        "✅ DECISION: Prompt '%s' has version %s but no previous version tracking - NEEDS INVESTIGATION",
                        prompt_name,
                        current_version,
                    )
                    return InvestigationDecision(
                        needs_investigation=True,
                        reason=f"Prompt '{prompt_name}' updated to v{current_version} (no previous version tracking)",
                        latest_commit=current_state.commit_sha,
                        branch_name=current_state.branch_name,
                        last_investigation=self._get_raw_investigation_data(last_investigation),
                    )
            self.logger.info(
                "   No prompt metadata from last investigation, all current prompts are v1 - treating as unchanged"
            )
        return None

    def _check_prompt_count_changes(
        self,
        current_state: RepositoryState,
        current_prompt_versions: dict[str, str],
        last_prompt_count: int,
        last_investigation: Any,
    ) -> InvestigationDecision | None:
        """Check if the number of prompts has changed."""
        current_prompt_count = len(current_prompt_versions)
        self.logger.info(
            "   Prompt count - Current: %s, Last: %s", current_prompt_count, last_prompt_count
        )

        if current_prompt_count != last_prompt_count:
            self.logger.info(
                "✅ DECISION: Prompt count changed from %s to %s - NEEDS INVESTIGATION",
                last_prompt_count,
                current_prompt_count,
            )
            return InvestigationDecision(
                needs_investigation=True,
                reason=f"Prompt count changed ({last_prompt_count} → {current_prompt_count})",
                latest_commit=current_state.commit_sha,
                branch_name=current_state.branch_name,
                last_investigation=self._get_raw_investigation_data(last_investigation),
            )
        else:
            self.logger.info("✅ CHECK: Prompt count unchanged")
            return None

    def _check_individual_prompt_versions(
        self,
        current_state: RepositoryState,
        current_prompt_versions: dict[str, str],
        last_prompt_versions: dict[str, str],
        last_investigation: Any,
    ) -> InvestigationDecision | None:
        """Check if individual prompt versions have changed."""
        self.logger.info("   Checking individual prompt versions...")

        for prompt_name, current_version in current_prompt_versions.items():
            last_version = last_prompt_versions.get(prompt_name)
            # If no last version exists (prompt wasn't tracked before), assume default version "1"
            if last_version is None:
                last_version = "1"
                self.logger.debug(
                    "      %s: v%s (no previous version, assuming v1)", prompt_name, current_version
                )
            else:
                self.logger.debug(
                    "      %s: v%s (was v%s)", last_version, current_version, prompt_name
                )

            if last_version != current_version:
                self.logger.info(
                    "✅ DECISION: Prompt '%s' version changed from %s to %s - NEEDS INVESTIGATION",
                    prompt_name,
                    last_version,
                    current_version,
                )
                return InvestigationDecision(
                    needs_investigation=True,
                    reason=f"Prompt '{prompt_name}' version changed (v{last_version} → v{current_version})",
                    latest_commit=current_state.commit_sha,
                    branch_name=current_state.branch_name,
                    last_investigation=self._get_raw_investigation_data(last_investigation),
                )

        self.logger.info("✅ CHECK: All prompt versions unchanged")
        return None

    def _check_removed_prompts(
        self,
        current_state: RepositoryState,
        current_prompt_versions: dict[str, str],
        last_prompt_versions: dict[str, str],
        last_investigation: Any,
    ) -> InvestigationDecision | None:
        """Check if any prompts have been removed."""
        self.logger.info("   Checking for removed prompts...")

        for prompt_name in last_prompt_versions:
            if prompt_name not in current_prompt_versions:
                self.logger.info(
                    "✅ DECISION: Prompt '%s' was removed - NEEDS INVESTIGATION", prompt_name
                )
                return InvestigationDecision(
                    needs_investigation=True,
                    reason=f"Prompt '{prompt_name}' was removed",
                    latest_commit=current_state.commit_sha,
                    branch_name=current_state.branch_name,
                    last_investigation=self._get_raw_investigation_data(last_investigation),
                )

        self.logger.info("✅ CHECK: No prompts removed")
        return None

    def _create_no_investigation_decision(
        self,
        repo_name: str,
        current_state: RepositoryState,
        last_investigation_data: dict[str, Any],
        last_investigation: Any,
    ) -> InvestigationDecision:
        """Create a decision indicating no investigation is needed."""
        last_investigation_date = last_investigation_data["date"]

        self.logger.info(
            "🎯 FINAL DECISION: Repository %s hasn't changed since last investigation - SKIPPING INVESTIGATION",
            repo_name,
        )
        self.logger.info("📅 Last investigation date: %s", last_investigation_date.isoformat())

        return InvestigationDecision(
            needs_investigation=False,
            reason=f"No changes since last investigation on {last_investigation_date.isoformat()}",
            latest_commit=current_state.commit_sha,
            branch_name=current_state.branch_name,
            last_investigation=self._get_raw_investigation_data(last_investigation),
        )

    def save_investigation_metadata(
        self,
        repo_name: str,
        repo_url: str,
        commit_sha: str,
        branch_name: str,
        analysis_summary: dict[str, Any] | None = None,
        prompt_versions: dict[str, str] | None = None,
        ttl_days: int = 90,
    ) -> dict[str, Any]:
        """
        Save investigation metadata to storage for future caching checks.

        Args:
            repo_name: Name of the repository
            repo_url: URL of the repository
            commit_sha: SHA of the commit that was investigated
            branch_name: Name of the branch that was investigated
            analysis_summary: Optional summary of the analysis results
            prompt_versions: Optional dict of prompt names to versions
            ttl_days: Time-to-live in days for the metadata

        Returns:
            Dictionary with save status and details
        """
        self.logger.info(
            "💾 METADATA: Saving investigation metadata for %s (commit: %s, branch: %s)",
            repo_name,
            commit_sha[:8],
            branch_name,
        )

        if prompt_versions:
            self.logger.info("   Including prompt metadata: %s prompts", len(prompt_versions))
            for name, version in prompt_versions.items():
                self.logger.debug("      - %s: v%s", version, name)
        else:
            self.logger.warning("   No prompt versions provided for metadata")

        try:
            # Prepare analysis data with prompt metadata using Pydantic models
            analysis_data = analysis_summary or {}
            if prompt_versions:
                prompt_metadata = PromptMetadata(
                    count=len(prompt_versions), versions=prompt_versions
                )
                analysis_data["prompt_metadata"] = prompt_metadata.dict()
                self.logger.debug("   Prepared analysis_data with validated prompt_metadata")

            # Save the investigation metadata
            saved_item = self.storage_client.save_investigation_metadata(
                repository_name=repo_name,
                repository_url=repo_url,
                latest_commit=commit_sha,
                branch_name=branch_name,
                analysis_type="investigation",
                analysis_data=analysis_data,
                ttl_days=ttl_days,
            )

            self.logger.info(
                "✅ METADATA SAVED: Successfully saved investigation metadata for %s (commit: %s, branch: %s)",
                repo_name,
                commit_sha[:8],
                branch_name,
            )

            return {
                "status": "success",
                "message": f"Saved investigation metadata for {repo_name}",
                "timestamp": saved_item.get("analysis_timestamp"),
            }

        except Exception as e:
            self.logger.error("💥 METADATA ERROR: Failed to save investigation metadata: %s", e)
            return {
                "status": "error",
                "message": f"Failed to save investigation metadata: {e!s}",
                "timestamp": None,
            }

    def check_prompt_needs_analysis(
        self, repo_name: str, step_name: str, commit_sha: str, prompt_version: str = "1"
    ) -> dict[str, Any]:
        """
        Check if a specific prompt needs to be analyzed for a given commit and version.

        Args:
            repo_name: Name of the repository
            step_name: Name of the analysis step/prompt
            commit_sha: Current commit SHA
            prompt_version: Version of the prompt

        Returns:
            Dictionary with:
                - needs_analysis: Boolean indicating if analysis is needed
                - cached_result_key: Reference key to cached result if available
                - cached_result: The cached content if available
                - reason: Explanation of the decision
                - version: Version of the cached result
        """
        # Use KeyNameCreator to generate consistent key
        cache_key_obj = KeyNameCreator.create_prompt_cache_key(
            repo_name=repo_name,
            step_name=step_name,
            commit_sha=commit_sha,
            prompt_version=prompt_version,
        )
        prompt_cache_key = cache_key_obj.to_storage_key()

        self.logger.info(
            "🔍 PROMPT CACHE: Checking cache for %s/%s at commit %s v%s",
            repo_name,
            step_name,
            commit_sha[:8],
            prompt_version,
        )
        self.logger.debug("   Cache key: %s", prompt_cache_key)

        try:
            # Try to get cached result for this exact prompt+commit+version combination
            cached_result = self.storage_client.get_analysis_result(prompt_cache_key)

            if cached_result:
                self.logger.info(
                    "✅ PROMPT CACHE HIT: Found cached result for %s/%s at commit %s v%s",
                    repo_name,
                    step_name,
                    commit_sha[:8],
                    prompt_version,
                )
                self.logger.debug(
                    "   Cached content length: %s characters",
                    len(cached_result) if cached_result else 0,
                )
                return {
                    "needs_analysis": False,
                    "cached_result_key": prompt_cache_key,
                    "cached_result": cached_result,
                    "reason": f"Using cached result from commit {commit_sha[:8]} v{prompt_version}",
                    "version": prompt_version,
                }
            else:
                self.logger.info(
                    "❌ PROMPT CACHE MISS: No cached result found for %s/%s at commit %s v%s",
                    repo_name,
                    step_name,
                    commit_sha[:8],
                    prompt_version,
                )
                return {
                    "needs_analysis": True,
                    "cached_result_key": None,
                    "cached_result": None,
                    "reason": f"No cached result for this prompt at commit {commit_sha[:8]} v{prompt_version}",
                    "version": prompt_version,
                }

        except Exception as e:
            self.logger.error(
                "💥 PROMPT CACHE ERROR: Error checking prompt cache for %s/%s: %s",
                repo_name,
                step_name,
                e,
            )
            # On error, safer to re-run the analysis
            return {
                "needs_analysis": True,
                "cached_result_key": None,
                "cached_result": None,
                "reason": f"Cache check failed: {e!s}",
            }

    def save_prompt_result(
        self,
        repo_name: str,
        step_name: str,
        commit_sha: str,
        result_content: str,
        prompt_version: str = "1",
        ttl_days: int = 90,
    ) -> dict[str, Any]:
        """
        Save the result of a prompt analysis for future cache hits.

        Args:
            repo_name: Name of the repository
            step_name: Name of the analysis step/prompt
            commit_sha: Commit SHA this result is for
            result_content: The analysis result content
            prompt_version: Version of the prompt
            ttl_days: Time-to-live in days for the cached result

        Returns:
            Dictionary with save status
        """
        # Use KeyNameCreator to generate consistent key
        cache_key_obj = KeyNameCreator.create_prompt_cache_key(
            repo_name=repo_name,
            step_name=step_name,
            commit_sha=commit_sha,
            prompt_version=prompt_version,
        )
        prompt_cache_key = cache_key_obj.to_storage_key()

        self.logger.info(
            "💾 PROMPT CACHE: Saving result for %s/%s at commit %s v%s",
            repo_name,
            step_name,
            commit_sha[:8],
            prompt_version,
        )
        self.logger.debug("   Cache key: %s", prompt_cache_key)
        self.logger.debug("   Content length: %s characters", len(result_content))

        try:
            # Convert TTL from days to minutes for the storage layer
            ttl_minutes = ttl_days * 24 * 60

            # Save the result using the existing analysis result storage
            saved_item = self.storage_client.save_analysis_result(
                reference_key=prompt_cache_key,
                result_content=result_content,
                step_name=step_name,
                ttl_minutes=ttl_minutes,
            )

            self.logger.info(
                "✅ PROMPT CACHE SAVED: Successfully cached prompt result for %s/%s at commit %s v%s",
                repo_name,
                step_name,
                commit_sha[:8],
                prompt_version,
            )

            return {
                "status": "success",
                "message": f"Cached result for {step_name}",
                "cache_key": prompt_cache_key,
                "timestamp": saved_item.get("timestamp"),
            }

        except Exception as e:
            self.logger.error(
                "💥 PROMPT CACHE ERROR: Failed to cache prompt result for %s/%s: %s",
                repo_name,
                step_name,
                e,
            )
            # Don't fail the workflow for cache save failures
            return {
                "status": "error",
                "message": f"Failed to cache result: {e!s}",
                "cache_key": None,
                "timestamp": None,
            }

    def save_dependencies(
        self, repo_name: str, dependencies_data: dict, reference_key: str, ttl_days: int = 90
    ) -> dict[str, Any]:
        """
        Save dependencies data to storage.

        Args:
            repo_name: Repository name
            dependencies_data: Dependencies data to save
            reference_key: Storage key for the dependencies
            ttl_days: TTL in days

        Returns:
            Dictionary with save status and reference key
        """
        try:
            # Convert TTL to minutes
            ttl_minutes = ttl_days * 24 * 60

            self.logger.info("💾 DEPENDENCIES: Caching dependencies for %s", repo_name)
            self.logger.debug("   Reference key: %s", reference_key)
            self.logger.debug("   TTL: %s days (%s minutes)", ttl_minutes, ttl_days)

            # Save using the storage client's abstracted method
            saved_item = self.storage_client.save_temporary_analysis_data(
                reference_key=reference_key, data_content=dependencies_data, ttl_minutes=ttl_minutes
            )

            self.logger.info(
                "✅ DEPENDENCIES CACHED: Successfully cached dependencies for %s", repo_name
            )

            return {
                "status": "success",
                "reference_key": reference_key,
                "timestamp": saved_item.get("timestamp"),
            }
        except Exception as e:
            self.logger.error(
                "💥 DEPENDENCIES ERROR: Failed to cache dependencies for %s: %s", repo_name, e
            )
            return {"status": "error", "reference_key": None, "error": str(e)}

    def get_dependencies(self, reference_key: str) -> dict[str, Any] | None:
        """
        Retrieve dependencies data from storage.

        Args:
            reference_key: Storage key for the dependencies

        Returns:
            Dependencies data or None if not found
        """
        try:
            self.logger.info("🔍 DEPENDENCIES: Retrieving dependencies with key: %s", reference_key)
            data = self.storage_client.get_temporary_analysis_data(reference_key)

            if data:
                self.logger.info("✅ DEPENDENCIES FOUND: Successfully retrieved dependencies")
                # Cast to proper type - get_temporary_analysis_data returns Any but should be dict
                return data if isinstance(data, dict) else None
            else:
                self.logger.warning(
                    "❌ DEPENDENCIES NOT FOUND: No dependencies found for key: %s", reference_key
                )
                return None

        except Exception as e:
            self.logger.error("💥 DEPENDENCIES ERROR: Failed to retrieve dependencies: %s", e)
            return None
