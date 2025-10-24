"""Unit tests for utility functions."""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import json

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    format_number,
    get_file_extension,
    map_extension_to_language,
    calculate_streak,
    truncate_text,
    get_time_period_label,
    save_json,
    load_json,
)


class TestFormatNumber:
    """Tests for format_number function."""
    
    def test_small_numbers(self):
        assert format_number(5) == "5"
        assert format_number(99) == "99"
        assert format_number(500) == "500"
    
    def test_thousands(self):
        assert format_number(1000) == "1.0K"
        assert format_number(5500) == "5.5K"
        assert format_number(12300) == "12.3K"
    
    def test_millions(self):
        assert format_number(1000000) == "1.0M"
        assert format_number(2500000) == "2.5M"


class TestFileExtension:
    """Tests for file extension functions."""
    
    def test_get_file_extension(self):
        assert get_file_extension("main.py") == "py"
        assert get_file_extension("index.html") == "html"
        assert get_file_extension("README") == "no_extension"
        assert get_file_extension("app.test.js") == "js"
    
    def test_map_extension_to_language(self):
        assert map_extension_to_language("py") == "Python"
        assert map_extension_to_language("js") == "JavaScript"
        assert map_extension_to_language("ts") == "TypeScript"
        assert map_extension_to_language("unknown") == "Other"


class TestCalculateStreak:
    """Tests for streak calculation."""
    
    def test_consecutive_dates(self):
        dates = pd.Series([
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
            datetime(2024, 1, 3),
            datetime(2024, 1, 4),
        ])
        assert calculate_streak(dates) == 4
    
    def test_non_consecutive_dates(self):
        dates = pd.Series([
            datetime(2024, 1, 1),
            datetime(2024, 1, 2),
            datetime(2024, 1, 5),
            datetime(2024, 1, 6),
        ])
        assert calculate_streak(dates) == 2
    
    def test_empty_series(self):
        dates = pd.Series([], dtype='datetime64[ns]')
        assert calculate_streak(dates) == 0


class TestTruncateText:
    """Tests for text truncation."""
    
    def test_short_text(self):
        text = "Short text"
        assert truncate_text(text, 50) == "Short text"
    
    def test_long_text(self):
        text = "This is a very long text that needs to be truncated"
        result = truncate_text(text, 20)
        assert len(result) == 20
        assert result.endswith("...")


class TestTimePeriodLabel:
    """Tests for time period labeling."""
    
    def test_late_night(self):
        assert get_time_period_label(2) == "Late Night"
        assert get_time_period_label(5) == "Late Night"
    
    def test_morning(self):
        assert get_time_period_label(8) == "Morning"
        assert get_time_period_label(11) == "Morning"
    
    def test_afternoon(self):
        assert get_time_period_label(13) == "Afternoon"
        assert get_time_period_label(16) == "Afternoon"
    
    def test_evening(self):
        assert get_time_period_label(18) == "Evening"
        assert get_time_period_label(20) == "Evening"
    
    def test_night(self):
        assert get_time_period_label(22) == "Night"
        assert get_time_period_label(23) == "Night"


class TestJSONOperations:
    """Tests for JSON save/load operations."""
    
    def test_save_and_load_json(self):
        data = {"test": "value", "number": 42, "list": [1, 2, 3]}
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_path = Path(f.name)
        
        try:
            save_json(data, temp_path)
            loaded_data = load_json(temp_path)
            assert loaded_data == data
        finally:
            if temp_path.exists():
                temp_path.unlink()
    
    def test_load_nonexistent_file(self):
        result = load_json(Path("nonexistent_file.json"))
        assert result is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
