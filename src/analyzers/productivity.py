"""
Productivity metrics analysis.

Calculates productivity metrics including consistency scores, hot streaks,
project devotion index, and velocity metrics.
"""

from typing import Dict, Any, List
from datetime import timedelta
import pandas as pd
import numpy as np

from ..utils import calculate_streak, format_number, setup_logging

logger = setup_logging()


class ProductivityAnalyzer:
    """Analyzes productivity patterns and metrics."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize productivity analyzer.
        
        Args:
            df: DataFrame with commit data
        """
        self.df = df
        
        if df.empty:
            logger.warning("Empty DataFrame provided to ProductivityAnalyzer")
    
    def calculate_consistency_score(self) -> Dict[str, Any]:
        """
        Calculate coding consistency score (0-100).
        
        Returns:
            Dictionary with consistency metrics
        """
        if self.df.empty:
            return {}
        
        # Get date range
        date_range = (self.df["timestamp"].max() - self.df["timestamp"].min()).days + 1
        unique_commit_days = self.df["date"].nunique()
        
        # Basic consistency: percentage of days with commits
        basic_consistency = (unique_commit_days / date_range * 100) if date_range > 0 else 0
        
        # Calculate standard deviation of daily commits
        daily_commits = self.df.groupby("date").size()
        
        # Fill missing dates with 0
        all_dates = pd.date_range(
            start=self.df["timestamp"].min().date(),
            end=self.df["timestamp"].max().date(),
            freq="D"
        )
        daily_commits_full = pd.Series(0, index=all_dates)
        daily_commits_full.update(daily_commits)
        
        # Lower standard deviation = more consistent
        commit_std = daily_commits_full.std()
        commit_mean = daily_commits_full.mean()
        
        # Coefficient of variation (inverted and normalized)
        cv = commit_std / commit_mean if commit_mean > 0 else 0
        variance_penalty = max(0, 100 - (cv * 20))  # Penalize high variance
        
        # Combine metrics
        consistency_score = (basic_consistency * 0.7) + (variance_penalty * 0.3)
        
        return {
            "consistency_score": float(consistency_score),
            "active_days": unique_commit_days,
            "total_days": date_range,
            "active_percentage": float(basic_consistency),
            "average_commits_per_day": float(commit_mean),
            "commit_std_deviation": float(commit_std),
            "interpretation": self._interpret_consistency(consistency_score),
        }
    
    def _interpret_consistency(self, score: float) -> str:
        """Interpret consistency score."""
        if score >= 80:
            return "Machine-like Consistency - You code almost every day! 🤖"
        elif score >= 60:
            return "Highly Consistent - Strong regular coding habit. 💪"
        elif score >= 40:
            return "Moderately Consistent - Room for more regularity. 📈"
        elif score >= 20:
            return "Sporadic Coder - Inconsistent commit patterns. 🎲"
        else:
            return "Burst Coder - Intense periods followed by breaks. 💥"
    
    def identify_hot_streaks(self, min_streak: int = 3) -> Dict[str, Any]:
        """
        Identify hot streaks (periods of intense activity).
        
        Args:
            min_streak: Minimum days to qualify as a hot streak
            
        Returns:
            Dictionary with hot streak statistics
        """
        if self.df.empty:
            return {}
        
        # Group by date and count commits
        daily_commits = self.df.groupby("date").size().sort_index()
        
        # Define hot streak as days with above-average commits
        threshold = daily_commits.mean() + daily_commits.std()
        hot_days = daily_commits[daily_commits >= threshold]
        
        # Find consecutive hot days
        streaks = []
        current_streak = []
        
        hot_dates = set(hot_days.index)
        all_dates = pd.date_range(
            start=self.df["timestamp"].min().date(),
            end=self.df["timestamp"].max().date(),
            freq="D"
        )
        
        for date in all_dates:
            if date.date() in hot_dates:
                current_streak.append(date.date())
            else:
                if len(current_streak) >= min_streak:
                    streaks.append(current_streak)
                current_streak = []
        
        # Don't forget last streak
        if len(current_streak) >= min_streak:
            streaks.append(current_streak)
        
        # Format streaks
        formatted_streaks = []
        for streak in streaks:
            streak_commits = self.df[
                self.df["date"].isin(streak)
            ]
            formatted_streaks.append({
                "start_date": str(min(streak)),
                "end_date": str(max(streak)),
                "duration_days": len(streak),
                "total_commits": len(streak_commits),
                "avg_commits_per_day": len(streak_commits) / len(streak),
            })
        
        # Sort by duration
        formatted_streaks.sort(key=lambda x: x["duration_days"], reverse=True)
        
        return {
            "total_hot_streaks": len(formatted_streaks),
            "longest_hot_streak": formatted_streaks[0] if formatted_streaks else None,
            "all_hot_streaks": formatted_streaks[:5],  # Top 5
            "hot_streak_threshold": float(threshold),
        }
    
    def calculate_project_devotion_index(self) -> Dict[str, Any]:
        """
        Calculate devotion index for each repository.
        
        Returns:
            Dictionary with devotion metrics per repository
        """
        if self.df.empty:
            return {}
        
        repo_metrics = []
        
        for repo_name in self.df["repo_name"].unique():
            repo_commits = self.df[self.df["repo_name"] == repo_name]
            
            # Calculate metrics
            total_commits = len(repo_commits)
            date_range = (repo_commits["timestamp"].max() - repo_commits["timestamp"].min()).days + 1
            active_days = repo_commits["date"].nunique()
            
            # Devotion index formula:
            # (commits * active_days / date_range) normalized to 0-100
            raw_devotion = (total_commits * active_days / date_range) if date_range > 0 else 0
            
            # Normalize (cap at reasonable maximum)
            devotion_index = min(100, raw_devotion * 5)
            
            repo_metrics.append({
                "repo_name": repo_name,
                "total_commits": total_commits,
                "date_range_days": date_range,
                "active_days": active_days,
                "devotion_index": float(devotion_index),
                "first_commit": str(repo_commits["timestamp"].min()),
                "last_commit": str(repo_commits["timestamp"].max()),
            })
        
        # Sort by devotion index
        repo_metrics.sort(key=lambda x: x["devotion_index"], reverse=True)
        
        return {
            "repositories": repo_metrics,
            "most_devoted_repo": repo_metrics[0] if repo_metrics else None,
            "total_repositories": len(repo_metrics),
        }
    
    def calculate_velocity_metrics(self) -> Dict[str, Any]:
        """
        Calculate code velocity metrics.
        
        Returns:
            Dictionary with velocity statistics
        """
        if self.df.empty:
            return {}
        
        # Overall velocity
        total_commits = len(self.df)
        date_range = (self.df["timestamp"].max() - self.df["timestamp"].min()).days + 1
        commits_per_day = total_commits / date_range if date_range > 0 else 0
        
        # Calculate moving average for trend
        daily_commits = self.df.groupby("date").size()
        
        # 7-day moving average
        if len(daily_commits) >= 7:
            ma7 = daily_commits.rolling(window=7).mean()
            recent_velocity = ma7.iloc[-1]
            early_velocity = ma7.iloc[6]  # First valid MA point
            
            velocity_trend = ((recent_velocity - early_velocity) / early_velocity * 100) if early_velocity > 0 else 0
        else:
            recent_velocity = commits_per_day
            velocity_trend = 0
        
        # Peak velocity day
        peak_day = daily_commits.idxmax()
        peak_commits = daily_commits.max()
        
        # Calculate percentile ranks for current velocity
        daily_values = daily_commits.values
        current_percentile = (daily_values <= recent_velocity).sum() / len(daily_values) * 100
        
        return {
            "average_commits_per_day": float(commits_per_day),
            "recent_velocity": float(recent_velocity),
            "velocity_trend_percentage": float(velocity_trend),
            "velocity_interpretation": "Accelerating 🚀" if velocity_trend > 10 
                                      else "Decelerating 📉" if velocity_trend < -10
                                      else "Stable ➡️",
            "peak_day": {
                "date": str(peak_day),
                "commits": int(peak_commits),
            },
            "current_velocity_percentile": float(current_percentile),
        }
    
    def generate_spotify_wrapped_stats(self) -> Dict[str, Any]:
        """
        Generate fun "Spotify Wrapped" style statistics.
        
        Returns:
            Dictionary with engaging statistics
        """
        if self.df.empty:
            return {}
        
        total_commits = len(self.df)
        
        # Calculate total lines changed (estimate)
        total_changes = 0
        for files_list in self.df["files_changed"]:
            for file in files_list:
                total_changes += file.get("changes", 0)
        
        # Most productive day
        daily_commits = self.df.groupby("date").size()
        best_day = daily_commits.idxmax()
        best_day_count = daily_commits.max()
        
        # Favorite hour
        favorite_hour = self.df["hour"].mode()[0] if not self.df["hour"].mode().empty else 12
        
        # Favorite day of week
        favorite_day = self.df["day_of_week"].mode()[0] if not self.df["day_of_week"].mode().empty else "Monday"
        
        # Most committed repo
        top_repo = self.df["repo_name"].value_counts().index[0]
        top_repo_commits = self.df["repo_name"].value_counts().iloc[0]
        
        return {
            "total_commits": total_commits,
            "total_changes": total_changes,
            "best_day": {
                "date": str(best_day),
                "commits": int(best_day_count),
            },
            "favorite_coding_hour": int(favorite_hour),
            "favorite_day_of_week": favorite_day,
            "most_committed_repo": {
                "name": top_repo,
                "commits": int(top_repo_commits),
            },
            "wrapped_message": self._generate_wrapped_message(
                total_commits, 
                favorite_hour, 
                favorite_day
            ),
        }
    
    def _generate_wrapped_message(self, commits: int, hour: int, day: str) -> str:
        """Generate personalized wrapped message."""
        time_emoji = "🌙" if hour >= 20 or hour < 6 else "☀️"
        
        return (
            f"You made {format_number(commits)} commits this year! "
            f"Your favorite time to code is {hour}:00 {time_emoji}, "
            f"and you love coding on {day}s. Keep building amazing things!"
        )
    
    def get_full_analysis(self) -> Dict[str, Any]:
        """
        Run all productivity analyses and return combined results.
        
        Returns:
            Dictionary with all productivity analysis results
        """
        logger.info("Running productivity analysis...")
        
        return {
            "consistency": self.calculate_consistency_score(),
            "hot_streaks": self.identify_hot_streaks(),
            "project_devotion": self.calculate_project_devotion_index(),
            "velocity": self.calculate_velocity_metrics(),
            "wrapped_stats": self.generate_spotify_wrapped_stats(),
        }


def analyze_productivity_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convenience function to run all productivity analyses.
    
    Args:
        df: DataFrame with commit data
        
    Returns:
        Dictionary with all productivity analysis results
    """
    analyzer = ProductivityAnalyzer(df)
    return analyzer.get_full_analysis()
