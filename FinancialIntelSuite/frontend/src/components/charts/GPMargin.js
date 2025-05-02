import React from 'react';
import { Line } from 'react-chartjs-2';

function GPMargin({ data }) {
  // Format data for the chart
  const chartData = {
    labels: data.years,
    datasets: [
      {
        label: 'Gross Profit Margin (%)',
        data: data.gross_profit_margin,
        fill: false,
        backgroundColor: '#009E73',
        borderColor: '#009E73',
        tension: 0.1,
        pointRadius: 5,
        pointHoverRadius: 7,
      },
      {
        label: 'Industry Average',
        data: Array(data.years.length).fill(data.industry_avg || 24.5),
        fill: false,
        backgroundColor: 'rgba(128, 128, 128, 0.8)',
        borderColor: 'rgba(128, 128, 128, 0.8)',
        borderDash: [5, 5],
        tension: 0,
        pointRadius: 0,
      }
    ],
  };

  // Chart options
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Gross Profit Margin Trend (5-Year)',
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toFixed(2) + '%';
            }
            return label;
          },
          afterLabel: function(context) {
            if (context.datasetIndex === 0) {
              // Calculate year-over-year change
              const index = context.dataIndex;
              if (index > 0 && data.gross_profit_margin) {
                const currentValue = data.gross_profit_margin[index];
                const previousValue = data.gross_profit_margin[index - 1];
                const change = currentValue - previousValue;
                return `YoY Change: ${change > 0 ? '+' : ''}${change.toFixed(2)} percentage points`;
              }
            }
            return null;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: 'Gross Profit Margin (%)'
        },
        ticks: {
          callback: function(value) {
            return value.toFixed(1) + '%';
          }
        }
      },
      x: {
        title: {
          display: true,
          text: 'Year'
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
    elements: {
      line: {
        borderWidth: 2
      }
    }
  };

  // Add annotations for significant events
  const annotations = {
    annotations: {
      easterAttack: {
        type: 'line',
        xMin: 2019,
        xMax: 2019,
        borderColor: 'rgba(255, 99, 132, 0.5)',
        borderWidth: 2,
        label: {
          display: true,
          content: 'Easter Sunday Attacks',
          position: 'start'
        }
      },
      taxChange: {
        type: 'line',
        xMin: 2022,
        xMax: 2022,
        borderColor: 'rgba(54, 162, 235, 0.5)',
        borderWidth: 2,
        label: {
          display: true,
          content: 'Tax Policy Changes',
          position: 'start'
        }
      }
    }
  };

  return (
    <div className="chart-container">
      <h3 className="chart-title">Gross Profit Margin</h3>
      <Line data={chartData} options={{...options, plugins: {...options.plugins, annotation: annotations}}} />
    </div>
  );
}

export default GPMargin;