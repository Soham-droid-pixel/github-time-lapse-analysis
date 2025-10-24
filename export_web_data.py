"""
Export analysis data to JSON for the React web app.
"""

import json
from pathlib import Path
from typing import Dict, Any
import pandas as pd

from src.config import OUTPUT_DIR
from src.utils import setup_logging

logger = setup_logging()


def export_for_web_app(
    df_summary: Dict[str, Any],
    analysis_results: Dict[str, Any],
    username: str
) -> Path:
    """
    Export analysis data as JSON for React app.
    
    Args:
        df_summary: Summary statistics
        analysis_results: All analysis results
        username: GitHub username
    
    Returns:
        Path to JSON file
    """
    logger.info("Exporting data for web app...")
    
    temporal = analysis_results.get("temporal", {})
    linguistic = analysis_results.get("linguistic", {})
    language = analysis_results.get("language", {})
    productivity = analysis_results.get("productivity", {})
    
    # Prepare stats cards
    stats = [
        {
            "icon": "📝",
            "value": str(df_summary.get("total_commits", 0)),
            "title": "Total Commits",
            "color": "#6366f1"
        },
        {
            "icon": "📦",
            "value": str(df_summary.get("total_repositories", 0)),
            "title": "Repositories",
            "color": "#ec4899"
        },
        {
            "icon": "📅",
            "value": str(df_summary.get("date_range_days", 0)),
            "title": "Days Active",
            "color": "#8b5cf6"
        },
        {
            "icon": "⚡",
            "value": f"{productivity.get('consistency', {}).get('consistency_score', 0):.0f}%",
            "title": "Consistency",
            "color": "#10b981"
        },
        {
            "icon": "🔥",
            "value": f"{temporal.get('streaks', {}).get('longest_streak', 0)} days",
            "title": "Longest Streak",
            "color": "#f59e0b"
        },
        {
            "icon": "💻",
            "value": language.get("distribution", {}).get("primary_language", "Unknown"),
            "title": "Primary Language",
            "color": "#06b6d4"
        }
    ]
    
    # Prepare insights
    insights = []
    personality = temporal.get("personality", {})
    if personality:
        insights.append({
            "icon": "🌟",
            "title": personality.get("personality_type", ""),
            "description": personality.get("description", "")
        })
    
    consistency = productivity.get("consistency", {})
    if consistency:
        insights.append({
            "icon": "📊",
            "title": "Coding Consistency",
            "description": consistency.get("interpretation", "")
        })
    
    diversity = language.get("diversity", {})
    if diversity:
        insights.append({
            "icon": "🌐",
            "title": "Language Diversity",
            "description": diversity.get("diversity_interpretation", "")
        })
    
    velocity = productivity.get("velocity", {})
    if velocity:
        insights.append({
            "icon": "🚀",
            "title": "Code Velocity",
            "description": f"Your velocity is {velocity.get('velocity_interpretation', 'stable')}. Recent average: {velocity.get('recent_velocity', 0):.1f} commits/day"
        })
    
    # Prepare chart data
    hour_data = temporal.get("hour_distribution", {}).get("hourly_counts", {})
    circadian_data = [
        {"hour": f"{h}:00", "commits": hour_data.get(h, 0)}
        for h in range(24)
    ]
    
    # Day of week
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_data = temporal.get("day_of_week", {})
    daily_counts = day_data.get("daily_counts", {})
    day_of_week_data = []
    for day in day_names:
        commits = daily_counts.get(day, 0)
        day_of_week_data.append({"day": day, "commits": commits})
    
    # Monthly activity
    monthly = temporal.get("monthly_trends", {})
    monthly_counts = monthly.get("monthly_counts", {})
    monthly_data = []
    if monthly_counts:
        for month, count in sorted(monthly_counts.items()):
            monthly_data.append({"month": str(month), "commits": int(count)})

    
    average_commits = sum(d["commits"] for d in monthly_data) / len(monthly_data) if monthly_data else 0
    
    # Language distribution
    top_languages = language.get("distribution", {}).get("top_languages", [])[:15]
    language_dist_data = []
    for lang in top_languages:
        if isinstance(lang, (list, tuple)) and len(lang) >= 2:
            language_dist_data.append({"name": lang[0], "value": lang[1]})
        elif isinstance(lang, dict):
            language_dist_data.append({"name": lang.get("language", "Unknown"), "value": lang.get("count", 0)})
    
    # Language evolution
    lang_evolution = language.get("evolution", {})
    timeline = lang_evolution.get("timeline", []) if isinstance(lang_evolution, dict) else []
    
    # Extract unique languages from timeline
    all_languages = set()
    for month_data in timeline:
        all_languages.update([k for k in month_data.keys() if k != 'month'])
    
    evolution_data = timeline
    languages_list = list(all_languages)[:8]
    
    # Sentiment
    sentiment_dist = linguistic.get("sentiment", {}).get("sentiment_distribution", {})
    sentiment_data = [
        {"name": "Positive", "value": sentiment_dist.get("positive", 0)},
        {"name": "Neutral", "value": sentiment_dist.get("neutral", 0)},
        {"name": "Negative", "value": sentiment_dist.get("negative", 0)}
    ]
    
    # Top lists
    action_verbs_data = linguistic.get("action_verbs", {})
    if isinstance(action_verbs_data, dict):
        action_verbs = action_verbs_data.get("top_action_verbs", [])[:10]
    else:
        action_verbs = []
    
    project_devotion = productivity.get("project_devotion", {})
    devoted_repos = project_devotion.get("repositories", [])[:10]
    devoted_repos_formatted = [
        {"name": repo.get("repo_name", "Unknown"), "commits": repo.get("total_commits", 0)}
        for repo in devoted_repos
    ]
    
    # Format top languages for list
    top_langs_for_list = []
    for lang in top_languages[:10]:
        if isinstance(lang, (list, tuple)) and len(lang) >= 2:
            top_langs_for_list.append(lang)
        elif isinstance(lang, dict):
            top_langs_for_list.append([lang.get("language", "Unknown"), lang.get("count", 0)])
    
    # Assemble final data
    web_data = {
        "username": username,
        "generated_at": pd.Timestamp.now().strftime("%B %d, %Y at %H:%M"),
        "stats": stats,
        "insights": insights,
        "charts": {
            "circadian": circadian_data,
            "day_of_week": day_of_week_data,
            "monthly_activity": {
                "months": monthly_data,
                "average": average_commits
            },
            "language_distribution": language_dist_data,
            "language_evolution": {
                "months": evolution_data,
                "languages": languages_list
            },
            "sentiment": sentiment_data
        },
        "top_lists": {
            "action_verbs": action_verbs,
            "languages": top_langs_for_list,
            "devoted_repos": devoted_repos_formatted
        }
    }
    
    # Save to JSON
    output_path = OUTPUT_DIR / "analysis_data.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(web_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Web app data exported to: {output_path}")
    return output_path
