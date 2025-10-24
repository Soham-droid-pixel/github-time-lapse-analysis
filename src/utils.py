"""Utility functions for GitHub Time-Lapse Analyzer."""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging for the application.
    
    Args:
        level: Logging level (default: INFO)
        
    Returns:
        Logger: Configured logger instance
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("github_analyzer")
    return logger


def save_json(data: Dict[str, Any], filepath: Path) -> None:
    """
    Save data to JSON file.
    
    Args:
        data: Dictionary to save
        filepath: Path to save the JSON file
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


def load_json(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Load data from JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        Dictionary loaded from JSON, or None if file doesn't exist
    """
    if not filepath.exists():
        return None
    
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def is_cache_valid(cache_metadata_path: Path, max_age_days: int = 7) -> bool:
    """
    Check if cached data is still valid.
    
    Args:
        cache_metadata_path: Path to cache metadata file
        max_age_days: Maximum age of cache in days
        
    Returns:
        True if cache is valid, False otherwise
    """
    if not cache_metadata_path.exists():
        return False
    
    metadata = load_json(cache_metadata_path)
    if not metadata or "timestamp" not in metadata:
        return False
    
    cache_time = datetime.fromisoformat(metadata["timestamp"])
    age = datetime.now() - cache_time
    
    return age < timedelta(days=max_age_days)


def format_number(num: int) -> str:
    """
    Format large numbers with K, M suffixes.
    
    Args:
        num: Number to format
        
    Returns:
        Formatted string (e.g., "1.2K", "3.5M")
    """
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)


def get_file_extension(filename: str) -> str:
    """
    Extract file extension from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        File extension without the dot
    """
    if "." not in filename:
        return "no_extension"
    return filename.split(".")[-1].lower()


def map_extension_to_language(extension: str) -> str:
    """
    Map file extension to programming language name.
    
    Args:
        extension: File extension
        
    Returns:
        Language name
    """
    language_map = {
        "py": "Python",
        "js": "JavaScript",
        "ts": "TypeScript",
        "jsx": "React/JSX",
        "tsx": "React/TSX",
        "java": "Java",
        "cpp": "C++",
        "cc": "C++",
        "cxx": "C++",
        "h": "C/C++ Header",
        "hpp": "C++ Header",
        "c": "C",
        "cs": "C#",
        "go": "Go",
        "rs": "Rust",
        "php": "PHP",
        "rb": "Ruby",
        "swift": "Swift",
        "kt": "Kotlin",
        "scala": "Scala",
        "r": "R",
        "m": "MATLAB",
        "sql": "SQL",
        "html": "HTML",
        "css": "CSS",
        "scss": "SCSS",
        "sass": "Sass",
        "vue": "Vue",
        "md": "Markdown",
        "json": "Config/JSON",
        "xml": "Config/XML",
        "yaml": "Config/YAML",
        "yml": "Config/YAML",
        "toml": "Config/TOML",
        "ini": "Config/INI",
        "sh": "Shell",
        "bash": "Bash",
        "ps1": "PowerShell",
        "ipynb": "Jupyter",
        "txt": "Text",
        "lock": "Lock File",
        "gitignore": "Git",
        "dockerignore": "Docker",
        "env": "Environment",
        # Binary and compiled files - exclude from language stats
        "exe": None,
        "dll": None,
        "so": None,
        "dylib": None,
        "pyc": None,
        "pyo": None,
        "pyd": None,
        "class": None,
        "o": None,
        "a": None,
        # Media files - exclude
        "png": None,
        "jpg": None,
        "jpeg": None,
        "gif": None,
        "svg": None,
        "ico": None,
        "mp4": None,
        "mp3": None,
        "wav": None,
        "pdf": None,
        "zip": None,
        "tar": None,
        "gz": None,
        "no_extension": "Other",
    }
    
    result = language_map.get(extension, "Other")
    # Return None for binary/media files to exclude them from stats
    return result if result is not None else None


def extract_hour_from_datetime(dt: datetime) -> int:
    """
    Extract hour (0-23) from datetime.
    
    Args:
        dt: Datetime object
        
    Returns:
        Hour as integer
    """
    return dt.hour


def extract_day_of_week(dt: datetime) -> str:
    """
    Extract day of week name from datetime.
    
    Args:
        dt: Datetime object
        
    Returns:
        Day name (e.g., "Monday")
    """
    return dt.strftime("%A")


def calculate_streak(dates: pd.Series) -> int:
    """
    Calculate longest consecutive day streak.
    
    Args:
        dates: Series of datetime objects
        
    Returns:
        Length of longest streak in days
    """
    if dates.empty:
        return 0
    
    # Convert to date only and sort
    unique_dates = pd.to_datetime(dates.dt.date).sort_values().unique()
    
    if len(unique_dates) == 0:
        return 0
    
    max_streak = 1
    current_streak = 1
    
    for i in range(1, len(unique_dates)):
        diff = (unique_dates[i] - unique_dates[i-1]).days
        
        if diff == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    
    return max_streak


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def get_time_period_label(hour: int) -> str:
    """
    Get human-readable time period label.
    
    Args:
        hour: Hour (0-23)
        
    Returns:
        Period label (e.g., "Late Night", "Morning")
    """
    if 0 <= hour < 6:
        return "Late Night"
    elif 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"
