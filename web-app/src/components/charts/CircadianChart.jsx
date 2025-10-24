import React from 'react'
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts'

function CircadianChart({ data }) {
  return (
    <div className="chart-container">
      <h3 className="chart-title">🌙 Circadian Coding Pattern</h3>
      <ResponsiveContainer width="100%" height={400}>
        <RadarChart data={data}>
          <PolarGrid stroke="#475569" />
          <PolarAngleAxis 
            dataKey="hour" 
            stroke="#94a3b8"
            tick={{ fill: '#cbd5e1', fontSize: 12 }}
          />
          <PolarRadiusAxis 
            angle={90} 
            domain={[0, 'auto']}
            stroke="#475569"
            tick={{ fill: '#94a3b8' }}
          />
          <Radar
            name="Commits"
            dataKey="commits"
            stroke="#6366f1"
            fill="#6366f1"
            fillOpacity={0.6}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#f1f5f9'
            }}
          />
        </RadarChart>
      </ResponsiveContainer>
      <p className="chart-subtitle">When do you code during the day?</p>
    </div>
  )
}

export default CircadianChart
