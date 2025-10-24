import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

function DayOfWeekChart({ data }) {
  // Vibrant gradient colors for each day - weekdays in blue/purple, weekends in pink
  const colors = [
    '#6366f1', // Monday - Indigo
    '#8b5cf6', // Tuesday - Purple
    '#a855f7', // Wednesday - Bright Purple
    '#c026d3', // Thursday - Fuchsia
    '#ec4899', // Friday - Pink
    '#f43f5e', // Saturday - Rose
    '#fb7185'  // Sunday - Light Rose
  ]
  
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
          backgroundColor: 'rgba(15, 23, 42, 0.95)',
          border: '2px solid #8b5cf6',
          borderRadius: '12px',
          padding: '12px 16px',
          boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)'
        }}>
          <p style={{ 
            color: '#f1f5f9', 
            fontWeight: '700',
            fontSize: '16px',
            margin: '0 0 4px 0'
          }}>
            {payload[0].payload.day}
          </p>
          <p style={{ 
            color: '#a78bfa', 
            fontWeight: '600',
            fontSize: '14px',
            margin: 0
          }}>
            Commits: <span style={{ color: '#c4b5fd' }}>{payload[0].value}</span>
          </p>
        </div>
      )
    }
    return null
  }
  
  return (
    <div className="chart-container">
      <h3 className="chart-title">📅 Day of Week Distribution</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" opacity={0.3} />
          <XAxis 
            dataKey="day" 
            stroke="#94a3b8"
            tick={{ fill: '#cbd5e1', fontWeight: 600 }}
          />
          <YAxis 
            stroke="#94a3b8"
            tick={{ fill: '#cbd5e1', fontWeight: 600 }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(139, 92, 246, 0.1)' }} />
          <Bar dataKey="commits" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={colors[index]}
                stroke={colors[index]}
                strokeWidth={2}
              />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p className="chart-subtitle">When are you most active?</p>
    </div>
  )
}

export default DayOfWeekChart
