"""Debug script to check analysis data structure."""
import json
from pathlib import Path
from src.data_fetcher import fetch_github_data
from src.analyzers.temporal import analyze_temporal_patterns
from src.analyzers.linguistic import analyze_linguistic_patterns
from src.analyzers.language import analyze_language_patterns
from src.analyzers.productivity import analyze_productivity_metrics

# Load data
df = fetch_github_data()

# Run temporal analysis
temporal_results = analyze_temporal_patterns(df)

print("=== TEMPORAL ANALYSIS KEYS ===")
print(temporal_results.keys())

print("\n=== DAY OF WEEK DATA ===")
print("Type:", type(temporal_results.get("day_of_week")))
print("Data:", temporal_results.get("day_of_week"))

print("\n=== MONTHLY TRENDS DATA ===")
monthly = temporal_results.get("monthly_trends", {})
print("Type:", type(monthly))
print("Keys:", monthly.keys() if isinstance(monthly, dict) else "N/A")
if isinstance(monthly, dict):
    counts = monthly.get("counts", {})
    print("Counts type:", type(counts))
    print("Sample entries:", list(counts.items())[:5] if counts else "Empty")

print("\n=== LINGUISTIC ANALYSIS ===")
linguistic_results = analyze_linguistic_patterns(df)
print("Keys:", linguistic_results.keys())
action_verbs = linguistic_results.get("action_verbs", [])
print("Action verbs:", action_verbs[:5] if isinstance(action_verbs, list) else action_verbs)

print("\n=== PRODUCTIVITY ANALYSIS ===")
productivity_results = analyze_productivity_metrics(df)
print("Keys:", productivity_results.keys())
devoted = productivity_results.get("devoted_repos", [])
print("Devoted repos:", devoted[:3] if devoted else "Empty")

print("\n=== LANGUAGE PATTERNS ===")
language_results = analyze_language_patterns(df)
print("Keys:", language_results.keys())
evolution = language_results.get("evolution", [])
print("Evolution type:", type(evolution))
if isinstance(evolution, dict):
    print("Evolution keys:", evolution.keys())
    print("Evolution sample:", list(evolution.items())[:3] if evolution else "Empty")
elif isinstance(evolution, list):
    print("Evolution sample:", evolution[:3] if evolution else "Empty")
else:
    print("Evolution:", evolution)
