import React, { useState, useEffect } from 'react';

function Filters({ onChange, filters }) {
  const [years, setYears] = useState(filters.years || []);
  const [industry, setIndustry] = useState(filters.industry || 'All');
  const [currency, setCurrency] = useState(filters.currency || 'LKR');

  // Available options
  const availableYears = [2019, 2020, 2021, 2022, 2023, 2024];
  const industries = ['All', 'Transportation', 'Leisure', 'Consumer Foods', 'Retail', 'Financial Services'];
  const currencies = ['LKR', 'USD'];

  useEffect(() => {
    // Initialize with default all years selected
    if (years.length === 0) {
      setYears(availableYears);
    }
  }, []);

  const handleYearChange = (e) => {
    const selectedYears = Array.from(
      e.target.selectedOptions,
      option => parseInt(option.value)
    );
    setYears(selectedYears);
    onChange({
      ...filters,
      years: selectedYears
    });
  };

  const handleIndustryChange = (e) => {
    setIndustry(e.target.value);
    onChange({
      ...filters,
      industry: e.target.value
    });
  };

  const handleCurrencyChange = (e) => {
    setCurrency(e.target.value);
    onChange({
      ...filters,
      currency: e.target.value
    });
  };

  return (
    <div className="filters-container">
      <h3>Filters</h3>
      
      <div className="filter-group">
        <label className="filter-label" htmlFor="years">Select Years:</label>
        <select 
          id="years" 
          className="filter-select" 
          multiple 
          value={years}
          onChange={handleYearChange}
        >
          {availableYears.map(year => (
            <option key={year} value={year}>{year}</option>
          ))}
        </select>
        <small className="filter-help">Hold Ctrl/Cmd to select multiple</small>
      </div>
      
      <div className="filter-group">
        <label className="filter-label" htmlFor="industry">Industry Group:</label>
        <select 
          id="industry" 
          className="filter-select"
          value={industry}
          onChange={handleIndustryChange}
        >
          {industries.map(ind => (
            <option key={ind} value={ind}>{ind}</option>
          ))}
        </select>
      </div>
      
      <div className="filter-group">
        <label className="filter-label" htmlFor="currency">Currency:</label>
        <select 
          id="currency" 
          className="filter-select"
          value={currency}
          onChange={handleCurrencyChange}
        >
          {currencies.map(curr => (
            <option key={curr} value={curr}>{curr}</option>
          ))}
        </select>
      </div>
      
      <button 
        className="apply-filters-button"
        onClick={() => onChange({ years, industry, currency })}
      >
        Apply Filters
      </button>
    </div>
  );
}

export default Filters;