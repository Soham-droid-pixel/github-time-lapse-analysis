"""
Linguistic analysis of commit messages using NLP.

Analyzes commit messages for sentiment, common patterns, action verbs,
and readability metrics using NLTK and TextBlob.
"""

import re
from collections import Counter
from typing import Dict, Any, List, Tuple
import warnings

import pandas as pd
import numpy as np

# NLP imports
try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from textblob import TextBlob
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    warnings.warn("NLTK or TextBlob not installed. Install with: pip install nltk textblob")

from ..config import NLTK_DATA_PATH, NLTK_PACKAGES, CUSTOM_STOPWORDS
from ..utils import setup_logging, truncate_text

logger = setup_logging()


def download_nltk_data():
    """Download required NLTK data packages."""
    if not NLTK_AVAILABLE:
        return
    
    NLTK_DATA_PATH.mkdir(exist_ok=True)
    nltk.data.path.append(str(NLTK_DATA_PATH))
    
    for package in NLTK_PACKAGES:
        try:
            nltk.data.find(f'tokenizers/{package}')
        except LookupError:
            try:
                nltk.download(package, download_dir=str(NLTK_DATA_PATH), quiet=True)
            except Exception as e:
                logger.warning(f"Failed to download NLTK package {package}: {e}")


class LinguisticAnalyzer:
    """Analyzes linguistic patterns in commit messages."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize linguistic analyzer.
        
        Args:
            df: DataFrame with commit data (must have 'message' column)
        """
        self.df = df
        
        if df.empty:
            logger.warning("Empty DataFrame provided to LinguisticAnalyzer")
        elif "message" not in df.columns:
            raise ValueError("DataFrame must have 'message' column")
        
        # Initialize NLP tools
        if NLTK_AVAILABLE:
            download_nltk_data()
            try:
                self.stop_words = set(stopwords.words('english'))
                self.stop_words.update(CUSTOM_STOPWORDS)
                self.lemmatizer = WordNetLemmatizer()
            except Exception as e:
                logger.warning(f"Error initializing NLTK: {e}")
                self.stop_words = CUSTOM_STOPWORDS
                self.lemmatizer = None
        else:
            self.stop_words = CUSTOM_STOPWORDS
            self.lemmatizer = None
    
    def preprocess_message(self, message: str) -> List[str]:
        """
        Preprocess commit message for NLP analysis.
        
        Args:
            message: Raw commit message
            
        Returns:
            List of processed tokens
        """
        # Convert to lowercase
        message = message.lower()
        
        # Remove URLs
        message = re.sub(r'http\S+|www.\S+', '', message)
        
        # Remove special characters but keep spaces
        message = re.sub(r'[^a-zA-Z\s]', ' ', message)
        
        # Tokenize
        if NLTK_AVAILABLE:
            try:
                tokens = word_tokenize(message)
            except:
                tokens = message.split()
        else:
            tokens = message.split()
        
        # Remove stopwords and short words
        tokens = [
            word for word in tokens 
            if word not in self.stop_words and len(word) > 2
        ]
        
        # Lemmatize
        if self.lemmatizer:
            try:
                tokens = [self.lemmatizer.lemmatize(word) for word in tokens]
            except:
                pass
        
        return tokens
    
    def extract_action_verbs(self, top_n: int = 20) -> Dict[str, Any]:
        """
        Extract most common action verbs from commit messages.
        
        Args:
            top_n: Number of top verbs to return
            
        Returns:
            Dictionary with verb statistics
        """
        if self.df.empty:
            return {}
        
        # Common action verbs in commit messages
        action_verbs = [
            'add', 'added', 'adding',
            'fix', 'fixed', 'fixing',
            'update', 'updated', 'updating',
            'remove', 'removed', 'removing',
            'refactor', 'refactored', 'refactoring',
            'implement', 'implemented', 'implementing',
            'create', 'created', 'creating',
            'delete', 'deleted', 'deleting',
            'change', 'changed', 'changing',
            'improve', 'improved', 'improving',
            'clean', 'cleaned', 'cleaning',
            'optimize', 'optimized', 'optimizing',
            'enhance', 'enhanced', 'enhancing',
            'merge', 'merged', 'merging',
            'revert', 'reverted', 'reverting',
        ]
        
        verb_counts = Counter()
        
        for message in self.df["message"]:
            tokens = self.preprocess_message(message)
            for token in tokens:
                if token in action_verbs:
                    verb_counts[token] += 1
        
        top_verbs = verb_counts.most_common(top_n)
        
        return {
            "top_action_verbs": [
                {"verb": verb, "count": count}
                for verb, count in top_verbs
            ],
            "total_action_verbs": sum(verb_counts.values()),
            "unique_action_verbs": len(verb_counts),
        }
    
    def analyze_sentiment(self) -> Dict[str, Any]:
        """
        Analyze sentiment of commit messages over time.
        
        Returns:
            Dictionary with sentiment statistics
        """
        if self.df.empty or not NLTK_AVAILABLE:
            return {}
        
        sentiments = []
        polarities = []
        subjectivities = []
        
        for message in self.df["message"]:
            try:
                blob = TextBlob(message)
                polarity = blob.sentiment.polarity
                subjectivity = blob.sentiment.subjectivity
                
                polarities.append(polarity)
                subjectivities.append(subjectivity)
                
                # Classify sentiment
                if polarity > 0.1:
                    sentiment = "positive"
                elif polarity < -0.1:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
                
                sentiments.append(sentiment)
            except Exception as e:
                polarities.append(0.0)
                subjectivities.append(0.0)
                sentiments.append("neutral")
        
        # Add to dataframe for temporal analysis
        self.df["sentiment"] = sentiments
        self.df["polarity"] = polarities
        self.df["subjectivity"] = subjectivities
        
        # Calculate statistics
        sentiment_counts = pd.Series(sentiments).value_counts()
        
        # Find most extreme messages
        df_with_sentiment = self.df.copy()
        most_positive_idx = df_with_sentiment["polarity"].idxmax()
        most_negative_idx = df_with_sentiment["polarity"].idxmin()
        
        return {
            "average_polarity": float(np.mean(polarities)),
            "average_subjectivity": float(np.mean(subjectivities)),
            "sentiment_distribution": sentiment_counts.to_dict(),
            "most_positive_commit": {
                "message": truncate_text(df_with_sentiment.loc[most_positive_idx, "message"]),
                "polarity": float(df_with_sentiment.loc[most_positive_idx, "polarity"]),
                "date": str(df_with_sentiment.loc[most_positive_idx, "timestamp"]),
            },
            "most_negative_commit": {
                "message": truncate_text(df_with_sentiment.loc[most_negative_idx, "message"]),
                "polarity": float(df_with_sentiment.loc[most_negative_idx, "polarity"]),
                "date": str(df_with_sentiment.loc[most_negative_idx, "timestamp"]),
            },
            "polarity_over_time": [
                {
                    "date": str(row["timestamp"]),
                    "polarity": float(row["polarity"]),
                }
                for _, row in df_with_sentiment[["timestamp", "polarity"]].iterrows()
            ],
        }
    
    def analyze_message_quality(self) -> Dict[str, Any]:
        """
        Analyze commit message quality and characteristics.
        
        Returns:
            Dictionary with message quality metrics
        """
        if self.df.empty:
            return {}
        
        # Message length statistics
        message_lengths = self.df["message_length"]
        word_counts = self.df["message_word_count"]
        
        # Classify message types
        def classify_message(msg: str) -> str:
            msg_lower = msg.lower()
            if any(word in msg_lower for word in ['merge', 'merging', 'merged']):
                return "merge"
            elif any(word in msg_lower for word in ['fix', 'bug', 'error']):
                return "bugfix"
            elif any(word in msg_lower for word in ['feat', 'feature', 'add', 'new']):
                return "feature"
            elif any(word in msg_lower for word in ['refactor', 'clean', 'improve']):
                return "refactor"
            elif any(word in msg_lower for word in ['doc', 'readme', 'comment']):
                return "documentation"
            elif any(word in msg_lower for word in ['test', 'testing']):
                return "test"
            else:
                return "other"
        
        message_types = self.df["message"].apply(classify_message)
        type_counts = message_types.value_counts()
        
        # Find interesting commits
        shortest_msg = self.df.loc[message_lengths.idxmin()]
        longest_msg = self.df.loc[message_lengths.idxmax()]
        
        return {
            "average_length": float(message_lengths.mean()),
            "median_length": float(message_lengths.median()),
            "average_word_count": float(word_counts.mean()),
            "median_word_count": float(word_counts.median()),
            "message_types": type_counts.to_dict(),
            "shortest_message": {
                "message": shortest_msg["message"],
                "length": int(shortest_msg["message_length"]),
                "date": str(shortest_msg["timestamp"]),
            },
            "longest_message": {
                "message": truncate_text(longest_msg["message"]),
                "length": int(longest_msg["message_length"]),
                "date": str(longest_msg["timestamp"]),
            },
        }
    
    def extract_common_phrases(self, n_gram: int = 2, top_n: int = 15) -> Dict[str, Any]:
        """
        Extract most common n-grams (phrases) from commit messages.
        
        Args:
            n_gram: Size of n-grams (2 for bigrams, 3 for trigrams)
            top_n: Number of top phrases to return
            
        Returns:
            Dictionary with common phrases
        """
        if self.df.empty:
            return {}
        
        all_ngrams = []
        
        for message in self.df["message"]:
            tokens = self.preprocess_message(message)
            
            # Generate n-grams
            if len(tokens) >= n_gram:
                ngrams = zip(*[tokens[i:] for i in range(n_gram)])
                all_ngrams.extend([' '.join(gram) for gram in ngrams])
        
        # Count most common
        ngram_counts = Counter(all_ngrams)
        top_ngrams = ngram_counts.most_common(top_n)
        
        return {
            f"top_{n_gram}grams": [
                {"phrase": phrase, "count": count}
                for phrase, count in top_ngrams
            ],
            "total_unique_phrases": len(ngram_counts),
        }
    
    def get_full_analysis(self) -> Dict[str, Any]:
        """
        Run all linguistic analyses and return combined results.
        
        Returns:
            Dictionary with all linguistic analysis results
        """
        logger.info("Running linguistic analysis...")
        
        results = {
            "action_verbs": self.extract_action_verbs(),
            "message_quality": self.analyze_message_quality(),
            "common_bigrams": self.extract_common_phrases(n_gram=2),
            "common_trigrams": self.extract_common_phrases(n_gram=3),
        }
        
        # Add sentiment analysis if available
        if NLTK_AVAILABLE:
            results["sentiment"] = self.analyze_sentiment()
        else:
            logger.warning("Sentiment analysis skipped - TextBlob not available")
            results["sentiment"] = {}
        
        return results


def analyze_linguistic_patterns(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Convenience function to run all linguistic analyses.
    
    Args:
        df: DataFrame with commit data
        
    Returns:
        Dictionary with all linguistic analysis results
    """
    analyzer = LinguisticAnalyzer(df)
    return analyzer.get_full_analysis()
