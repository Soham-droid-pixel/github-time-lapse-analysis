"""
Configuration management for GitHub Time-Lapse Analyzer.

Uses pydantic-settings for environment variable validation and type safety.
"""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # GitHub Configuration
    github_token: str = Field(..., description="GitHub Personal Access Token")
    github_username: str = Field(..., description="GitHub username to analyze")
    
    # Cache Settings
    cache_enabled: bool = Field(default=True, description="Enable local caching")
    cache_days: int = Field(default=7, description="Days to keep cache valid")
    
    # Analysis Limits
    max_repositories: int = Field(default=100, description="Maximum repositories to analyze")
    commits_per_repo: int = Field(default=1000, description="Maximum commits per repository")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator("github_token")
    @classmethod
    def validate_token(cls, v: str) -> str:
        """Validate GitHub token format."""
        if not v or v == "ghp_your_token_here":
            raise ValueError(
                "Invalid GitHub token. Please set GITHUB_TOKEN in .env file. "
                "Generate a token at: https://github.com/settings/tokens"
            )
        return v
    
    @field_validator("github_username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Validate GitHub username."""
        if not v or v == "your_username_here":
            raise ValueError("Please set GITHUB_USERNAME in .env file")
        return v
    
    @field_validator("cache_days")
    @classmethod
    def validate_cache_days(cls, v: int) -> int:
        """Ensure cache days is positive."""
        if v < 1:
            raise ValueError("cache_days must be at least 1")
        return v


# Project Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"
CACHE_FILE = DATA_DIR / "commits_cache.json"
CACHE_METADATA_FILE = DATA_DIR / "cache_metadata.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)


# Color Palette for Visualizations
COLORS = {
    "primary": "#6366f1",      # Indigo
    "secondary": "#8b5cf6",    # Purple
    "accent": "#ec4899",       # Pink
    "success": "#10b981",      # Green
    "warning": "#f59e0b",      # Amber
    "danger": "#ef4444",       # Red
    "info": "#3b82f6",         # Blue
    "background": "#0f172a",   # Dark slate
    "surface": "#1e293b",      # Slate
    "text": "#f1f5f9",         # Light slate
    "muted": "#64748b",        # Gray
}

# Chart Theme Configuration
CHART_THEME = {
    "template": "plotly_dark",
    "font_family": "Inter, system-ui, -apple-system, sans-serif",
    "font_color": COLORS["text"],
    "paper_bgcolor": COLORS["background"],
    "plot_bgcolor": COLORS["surface"],
    "colorscale": "Viridis",
}

# GitHub API Configuration
GITHUB_API_BASE = "https://api.github.com"
RATE_LIMIT_BUFFER = 100  # Minimum remaining requests before stopping
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2  # seconds


# NLP Configuration
NLTK_DATA_PATH = BASE_DIR / "nltk_data"
NLTK_PACKAGES = ["punkt", "stopwords", "wordnet", "averaged_perceptron_tagger", "vader_lexicon"]

# Stopwords to remove from commit message analysis
CUSTOM_STOPWORDS = {
    "add", "added", "update", "updated", "fix", "fixed", "remove", "removed",
    "change", "changed", "modify", "modified", "delete", "deleted",
    "merge", "merging", "commit", "committed", "push", "pushed",
}


def get_settings() -> Settings:
    """
    Load and validate application settings.
    
    Returns:
        Settings: Validated settings object
        
    Raises:
        ValueError: If required environment variables are missing or invalid
    """
    return Settings()


def get_output_path(filename: str) -> Path:
    """
    Get full path for an output file.
    
    Args:
        filename: Name of the output file
        
    Returns:
        Path: Full path to the output file
    """
    return OUTPUT_DIR / filename


def get_cache_path() -> Path:
    """
    Get path to the cache file.
    
    Returns:
        Path: Full path to the cache file
    """
    return CACHE_FILE


# Load settings on import (will validate environment)
try:
    settings = get_settings()
except Exception as e:
    print(f"⚠️  Configuration Error: {e}")
    print("Please check your .env file and ensure all required variables are set.")
    print("See .env.example for reference.")
    raise
