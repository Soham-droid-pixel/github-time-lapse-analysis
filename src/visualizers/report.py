"""
HTML report builder using Jinja2.

Generates a beautiful, interactive HTML dashboard with all visualizations
and statistics.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import json

from jinja2 import Environment, FileSystemLoader
import plotly.graph_objects as go

from ..config import TEMPLATES_DIR, OUTPUT_DIR, settings, COLORS
from ..utils import setup_logging, format_number

logger = setup_logging()


class ReportBuilder:
    """Builds HTML dashboard from analysis results and charts."""
    
    def __init__(
        self, 
        df_summary: Dict[str, Any],
        analysis_results: Dict[str, Any],
        charts: Dict[str, go.Figure]
    ):
        """
        Initialize report builder.
        
        Args:
            df_summary: Summary statistics about the dataset
            analysis_results: Dictionary with all analysis results
            charts: Dictionary of Plotly figures
        """
        self.df_summary = df_summary
        self.results = analysis_results
        self.charts = charts
        
        # Setup Jinja2 environment
        self.env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
        self.env.filters["format_number"] = format_number
    
    def _convert_charts_to_html(self) -> Dict[str, str]:
        """
        Convert Plotly figures to HTML divs.
        
        Returns:
            Dictionary mapping chart names to HTML strings
        """
        html_charts = {}
        
        for name, fig in self.charts.items():
            html_charts[name] = fig.to_html(
                include_plotlyjs=False,
                full_html=False,  # Only output div+script, not full HTML document
                div_id=f"chart_{name}",
                config={
                    "displayModeBar": True,
                    "displaylogo": False,
                    "modeBarButtonsToRemove": ["select2d", "lasso2d"],
                    "responsive": True,
                }
            )
        
        return html_charts
    
    def _prepare_stats_cards(self) -> List[Dict[str, Any]]:
        """
        Prepare statistics cards for dashboard.
        
        Returns:
            List of stat card dictionaries
        """
        temporal = self.results.get("temporal", {})
        linguistic = self.results.get("linguistic", {})
        language = self.results.get("language", {})
        productivity = self.results.get("productivity", {})
        
        # Extract key metrics
        total_commits = self.df_summary.get("total_commits", 0)
        total_repos = self.df_summary.get("total_repositories", 0)
        date_range_days = self.df_summary.get("date_range_days", 0)
        
        consistency_score = productivity.get("consistency", {}).get("consistency_score", 0)
        longest_streak = temporal.get("streaks", {}).get("longest_streak", 0)
        primary_language = language.get("distribution", {}).get("primary_language", "Unknown")
        personality = temporal.get("personality", {}).get("personality_type", "Coder")
        
        cards = [
            {
                "title": "Total Commits",
                "value": format_number(total_commits),
                "icon": "📝",
                "color": COLORS["primary"],
            },
            {
                "title": "Repositories",
                "value": str(total_repos),
                "icon": "📦",
                "color": COLORS["secondary"],
            },
            {
                "title": "Days Active",
                "value": str(date_range_days),
                "icon": "📅",
                "color": COLORS["accent"],
            },
            {
                "title": "Consistency",
                "value": f"{consistency_score:.0f}%",
                "icon": "⚡",
                "color": COLORS["success"],
            },
            {
                "title": "Longest Streak",
                "value": f"{longest_streak} days",
                "icon": "🔥",
                "color": COLORS["warning"],
            },
            {
                "title": "Primary Language",
                "value": primary_language,
                "icon": "💻",
                "color": COLORS["info"],
            },
        ]
        
        return cards
    
    def _prepare_insights(self) -> List[Dict[str, str]]:
        """
        Prepare key insights for the dashboard.
        
        Returns:
            List of insight dictionaries
        """
        temporal = self.results.get("temporal", {})
        linguistic = self.results.get("linguistic", {})
        language = self.results.get("language", {})
        productivity = self.results.get("productivity", {})
        
        insights = []
        
        # Personality insight
        personality = temporal.get("personality", {})
        if personality:
            insights.append({
                "title": personality.get("personality_type", ""),
                "description": personality.get("description", ""),
                "icon": "🌟",
            })
        
        # Consistency insight
        consistency = productivity.get("consistency", {})
        if consistency:
            insights.append({
                "title": "Coding Consistency",
                "description": consistency.get("interpretation", ""),
                "icon": "📊",
            })
        
        # Language diversity insight
        diversity = language.get("diversity", {})
        if diversity:
            insights.append({
                "title": "Language Diversity",
                "description": diversity.get("diversity_interpretation", ""),
                "icon": "🌐",
            })
        
        # Velocity insight
        velocity = productivity.get("velocity", {})
        if velocity:
            insights.append({
                "title": "Code Velocity",
                "description": f"Your velocity is {velocity.get('velocity_interpretation', 'stable')}. "
                              f"Recent average: {velocity.get('recent_velocity', 0):.1f} commits/day",
                "icon": "🚀",
            })
        
        return insights
    
    def _prepare_top_lists(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Prepare top lists (repos, languages, etc.).
        
        Returns:
            Dictionary of top lists
        """
        linguistic = self.results.get("linguistic", {})
        language = self.results.get("language", {})
        productivity = self.results.get("productivity", {})
        
        # Top action verbs
        action_verbs = linguistic.get("action_verbs", {}).get("top_action_verbs", [])[:10]
        
        # Top languages
        top_languages = language.get("distribution", {}).get("top_languages", [])[:10]
        
        # Most devoted repos
        devotion = productivity.get("project_devotion", {}).get("repositories", [])[:10]
        
        return {
            "action_verbs": action_verbs,
            "languages": top_languages,
            "devoted_repos": devotion,
        }
    
    def build_report(self, output_filename: str = "github_analysis_report.html") -> Path:
        """
        Build the HTML report.
        
        Args:
            output_filename: Name of the output HTML file
            
        Returns:
            Path to the generated HTML file
        """
        logger.info("Building HTML report...")
        
        # Convert charts to HTML
        html_charts = self._convert_charts_to_html()
        
        # Prepare template context
        context = {
            "username": settings.github_username,
            "generated_at": datetime.now().strftime("%B %d, %Y at %H:%M"),
            "stats_cards": self._prepare_stats_cards(),
            "insights": self._prepare_insights(),
            "top_lists": self._prepare_top_lists(),
            "charts": html_charts,
            "summary": self.df_summary,
            "results": self.results,
            "colors": COLORS,
        }
        
        # Load and render template
        template = self.env.get_template("dashboard.html")
        html_content = template.render(**context)
        
        # Save to file
        output_path = OUTPUT_DIR / output_filename
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        logger.info(f"Report saved to: {output_path}")
        return output_path


def build_dashboard(
    df_summary: Dict[str, Any],
    analysis_results: Dict[str, Any],
    charts: Dict[str, go.Figure],
    output_filename: str = "github_analysis_report.html"
) -> Path:
    """
    Convenience function to build dashboard report.
    
    Args:
        df_summary: Summary statistics about the dataset
        analysis_results: Dictionary with all analysis results
        charts: Dictionary of Plotly figures
        output_filename: Name of the output HTML file
        
    Returns:
        Path to the generated HTML file
    """
    builder = ReportBuilder(df_summary, analysis_results, charts)
    return builder.build_report(output_filename)
