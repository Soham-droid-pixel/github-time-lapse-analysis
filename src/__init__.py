"""GitHub Time-Lapse Analyzer - Analyze your GitHub commit history."""

__version__ = "1.0.0"
__author__ = "Your Name"

from .config import settings
from .data_fetcher import fetch_github_data

__all__ = ["settings", "fetch_github_data"]
