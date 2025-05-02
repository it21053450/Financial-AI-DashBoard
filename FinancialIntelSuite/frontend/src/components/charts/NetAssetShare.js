import React from 'react';
import { Line } from 'react-chartjs-2';

function NetAssetShare({ data }) {
  // Format data for the chart
  const chartData = {
    labels: data.years,
    datasets: [
      {
        label: 'Net Asset Per Share (LKR)',
        data: data.net_asset_per_share,
        fill: false,
        backgroundColor: '#56B4E9',
        borderColor: '#56B4E9',
        tension: 0.1,
        pointRadius: 5,
        pointHoverRadius: 7,
      },
      {
        label: 'Industry Benchmark',
        data: Array(data.years.length).fill(data.industry_benchmark || 85),
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
        text: 'Net Asset Per Share Trend',
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
            if (context.datasetIndex === 0) {
              // Calculate year-over-year change
              const index = context.dataIndex;
              if (index > 0 && data.net_asset_per_share) {
                const currentValue = data.net_asset_per_share[index];
                const previousValue = data.net_asset_per_share[index - 1];
                const change = currentValue - previousValue;
                const percentChange = (change / previousValue) * 100;
                return [
                  `YoY Change: ${change > 0 ? '+' : ''}${change.toFixed(2)} LKR`,
                  `YoY Growth: ${percentChange.toFixed(1)}%`
                ];
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
          text: 'Net Asset Per Share (LKR)'
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
      <h3 className="chart-title">Net Asset Per Share</h3>
      <Line data={chartData} options={options} />
    </div>
  );
}

export default NetAssetShare;