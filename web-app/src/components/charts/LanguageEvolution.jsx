import React from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

function LanguageEvolution({ data }) {
  const COLORS = {
    'Python': '#6366f1',
    'React/JSX': '#ec4899',
    'JavaScript': '#f59e0b',
    'Other': '#8b5cf6',
    'Markdown': '#06b6d4',
    'React/TSX': '#ef4444',
    'C++': '#10b981',
    'Config/JSON': '#84cc16'
  }
  
  const languages = data.languages || []
  
  return (
    <div className="chart-container">
      <h3 className="chart-title">🌈 Technology Stack Evolution</h3>
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data.months}>
          <defs>
            {languages.map((lang, index) => (
              <linearGradient key={lang} id={`color${lang.replace(/\//g, '')}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={COLORS[lang] || '#6366f1'} stopOpacity={0.8}/>
                <stop offset="95%" stopColor={COLORS[lang] || '#6366f1'} stopOpacity={0.1}/>
              </linearGradient>
            ))}
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis 
            dataKey="month" 
            stroke="#94a3b8"
            tick={{ fill: '#cbd5e1', fontSize: 11 }}
          />
          <YAxis 
            stroke="#94a3b8"
            tick={{ fill: '#cbd5e1' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#f1f5f9'
            }}
          />
          <Legend 
            wrapperStyle={{ color: '#cbd5e1' }}
          />
          {languages.slice(0, 8).map((lang) => (
            <Area
              key={lang}
              type="monotone"
              dataKey={lang}
              stackId="1"
              stroke={COLORS[lang] || '#6366f1'}
              fill={`url(#color${lang.replace(/\//g, '')})`}
            />
          ))}
        </AreaChart>
      </ResponsiveContainer>
      <p className="chart-subtitle">Language usage over time</p>
    </div>
  )
}

export default LanguageEvolution
