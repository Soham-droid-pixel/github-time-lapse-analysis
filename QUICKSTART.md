# 🚀 Quick Start Guide - GitHub Time-Lapse Analyzer

## Prerequisites Checklist

✅ **Python 3.10+** installed  
✅ **Virtual environment** created  
✅ **GitHub Personal Access Token** ready

---

## Step-by-Step Setup

### 1. Install Dependencies

Make sure your virtual environment is activated:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Create Your `.env` File

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your favorite text editor and add:

```env
# Your GitHub Personal Access Token
GITHUB_TOKEN=ghp_YOUR_ACTUAL_TOKEN_HERE

# Your GitHub Username
GITHUB_USERNAME=your_actual_username

# Optional: Cache settings (defaults shown)
CACHE_ENABLED=true
CACHE_DAYS=7
MAX_REPOSITORIES=100
COMMITS_PER_REPO=1000
```

### 3. Generate GitHub Token

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a descriptive name: "GitHub Time-Lapse Analyzer"
4. Select scopes:
   - ✅ `repo` (for private repositories)
   - OR ✅ `public_repo` (for public repositories only)
5. Click "Generate token"
6. **IMPORTANT**: Copy the token immediately and paste it into your `.env` file

### 4. Run the Analyzer

```bash
python main.py
```

The script will:
1. 📥 Fetch your commit data from GitHub
2. 🔍 Analyze temporal patterns, commit messages, languages, and productivity
3. 📊 Generate interactive Plotly visualizations
4. 🎨 Build a beautiful HTML dashboard

### 5. View Your Report

Open the generated HTML file:
```
output/github_analysis_report.html
```

The report includes:
- 🕐 Circadian coding patterns (when you code)
- 💬 Commit message sentiment analysis
- 🌐 Programming language evolution
- 📈 Productivity metrics and streaks
- 🎯 Coding personality classification
- And much more!

---

## 🔧 Troubleshooting

### Issue: "Invalid GitHub token"
**Solution**: Make sure you've replaced `ghp_your_token_here` with your actual token in `.env`

### Issue: "No commits found"
**Solution**: 
- Verify your GitHub username is correct in `.env`
- Ensure your token has the right permissions
- Check if you have public repositories with commits

### Issue: "Rate limit exceeded"
**Solution**: 
- Wait for the rate limit to reset (usually 1 hour)
- The script will automatically wait if it detects rate limiting
- Use caching to avoid repeated API calls

### Issue: "NLTK data not found"
**Solution**: The script will automatically download NLTK data on first run. If it fails, manually download:
```python
import nltk
nltk.download('all')
```

### Issue: Import errors
**Solution**: Make sure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
```

---

## 🧪 Running Tests

Run the unit tests to verify everything works:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_utils.py -v
```

---

## 📊 Using the Cache

The first run will fetch all data from GitHub (may take a few minutes).

Subsequent runs will use cached data for faster analysis.

To force a fresh fetch:
1. Delete `data/commits_cache.json` and `data/cache_metadata.json`
2. Or set `CACHE_ENABLED=false` in `.env`

---

## 🎨 Customization

### Change Color Theme

Edit `src/config.py` and modify the `COLORS` dictionary:

```python
COLORS = {
    "primary": "#6366f1",      # Your primary color
    "secondary": "#8b5cf6",    # Your secondary color
    "accent": "#ec4899",       # Your accent color
    # ... etc
}
```

### Adjust Analysis Parameters

Edit `.env` to change:
- `MAX_REPOSITORIES`: Number of repos to analyze (default: 100)
- `COMMITS_PER_REPO`: Max commits per repo (default: 1000)
- `CACHE_DAYS`: How long to keep cache valid (default: 7)

---

## 🚀 Next Steps

1. **Share Your Report**: The HTML file is self-contained and can be:
   - Hosted on GitHub Pages
   - Added to your portfolio website
   - Shared directly with others

2. **Automate Updates**: Set up a cron job or GitHub Action to:
   - Regenerate the report weekly/monthly
   - Automatically commit and push the updated HTML

3. **Extend the Analysis**: Add your own custom analyzers in `src/analyzers/`

4. **Contribute**: Found a bug or have an improvement? Submit a PR!

---

## 📧 Need Help?

- 📖 Check the full README.md
- 🐛 Open an issue on GitHub
- 💬 Reach out on social media

Happy analyzing! 🎉
