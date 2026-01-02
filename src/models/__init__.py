"""
Pydantic models for the investigation system.

This package contains all data models used throughout the application
for type safety, validation, and documentation.
"""

# Core investigation models
# Activity models
from .activities import (
    AnalyzeStructureInput,
    AnalyzeStructureOutput,
    AnalyzeWithClaudeInput,
    AnalyzeWithClaudeOutput,
    CacheCheckInput,
    CacheCheckOutput,
    ClaudeConfigOverrides,
    PromptContextDict,
    SaveMetadataInput,
    SaveMetadataOutput,
)

# Cache models
from .cache import (
    AnalysisResult,
    CacheCheckResult,
    PromptCacheResult,
)
from .investigation import (
    InvestigationDecision,
    InvestigationMetadata,
    PromptMetadata,
    RepositoryState,
)

# Workflow models
from .workflows import (
    AnalysisStepResult,
    AnalysisSummary,
    CloneRepositoryResult,
    # New workflow models
    ConfigOverrides,
    InvestigateReposRequest,
    InvestigateReposResult,
    InvestigateSingleRepoRequest,
    InvestigateSingleRepoResult,
    InvestigationResult,
    ProcessAnalysisResult,
    PromptsConfigResult,
    RepositoryAnalysis,
    SaveToDynamoResult,
    SaveToHubResult,
    WorkflowParams,
    WorkflowResult,
    WriteResultsOutput,
)

__all__ = [
    # Cache
    "AnalysisResult",
    "AnalysisStepResult",
    "AnalysisSummary",
    "AnalyzeStructureInput",
    "AnalyzeStructureOutput",
    "AnalyzeWithClaudeInput",
    "AnalyzeWithClaudeOutput",
    # Activities
    "CacheCheckInput",
    "CacheCheckOutput",
    "CacheCheckResult",
    "ClaudeConfigOverrides",
    "CloneRepositoryResult",
    # Workflows (new)
    "ConfigOverrides",
    "InvestigateReposRequest",
    "InvestigateReposResult",
    "InvestigateSingleRepoRequest",
    "InvestigateSingleRepoResult",
    "InvestigationDecision",
    "InvestigationMetadata",
    "InvestigationResult",
    "ProcessAnalysisResult",
    "PromptCacheResult",
    "PromptContextDict",
    # Investigation
    "PromptMetadata",
    "PromptsConfigResult",
    "RepositoryAnalysis",
    "RepositoryState",
    "SaveMetadataInput",
    "SaveMetadataOutput",
    "SaveToDynamoResult",
    "SaveToHubResult",
    # Workflows (legacy)
    "WorkflowParams",
    "WorkflowResult",
    "WriteResultsOutput",
]
