import React from 'react'
import './TopLists.css'

function TopLists({ lists }) {
  return (
    <section className="section">
      <h2 className="section-title">🏆 Top Rankings</h2>
      <div className="top-lists-grid">
        <div className="top-list-card">
          <h3 className="list-title">🔤 Top Action Verbs</h3>
          <div className="list-items">
            {lists.action_verbs.map((item, index) => (
              <div key={index} className="list-item">
                <span className="rank">#{index + 1}</span>
                <span className="item-name">{item[0]}</span>
                <span className="item-value">{item[1]}</span>
              </div>
            ))}
          </div>
        </div>
        
        <div className="top-list-card">
          <h3 className="list-title">💻 Top Languages</h3>
          <div className="list-items">
            {lists.languages.map((item, index) => (
              <div key={index} className="list-item">
                <span className="rank">#{index + 1}</span>
                <span className="item-name">{item[0]}</span>
                <span className="item-value">{item[1]} files</span>
              </div>
            ))}
          </div>
        </div>
        
        <div className="top-list-card">
          <h3 className="list-title">📦 Most Devoted Repos</h3>
          <div className="list-items">
            {lists.devoted_repos.map((item, index) => (
              <div key={index} className="list-item">
                <span className="rank">#{index + 1}</span>
                <span className="item-name">{item.name}</span>
                <span className="item-value">{item.commits} commits</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

export default TopLists
