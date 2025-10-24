import React from 'react'
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts'

function LanguageDistribution({ data }) {
  const COLORS = ['#6366f1', '#ec4899', '#8b5cf6', '#10b981', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16']
  
  const formattedData = data.map((item, index) => ({
    ...item,
    fill: COLORS[index % COLORS.length]
  }))
  
  const CustomizedContent = (props) => {
    const { x, y, width, height, name, value, fill } = props
    
    return (
      <g>
        <rect
          x={x}
          y={y}
          width={width}
          height={height}
          style={{
            fill,
            stroke: '#1e293b',
            strokeWidth: 2,
          }}
        />
        {width > 60 && height > 30 && (
          <>
            <text
              x={x + width / 2}
              y={y + height / 2 - 7}
              textAnchor="middle"
              fill="#fff"
              fontSize={14}
              fontWeight="bold"
            >
              {name}
            </text>
            <text
              x={x + width / 2}
              y={y + height / 2 + 10}
              textAnchor="middle"
              fill="#fff"
              fontSize={12}
            >
              {value}
            </text>
          </>
        )}
      </g>
    )
  }
  
  return (
    <div className="chart-container">
      <h3 className="chart-title">💻 Programming Language Distribution</h3>
      <ResponsiveContainer width="100%" height={400}>
        <Treemap
          data={formattedData}
          dataKey="value"
          aspectRatio={4 / 3}
          stroke="#1e293b"
          content={<CustomizedContent />}
        >
          <Tooltip 
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#f1f5f9'
            }}
          />
        </Treemap>
      </ResponsiveContainer>
      <p className="chart-subtitle">Your technology stack</p>
    </div>
  )
}

export default LanguageDistribution
