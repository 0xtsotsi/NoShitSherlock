"""
Core components for the Claude Investigator.
"""

from .config import Config
from .file_manager import FileManager
from .git_manager import GitRepositoryManager
from .repository_analyzer import RepositoryAnalyzer
from .repository_type_detector import RepositoryTypeDetector
from .utils import Utils

# NOTE: ClaudeAnalyzer is intentionally excluded from __init__.py to avoid
# importing anthropic in workflow contexts (Temporal sandbox restriction)

__all__ = [
    "Config",
    "FileManager",
    "GitRepositoryManager",
    "RepositoryAnalyzer",
    "RepositoryTypeDetector",
    "Utils",
]
