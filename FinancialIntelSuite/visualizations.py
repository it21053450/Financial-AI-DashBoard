import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

def plot_revenue_trend(data):
    """
    Plot the 5-year revenue trend with annotations.
    
    Args:
        data (pd.DataFrame): Filtered financial data
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure for revenue trend
    """
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Create the figure
        fig = go.Figure()
        
        # Add revenue line
        fig.add_trace(
            go.Scatter(
                x=annual_data['Year'],
                y=annual_data['Revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#0072B2', width=3),
                marker=dict(size=10),
                hovertemplate='%{x}: %{y:.2f} Billion ' + annual_data['Currency'].iloc[0] + '<extra></extra>'
            )
        )
        
        # Add annotations for year-over-year growth
        if 'Revenue_YoY_Growth' in annual_data.columns:
            for i in range(1, len(annual_data)):
                growth = annual_data['Revenue_YoY_Growth'].iloc[i]
                if not pd.isna(growth):
                    fig.add_annotation(
                        x=annual_data['Year'].iloc[i],
                        y=annual_data['Revenue'].iloc[i],
                        text=f"{growth:.1f}%",
                        showarrow=True,
                        arrowhead=4,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=0,
                        ay=-40,
                        font=dict(
                            size=12,
                            color="white" if growth < 0 else "black"
                        ),
                        bgcolor="#EF4444" if growth < 0 else "#10B981",
                        bordercolor="#636363",
                        borderwidth=1,
                        borderpad=4,
                        opacity=0.8
                    )
        
        # Customize layout
        fig.update_layout(
            title='Revenue Trend (2019-2024)',
            xaxis_title='Year',
            yaxis_title=f'Revenue (Billions {annual_data["Currency"].iloc[0]})',
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
        fig.update_xaxes(
            tickmode='array',
            tickvals=annual_data['Year'],
            ticktext=[str(year) for year in annual_data['Year']]
        )
        
        # Add a slight grid for better readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
        
    except Exception as e:
        st.error(f"Error plotting revenue trend: {e}")
        # Return a placeholder figure
        fig = go.Figure()
        fig.update_layout(
            title='Revenue Trend (Data Unavailable)',
            annotations=[dict(
                text="Error: " + str(e),
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5
            )]
        )
        return fig

def plot_cost_vs_expenses(data):
    """
    Plot cost of sales vs. operating expenses over 5 years.
    
    Args:
        data (pd.DataFrame): Filtered financial data
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure for cost comparison
    """
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Create the figure
        fig = go.Figure()
        
        # Add Cost of Sales bars
        fig.add_trace(
            go.Bar(
                x=annual_data['Year'],
                y=annual_data['Cost_of_Sales'],
                name='Cost of Sales',
                marker_color='#0072B2',
                hovertemplate='%{x}: %{y:.2f} Billion ' + annual_data['Currency'].iloc[0] + '<extra></extra>'
            )
        )
        
        # Add Operating Expenses bars
        fig.add_trace(
            go.Bar(
                x=annual_data['Year'],
                y=annual_data['Operating_Expenses'],
                name='Operating Expenses',
                marker_color='#E69F00',
                hovertemplate='%{x}: %{y:.2f} Billion ' + annual_data['Currency'].iloc[0] + '<extra></extra>'
            )
        )
        
        # Add a line for Cost-to-Revenue ratio if available
        if 'Revenue' in annual_data.columns:
            cost_ratio = (annual_data['Cost_of_Sales'] / annual_data['Revenue']) * 100
            
            # Create a secondary y-axis
            fig.add_trace(
                go.Scatter(
                    x=annual_data['Year'],
                    y=cost_ratio,
                    mode='lines+markers',
                    name='Cost-to-Revenue Ratio',
                    line=dict(color='#D55E00', width=3, dash='dot'),
                    marker=dict(size=8),
                    yaxis='y2',
                    hovertemplate='%{x}: %{y:.1f}%<extra></extra>'
                )
            )
        
        # Customize layout
        fig.update_layout(
            title='Cost of Sales vs. Operating Expenses',
            xaxis_title='Year',
            yaxis_title=f'Amount (Billions {annual_data["Currency"].iloc[0]})',
            template='plotly_white',
            barmode='group',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            yaxis2=dict(
                title='Cost-to-Revenue Ratio (%)',
                overlaying='y',
                side='right',
                showgrid=False,
                zeroline=False
            )
        )
        
        # Customize x-axis to show only years
        fig.update_xaxes(
            tickmode='array',
            tickvals=annual_data['Year'],
            ticktext=[str(year) for year in annual_data['Year']]
        )
        
        # Add a slight grid for better readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
        
    except Exception as e:
        st.error(f"Error plotting cost vs expenses: {e}")
        # Return a placeholder figure
        fig = go.Figure()
        fig.update_layout(
            title='Cost of Sales vs. Operating Expenses (Data Unavailable)',
            annotations=[dict(
                text="Error: " + str(e),
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5
            )]
        )
        return fig

def plot_gross_profit_margin(data):
    """
    Plot the 5-year gross profit margin trend with annotations.
    
    Args:
        data (pd.DataFrame): Filtered financial data
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure for gross profit margin
    """
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Calculate Gross Profit Margin if not already present
        if 'Gross_Profit_Margin' not in annual_data.columns and 'Gross_Profit' in annual_data.columns and 'Revenue' in annual_data.columns:
            annual_data['Gross_Profit_Margin'] = (annual_data['Gross_Profit'] / annual_data['Revenue']) * 100
        
        # Create the figure
        fig = go.Figure()
        
        # Add Gross Profit Margin line
        fig.add_trace(
            go.Scatter(
                x=annual_data['Year'],
                y=annual_data['Gross_Profit_Margin'],
                mode='lines+markers',
                name='Gross Profit Margin',
                line=dict(color='#009E73', width=3),
                marker=dict(size=10),
                hovertemplate='%{x}: %{y:.2f}%<extra></extra>'
            )
        )
        
        # Add industry average line
        industry_avg = 24.5  # Example value, should be calculated from real data
        fig.add_trace(
            go.Scatter(
                x=annual_data['Year'],
                y=[industry_avg] * len(annual_data),
                mode='lines',
                name='Industry Average',
                line=dict(color='gray', width=2, dash='dash'),
                hovertemplate='Industry Average: %{y:.2f}%<extra></extra>'
            )
        )
        
        # Add annotations for year-over-year change
        if 'Gross_Profit_YoY_Growth' in annual_data.columns:
            for i in range(1, len(annual_data)):
                growth = annual_data['Gross_Profit_YoY_Growth'].iloc[i]
                if not pd.isna(growth):
                    fig.add_annotation(
                        x=annual_data['Year'].iloc[i],
                        y=annual_data['Gross_Profit_Margin'].iloc[i],
                        text=f"{growth:.1f}%",
                        showarrow=True,
                        arrowhead=4,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=0,
                        ay=-40,
                        font=dict(
                            size=12,
                            color="white" if growth < 0 else "black"
                        ),
                        bgcolor="#EF4444" if growth < 0 else "#10B981",
                        bordercolor="#636363",
                        borderwidth=1,
                        borderpad=4,
                        opacity=0.8
                    )
        
        # Customize layout
        fig.update_layout(
            title='Gross Profit Margin Trend',
            xaxis_title='Year',
            yaxis_title='Gross Profit Margin (%)',
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
        fig.update_xaxes(
            tickmode='array',
            tickvals=annual_data['Year'],
            ticktext=[str(year) for year in annual_data['Year']]
        )
        
        # Add a slight grid for better readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
        
    except Exception as e:
        st.error(f"Error plotting gross profit margin: {e}")
        # Return a placeholder figure
        fig = go.Figure()
        fig.update_layout(
            title='Gross Profit Margin Trend (Data Unavailable)',
            annotations=[dict(
                text="Error: " + str(e),
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5
            )]
        )
        return fig

def plot_eps_trend(data):
    """
    Plot the 5-year Earnings Per Share (EPS) trend with tooltips.
    
    Args:
        data (pd.DataFrame): Filtered financial data
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure for EPS trend
    """
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Create the figure
        fig = go.Figure()
        
        # Add EPS line
        fig.add_trace(
            go.Scatter(
                x=annual_data['Year'],
                y=annual_data['EPS'],
                mode='lines+markers',
                name='EPS',
                line=dict(color='#CC79A7', width=3),
                marker=dict(size=10),
                hovertemplate='%{x}: %{y:.2f} ' + annual_data['Currency'].iloc[0] + '<extra></extra>'
            )
        )
        
        # Add annotations for year-over-year growth
        if 'EPS_YoY_Growth' in annual_data.columns:
            for i in range(1, len(annual_data)):
                growth = annual_data['EPS_YoY_Growth'].iloc[i]
                if not pd.isna(growth):
                    fig.add_annotation(
                        x=annual_data['Year'].iloc[i],
                        y=annual_data['EPS'].iloc[i],
                        text=f"{growth:.1f}%",
                        showarrow=True,
                        arrowhead=4,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=0,
                        ay=-40,
                        font=dict(
                            size=12,
                            color="white" if growth < 0 else "black"
                        ),
                        bgcolor="#EF4444" if growth < 0 else "#10B981",
                        bordercolor="#636363",
                        borderwidth=1,
                        borderpad=4,
                        opacity=0.8
                    )
        
        # Customize layout
        fig.update_layout(
            title='Earnings Per Share (EPS) Trend',
            xaxis_title='Year',
            yaxis_title=f'EPS ({annual_data["Currency"].iloc[0]})',
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
        fig.update_xaxes(
            tickmode='array',
            tickvals=annual_data['Year'],
            ticktext=[str(year) for year in annual_data['Year']]
        )
        
        # Add a slight grid for better readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
        
    except Exception as e:
        st.error(f"Error plotting EPS trend: {e}")
        # Return a placeholder figure
        fig = go.Figure()
        fig.update_layout(
            title='Earnings Per Share Trend (Data Unavailable)',
            annotations=[dict(
                text="Error: " + str(e),
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5
            )]
        )
        return fig

def plot_net_asset_per_share(data):
    """
    Plot the 5-year Net Asset Per Share trend with industry benchmark.
    
    Args:
        data (pd.DataFrame): Filtered financial data
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure for net asset per share
    """
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Create the figure
        fig = go.Figure()
        
        # Add Net Asset Per Share line
        fig.add_trace(
            go.Scatter(
                x=annual_data['Year'],
                y=annual_data['Net_Asset_Per_Share'],
                mode='lines+markers',
                name='Net Asset Per Share',
                line=dict(color='#56B4E9', width=3),
                marker=dict(size=10),
                hovertemplate='%{x}: %{y:.2f} ' + annual_data['Currency'].iloc[0] + '<extra></extra>'
            )
        )
        
        # Add industry benchmark line
        industry_benchmark = 85  # Example value, should be calculated from real data
        fig.add_trace(
            go.Scatter(
                x=annual_data['Year'],
                y=[industry_benchmark] * len(annual_data),
                mode='lines',
                name='Industry Benchmark',
                line=dict(color='gray', width=2, dash='dash'),
                hovertemplate='Industry Benchmark: %{y:.2f} ' + annual_data['Currency'].iloc[0] + '<extra></extra>'
            )
        )
        
        # Add annotations for year-over-year growth
        if 'NAPS_YoY_Growth' in annual_data.columns:
            for i in range(1, len(annual_data)):
                growth = annual_data['NAPS_YoY_Growth'].iloc[i]
                if not pd.isna(growth):
                    fig.add_annotation(
                        x=annual_data['Year'].iloc[i],
                        y=annual_data['Net_Asset_Per_Share'].iloc[i],
                        text=f"{growth:.1f}%",
                        showarrow=True,
                        arrowhead=4,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="#636363",
                        ax=0,
                        ay=-40,
                        font=dict(
                            size=12,
                            color="white" if growth < 0 else "black"
                        ),
                        bgcolor="#EF4444" if growth < 0 else "#10B981",
                        bordercolor="#636363",
                        borderwidth=1,
                        borderpad=4,
                        opacity=0.8
                    )
        
        # Customize layout
        fig.update_layout(
            title='Net Asset Per Share Trend',
            xaxis_title='Year',
            yaxis_title=f'Net Asset Per Share ({annual_data["Currency"].iloc[0]})',
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
        fig.update_xaxes(
            tickmode='array',
            tickvals=annual_data['Year'],
            ticktext=[str(year) for year in annual_data['Year']]
        )
        
        # Add a slight grid for better readability
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)')
        
        return fig
        
    except Exception as e:
        st.error(f"Error plotting net asset per share: {e}")
        # Return a placeholder figure
        fig = go.Figure()
        fig.update_layout(
            title='Net Asset Per Share Trend (Data Unavailable)',
            annotations=[dict(
                text="Error: " + str(e),
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5
            )]
        )
        return fig

def plot_top_shareholders(data):
    """
    Plot the top 20 shareholders over 5 years.
    
    Args:
        data (pd.DataFrame): Filtered financial data
        
    Returns:
        plotly.graph_objects.Figure: Plotly figure for top shareholders
    """
    try:
        # In this case, we need to handle the shareholders data differently
        # as it might be stored in a different format than the financial metrics
        
        # Check if shareholders data is available
        if 'shareholders_data' in data:
            shareholders_data = data['shareholders_data']
            
            # Example structure of shareholders_data:
            # List of lists, each containing dictionaries for each year
            # [ [{'name': 'Investor 1', 'ownership_percentage': 15.5}, ...], [...] ]
            
            # For simplicity, we'll use the most recent year's data
            latest_year = max(data['Year']) if 'Year' in data.columns else 2024
            latest_shareholders = None
            
            # Find the shareholders data for the latest year
            for year_data in shareholders_data:
                if year_data and year_data[0].get('Year') == latest_year:
                    latest_shareholders = year_data
                    break
            
            if latest_shareholders:
                # Sort shareholders by ownership percentage (descending)
                sorted_shareholders = sorted(latest_shareholders, key=lambda x: x['Ownership_Percentage'], reverse=True)
                
                # Take top 10 shareholders
                top_10 = sorted_shareholders[:10]
                
                # Extract names and percentages
                names = [s['Shareholder_Name'] for s in top_10]
                percentages = [s['Ownership_Percentage'] for s in top_10]
                
                # Create the figure
                fig = px.bar(
                    x=percentages,
                    y=names,
                    orientation='h',
                    labels={'x': 'Ownership Percentage (%)', 'y': 'Shareholder'},
                    title=f'Top 10 Shareholders ({latest_year})'
                )
                
                # Customize layout
                fig.update_layout(
                    template='plotly_white',
                    yaxis=dict(autorange="reversed"),  # Largest at the top
                    hoverlabel=dict(
                        bgcolor="white",
                        font_size=12,
                        font_family="Arial"
                    )
                )
                
                # Customize bars
                fig.update_traces(
                    marker_color='#0072B2',
                    hovertemplate='%{y}: %{x:.2f}%<extra></extra>'
                )
                
                return fig
            else:
                # Generate a placeholder figure when no data available
                names = [f"Major Investor {i+1}" for i in range(10)]
                percentages = [15 - i*1.2 for i in range(10)]
                
                # Create the figure
                fig = px.bar(
                    x=percentages,
                    y=names,
                    orientation='h',
                    labels={'x': 'Ownership Percentage (%)', 'y': 'Shareholder'},
                    title=f'Top 10 Shareholders ({latest_year}) - Sample Data'
                )
                
                # Customize layout
                fig.update_layout(
                    template='plotly_white',
                    yaxis=dict(autorange="reversed"),  # Largest at the top
                    annotations=[dict(
                        text="Note: Sample visualization with estimated data",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.5, y=-0.15
                    )]
                )
                
                # Customize bars
                fig.update_traces(
                    marker_color='#0072B2',
                    hovertemplate='%{y}: %{x:.2f}%<extra></extra>'
                )
                
                return fig
        else:
            # Return a placeholder figure
            fig = go.Figure()
            fig.update_layout(
                title='Top Shareholders (Data Unavailable)',
                annotations=[dict(
                    text="No shareholders data available",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.5, y=0.5
                )]
            )
            return fig
        
    except Exception as e:
        st.error(f"Error plotting top shareholders: {e}")
        # Return a placeholder figure
        fig = go.Figure()
        fig.update_layout(
            title='Top Shareholders (Data Unavailable)',
            annotations=[dict(
                text="Error: " + str(e),
                showarrow=False,
                xref="paper", yref="paper",
                x=0.5, y=0.5
            )]
        )
        return fig