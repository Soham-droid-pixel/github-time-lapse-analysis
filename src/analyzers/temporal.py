"""
Temporal analysis of commit patterns.

Analyzes time-based patterns in commit history including circadian rhythms,
day-of-week preferences, and activity streaks.
"""

from typing import Dict, Any, List, Tuple
import pandas as pd
import numpy as np

from ..utils import calculate_streak, get_time_period_label, setup_logging

logger = setup_logging()


class TemporalAnalyzer:
    """Analyzes temporal patterns in commit history."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize temporal analyzer.
        
        Args:
            df: DataFrame with commit data (must have 'timestamp' column)
        """
        self.df = df
        
        if df.empty:
            logger.warning("Empty DataFrame provided to TemporalAnalyzer")
        elif "timestamp" not in df.columns:
            raise ValueError("DataFrame must have 'timestamp' column")
    
    def analyze_hour_distribution(self) -> Dict[str, Any]:
        """
        Analyze commit distribution across hours of the day.
        
        Returns:
            Dictionary with hourly statistics
        """
        if self.df.empty:
            return {}
        
        hour_counts = self.df["hour"].value_counts().sort_index()
        
        # Fill missing hours with 0
        full_hours = pd.Series(0, index=range(24))
        full_hours.update(hour_counts)
        
        # Calculate percentages
        total_commits = len(self.df)
        hour_percentages = (full_hours / total_commits * 100).to_dict()
        
        # Find peak hours
        top_3_hours = full_hours.nlargest(3)
        
        return {
            "hourly_counts": full_hours.to_dict(),
            "hourly_percentages": hour_percentages,
            "peak_hours": [
                {
                    "hour": int(hour),
                    "count": int(count),
                    "percentage": float(count / total_commits * 100),
                }
                for hour, count in top_3_hours.items()
            ],
            "most_active_hour": int(full_hours.idxmax()),
            "least_active_hour": int(full_hours.idxmin()),
        }
    
    def analyze_day_of_week(self) -> Dict[str, Any]:
        """
        Analyze commit distribution across days of the week.
        
        Returns:
            Dictionary with day-of-week statistics
        """
        if self.df.empty:
            return {}
        
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_counts = self.df["day_of_week"].value_counts()
        
        # Reorder by day of week
        ordered_counts = pd.Series(
            [day_counts.get(day, 0) for day in day_order],
            index=day_order
        )
        
        total_commits = len(self.df)
        day_percentages = (ordered_counts / total_commits * 100).to_dict()
        
        # Classify weekday vs weekend
        weekday_commits = self.df[self.df["day_of_week_num"] < 5]
        weekend_commits = self.df[self.df["day_of_week_num"] >= 5]
        
        return {
            "daily_counts": ordered_counts.to_dict(),
            "daily_percentages": day_percentages,
            "most_active_day": ordered_counts.idxmax(),
            "least_active_day": ordered_counts.idxmin(),
            "weekday_percentage": len(weekday_commits) / total_commits * 100,
            "weekend_percentage": len(weekend_commits) / total_commits * 100,
        }
    
    def classify_coding_personality(self) -> Dict[str, Any]:
        """
        Classify user as "Night Owl" vs "Early Bird" and other personality traits.
        
        Returns:
            Dictionary with personality classification
        """
        if self.df.empty:
            return {}
        
        total_commits = len(self.df)
        
        # Time period classifications
        late_night_commits = len(self.df[(self.df["hour"] >= 0) & (self.df["hour"] < 6)])
        morning_commits = len(self.df[(self.df["hour"] >= 6) & (self.df["hour"] < 12)])
        afternoon_commits = len(self.df[(self.df["hour"] >= 12) & (self.df["hour"] < 17)])
        evening_commits = len(self.df[(self.df["hour"] >= 17) & (self.df["hour"] < 21)])
        night_commits = len(self.df[(self.df["hour"] >= 21) & (self.df["hour"] < 24)])
        
        # Percentages
        late_night_pct = late_night_commits / total_commits * 100
        night_pct = (night_commits + late_night_commits) / total_commits * 100
        morning_pct = morning_commits / total_commits * 100
        
        # Primary classification
        if night_pct > 30:
            personality = "Night Owl 🦉"
            description = "You thrive in the quiet hours after sunset, crafting code when the world sleeps."
        elif morning_pct > 35:
            personality = "Early Bird 🐦"
            description = "You harness the morning's energy, coding with the sunrise."
        elif afternoon_commits / total_commits > 40:
            personality = "Afternoon Achiever ☀️"
            description = "Peak productivity hits in the afternoon hours."
        else:
            personality = "Balanced Coder ⚖️"
            description = "You code consistently throughout the day, adapting to the rhythm of life."
        
        return {
            "personality_type": personality,
            "description": description,
            "time_distribution": {
                "late_night": {"percentage": late_night_pct, "count": late_night_commits},
                "morning": {"percentage": morning_pct, "count": morning_commits},
                "afternoon": {"percentage": afternoon_commits / total_commits * 100, "count": afternoon_commits},
                "evening": {"percentage": evening_commits / total_commits * 100, "count": evening_commits},
                "night": {"percentage": (night_commits / total_commits * 100), "count": night_commits},
            },
        }
    
    def calculate_streaks(self) -> Dict[str, Any]:
        """
        Calculate commit streaks and consistency metrics.
        
        Returns:
            Dictionary with streak statistics
        """
        if self.df.empty:
            return {}
        
        # Calculate longest streak
        longest_streak = calculate_streak(self.df["timestamp"])
        
        # Current streak (from most recent commit to today)
        most_recent = self.df["timestamp"].max()
        # Handle timezone-aware timestamps
        now = pd.Timestamp.now(tz=most_recent.tz) if most_recent.tz else pd.Timestamp.now()
        days_since_last = (now - most_recent).days
        
        # Get unique commit dates
        commit_dates = pd.to_datetime(self.df["timestamp"].dt.date).sort_values()
        unique_dates = commit_dates.unique()
        
        # Calculate current streak
        current_streak = 0
        if days_since_last <= 1:  # Active within last day
            current_streak = 1
            check_date = (now.normalize() if hasattr(now, 'normalize') else now.floor('D')) - pd.Timedelta(days=1)
            
            for i in range(len(unique_dates) - 1, -1, -1):
                if pd.Timestamp(unique_dates[i]) >= check_date:
                    current_streak += 1
                    check_date -= pd.Timedelta(days=1)
                else:
                    break
        
        # Calculate active days
        total_days = (self.df["timestamp"].max() - self.df["timestamp"].min()).days + 1
        active_days = len(unique_dates)
        consistency_score = (active_days / total_days * 100) if total_days > 0 else 0
        
        return {
            "longest_streak": longest_streak,
            "current_streak": current_streak,
            "total_active_days": active_days,
            "total_days_span": total_days,
            "consistency_score": consistency_score,
            "average_commits_per_active_day": len(self.df) / active_days if active_days > 0 else 0,
        }
    
    def analyze_monthly_trends(self) -> Dict[str, Any]:
        """
        Analyze commit trends over months.
        
        Returns:
            Dictionary with monthly statistics
        """
        if self.df.empty:
            return {}
        
        monthly_counts = self.df.groupby("month").size()
        
        return {
            "monthly_counts": {str(k): int(v) for k, v in monthly_counts.items()},
            "most_productive_month": str(monthly_counts.idxmax()),
            "least_productive_month": str(monthly_counts.idxmin()),
            "average_commits_per_month": float(monthly_counts.mean()),
            "total_months": len(monthly_counts),
        }
    
    def get_full_analysis(self) -> Dict[str, Any]:
        """
        Run all temporal analyses and return combined results.
        
        Returns:
            Dictionary with all temporal analysis results
        """
        logger.info("Running temporal analysis...")
        
        return {
            "hour_distribution": self.analyze_hour_distribution(),
            "day_of_week": self.analyze_day_of_week(),
            "personality": self.classify_coding_personality(),
            "streaks": self.calculate_streaks(),
            "monthly_trends": self.analyze_monthly_trends(),
        }


def analyze_temporal_patterns(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convenience function to run all temporal analyses.
    
    Args:
        df: DataFrame with commit data
        
    Returns:
        Dictionary with all temporal analysis results
    """
    analyzer = TemporalAnalyzer(df)
    return analyzer.get_full_analysis()
