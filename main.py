"""
Main entry point for GitHub Time-Lapse Analyzer.

This script orchestrates the entire analysis pipeline:
1. Fetch commit data from GitHub API
2. Run all analysis modules
3. Generate visualizations
4. Build HTML dashboard
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import settings, get_output_path
from src.data_fetcher import fetch_github_data
from src.analyzers.temporal import analyze_temporal_patterns
from src.analyzers.linguistic import analyze_linguistic_patterns
from src.analyzers.language import analyze_language_patterns
from src.analyzers.productivity import analyze_productivity_metrics
from src.visualizers.charts import generate_charts
from src.visualizers.report import build_dashboard
from src.utils import setup_logging, format_number
from export_web_data import export_for_web_app

logger = setup_logging()


def create_summary_stats(df) -> dict:
    """
    Create summary statistics from the DataFrame.
    
    Args:
        df: DataFrame with commit data
        
    Returns:
        Dictionary with summary statistics
    """
    if df.empty:
        return {
            "total_commits": 0,
            "total_repositories": 0,
            "date_range_days": 0,
            "first_commit": None,
            "last_commit": None,
        }
    
    return {
        "total_commits": len(df),
        "total_repositories": df["repo_name"].nunique(),
        "date_range_days": (df["timestamp"].max() - df["timestamp"].min()).days + 1,
        "first_commit": str(df["timestamp"].min()),
        "last_commit": str(df["timestamp"].max()),
    }


def main():
    """Main execution function."""
    print("=" * 70)
    print("🚀 GitHub Time-Lapse Analyzer")
    print("=" * 70)
    print(f"\nAnalyzing GitHub user: @{settings.github_username}")
    print(f"Cache enabled: {settings.cache_enabled}")
    print("-" * 70)
    
    try:
        # Step 1: Fetch data
        print("\n📥 STEP 1: Fetching commit data from GitHub...")
        df = fetch_github_data(use_cache=settings.cache_enabled)
        
        if df.empty:
            print("❌ No commit data found! Please check your GitHub username and token.")
            return 1
        
        summary = create_summary_stats(df)
        print(f"✅ Fetched {format_number(summary['total_commits'])} commits "
              f"from {summary['total_repositories']} repositories")
        print(f"   Date range: {summary['first_commit'][:10]} to {summary['last_commit'][:10]}")
        
        # Step 2: Run analyses
        print("\n🔍 STEP 2: Running analyses...")
        
        print("   ⏰ Temporal analysis...")
        temporal_results = analyze_temporal_patterns(df)
        
        print("   💬 Linguistic analysis...")
        linguistic_results = analyze_linguistic_patterns(df)
        
        print("   🌐 Language analysis...")
        language_results = analyze_language_patterns(df)
        
        print("   📈 Productivity analysis...")
        productivity_results = analyze_productivity_metrics(df)
        
        # Combine all results
        analysis_results = {
            "temporal": temporal_results,
            "linguistic": linguistic_results,
            "language": language_results,
            "productivity": productivity_results,
        }
        
        print("✅ All analyses completed successfully!")
        
        # Step 3: Generate visualizations
        print("\n📊 STEP 3: Generating visualizations...")
        charts = generate_charts(df, analysis_results)
        print(f"✅ Generated {len(charts)} interactive charts")
        
        # Step 4: Build dashboard
        print("\n🎨 STEP 4: Building HTML dashboard...")
        output_path = build_dashboard(
            df_summary=summary,
            analysis_results=analysis_results,
            charts=charts
        )
        print(f"✅ Dashboard generated successfully!")
        
        # Step 5: Export data for React web app
        print("\n📤 STEP 5: Exporting data for React web app...")
        web_data_path = export_for_web_app(
            df_summary=summary,
            analysis_results=analysis_results,
            username=settings.github_username
        )
        print("✅ Web app data exported successfully!")
        
        # Summary
        print("\n" + "=" * 70)
        print("🎉 ANALYSIS COMPLETE!")
        print("=" * 70)
        print(f"\n📄 Report location: {output_path}")
        print(f"📊 Total commits analyzed: {format_number(summary['total_commits'])}")
        print(f"📦 Repositories: {summary['total_repositories']}")
        print(f"📅 Days of activity: {summary['date_range_days']}")
        
        # Key highlights
        print("\n🌟 KEY HIGHLIGHTS:")
        personality = temporal_results.get("personality", {}).get("personality_type", "Coder")
        print(f"   • Coding Personality: {personality}")
        
        consistency = productivity_results.get("consistency", {}).get("consistency_score", 0)
        print(f"   • Consistency Score: {consistency:.1f}/100")
        
        longest_streak = temporal_results.get("streaks", {}).get("longest_streak", 0)
        print(f"   • Longest Streak: {longest_streak} days")
        
        primary_lang = language_results.get("distribution", {}).get("primary_language", "Unknown")
        print(f"   • Primary Language: {primary_lang}")
        
        print("\n💡 Open the HTML report in your browser to explore the full analysis!")
        print("=" * 70)
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user.")
        return 130
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        logger.exception("Analysis failed with exception:")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
