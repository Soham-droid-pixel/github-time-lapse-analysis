# 🕐 GitHub Time-Lapse Analyzer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Analyze your GitHub commit history to uncover fascinating insights about your coding habits, productivity patterns, and evolution as a developer.

## 🌟 Features

- **📊 Circadian Coding Pattern**: 24-hour heatmap revealing when you're most productive
- **💬 Commit Message DNA**: NLP analysis of your commit messages (sentiment, action verbs, patterns)
- **🎯 Project Devotion Index**: Measure commitment and consistency across repositories
- **🔄 Technology Evolution**: Track programming language trends over time
- **⚡ Code Velocity Metrics**: Streaks, consistency scores, and productivity insights
- **📈 Interactive Dashboard**: Beautiful, responsive HTML report with Plotly visualizations

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- GitHub Personal Access Token ([Generate here](https://github.com/settings/tokens))
- Git installed on your system

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd github_time_analyser
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your GitHub credentials
   # Add your GITHUB_TOKEN and GITHUB_USERNAME
   ```

5. **Run the analyzer**
   ```bash
   python main.py
   ```

The analysis will generate an interactive HTML dashboard in the `output/` directory.

## 📁 Project Structure

```
github_analyzer/
├── src/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── data_fetcher.py        # GitHub API integration
│   ├── analyzers/
│   │   ├── __init__.py
│   │   ├── temporal.py        # Time-based analysis
│   │   ├── linguistic.py      # Commit message NLP
│   │   ├── language.py        # Programming language trends
│   │   └── productivity.py    # Metrics calculation
│   ├── visualizers/
│   │   ├── __init__.py
│   │   ├── charts.py          # Plotly chart generators
│   │   └── report.py          # HTML report builder
│   └── utils.py               # Helper functions
├── templates/
│   └── dashboard.html         # Jinja2 template
├── data/                      # Cached API data (gitignored)
├── output/                    # Generated reports
├── tests/                     # Unit tests
├── main.py                    # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

## 🔧 Configuration

Edit `.env` to customize:

```env
GITHUB_TOKEN=your_token_here
GITHUB_USERNAME=your_username
CACHE_ENABLED=true
CACHE_DAYS=7
MAX_REPOSITORIES=100
COMMITS_PER_REPO=1000
```

## 📊 Analysis Modules

### Temporal Analysis
- Hour-of-day distribution
- Day-of-week patterns
- Peak coding hours identification
- Night Owl vs Early Bird classification
- Longest active streaks

### Linguistic Analysis
- Action verb extraction from commit messages
- Sentiment analysis over time
- Commit message quality scoring
- Signature phrase identification
- Readability metrics

### Language Analysis
- Programming language usage trends
- Technology stack evolution
- File extension statistics
- Language diversity score

### Productivity Analysis
- Commit frequency metrics
- Consistency scoring
- Hot streak detection
- Project devotion index
- Productivity predictions

## 🎨 Visualization Examples

The dashboard includes:
- Interactive Plotly charts with zoom and hover tooltips
- Dark-themed modern design
- Responsive layout for mobile devices
- Animated statistics cards
- "Spotify Wrapped" style metrics

## 🧪 Testing

Run tests with:
```bash
pytest tests/
pytest --cov=src tests/  # With coverage
```

## 📝 Development

### Code Quality
```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/
```

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome! Feel free to:
- Open issues for bugs or feature requests
- Submit pull requests with improvements
- Share your analysis results

## 📄 License

MIT License - feel free to use this project for your own portfolio!

## 🙏 Acknowledgments

- GitHub API via PyGithub
- Plotly for amazing visualizations
- NLTK team for NLP tools
- The open-source community

## 📧 Contact

Created by [Your Name] - [your.email@example.com]

Portfolio: [your-portfolio.com]
LinkedIn: [linkedin.com/in/yourprofile]

---

⭐ Star this repo if you found it useful!
