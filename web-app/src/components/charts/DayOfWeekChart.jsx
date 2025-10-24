import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

function DayOfWeekChart({ data }) {
  const colors = ['#6366f1', '#6366f1', '#6366f1', '#6366f1', '#6366f1', '#ec4899', '#ec4899']
  
  return (
    <div className="chart-container">
      <h3 className="chart-title">📅 Day of Week Distribution</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis 
            dataKey="day" 
            stroke="#94a3b8"
            tick={{ fill: '#cbd5e1' }}
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
          <Bar dataKey="commits" radius={[8, 8, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={colors[index]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <p className="chart-subtitle">When are you most active?</p>
    </div>
  )
}

export default DayOfWeekChart
