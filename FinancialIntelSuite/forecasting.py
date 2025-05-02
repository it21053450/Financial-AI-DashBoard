import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
import streamlit as st

def forecast_metrics(data, metric, periods=4):
    """
    Forecast financial metrics using time series analysis.
    
    Args:
        data (pd.DataFrame): Processed financial data
        metric (str): Metric to forecast (e.g., 'Revenue', 'EPS')
        periods (int): Number of periods to forecast
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure with forecast
    """
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Check if we have the required metric and enough data points
        if metric not in annual_data.columns:
            raise ValueError(f"Metric '{metric}' not found in data")
        
        if len(annual_data) < 3:
            raise ValueError(f"Not enough historical data points for reliable forecasting (minimum 3 required, found {len(annual_data)})")
        
        # Prepare the time series data
        ts_data = annual_data[[metric]].copy()
        
        # Remove any NaN values
        ts_data = ts_data.dropna()
        
        if len(ts_data) < 3:
            raise ValueError(f"Not enough non-NaN data points for reliable forecasting (minimum 3 required, found {len(ts_data)})")
        
        # Convert the metric name for display
        display_metric = metric.replace('_', ' ')
        
        # Determine the best ARIMA parameters (simplified approach)
        # In a real application, you would use auto_arima or grid search
        p, d, q = 1, 1, 0  # Default ARIMA parameters
        
        try:
            # Fit ARIMA model
            model = ARIMA(ts_data[metric].values, order=(p, d, q))
            model_fit = model.fit()
            
            # Generate forecast
            forecast_result = model_fit.forecast(steps=periods)
            forecast_values = forecast_result
            
            # Calculate confidence intervals (simplified approach)
            # In a real application, use prediction_intervals from the model
            std_error = np.std(ts_data[metric].values) * 1.96  # 95% confidence interval
            lower_bound = forecast_values - std_error
            upper_bound = forecast_values + std_error
            
            # Create the forecast years
            last_year = annual_data['Year'].max()
            forecast_years = list(range(last_year + 1, last_year + periods + 1))
            
            # Create the plotting data
            historical_years = annual_data['Year'].tolist()
            historical_values = annual_data[metric].tolist()
            
            # Create the figure
            fig = go.Figure()
            
            # Add historical data
            fig.add_trace(
                go.Scatter(
                    x=historical_years,
                    y=historical_values,
                    mode='lines+markers',
                    name='Historical Data',
                    line=dict(color='#1F77B4', width=3),
                    marker=dict(size=10),
                )
            )
            
            # Add forecast
            fig.add_trace(
                go.Scatter(
                    x=forecast_years,
                    y=forecast_values,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='#FF7F0E', width=3, dash='dot'),
                    marker=dict(size=10),
                )
            )
            
            # Add confidence intervals
            fig.add_trace(
                go.Scatter(
                    x=forecast_years + forecast_years[::-1],
                    y=list(upper_bound) + list(lower_bound)[::-1],
                    fill='toself',
                    fillcolor='rgba(255, 127, 14, 0.2)',
                    line=dict(color='rgba(255, 127, 14, 0)'),
                    hoverinfo='skip',
                    showlegend=False,
                )
            )
            
            # Customize layout
            fig.update_layout(
                title=f'{display_metric} Forecast ({periods} Years)',
                xaxis_title='Year',
                yaxis_title=display_metric,
                template='plotly_white',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # Customize x-axis to show only years
            all_years = historical_years + forecast_years
            fig.update_xaxes(
                tickmode='array',
                tickvals=all_years,
                ticktext=[str(year) for year in all_years]
            )
            
            # Add a marker for the forecast start
            fig.add_shape(
                type="line",
                x0=historical_years[-1],
                y0=0,
                x1=historical_years[-1],
                y1=max(historical_values + list(upper_bound)) * 1.1,
                line=dict(
                    color="Gray",
                    width=1,
                    dash="dash",
                ),
            )
            
            fig.add_annotation(
                x=historical_years[-1],
                y=max(historical_values + list(upper_bound)) * 1.05,
                text="Forecast Start",
                showarrow=False,
                yshift=10,
            )
            
            # Add annotations for CAGR
            last_historical = historical_values[-1]
            last_forecast = forecast_values[-1]
            years_diff = forecast_years[-1] - historical_years[-1]
            
            if last_historical > 0:
                cagr = ((last_forecast / last_historical) ** (1/years_diff) - 1) * 100
                
                fig.add_annotation(
                    x=(historical_years[-1] + forecast_years[-1]) / 2,
                    y=max(historical_values + list(upper_bound)) * 0.8,
                    text=f"Projected CAGR: {cagr:.1f}%",
                    showarrow=False,
                    font=dict(
                        size=14,
                        color="black"
                    ),
                    bgcolor="white",
                    bordercolor="#FF7F0E",
                    borderwidth=2,
                    borderpad=4,
                    opacity=0.8
                )
            
            return fig
            
        except Exception as e:
            # Fall back to a simpler forecast method if ARIMA fails
            st.warning(f"Advanced forecasting model failed: {e}. Using simple trend-based forecast instead.")
            
            # Calculate average growth rate from historical data
            growth_rates = []
            for i in range(1, len(ts_data)):
                prev_value = ts_data[metric].iloc[i-1]
                curr_value = ts_data[metric].iloc[i]
                if prev_value > 0:
                    growth_rate = (curr_value / prev_value) - 1
                    growth_rates.append(growth_rate)
            
            # If we have growth rates, use the median for forecasting
            if growth_rates:
                avg_growth_rate = np.median(growth_rates)
            else:
                avg_growth_rate = 0.05  # Default 5% growth if no historical growth data
            
            # Last known value
            last_value = ts_data[metric].iloc[-1]
            
            # Generate forecast using the growth rate
            forecast_values = []
            for i in range(periods):
                next_value = last_value * (1 + avg_growth_rate)
                forecast_values.append(next_value)
                last_value = next_value
            
            # Create the forecast years
            last_year = annual_data['Year'].max()
            forecast_years = list(range(last_year + 1, last_year + periods + 1))
            
            # Create the plotting data
            historical_years = annual_data['Year'].tolist()
            historical_values = annual_data[metric].tolist()
            
            # Create the figure
            fig = go.Figure()
            
            # Add historical data
            fig.add_trace(
                go.Scatter(
                    x=historical_years,
                    y=historical_values,
                    mode='lines+markers',
                    name='Historical Data',
                    line=dict(color='#1F77B4', width=3),
                    marker=dict(size=10),
                )
            )
            
            # Add forecast
            fig.add_trace(
                go.Scatter(
                    x=forecast_years,
                    y=forecast_values,
                    mode='lines+markers',
                    name='Forecast',
                    line=dict(color='#FF7F0E', width=3, dash='dot'),
                    marker=dict(size=10),
                )
            )
            
            # Customize layout
            fig.update_layout(
                title=f'{display_metric} Forecast ({periods} Years) - Simple Growth Model',
                xaxis_title='Year',
                yaxis_title=display_metric,
                template='plotly_white',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # Customize x-axis to show only years
            all_years = historical_years + forecast_years
            fig.update_xaxes(
                tickmode='array',
                tickvals=all_years,
                ticktext=[str(year) for year in all_years]
            )
            
            # Add a marker for the forecast start
            fig.add_shape(
                type="line",
                x0=historical_years[-1],
                y0=0,
                x1=historical_years[-1],
                y1=max(historical_values + forecast_values) * 1.1,
                line=dict(
                    color="Gray",
                    width=1,
                    dash="dash",
                ),
            )
            
            fig.add_annotation(
                x=historical_years[-1],
                y=max(historical_values + forecast_values) * 1.05,
                text="Forecast Start",
                showarrow=False,
                yshift=10,
            )
            
            # Add annotation for growth rate
            fig.add_annotation(
                x=(historical_years[-1] + forecast_years[-1]) / 2,
                y=max(historical_values + forecast_values) * 0.8,
                text=f"Growth Rate: {avg_growth_rate*100:.1f}% per year",
                showarrow=False,
                font=dict(
                    size=14,
                    color="black"
                ),
                bgcolor="white",
                bordercolor="#FF7F0E",
                borderwidth=2,
                borderpad=4,
                opacity=0.8
            )
            
            return fig
            
    except Exception as e:
        st.error(f"Error forecasting {metric}: {e}")
        
        # Return a placeholder figure
        fig = go.Figure()
        fig.update_layout(
            title=f'Forecast Error - {metric}',
            annotations=[dict(
                text=f"Error: {str(e)}",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5
            )],
            template='plotly_white'
        )
        return fig