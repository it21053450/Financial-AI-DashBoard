import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import { Bar, Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

// Components
import Dashboard from './components/Dashboard';
import UploadForm from './components/UploadForm';
import Filters from './components/Filters';
import RevenueTrend from './components/charts/RevenueTrend';
import CostExpenses from './components/charts/CostExpenses';
import GPMargin from './components/charts/GPMargin';
import EPSTrend from './components/charts/EPSTrend';
import NetAssetShare from './components/charts/NetAssetShare';
import TopShareholders from './components/charts/TopShareholders';

function App() {
  const [data, setData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    years: [],
    industry: 'All',
    currency: 'LKR'
  });

  const handleFileUpload = async (files) => {
    setIsLoading(true);
    setError(null);
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append('files', files[i]);
    }
    
    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setData(response.data);
    } catch (error) {
      console.error('Error uploading files:', error);
      setError('Failed to upload files. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    // Make API call to filter data
    fetchFilteredData(newFilters);
  };

  const fetchFilteredData = async (filters) => {
    setIsLoading(true);
    try {
      const response = await axios.get('/api/filter', { params: filters });
      setData(response.data);
    } catch (error) {
      console.error('Error fetching filtered data:', error);
      setError('Failed to filter data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>John Keells Holdings PLC Financial Dashboard</h1>
      </header>
      
      <div className="dashboard-container">
        <div className="sidebar">
          <UploadForm onUpload={handleFileUpload} isLoading={isLoading} />
          <Filters onChange={handleFilterChange} filters={filters} />
        </div>
        
        <div className="main-content">
          {error && <div className="error-message">{error}</div>}
          
          {isLoading ? (
            <div className="loading">Loading data...</div>
          ) : !data ? (
            <div className="upload-prompt">
              <p>Please upload John Keells annual reports to begin analysis</p>
            </div>
          ) : (
            <Dashboard data={data}>
              <div className="chart-row">
                <RevenueTrend data={data} />
                <CostExpenses data={data} />
              </div>
              <div className="chart-row">
                <GPMargin data={data} />
                <EPSTrend data={data} />
              </div>
              <div className="chart-row">
                <NetAssetShare data={data} />
                <TopShareholders data={data} />
              </div>
            </Dashboard>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;