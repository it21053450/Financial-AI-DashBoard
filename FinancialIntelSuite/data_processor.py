import pandas as pd
import numpy as np
import streamlit as st

def process_financial_data(raw_data):
    """
    Process raw financial data into a structured format.
    
    Args:
        raw_data (pd.DataFrame): Raw financial data
        
    Returns:
        pd.DataFrame: Processed financial data
    """
    try:
        # Make a copy to avoid modifying the original
        processed_data = raw_data.copy()
        
        # Convert Year to integer if it's not already
        if 'Year' in processed_data.columns:
            processed_data['Year'] = processed_data['Year'].astype(int)
        
        # Ensure all numeric columns are float
        numeric_columns = [
            'Revenue', 'Cost_of_Sales', 'Gross_Profit', 'Operating_Expenses',
            'Operating_Profit', 'Net_Profit', 'EPS', 'Net_Asset_Per_Share'
        ]
        
        for col in numeric_columns:
            if col in processed_data.columns:
                processed_data[col] = pd.to_numeric(processed_data[col], errors='coerce')
        
        # Calculate Gross Profit if not present but Revenue and Cost_of_Sales are
        if 'Gross_Profit' not in processed_data.columns and 'Revenue' in processed_data.columns and 'Cost_of_Sales' in processed_data.columns:
            processed_data['Gross_Profit'] = processed_data['Revenue'] - processed_data['Cost_of_Sales']
        
        # Calculate Operating Profit if not present but Gross_Profit and Operating_Expenses are
        if 'Operating_Profit' not in processed_data.columns and 'Gross_Profit' in processed_data.columns and 'Operating_Expenses' in processed_data.columns:
            processed_data['Operating_Profit'] = processed_data['Gross_Profit'] - processed_data['Operating_Expenses']
        
        # Calculate Gross Profit Margin
        if 'Gross_Profit' in processed_data.columns and 'Revenue' in processed_data.columns:
            processed_data['Gross_Profit_Margin'] = (processed_data['Gross_Profit'] / processed_data['Revenue']) * 100
        
        # Calculate Operating Profit Margin
        if 'Operating_Profit' in processed_data.columns and 'Revenue' in processed_data.columns:
            processed_data['Operating_Profit_Margin'] = (processed_data['Operating_Profit'] / processed_data['Revenue']) * 100
        
        # Calculate Net Profit Margin
        if 'Net_Profit' in processed_data.columns and 'Revenue' in processed_data.columns:
            processed_data['Net_Profit_Margin'] = (processed_data['Net_Profit'] / processed_data['Revenue']) * 100
        
        # Add growth rates for key metrics
        processed_data = add_growth_rates(processed_data)
        
        return processed_data
        
    except Exception as e:
        st.error(f"Error processing financial data: {e}")
        return raw_data

def add_growth_rates(data):
    """Add year-over-year growth rates for key metrics"""
    try:
        # Make a copy to avoid modifying the original
        data_with_growth = data.copy()
        
        # Sort by Year to ensure correct calculation
        if 'Year' in data_with_growth.columns:
            data_with_growth = data_with_growth.sort_values('Year')
        
        # Metrics to calculate growth rates for
        growth_metrics = {
            'Revenue': 'Revenue_YoY_Growth',
            'Gross_Profit': 'Gross_Profit_YoY_Growth',
            'Operating_Profit': 'Operating_Profit_YoY_Growth',
            'Net_Profit': 'Net_Profit_YoY_Growth',
            'EPS': 'EPS_YoY_Growth',
            'Net_Asset_Per_Share': 'NAPS_YoY_Growth'
        }
        
        # Calculate growth rates for each metric
        for metric, growth_col in growth_metrics.items():
            if metric in data_with_growth.columns:
                # Create a new column for the growth rate
                data_with_growth[growth_col] = np.nan
                
                # Group by Industry and Quarter to calculate growth within each group
                if 'Industry' in data_with_growth.columns and 'Quarter' in data_with_growth.columns:
                    for (industry, quarter), group in data_with_growth.groupby(['Industry', 'Quarter']):
                        # Sort by Year within each group
                        group = group.sort_values('Year')
                        
                        # Calculate growth rates
                        group_indices = group.index
                        for i in range(1, len(group_indices)):
                            curr_value = group[metric].iloc[i]
                            prev_value = group[metric].iloc[i-1]
                            
                            if prev_value != 0 and not pd.isna(prev_value) and not pd.isna(curr_value):
                                growth_rate = ((curr_value - prev_value) / prev_value) * 100
                                data_with_growth.at[group_indices[i], growth_col] = growth_rate
                else:
                    # If no grouping columns, calculate growth rates for all data
                    for i in range(1, len(data_with_growth)):
                        curr_value = data_with_growth[metric].iloc[i]
                        prev_value = data_with_growth[metric].iloc[i-1]
                        
                        if prev_value != 0 and not pd.isna(prev_value) and not pd.isna(curr_value):
                            growth_rate = ((curr_value - prev_value) / prev_value) * 100
                            data_with_growth.at[data_with_growth.index[i], growth_col] = growth_rate
        
        return data_with_growth
        
    except Exception as e:
        st.warning(f"Error calculating growth rates: {e}")
        return data

def filter_data(data, selected_years, selected_industry, selected_currency):
    """
    Filter the financial data based on user selections.
    
    Args:
        data (pd.DataFrame): Processed financial data
        selected_years (list): List of selected years
        selected_industry (str): Selected industry or 'All'
        selected_currency (str): Selected currency ('LKR' or 'USD')
        
    Returns:
        pd.DataFrame: Filtered financial data
    """
    try:
        # Start with a copy of the data
        filtered_data = data.copy()
        
        # Filter by Year
        if selected_years and 'Year' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['Year'].isin(selected_years)]
        
        # Filter by Industry
        if selected_industry != 'All' and 'Industry' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['Industry'] == selected_industry]
        
        # Convert currency if needed
        if selected_currency == 'USD' and 'Currency' in filtered_data.columns and (filtered_data['Currency'] == 'LKR').any():
            # Define conversion rate (example: 1 USD = 200 LKR)
            # In a real application, this would use an API or database to get current rates
            usd_to_lkr_rate = 200.0
            
            # Convert numeric columns
            numeric_columns = [
                'Revenue', 'Cost_of_Sales', 'Gross_Profit', 'Operating_Expenses',
                'Operating_Profit', 'Net_Profit', 'EPS', 'Net_Asset_Per_Share'
            ]
            
            for col in numeric_columns:
                if col in filtered_data.columns:
                    # Only convert values marked as LKR
                    lkr_mask = filtered_data['Currency'] == 'LKR'
                    filtered_data.loc[lkr_mask, col] = filtered_data.loc[lkr_mask, col] / usd_to_lkr_rate
            
            # Update currency column
            filtered_data['Currency'] = selected_currency
        
        return filtered_data
        
    except Exception as e:
        st.error(f"Error filtering data: {e}")
        return data