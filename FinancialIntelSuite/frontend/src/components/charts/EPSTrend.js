import React from 'react';
import { Line } from 'react-chartjs-2';

function EPSTrend({ data }) {
  // Format data for the chart
  const chartData = {
    labels: data.years,
    datasets: [
      {
        label: 'Earnings Per Share (LKR)',
        data: data.eps,
        fill: false,
        backgroundColor: '#CC79A7',
        borderColor: '#CC79A7',
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
        text: 'Earnings Per Share (EPS) Trend',
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += 'LKR ' + context.parsed.y.toFixed(2);
            }
            return label;
          },
          afterLabel: function(context) {
            const index = context.dataIndex;
            const labels = [];
            
            // Add net profit information if available
            if (data.net_profit && data.net_profit[index]) {
              labels.push(`Net Profit: ${data.net_profit[index].toFixed(2)} Billion`);
            }
            
            // Add YoY growth if available
            if (index > 0 && data.eps_growth && data.eps_growth[index - 1]) {
              const growth = data.eps_growth[index - 1];
              labels.push(`YoY Growth: ${growth > 0 ? '+' : ''}${growth.toFixed(1)}%`);
            }
            
            return labels;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: 'Earnings Per Share (LKR)'
        },
        ticks: {
          callback: function(value) {
            return value.toFixed(2);
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

  return (
    <div className="chart-container">
      <h3 className="chart-title">Earnings Per Share (EPS)</h3>
      <Line data={chartData} options={options} />
    </div>
  );
}

export default EPSTrend;