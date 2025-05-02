import React from 'react';

function Dashboard({ children, data }) {
  return (
    <div className="dashboard">
      <div className="summary-container">
        <h2>Financial Overview</h2>
        <p className="summary-text">
          {data.summary}
        </p>
      </div>
      
      <div className="insights-container">
        <h2>AI-Generated Insights</h2>
        <ul className="insights-list">
          {data.insights && data.insights.map((insight, index) => (
            <li key={index} className="insight-item">{insight}</li>
          ))}
        </ul>
      </div>
      
      <div className="charts-container">
        {children}
      </div>
      
      <div className="forecast-container">
        <h2>Financial Forecasting</h2>
        {data.forecast ? (
          <div className="forecast-chart">
            {/* Forecast chart would be rendered here */}
          </div>
        ) : (
          <button className="forecast-button">Generate Forecast</button>
        )}
      </div>
    </div>
  );
}

export default Dashboard;