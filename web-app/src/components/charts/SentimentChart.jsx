import React from 'react'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'

function SentimentChart({ data }) {
  const COLORS = {
    'Positive': '#10b981',
    'Neutral': '#6366f1',
    'Negative': '#ef4444'
  }
  
  return (
    <div className="chart-container">
      <h3 className="chart-title">💬 Commit Message Sentiment</h3>
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
            outerRadius={120}
            fill="#8884d8"
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#f1f5f9'
            }}
          />
          <Legend wrapperStyle={{ color: '#cbd5e1' }} />
        </PieChart>
      </ResponsiveContainer>
      <p className="chart-subtitle">Analysis of your commit messages</p>
    </div>
  )
}

export default SentimentChart
