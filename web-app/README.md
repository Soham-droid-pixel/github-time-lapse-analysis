# GitHub Time-Lapse Analyzer - React Web App

## 🚀 Quick Start

### 1. Generate Analysis Data
First, run the Python analyzer to generate the data:
```bash
cd ..
python main.py
```

This will create `output/analysis_data.json` that the React app needs.

### 2. Install Dependencies
```bash
npm install
```

### 3. Run Development Server
```bash
npm run dev
```

The app will automatically open in your browser at `http://localhost:3000`

### 4. Build for Production
```bash
npm run build
```

The production build will be in the `dist` folder.

## ✨ Features

- **Interactive Charts** using Recharts library
- **Responsive Design** works on mobile, tablet, and desktop
- **Modern UI** with glassmorphism effects
- **Fast Performance** powered by Vite and React 18
- **Beautiful Animations** smooth transitions and hover effects

## 📊 Available Visualizations

1. **Circadian Coding Pattern** - Radar chart showing when you code
2. **Day of Week Distribution** - Bar chart of weekly activity
3. **Monthly Activity** - Timeline of commits over months
4. **Language Distribution** - Treemap of your tech stack
5. **Language Evolution** - Stacked area chart of language usage
6. **Sentiment Analysis** - Pie chart of commit message tone
7. **Top Rankings** - Lists of most used verbs, languages, and repos

## 🛠️ Tech Stack

- React 18
- Vite
- Recharts (Chart library)
- Lucide React (Icons)
- CSS3 (Glassmorphism styling)

## 📝 Notes

- Make sure to run `python main.py` first to generate the data
- The app looks for `../output/analysis_data.json` relative to the web-app folder
- All visualizations are fully interactive with tooltips and hover effects

Enjoy exploring your GitHub coding patterns! 🎉
