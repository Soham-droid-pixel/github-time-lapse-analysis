import React from 'react'
import './StatsCards.css'

function StatsCards({ stats }) {
  return (
    <div className="stats-grid">
      {stats.map((stat, index) => (
        <div 
          key={index}
          className="stat-card"
          style={{ animationDelay: `${index * 0.1}s` }}
        >
          <div className="stat-icon" style={{ color: stat.color }}>
            {stat.icon}
          </div>
          <div className="stat-value">{stat.value}</div>
          <div className="stat-title">{stat.title}</div>
        </div>
      ))}
    </div>
  )
}

export default StatsCards
