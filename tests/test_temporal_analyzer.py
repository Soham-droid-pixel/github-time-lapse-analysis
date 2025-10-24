"""Unit tests for temporal analyzer."""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzers.temporal import TemporalAnalyzer, analyze_temporal_patterns


@pytest.fixture
def sample_commit_data():
    """Create sample commit DataFrame for testing."""
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    
    data = []
    for date in dates:
        # Add commits at different hours
        for hour in [9, 14, 20]:
            data.append({
                'timestamp': date.replace(hour=hour),
                'message': f'Commit at {hour}:00',
                'repo_name': 'test-repo',
            })
    
    df = pd.DataFrame(data)
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['day_of_week_num'] = df['timestamp'].dt.dayofweek
    df['date'] = df['timestamp'].dt.date
    df['month'] = df['timestamp'].dt.to_period('M')
    
    return df


class TestTemporalAnalyzer:
    """Tests for TemporalAnalyzer class."""
    
    def test_initialization_with_valid_data(self, sample_commit_data):
        analyzer = TemporalAnalyzer(sample_commit_data)
        assert analyzer.df is not None
        assert len(analyzer.df) > 0
    
    def test_initialization_with_empty_data(self):
        df = pd.DataFrame()
        analyzer = TemporalAnalyzer(df)
        assert analyzer.df.empty
    
    def test_hour_distribution(self, sample_commit_data):
        analyzer = TemporalAnalyzer(sample_commit_data)
        result = analyzer.analyze_hour_distribution()
        
        assert 'hourly_counts' in result
        assert 'peak_hours' in result
        assert len(result['peak_hours']) <= 3
        assert 'most_active_hour' in result
    
    def test_day_of_week_analysis(self, sample_commit_data):
        analyzer = TemporalAnalyzer(sample_commit_data)
        result = analyzer.analyze_day_of_week()
        
        assert 'daily_counts' in result
        assert 'weekday_percentage' in result
        assert 'weekend_percentage' in result
        assert result['weekday_percentage'] + result['weekend_percentage'] == 100
    
    def test_personality_classification(self, sample_commit_data):
        analyzer = TemporalAnalyzer(sample_commit_data)
        result = analyzer.classify_coding_personality()
        
        assert 'personality_type' in result
        assert 'description' in result
        assert 'time_distribution' in result
    
    def test_streak_calculation(self, sample_commit_data):
        analyzer = TemporalAnalyzer(sample_commit_data)
        result = analyzer.calculate_streaks()
        
        assert 'longest_streak' in result
        assert 'current_streak' in result
        assert 'consistency_score' in result
        assert result['longest_streak'] > 0
    
    def test_full_analysis(self, sample_commit_data):
        analyzer = TemporalAnalyzer(sample_commit_data)
        result = analyzer.get_full_analysis()
        
        assert 'hour_distribution' in result
        assert 'day_of_week' in result
        assert 'personality' in result
        assert 'streaks' in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
