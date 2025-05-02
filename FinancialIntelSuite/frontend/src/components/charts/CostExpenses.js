import React from 'react';
import { Bar } from 'react-chartjs-2';

function CostExpenses({ data }) {
  // Format data for the chart
  const chartData = {
    labels: data.years,
    datasets: [
      {
        label: 'Cost of Sales',
        data: data.cost_of_sales,
        backgroundColor: '#0072B2',
        stack: 'Stack 0',
      },
      {
        label: 'Operating Expenses',
        data: data.operating_expenses,
        backgroundColor: '#E69F00',
        stack: 'Stack 1',
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
        text: 'Cost of Sales vs. Operating Expenses',
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
          afterBody: function(tooltipItems) {
            const index = tooltipItems[0].dataIndex;
            if (data.cost_ratio && data.cost_ratio[index]) {
              return [`Cost-to-Revenue Ratio: ${data.cost_ratio[index].toFixed(1)}%`];
            }
            return null;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Amount (Billions)'
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
    }
  };

  return (
    <div className="chart-container">
      <h3 className="chart-title">Cost of Sales vs. Operating Expenses</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
}

export default CostExpenses;