import React from 'react'
import './Header.css'

function Header({ username, generatedAt }) {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">
          <span className="emoji">🚀</span>
          GitHub Time-Lapse Analysis
        </h1>
        <p className="header-subtitle">@{username}</p>
        <p className="header-timestamp">Generated on {generatedAt}</p>
      </div>
    </header>
  )
}

export default Header
