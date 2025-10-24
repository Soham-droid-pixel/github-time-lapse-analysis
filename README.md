# 🕐 GitHub Time-Lapse Analyzer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.0-61dafb.svg)](https://reactjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> 🚀 Analyze your GitHub commit history to uncover fascinating insights about your coding habits, productivity patterns, and evolution as a developer. Features both a comprehensive Python analysis engine and a stunning React visualization dashboard.

![GitHub Time-Lapse Analyzer](https://img.shields.io/badge/status-active-success.svg)

## ✨ Highlights

Transform your GitHub commit data into a beautiful "Spotify Wrapped" style experience:

- **📊 Interactive React Dashboard**: Modern, responsive web app with real-time visualizations
- **🎯 13 Distinct Metrics**: From circadian patterns to language evolution
- **🧠 AI-Powered Insights**: NLP analysis of commit messages and coding personality
- **🌈 Beautiful UI**: Glassmorphism effects, smooth animations, and gradient designs
- **📈 Portfolio Ready**: Professional-grade project showcasing full-stack skills

## 🌟 Features

### Backend Analysis (Python)
- **📊 Circadian Coding Pattern**: 24-hour heatmap revealing when you're most productive
- **💬 Commit Message DNA**: NLP analysis with sentiment scoring and action verb extraction
- **🎯 Project Devotion Index**: Measure commitment and consistency across repositories
- **🔄 Technology Evolution**: Track programming language trends month-by-month
- **⚡ Code Velocity Metrics**: Streaks, consistency scores, and productivity predictions
- **🌍 Language Diversity**: Polyglot score and technology stack analysis

### Frontend Dashboard (React)
- **🎨 Modern UI/UX**: Glassmorphism design with smooth animations and gradients
- **📱 Fully Responsive**: Perfect on desktop, tablet, and mobile devices
- **📊 6 Chart Types**: Radar, bar, area, treemap, stacked area, and pie charts
- **🏆 Top Rankings**: Action verbs, languages, and most devoted repositories
- **💡 Smart Insights**: AI-generated personality traits and coding patterns
- **⚡ Lightning Fast**: Vite build system with hot module replacement

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 16+ and npm
- GitHub Personal Access Token ([Generate here](https://github.com/settings/tokens))
- Git installed on your system

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Soham-droid-pixel/github-time-lapse-analysis.git
   cd github_time_analyser
   ```

2. **Backend Setup (Python)**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your GitHub credentials
   # Add your GITHUB_TOKEN and GITHUB_USERNAME
   ```

4. **Run Python analysis**
   ```bash
   python main.py
   ```
   This generates:
   - `output/github_analysis_report.html` - Full HTML report
   - `output/analysis_data.json` - Data for React app

5. **Frontend Setup (React)**
   ```bash
   # Navigate to web app
   cd web-app
   
   # Install dependencies
   npm install
   
   # Copy JSON data to public folder
   cp ../output/analysis_data.json public/
   
   # Start dev server
   npm run dev
   ```

6. **Open your browser**
   - React App: `http://localhost:5173`
   - HTML Report: Open `output/github_analysis_report.html`

## 📁 Project Structure

```
github_time_analyser/
├── src/                       # Python backend
│   ├── analyzers/
│   │   ├── temporal.py        # Time-based analysis
│   │   ├── linguistic.py      # Commit message NLP
│   │   ├── language.py        # Programming language trends
│   │   └── productivity.py    # Metrics calculation
│   ├── visualizers/
│   │   ├── charts.py          # Plotly chart generators
│   │   └── report.py          # HTML report builder
│   ├── config.py              # Configuration management
│   ├── data_fetcher.py        # GitHub API integration
│   └── utils.py               # Helper functions
│
├── web-app/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── StatsCards.jsx
│   │   │   ├── InsightCards.jsx
│   │   │   ├── TopLists.jsx
│   │   │   └── charts/        # 6 chart components
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   │   └── analysis_data.json # Generated data
│   ├── package.json
│   └── vite.config.js
│
├── templates/
│   └── dashboard.html         # Jinja2 template
├── output/                    # Generated reports
├── data/                      # Cached API data
├── main.py                    # Entry point
├── export_web_data.py         # JSON export for React
├── requirements.txt
└── README.md
```

## 🔧 Configuration

Edit `.env` to customize analysis:

```env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=your_username
CACHE_ENABLED=true
CACHE_DAYS=7
MAX_REPOSITORIES=100
COMMITS_PER_REPO=1000
```

## 📊 Analysis Modules

### 1. Temporal Analysis 🕐
- **Hour-of-day distribution**: 24-hour activity heatmap
- **Day-of-week patterns**: Weekly coding rhythm
- **Monthly trends**: Long-term activity tracking
- **Peak hours identification**: When you code best
- **Personality classification**: Night Owl 🦉 vs Early Bird 🐦
- **Longest streaks**: Consistency tracking

### 2. Linguistic Analysis 💬
- **Action verb extraction**: Most used commit verbs
- **Sentiment analysis**: Positive/negative/neutral trends
- **Commit quality scoring**: Message readability metrics
- **Common patterns**: Bigrams and trigrams
- **Signature phrases**: Your coding vocabulary

### 3. Language Analysis 🌐
- **Language distribution**: Which languages you use most
- **Evolution timeline**: Technology journey over time
- **Emerging technologies**: Languages gaining momentum
- **Declining technologies**: Languages being phased out
- **Diversity score**: Polyglot vs specialist rating

### 4. Productivity Analysis 📈
- **Consistency scoring**: Regular coding habits (0-100)
- **Hot streaks**: Periods of intense activity
- **Project devotion**: Commitment to repositories
- **Velocity metrics**: Commits per day trends
- **Wrapped stats**: Year-in-review style summary

## 🎨 React Dashboard Features

### Charts & Visualizations
1. **Circadian Pattern** (Radar Chart) - 24-hour coding rhythm
2. **Day of Week** (Bar Chart) - Weekly activity distribution  
3. **Monthly Activity** (Area Chart) - Trends with average line
4. **Language Distribution** (Treemap) - Tech stack visualization
5. **Language Evolution** (Stacked Area) - Technology timeline
6. **Sentiment** (Pie Chart) - Commit message mood analysis

### UI Components
- **Stats Cards**: 6 key metrics with icons and colors
- **Insight Cards**: 4 AI-generated personality insights
- **Top Lists**: Action verbs, languages, devoted repos
- **Header**: Username and generation timestamp
- **Glassmorphism**: Modern blur effects throughout
- **Smooth Animations**: Fade-in, slide-up, and hover effects

## 🧪 Testing

Run Python tests:
```bash
pytest tests/
pytest --cov=src tests/  # With coverage
```

Test React components:
```bash
cd web-app
npm run test
```

## 🎯 Tech Stack

### Backend
- Python 3.10+
- PyGithub (GitHub API)
- Pandas (Data processing)
- NLTK (NLP analysis)
- Plotly (Visualizations)
- Jinja2 (Templates)

### Frontend
- React 18
- Vite 5.4
- Recharts 2.10 (Charts)
- Lucide React (Icons)
- Modern CSS (Glassmorphism)

## 📝 Development

### Code Quality
```bash
# Python formatting
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

### React Development
```bash
cd web-app
npm run dev     # Start dev server
npm run build   # Production build
npm run preview # Preview production build
```

## 🚢 Deployment

### Deploy React App
```bash
cd web-app
npm run build
# Deploy dist/ folder to Vercel, Netlify, or GitHub Pages
```

### Generate Fresh Analysis
```bash
# Delete cache to force re-fetch
rm -rf data/commits_cache.json

# Run analysis
python main.py

# Copy to web app
cp output/analysis_data.json web-app/public/
```

## 🤝 Contributing

Contributions are welcome! This is a portfolio project showcasing:
- Full-stack development (Python + React)
- API integration (GitHub REST API)
- Data analysis and NLP
- Modern frontend design
- DevOps and tooling

Feel free to:
- 🐛 Open issues for bugs
- 💡 Suggest new features
- 🔧 Submit pull requests
- ⭐ Star the repository

## 📄 License

MIT License - Feel free to use this project for learning or your own portfolio!

## 🙏 Acknowledgments

- **GitHub API** via PyGithub
- **Plotly** for interactive visualizations  
- **Recharts** for React chart library
- **NLTK** team for NLP tools
- **Vite** for blazing fast dev experience
- The open-source community ❤️

## 📧 Contact

Created by **Soham** - Aspiring Full-Stack Developer

- 🔗 GitHub: [@Soham-droid-pixel](https://github.com/Soham-droid-pixel)
- 💼 Portfolio: [Coming Soon]
- 📫 Email: [Your Email]

---

<div align="center">

### ⭐ Star this repo if you found it useful!

**Made with ❤️ using Python & React**

</div>
