import React, { useState } from 'react';
import { Bar } from 'react-chartjs-2';

function TopShareholders({ data }) {
  const [selectedYear, setSelectedYear] = useState(data.years[data.years.length - 1]);
  
  // Get data for selected year
  const yearIndex = data.years.indexOf(selectedYear);
  const yearData = data.shareholders && data.shareholders[yearIndex] ? data.shareholders[yearIndex] : [];
  
  // Sort shareholders by ownership percentage (descending)
  const sortedShareholders = [...yearData].sort((a, b) => b.ownership_percentage - a.ownership_percentage);
  
  // Take top 10 shareholders
  const top10Shareholders = sortedShareholders.slice(0, 10);

  // Format data for the chart
  const chartData = {
    labels: top10Shareholders.map(s => s.name),
    datasets: [
      {
        label: 'Ownership Percentage',
        data: top10Shareholders.map(s => s.ownership_percentage),
        backgroundColor: Array(10).fill().map((_, i) => {
          const colors = [
            '#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9',
            '#D55E00', '#F0E442', '#000000', '#0072B2', '#E69F00'
          ];
          return colors[i % colors.length];
        }),
        borderColor: 'rgba(255, 255, 255, 0.5)',
        borderWidth: 1,
      },
    ],
  };

  // Chart options
  const options = {
    indexAxis: 'y',
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: `Top 10 Shareholders (${selectedYear})`,
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = 'Ownership: ';
            if (context.parsed.x !== null) {
              label += context.parsed.x.toFixed(2) + '%';
            }
            return label;
          }
        }
      }
    },
    scales: {
      x: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Ownership Percentage (%)'
        },
        ticks: {
          callback: function(value) {
            return value.toFixed(1) + '%';
          }
        }
      },
      y: {
        title: {
          display: true,
          text: 'Shareholder'
        }
      }
    },
  };

  // Year selector handler
  const handleYearChange = (e) => {
    setSelectedYear(parseInt(e.target.value));
  };

  return (
    <div className="chart-container">
      <div className="chart-header">
        <h3 className="chart-title">Top Shareholders</h3>
        <select 
          className="year-selector" 
          value={selectedYear} 
          onChange={handleYearChange}
        >
          {data.years.map(year => (
            <option key={year} value={year}>{year}</option>
          ))}
        </select>
      </div>
      
      {yearData.length > 0 ? (
        <Bar data={chartData} options={options} />
      ) : (
        <div className="no-data-message">No shareholder data available for {selectedYear}</div>
      )}
    </div>
  );
}

export default TopShareholders;