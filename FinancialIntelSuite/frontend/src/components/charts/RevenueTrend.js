import React from 'react';
import { Line } from 'react-chartjs-2';

function RevenueTrend({ data }) {
  // Format data for the chart
  const chartData = {
    labels: data.years,
    datasets: [
      {
        label: 'Revenue (Billions)',
        data: data.revenue,
        fill: false,
        backgroundColor: '#0072B2',
        borderColor: '#0072B2',
        tension: 0.1,
        pointRadius: 5,
        pointHoverRadius: 7,
      },
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
        text: 'Total Revenue (5-Year Trend)',
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toFixed(2) + ' Billion';
            }
            return label;
          },
          afterLabel: function(context) {
            // Include YoY growth if available
            const index = context.dataIndex;
            if (index > 0 && data.revenue_growth && data.revenue_growth[index - 1]) {
              const growth = data.revenue_growth[index - 1];
              return `YoY Growth: ${growth > 0 ? '+' : ''}${growth.toFixed(1)}%`;
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
          text: 'Revenue (Billions)'
        },
        ticks: {
          callback: function(value) {
            return value.toFixed(1);
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
      covid: {
        type: 'line',
        xMin: 2019.5,
        xMax: 2019.5,
        borderColor: 'rgba(255, 99, 132, 0.5)',
        borderWidth: 2,
        label: {
          display: true,
          content: 'COVID-19 Impact',
          position: 'start'
        }
      }
    }
  };

  return (
    <div className="chart-container">
      <h3 className="chart-title">Total Revenue Trend</h3>
      <Line data={chartData} options={{...options, plugins: {...options.plugins, annotation: annotations}}} />
    </div>
  );
}

export default RevenueTrend;