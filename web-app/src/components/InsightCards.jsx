import React from 'react'
import './InsightCards.css'

function InsightCards({ insights }) {
  return (
    <section className="section">
      <h2 className="section-title">💡 Key Insights</h2>
      <div className="insights-grid">
        {insights.map((insight, index) => (
          <div 
            key={index}
            className="insight-card"
            style={{ animationDelay: `${index * 0.15}s` }}
          >
            <div className="insight-icon">{insight.icon}</div>
            <h3 className="insight-title">{insight.title}</h3>
            <p className="insight-description">{insight.description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export default InsightCards
