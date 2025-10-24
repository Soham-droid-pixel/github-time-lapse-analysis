"""
GitHub API data fetcher with authentication, rate limiting, and caching.

This module handles all interactions with the GitHub API using PyGithub,
including fetching repositories and commits with proper error handling.
"""

import time
from datetime import datetime
from typing import Dict, List, Optional, Any

import pandas as pd
from github import Github, GithubException, RateLimitExceededException
from tqdm import tqdm

from .config import (
    settings,
    CACHE_FILE,
    CACHE_METADATA_FILE,
    RATE_LIMIT_BUFFER,
    RETRY_ATTEMPTS,
    RETRY_DELAY,
)
from .utils import (
    setup_logging,
    save_json,
    load_json,
    is_cache_valid,
    get_file_extension,
)

logger = setup_logging()


class GitHubDataFetcher:
    """Fetches and processes commit data from GitHub API."""
    
    def __init__(self, use_cache: bool = True):
        """
        Initialize GitHub API client.
        
        Args:
            use_cache: Whether to use cached data if available
        """
        self.use_cache = use_cache and settings.cache_enabled
        self.github = Github(settings.github_token)
        self.username = settings.github_username
        logger.info(f"Initialized GitHub API client for user: {self.username}")
        
    def _check_rate_limit(self) -> None:
        """
        Check GitHub API rate limit and wait if necessary.
        
        Raises:
            RateLimitExceededException: If rate limit is exceeded
        """
        rate_limit = self.github.get_rate_limit()
        remaining = rate_limit.core.remaining
        
        if remaining < RATE_LIMIT_BUFFER:
            reset_time = rate_limit.core.reset
            wait_time = (reset_time - datetime.now()).total_seconds()
            
            if wait_time > 0:
                logger.warning(
                    f"Rate limit low ({remaining} remaining). "
                    f"Waiting {wait_time:.0f} seconds until reset..."
                )
                time.sleep(wait_time + 10)  # Add 10 second buffer
    
    def _retry_on_failure(self, func, *args, **kwargs) -> Any:
        """
        Retry a function call with exponential backoff.
        
        Args:
            func: Function to call
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
            
        Returns:
            Result of the function call
            
        Raises:
            Exception: If all retry attempts fail
        """
        for attempt in range(RETRY_ATTEMPTS):
            try:
                return func(*args, **kwargs)
            except RateLimitExceededException:
                self._check_rate_limit()
            except GithubException as e:
                if e.status == 403:  # Rate limit or abuse detection
                    logger.warning(f"GitHub API error 403, waiting...")
                    time.sleep(RETRY_DELAY * (2 ** attempt))
                elif attempt == RETRY_ATTEMPTS - 1:
                    raise
                else:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(RETRY_DELAY * (2 ** attempt))
            except Exception as e:
                if attempt == RETRY_ATTEMPTS - 1:
                    raise
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(RETRY_DELAY * (2 ** attempt))
        
        raise Exception("All retry attempts failed")
    
    def fetch_repositories(self) -> List[Any]:
        """
        Fetch all repositories for the authenticated user.
        
        Returns:
            List of repository objects
        """
        logger.info("Fetching repositories...")
        user = self._retry_on_failure(self.github.get_user, self.username)
        
        repos = []
        try:
            # Get all repos (both owned and contributed to)
            all_repos = list(user.get_repos())[:settings.max_repositories]
            
            # Filter to only include repos where user has commits
            for repo in tqdm(all_repos, desc="Filtering repositories"):
                try:
                    # Quick check if user has any commits
                    commits = list(repo.get_commits(author=self.username)[:1])
                    if commits:
                        repos.append(repo)
                except GithubException:
                    continue  # Skip repos we can't access
                    
            logger.info(f"Found {len(repos)} repositories with commits")
            return repos
            
        except GithubException as e:
            logger.error(f"Error fetching repositories: {e}")
            return []
    
    def fetch_commits_from_repo(self, repo: Any) -> List[Dict[str, Any]]:
        """
        Fetch all commits from a repository for the authenticated user.
        
        Args:
            repo: Repository object from PyGithub
            
        Returns:
            List of commit dictionaries with extracted data
        """
        commits_data = []
        
        try:
            commits = repo.get_commits(
                author=self.username
            )[:settings.commits_per_repo]
            
            for commit in commits:
                try:
                    # Extract commit data
                    commit_data = {
                        "sha": commit.sha,
                        "message": commit.commit.message,
                        "timestamp": commit.commit.author.date.isoformat(),
                        "repo_name": repo.name,
                        "repo_full_name": repo.full_name,
                        "author": commit.commit.author.name,
                        "files_changed": [],
                    }
                    
                    # Extract file information
                    try:
                        files = commit.files
                        for file in files[:50]:  # Limit to avoid rate limits
                            commit_data["files_changed"].append({
                                "filename": file.filename,
                                "extension": get_file_extension(file.filename),
                                "additions": file.additions,
                                "deletions": file.deletions,
                                "changes": file.changes,
                            })
                    except GithubException:
                        # Some commits don't have file info available
                        pass
                    
                    commits_data.append(commit_data)
                    
                except Exception as e:
                    logger.warning(f"Error processing commit {commit.sha}: {e}")
                    continue
                    
        except GithubException as e:
            logger.warning(f"Error fetching commits from {repo.name}: {e}")
            
        return commits_data
    
    def fetch_all_commits(self) -> pd.DataFrame:
        """
        Fetch all commits from all repositories.
        
        Returns:
            DataFrame containing all commit data
        """
        # Check cache first
        if self.use_cache and is_cache_valid(CACHE_METADATA_FILE, settings.cache_days):
            logger.info("Loading commits from cache...")
            cached_data = load_json(CACHE_FILE)
            if cached_data:
                df = pd.DataFrame(cached_data)
                logger.info(f"Loaded {len(df)} commits from cache")
                return self._process_dataframe(df)
        
        # Fetch fresh data
        logger.info("Fetching fresh data from GitHub API...")
        repos = self.fetch_repositories()
        
        if not repos:
            logger.error("No repositories found!")
            return pd.DataFrame()
        
        all_commits = []
        
        # Fetch commits from each repo
        for repo in tqdm(repos, desc="Fetching commits"):
            self._check_rate_limit()
            commits = self._retry_on_failure(self.fetch_commits_from_repo, repo)
            all_commits.extend(commits)
            
            # Small delay to be nice to GitHub
            time.sleep(0.1)
        
        logger.info(f"Fetched {len(all_commits)} total commits")
        
        # Save to cache
        if self.use_cache and all_commits:
            logger.info("Saving to cache...")
            save_json(all_commits, CACHE_FILE)
            save_json(
                {
                    "timestamp": datetime.now().isoformat(),
                    "commit_count": len(all_commits),
                    "repository_count": len(repos),
                    "username": self.username,
                },
                CACHE_METADATA_FILE
            )
        
        # Convert to DataFrame
        df = pd.DataFrame(all_commits)
        return self._process_dataframe(df)
    
    def _process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process raw DataFrame to add computed columns.
        
        Args:
            df: Raw DataFrame from API or cache
            
        Returns:
            Processed DataFrame with additional columns
        """
        if df.empty:
            return df
        
        # Convert timestamp to datetime
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        
        # Extract temporal features
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.day_name()
        df["day_of_week_num"] = df["timestamp"].dt.dayofweek
        df["date"] = df["timestamp"].dt.date
        df["month"] = df["timestamp"].dt.to_period("M")
        df["year"] = df["timestamp"].dt.year
        
        # Extract message features
        df["message_length"] = df["message"].str.len()
        df["message_word_count"] = df["message"].str.split().str.len()
        
        # Count files per commit
        df["files_count"] = df["files_changed"].apply(len)
        
        # Sort by timestamp
        df = df.sort_values("timestamp").reset_index(drop=True)
        
        logger.info("DataFrame processed successfully")
        return df
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """
        Get current rate limit status.
        
        Returns:
            Dictionary with rate limit information
        """
        rate_limit = self.github.get_rate_limit()
        return {
            "remaining": rate_limit.core.remaining,
            "limit": rate_limit.core.limit,
            "reset_time": rate_limit.core.reset.isoformat(),
        }


def fetch_github_data(use_cache: bool = True) -> pd.DataFrame:
    """
    Main function to fetch GitHub commit data.
    
    Args:
        use_cache: Whether to use cached data if available
        
    Returns:
        DataFrame containing all commit data
        
    Example:
        >>> df = fetch_github_data()
        >>> print(f"Fetched {len(df)} commits")
    """
    fetcher = GitHubDataFetcher(use_cache=use_cache)
    
    # Log rate limit status
    rate_status = fetcher.get_rate_limit_status()
    logger.info(
        f"GitHub API Rate Limit: {rate_status['remaining']}/{rate_status['limit']} remaining"
    )
    
    # Fetch data
    df = fetcher.fetch_all_commits()
    
    if not df.empty:
        logger.info(f"Successfully fetched {len(df)} commits from {df['repo_name'].nunique()} repositories")
        logger.info(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
    else:
        logger.warning("No commits were fetched!")
    
    return df
