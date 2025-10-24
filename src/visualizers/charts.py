"""
Chart generation using Plotly.

Creates interactive visualizations for the GitHub analysis dashboard.
"""

from typing import Dict, Any, List
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

from ..config import COLORS, CHART_THEME
from ..utils import format_number, setup_logging

logger = setup_logging()


class ChartGenerator:
    """Generates interactive Plotly charts for commit analysis."""
    
    def __init__(self, df: pd.DataFrame, analysis_results: Dict[str, Any]):
        """
        Initialize chart generator.
        
        Args:
            df: DataFrame with commit data
            analysis_results: Dictionary with all analysis results
        """
        self.df = df
        self.results = analysis_results
        self.template = CHART_THEME["template"]
    
    def create_circadian_heatmap(self) -> go.Figure:
        """
        Create 24-hour circadian rhythm heatmap.
        
        Returns:
            Plotly figure object
        """
        hour_data = self.results["temporal"]["hour_distribution"]
        hourly_counts = hour_data.get("hourly_counts", {})
        
        # Prepare data
        hours = list(range(24))
        counts = [hourly_counts.get(h, 0) for h in hours]
        
        # Create polar bar chart
        fig = go.Figure(go.Barpolar(
            r=counts,
            theta=[h * 15 for h in hours],  # Convert to degrees
            marker=dict(
                color=counts,
                colorscale="Viridis",
                showscale=True,
                colorbar=dict(title="Commits"),
            ),
            hovertemplate="<b>%{theta}°</b><br>Hour: %{customdata}<br>Commits: %{r}<extra></extra>",
            customdata=[f"{h}:00" for h in hours],
        ))
        
        fig.update_layout(
            template=self.template,
            title="Circadian Coding Pattern - When Do You Code?",
            polar=dict(
                radialaxis=dict(showticklabels=True, range=[0, max(counts) * 1.1]),
                angularaxis=dict(
                    tickmode="array",
                    tickvals=[0, 45, 90, 135, 180, 225, 270, 315],
                    ticktext=["0:00", "3:00", "6:00", "9:00", "12:00", "15:00", "18:00", "21:00"],
                ),
            ),
            showlegend=False,
        )
        
        return fig
    
    def create_day_of_week_chart(self) -> go.Figure:
        """
        Create day of week bar chart.
        
        Returns:
            Plotly figure object
        """
        day_data = self.results["temporal"]["day_of_week"]
        daily_counts = day_data.get("daily_counts", {})
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        counts = [daily_counts.get(day, 0) for day in days]
        
        colors_list = [
            COLORS["primary"] if i < 5 else COLORS["accent"]
            for i in range(7)
        ]
        
        fig = go.Figure(go.Bar(
            x=days,
            y=counts,
            marker=dict(color=colors_list),
            hovertemplate="<b>%{x}</b><br>Commits: %{y}<extra></extra>",
        ))
        
        fig.update_layout(
            template=self.template,
            title="Day of Week Distribution - When Are You Most Active?",
            xaxis_title="Day of Week",
            yaxis_title="Number of Commits",
            showlegend=False,
        )
        
        return fig
    
    def create_language_evolution_chart(self) -> go.Figure:
        """
        Create stacked area chart showing language evolution over time.
        
        Returns:
            Plotly figure object
        """
        lang_data = self.results["language"]["evolution"].get("timeline", [])
        
        if not lang_data:
            return self._create_empty_chart("Language Evolution Over Time")
        
        df_lang = pd.DataFrame(lang_data)
        
        # Get top languages
        lang_totals = df_lang.drop(columns=["month"]).sum().sort_values(ascending=False)
        top_languages = lang_totals.head(8).index.tolist()
        
        fig = go.Figure()
        
        for lang in top_languages:
            if lang in df_lang.columns:
                fig.add_trace(go.Scatter(
                    x=df_lang["month"],
                    y=df_lang[lang],
                    mode="lines",
                    stackgroup="one",
                    name=lang,
                    hovertemplate=f"<b>{lang}</b><br>Month: %{{x}}<br>Files: %{{y}}<extra></extra>",
                ))
        
        fig.update_layout(
            template=self.template,
            title="Technology Stack Evolution - Language Usage Over Time",
            xaxis_title="Month",
            yaxis_title="Files Changed",
            hovermode="x unified",
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=1.01,
            ),
        )
        
        return fig
    
    def create_sentiment_timeline(self) -> go.Figure:
        """
        Create sentiment analysis timeline.
        
        Returns:
            Plotly figure object
        """
        sentiment_data = self.results["linguistic"].get("sentiment", {})
        polarity_timeline = sentiment_data.get("polarity_over_time", [])
        
        if not polarity_timeline:
            return self._create_empty_chart("Commit Message Sentiment Over Time")
        
        df_sentiment = pd.DataFrame(polarity_timeline)
        df_sentiment["date"] = pd.to_datetime(df_sentiment["date"])
        
        # Calculate rolling average
        df_sentiment = df_sentiment.sort_values("date")
        df_sentiment["rolling_avg"] = df_sentiment["polarity"].rolling(window=20, min_periods=1).mean()
        
        # Create figure with both raw and smoothed data
        fig = go.Figure()
        
        # Raw sentiment
        fig.add_trace(go.Scatter(
            x=df_sentiment["date"],
            y=df_sentiment["polarity"],
            mode="markers",
            name="Individual Commits",
            marker=dict(
                size=4,
                color=df_sentiment["polarity"],
                colorscale=[[0, COLORS["danger"]], [0.5, COLORS["muted"]], [1, COLORS["success"]]],
                showscale=False,
                opacity=0.5,
            ),
            hovertemplate="<b>%{x}</b><br>Sentiment: %{y:.2f}<extra></extra>",
        ))
        
        # Rolling average
        fig.add_trace(go.Scatter(
            x=df_sentiment["date"],
            y=df_sentiment["rolling_avg"],
            mode="lines",
            name="Trend (20-commit avg)",
            line=dict(color=COLORS["primary"], width=3),
            hovertemplate="<b>%{x}</b><br>Avg Sentiment: %{y:.2f}<extra></extra>",
        ))
        
        # Add zero line
        fig.add_hline(
            y=0, 
            line=dict(color=COLORS["muted"], dash="dash", width=1),
            annotation_text="Neutral",
        )
        
        fig.update_layout(
            template=self.template,
            title="Commit Message Sentiment Over Time - Are You Happy While Coding?",
            xaxis_title="Date",
            yaxis_title="Sentiment Polarity",
            hovermode="x unified",
            showlegend=True,
        )
        
        return fig
    
    def create_repository_commits_chart(self) -> go.Figure:
        """
        Create horizontal bar chart of top repositories by commit count.
        
        Returns:
            Plotly figure object
        """
        repo_counts = self.df["repo_name"].value_counts().head(15)
        
        fig = go.Figure(go.Bar(
            y=repo_counts.index[::-1],  # Reverse for top-to-bottom
            x=repo_counts.values[::-1],
            orientation="h",
            marker=dict(
                color=repo_counts.values[::-1],
                colorscale="Viridis",
                showscale=False,
            ),
            hovertemplate="<b>%{y}</b><br>Commits: %{x}<extra></extra>",
        ))
        
        fig.update_layout(
            template=self.template,
            title="Top Repositories by Commit Count - Where Do You Spend Your Time?",
            xaxis_title="Number of Commits",
            yaxis_title="Repository",
            height=500,
        )
        
        return fig
    
    def create_monthly_activity_chart(self) -> go.Figure:
        """
        Create monthly activity line chart.
        
        Returns:
            Plotly figure object
        """
        monthly_data = self.results["temporal"]["monthly_trends"]
        monthly_counts = monthly_data.get("monthly_counts", {})
        
        if not monthly_counts:
            return self._create_empty_chart("Monthly Commit Activity")
        
        months = sorted(monthly_counts.keys())
        counts = [monthly_counts[m] for m in months]
        
        fig = go.Figure()
        
        # Line chart
        fig.add_trace(go.Scatter(
            x=months,
            y=counts,
            mode="lines+markers",
            line=dict(color=COLORS["primary"], width=3),
            marker=dict(size=8),
            fill="tozeroy",
            fillcolor=f"rgba(99, 102, 241, 0.1)",
            hovertemplate="<b>%{x}</b><br>Commits: %{y}<extra></extra>",
        ))
        
        # Add average line
        avg = sum(counts) / len(counts)
        fig.add_hline(
            y=avg,
            line=dict(color=COLORS["accent"], dash="dash", width=2),
            annotation_text=f"Average: {avg:.0f}",
        )
        
        fig.update_layout(
            template=self.template,
            title="Monthly Commit Activity - How Has Your Productivity Evolved?",
            xaxis_title="Month",
            yaxis_title="Number of Commits",
            hovermode="x unified",
        )
        
        return fig
    
    def create_commit_message_types_chart(self) -> go.Figure:
        """
        Create pie chart of commit message types.
        
        Returns:
            Plotly figure object
        """
        message_quality = self.results["linguistic"]["message_quality"]
        message_types = message_quality.get("message_types", {})
        
        if not message_types:
            return self._create_empty_chart("Commit Message Types")
        
        fig = go.Figure(go.Pie(
            labels=list(message_types.keys()),
            values=list(message_types.values()),
            hole=0.4,
            marker=dict(
                colors=[COLORS["primary"], COLORS["secondary"], COLORS["accent"],
                       COLORS["success"], COLORS["warning"], COLORS["info"], COLORS["danger"]],
            ),
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>",
        ))
        
        fig.update_layout(
            template=self.template,
            title="Commit Message Types - What Are You Working On?",
            showlegend=True,
        )
        
        return fig
    
    def create_language_distribution_chart(self) -> go.Figure:
        """
        Create treemap of language distribution.
        
        Returns:
            Plotly figure object
        """
        lang_dist = self.results["language"]["distribution"]
        lang_counts = lang_dist.get("language_counts", {})
        
        if not lang_counts:
            return self._create_empty_chart("Programming Language Distribution")
        
        # Get top languages for better visualization
        top_langs = sorted(lang_counts.items(), key=lambda x: x[1], reverse=True)[:15]
        
        languages = [lang for lang, _ in top_langs]
        counts = [count for _, count in top_langs]
        
        fig = go.Figure(go.Treemap(
            labels=languages,
            parents=[""] * len(languages),
            values=counts,
            marker=dict(
                colorscale="Viridis",
                showscale=False,
            ),
            hovertemplate="<b>%{label}</b><br>Files: %{value}<br>%{percentParent}<extra></extra>",
        ))
        
        fig.update_layout(
            template=self.template,
            title="Programming Language Distribution - Your Tech Stack",
        )
        
        return fig
    
    def create_productivity_gauge(self) -> go.Figure:
        """
        Create gauge chart for consistency score.
        
        Returns:
            Plotly figure object
        """
        consistency_data = self.results["productivity"]["consistency"]
        score = consistency_data.get("consistency_score", 0)
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Consistency Score"},
            delta={"reference": 70, "valueformat": ".0f"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": COLORS["primary"]},
                "steps": [
                    {"range": [0, 40], "color": "rgba(239, 68, 68, 0.2)"},
                    {"range": [40, 70], "color": "rgba(245, 158, 11, 0.2)"},
                    {"range": [70, 100], "color": "rgba(16, 185, 129, 0.2)"},
                ],
                "threshold": {
                    "line": {"color": COLORS["accent"], "width": 4},
                    "thickness": 0.75,
                    "value": 80,
                },
            },
        ))
        
        fig.update_layout(
            template=self.template,
            height=350,
        )
        
        return fig
    
    def _create_empty_chart(self, title: str) -> go.Figure:
        """Create empty chart placeholder."""
        fig = go.Figure()
        
        fig.add_annotation(
            text="No data available for this visualization",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16, color=COLORS["muted"]),
        )
        
        fig.update_layout(
            template=self.template,
            title=title,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        )
        
        return fig
    
    def generate_all_charts(self) -> Dict[str, go.Figure]:
        """
        Generate all charts for the dashboard.
        
        Returns:
            Dictionary mapping chart names to Plotly figures
        """
        logger.info("Generating charts...")
        
        return {
            "circadian_heatmap": self.create_circadian_heatmap(),
            "day_of_week": self.create_day_of_week_chart(),
            "language_evolution": self.create_language_evolution_chart(),
            "sentiment_timeline": self.create_sentiment_timeline(),
            "top_repositories": self.create_repository_commits_chart(),
            "monthly_activity": self.create_monthly_activity_chart(),
            "message_types": self.create_commit_message_types_chart(),
            "language_distribution": self.create_language_distribution_chart(),
            "consistency_gauge": self.create_productivity_gauge(),
        }


def generate_charts(df: pd.DataFrame, analysis_results: Dict[str, Any]) -> Dict[str, go.Figure]:
    """
    Convenience function to generate all charts.
    
    Args:
        df: DataFrame with commit data
        analysis_results: Dictionary with all analysis results
        
    Returns:
        Dictionary mapping chart names to Plotly figures
    """
    generator = ChartGenerator(df, analysis_results)
    return generator.generate_all_charts()
