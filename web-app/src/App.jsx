import React, { useState, useEffect } from 'react'
import Header from './components/Header'
import StatsCards from './components/StatsCards'
import InsightCards from './components/InsightCards'
import CircadianChart from './components/charts/CircadianChart'
import DayOfWeekChart from './components/charts/DayOfWeekChart'
import MonthlyActivityChart from './components/charts/MonthlyActivityChart'
import LanguageDistribution from './components/charts/LanguageDistribution'
import LanguageEvolution from './components/charts/LanguageEvolution'
import SentimentChart from './components/charts/SentimentChart'
import TopLists from './components/TopLists'
import './App.css'

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Load the analysis data from JSON
    fetch('/analysis_data.json')
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`)
        }
        return res.json()
      })
      .then(data => {
        setData(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error loading data:', err)
        setError('Failed to load analysis data. Make sure analysis_data.json is in the public folder.')
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading your GitHub analysis...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>⚠️ Error</h2>
        <p>{error}</p>
        <p className="error-hint">Make sure you've run the Python analyzer first to generate the data.</p>
      </div>
    )
  }

  return (
    <div className="app">
      <Header username={data.username} generatedAt={data.generated_at} />
      
      <div className="container">
        <StatsCards stats={data.stats} />
        
        <InsightCards insights={data.insights} />
        
        <section className="section">
          <h2 className="section-title">📊 Visual Analytics</h2>
          
          <div className="chart-grid">
            <CircadianChart data={data.charts.circadian} />
            <DayOfWeekChart data={data.charts.day_of_week} />
          </div>
          
          <MonthlyActivityChart data={data.charts.monthly_activity} />
          
          <div className="chart-grid">
            <LanguageEvolution data={data.charts.language_evolution} />
            <LanguageDistribution data={data.charts.language_distribution} />
          </div>
          
          <div className="chart-grid">
            <SentimentChart data={data.charts.sentiment} />
          </div>
        </section>
        
        <TopLists lists={data.top_lists} />
      </div>
    </div>
  )
}

export default App
