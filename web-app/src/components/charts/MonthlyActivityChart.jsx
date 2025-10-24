import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart, ReferenceLine } from 'recharts'

function MonthlyActivityChart({ data }) {
  const average = data.average || 0
  
  return (
    <div className="chart-container">
      <h3 className="chart-title">📈 Monthly Commit Activity</h3>
      <ResponsiveContainer width="100%" height={400}>
        <AreaChart data={data.months}>
          <defs>
            <linearGradient id="colorCommits" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis 
            dataKey="month" 
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
          <ReferenceLine 
            y={average} 
            stroke="#ec4899" 
            strokeDasharray="3 3"
            label={{ value: `Avg: ${Math.round(average)}`, fill: '#ec4899', position: 'right' }}
          />
          <Area
            type="monotone"
            dataKey="commits"
            stroke="#6366f1"
            strokeWidth={3}
            fillOpacity={1}
            fill="url(#colorCommits)"
          />
        </AreaChart>
      </ResponsiveContainer>
      <p className="chart-subtitle">How has your productivity evolved?</p>
    </div>
  )
}

export default MonthlyActivityChart
