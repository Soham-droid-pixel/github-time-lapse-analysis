"""
Programming language analysis.

Analyzes programming language usage trends, technology stack evolution,
and language diversity over time.
"""

from collections import Counter
from typing import Dict, Any, List
import pandas as pd
import numpy as np

from ..utils import map_extension_to_language, setup_logging

logger = setup_logging()


class LanguageAnalyzer:
    """Analyzes programming language usage patterns."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize language analyzer.
        
        Args:
            df: DataFrame with commit data (must have 'files_changed' column)
        """
        self.df = df
        
        if df.empty:
            logger.warning("Empty DataFrame provided to LanguageAnalyzer")
        elif "files_changed" not in df.columns:
            raise ValueError("DataFrame must have 'files_changed' column")
    
    def extract_languages_from_commits(self) -> pd.DataFrame:
        """
        Extract language information from file changes.
        
        Returns:
            DataFrame with language usage per commit
        """
        if self.df.empty:
            return pd.DataFrame()
        
        language_data = []
        
        for idx, row in self.df.iterrows():
            files = row["files_changed"]
            if not files:
                continue
            
            # Count languages in this commit
            language_counts = Counter()
            
            for file_info in files:
                extension = file_info.get("extension", "no_extension")
                language = map_extension_to_language(extension)
                # Skip binary/media files (None values)
                if language is not None:
                    language_counts[language] += 1
            
            # Add to data
            for language, count in language_counts.items():
                language_data.append({
                    "timestamp": row["timestamp"],
                    "date": row["date"],
                    "month": row["month"],
                    "year": row["year"],
                    "repo_name": row["repo_name"],
                    "language": language,
                    "file_count": count,
                })
        
        return pd.DataFrame(language_data)
    
    def analyze_overall_distribution(self) -> Dict[str, Any]:
        """
        Analyze overall language distribution across all commits.
        
        Returns:
            Dictionary with language distribution statistics
        """
        lang_df = self.extract_languages_from_commits()
        
        if lang_df.empty:
            return {}
        
        # Count total files per language
        language_counts = lang_df.groupby("language")["file_count"].sum().sort_values(ascending=False)
        
        # Calculate percentages
        total_files = language_counts.sum()
        language_percentages = (language_counts / total_files * 100).to_dict()
        
        # Top languages
        top_10 = language_counts.head(10)
        
        return {
            "total_languages": len(language_counts),
            "total_files_changed": int(total_files),
            "language_counts": language_counts.to_dict(),
            "language_percentages": language_percentages,
            "top_languages": [
                {
                    "language": lang,
                    "count": int(count),
                    "percentage": float(count / total_files * 100),
                }
                for lang, count in top_10.items()
            ],
            "primary_language": language_counts.idxmax() if len(language_counts) > 0 else "Unknown",
        }
    
    def analyze_temporal_evolution(self) -> Dict[str, Any]:
        """
        Analyze how language usage evolved over time.
        
        Returns:
            Dictionary with temporal language trends
        """
        lang_df = self.extract_languages_from_commits()
        
        if lang_df.empty:
            return {}
        
        # Group by month and language
        monthly_lang = lang_df.groupby(["month", "language"])["file_count"].sum().unstack(fill_value=0)
        
        # Convert to format suitable for visualization
        timeline_data = []
        for month in monthly_lang.index:
            month_data = {"month": str(month)}
            for language in monthly_lang.columns:
                month_data[language] = int(monthly_lang.loc[month, language])
            timeline_data.append(month_data)
        
        # Identify emerging and declining languages
        if len(monthly_lang) >= 3:
            # Compare first third vs last third
            split_point = len(monthly_lang) // 3
            early_period = monthly_lang.iloc[:split_point].sum()
            late_period = monthly_lang.iloc[-split_point:].sum()
            
            # Calculate growth rates
            growth_rates = {}
            for lang in monthly_lang.columns:
                early = early_period.get(lang, 0)
                late = late_period.get(lang, 0)
                
                if early > 0:
                    growth = ((late - early) / early) * 100
                    growth_rates[lang] = growth
                elif late > 0:
                    growth_rates[lang] = 100.0  # New language
            
            # Sort by growth
            emerging = sorted(
                [(lang, rate) for lang, rate in growth_rates.items() if rate > 20],
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            declining = sorted(
                [(lang, rate) for lang, rate in growth_rates.items() if rate < -20],
                key=lambda x: x[1]
            )[:5]
            
            evolution_stats = {
                "emerging_languages": [
                    {"language": lang, "growth_rate": float(rate)}
                    for lang, rate in emerging
                ],
                "declining_languages": [
                    {"language": lang, "growth_rate": float(rate)}
                    for lang, rate in declining
                ],
            }
        else:
            evolution_stats = {
                "emerging_languages": [],
                "declining_languages": [],
            }
        
        return {
            "timeline": timeline_data,
            **evolution_stats,
        }
    
    def analyze_by_repository(self) -> Dict[str, Any]:
        """
        Analyze primary language for each repository.
        
        Returns:
            Dictionary with per-repository language statistics
        """
        lang_df = self.extract_languages_from_commits()
        
        if lang_df.empty:
            return {}
        
        # Get primary language per repo
        repo_languages = lang_df.groupby(["repo_name", "language"])["file_count"].sum()
        
        repo_primary = {}
        for repo in lang_df["repo_name"].unique():
            if repo in repo_languages.index.get_level_values(0):
                repo_data = repo_languages[repo].sort_values(ascending=False)
                repo_primary[repo] = {
                    "primary_language": repo_data.idxmax(),
                    "languages": repo_data.to_dict(),
                }
        
        return {
            "repositories": repo_primary,
            "total_repositories": len(repo_primary),
        }
    
    def calculate_diversity_score(self) -> Dict[str, Any]:
        """
        Calculate language diversity metrics.
        
        Returns:
            Dictionary with diversity statistics
        """
        lang_df = self.extract_languages_from_commits()
        
        if lang_df.empty:
            return {}
        
        # Count unique languages
        unique_languages = lang_df["language"].nunique()
        
        # Calculate Shannon diversity index
        language_counts = lang_df.groupby("language")["file_count"].sum()
        total = language_counts.sum()
        proportions = language_counts / total
        
        # Shannon entropy
        shannon_index = -np.sum(proportions * np.log(proportions))
        
        # Normalize to 0-100 scale
        # Maximum entropy would be log(n) where n is number of possible languages
        max_entropy = np.log(unique_languages) if unique_languages > 1 else 1
        diversity_score = (shannon_index / max_entropy * 100) if max_entropy > 0 else 0
        
        return {
            "unique_languages": unique_languages,
            "shannon_diversity_index": float(shannon_index),
            "diversity_score": float(diversity_score),
            "diversity_interpretation": self._interpret_diversity(diversity_score),
        }
    
    def _interpret_diversity(self, score: float) -> str:
        """Interpret diversity score."""
        if score >= 75:
            return "Polyglot Master - You're fluent in many languages! 🌐"
        elif score >= 50:
            return "Multi-language Developer - You work comfortably across several languages. 💪"
        elif score >= 25:
            return "Focused Specialist - You concentrate on a core set of languages. 🎯"
        else:
            return "Single Language Expert - Deep mastery in one primary language. 🔬"
    
    def get_full_analysis(self) -> Dict[str, Any]:
        """
        Run all language analyses and return combined results.
        
        Returns:
            Dictionary with all language analysis results
        """
        logger.info("Running language analysis...")
        
        return {
            "distribution": self.analyze_overall_distribution(),
            "evolution": self.analyze_temporal_evolution(),
            "by_repository": self.analyze_by_repository(),
            "diversity": self.calculate_diversity_score(),
        }


def analyze_language_patterns(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convenience function to run all language analyses.
    
    Args:
        df: DataFrame with commit data
        
    Returns:
        Dictionary with all language analysis results
    """
    analyzer = LanguageAnalyzer(df)
    return analyzer.get_full_analysis()
