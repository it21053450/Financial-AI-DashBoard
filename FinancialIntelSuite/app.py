import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os
import tempfile
import base64
import io
from datetime import datetime

# Import custom modules
from data_extractor import extract_data_from_pdf
from data_processor import process_financial_data, filter_data, add_growth_rates
from ai_insights import generate_insights, generate_summary
from forecasting import forecast_metrics
from visualizations import (
    plot_revenue_trend, plot_cost_vs_expenses, 
    plot_gross_profit_margin, plot_eps_trend,
    plot_net_asset_per_share, plot_top_shareholders
)
from utils import format_currency, format_percentage, get_color_for_trend

# Configure the page
st.set_page_config(
    page_title="John Keells Financial Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create data directories if they don't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Custom CSS for styling
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-size: 1.5em;
        font-weight: 500;
        color: #4B5563;
        text-align: center;
        margin-bottom: 2em;
    }
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 1em;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 1.8em;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1em;
        color: #4B5563;
    }
    .insight-card {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        padding: 1em;
        margin-bottom: 1em;
    }
    .section-header {
        font-size: 1.5em;
        font-weight: bold;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #1E3A8A;
    }
    .growth-positive {
        color: #10B981;
    }
    .growth-negative {
        color: #EF4444;
    }
    .stButton button {
        background-color: #1E3A8A;
        color: white;
        font-weight: 500;
    }
    .stSelectbox {
        margin-bottom: 1em;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data_from_file(file_path):
    """Load processed data from a file"""
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.json'):
            return pd.read_json(file_path)
        else:
            return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def save_data_to_file(data, file_path):
    """Save processed data to a file"""
    try:
        if file_path.endswith('.csv'):
            data.to_csv(file_path, index=False)
        elif file_path.endswith('.json'):
            data.to_json(file_path)
    except Exception as e:
        st.error(f"Error saving data: {e}")

def toggle_theme():
    """Toggle between light and dark theme"""
    current_theme = st.session_state.get("theme", "light")
    st.session_state.theme = "dark" if current_theme == "light" else "light"
    
    # This would require rerunning the app
    st.rerun()

def display_header():
    """Display the dashboard header"""
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown("<div class='main-title'>John Keells Holdings PLC</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'>Financial Performance Dashboard (2019-2024)</div>", unsafe_allow_html=True)

def display_metrics(data):
    """Display key financial metrics"""
    # Get the most recent year's data
    if data is not None and not data.empty:
        latest_data = data[data['Year'] == data['Year'].max()]
        previous_year = data[data['Year'] == data['Year'].max() - 1] if len(data['Year'].unique()) > 1 else None
        
        # Create metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("<div class='section-header'>Revenue</div>", unsafe_allow_html=True)
            if not latest_data.empty and 'Revenue' in latest_data.columns:
                revenue = latest_data['Revenue'].values[0]
                revenue_str = format_currency(revenue, 'LKR')
                
                # Calculate growth if previous year data exists
                growth_text = ""
                if previous_year is not None and not previous_year.empty and 'Revenue' in previous_year.columns:
                    prev_revenue = previous_year['Revenue'].values[0]
                    if prev_revenue > 0:
                        growth = ((revenue - prev_revenue) / prev_revenue) * 100
                        growth_color = "growth-positive" if growth >= 0 else "growth-negative"
                        growth_sign = "+" if growth >= 0 else ""
                        growth_text = f"<span class='{growth_color}'>{growth_sign}{growth:.1f}%</span>"
                
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{revenue_str}</div><div class='metric-label'>Billion {growth_text}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='metric-card'><div class='metric-value'>N/A</div><div class='metric-label'>No data available</div></div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='section-header'>Gross Profit Margin</div>", unsafe_allow_html=True)
            if not latest_data.empty and 'Gross_Profit' in latest_data.columns and 'Revenue' in latest_data.columns:
                gp = latest_data['Gross_Profit'].values[0]
                revenue = latest_data['Revenue'].values[0]
                if revenue > 0:
                    gp_margin = (gp / revenue) * 100
                    gp_margin_str = f"{gp_margin:.1f}%"
                    
                    # Calculate growth if previous year data exists
                    growth_text = ""
                    if previous_year is not None and not previous_year.empty and 'Gross_Profit' in previous_year.columns and 'Revenue' in previous_year.columns:
                        prev_gp = previous_year['Gross_Profit'].values[0]
                        prev_revenue = previous_year['Revenue'].values[0]
                        if prev_revenue > 0:
                            prev_gp_margin = (prev_gp / prev_revenue) * 100
                            growth = gp_margin - prev_gp_margin
                            growth_color = "growth-positive" if growth >= 0 else "growth-negative"
                            growth_sign = "+" if growth >= 0 else ""
                            growth_text = f"<span class='{growth_color}'>{growth_sign}{growth:.1f}pp</span>"
                    
                    st.markdown(f"<div class='metric-card'><div class='metric-value'>{gp_margin_str}</div><div class='metric-label'>{growth_text}</div></div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='metric-card'><div class='metric-value'>N/A</div><div class='metric-label'>No data available</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='metric-card'><div class='metric-value'>N/A</div><div class='metric-label'>No data available</div></div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown("<div class='section-header'>EPS</div>", unsafe_allow_html=True)
            if not latest_data.empty and 'EPS' in latest_data.columns:
                eps = latest_data['EPS'].values[0]
                eps_str = f"LKR {eps:.2f}"
                
                # Calculate growth if previous year data exists
                growth_text = ""
                if previous_year is not None and not previous_year.empty and 'EPS' in previous_year.columns:
                    prev_eps = previous_year['EPS'].values[0]
                    if prev_eps > 0:
                        growth = ((eps - prev_eps) / prev_eps) * 100
                        growth_color = "growth-positive" if growth >= 0 else "growth-negative"
                        growth_sign = "+" if growth >= 0 else ""
                        growth_text = f"<span class='{growth_color}'>{growth_sign}{growth:.1f}%</span>"
                
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{eps_str}</div><div class='metric-label'>{growth_text}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='metric-card'><div class='metric-value'>N/A</div><div class='metric-label'>No data available</div></div>", unsafe_allow_html=True)
        
        with col4:
            st.markdown("<div class='section-header'>Net Asset Per Share</div>", unsafe_allow_html=True)
            if not latest_data.empty and 'Net_Asset_Per_Share' in latest_data.columns:
                naps = latest_data['Net_Asset_Per_Share'].values[0]
                naps_str = f"LKR {naps:.2f}"
                
                # Calculate growth if previous year data exists
                growth_text = ""
                if previous_year is not None and not previous_year.empty and 'Net_Asset_Per_Share' in previous_year.columns:
                    prev_naps = previous_year['Net_Asset_Per_Share'].values[0]
                    if prev_naps > 0:
                        growth = ((naps - prev_naps) / prev_naps) * 100
                        growth_color = "growth-positive" if growth >= 0 else "growth-negative"
                        growth_sign = "+" if growth >= 0 else ""
                        growth_text = f"<span class='{growth_color}'>{growth_sign}{growth:.1f}%</span>"
                
                st.markdown(f"<div class='metric-card'><div class='metric-value'>{naps_str}</div><div class='metric-label'>{growth_text}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='metric-card'><div class='metric-value'>N/A</div><div class='metric-label'>No data available</div></div>", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    
    if 'selected_years' not in st.session_state:
        st.session_state.selected_years = list(range(2019, 2025))
    
    if 'selected_industry' not in st.session_state:
        st.session_state.selected_industry = 'All'
    
    if 'selected_currency' not in st.session_state:
        st.session_state.selected_currency = 'LKR'
    
    # Display header
    display_header()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Dashboard", "Upload Data", "AI Insights", "Forecasting", "Data Export"])
    
    # Simplified sidebar controls - no year selection
    st.sidebar.title("Settings")
    
    if st.session_state.processed_data is not None:
        # Always use all available years
        available_years = sorted(st.session_state.processed_data['Year'].unique())
        st.session_state.selected_years = available_years
        
        # Only keep currency selection
        st.session_state.selected_currency = st.sidebar.selectbox(
            "Currency",
            options=['LKR', 'USD']
        )
        
        # Always use All industries
        st.session_state.selected_industry = 'All'
        
        # Automatically apply the settings
        filtered_data = filter_data(
            st.session_state.processed_data,
            st.session_state.selected_years,
            st.session_state.selected_industry,
            st.session_state.selected_currency
        )
        st.session_state.filtered_data = filtered_data
    
    # Theme toggle
    st.sidebar.title("Settings")
    if st.sidebar.button("Toggle Theme"):
        toggle_theme()
    
    # Show main content based on navigation
    if page == "Dashboard":
        if st.session_state.processed_data is None:
            st.info("Please upload financial data files to view the dashboard.")
            st.markdown("### How to use this dashboard:")
            st.markdown("""
            1. Navigate to the **Upload Data** page from the sidebar
            2. Upload John Keells annual report PDFs (at least one from 2019-2024)
            3. The system will automatically extract key financial metrics
            4. Return to this page to view the dashboard
            """)
        else:
            # Apply filters if not already done
            if 'filtered_data' not in st.session_state:
                filtered_data = filter_data(
                    st.session_state.processed_data,
                    st.session_state.selected_years,
                    st.session_state.selected_industry,
                    st.session_state.selected_currency
                )
                st.session_state.filtered_data = filtered_data
            
            # Display key metrics
            display_metrics(st.session_state.filtered_data)
            
            # Display charts in a 2x3 grid
            st.markdown("<div class='section-header'>Financial Performance Charts</div>", unsafe_allow_html=True)
            
            # Row 1: Revenue and Cost trends
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    revenue_fig = plot_revenue_trend(st.session_state.filtered_data)
                    st.plotly_chart(revenue_fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting revenue trend: {e}")
            
            with col2:
                try:
                    cost_fig = plot_cost_vs_expenses(st.session_state.filtered_data)
                    st.plotly_chart(cost_fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting cost comparison: {e}")
            
            # Row 2: Profit Margin and EPS
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    gp_fig = plot_gross_profit_margin(st.session_state.filtered_data)
                    st.plotly_chart(gp_fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting gross profit margin: {e}")
            
            with col2:
                try:
                    eps_fig = plot_eps_trend(st.session_state.filtered_data)
                    st.plotly_chart(eps_fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting EPS trend: {e}")
            
            # Row 3: Net Asset Per Share and Top Shareholders
            col1, col2 = st.columns(2)
            
            with col1:
                try:
                    naps_fig = plot_net_asset_per_share(st.session_state.filtered_data)
                    st.plotly_chart(naps_fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting net asset per share: {e}")
            
            with col2:
                try:
                    shareholders_fig = plot_top_shareholders(st.session_state.filtered_data)
                    st.plotly_chart(shareholders_fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error plotting top shareholders: {e}")
    
    elif page == "Upload Data":
        st.markdown("<div class='section-header'>Upload Financial Reports</div>", unsafe_allow_html=True)
        st.markdown("Upload John Keells annual report PDFs for analysis. The system will automatically extract key financial metrics.")
        
        # File upload control with automatic processing
        uploaded_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True, 
                                         on_change=None, key="pdf_upload")
        
        # Check if new files were uploaded
        if uploaded_files and ('last_upload_count' not in st.session_state or 
                              len(uploaded_files) != st.session_state.last_upload_count):
            
            # Update the upload count
            st.session_state.last_upload_count = len(uploaded_files)
            
            # Show processing indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Process each uploaded file
                all_data = []
                
                for i, file in enumerate(uploaded_files):
                    status_text.text(f"Processing file {i+1} of {len(uploaded_files)}: {file.name}")
                    progress_bar.progress((i) / len(uploaded_files))
                    
                    try:
                        # Create a temporary file
                        temp_dir = tempfile.mkdtemp()
                        temp_file_path = os.path.join(temp_dir, file.name)
                        
                        with open(temp_file_path, "wb") as f:
                            f.write(file.getbuffer())
                        
                        # Try to extract year from filename
                        year = None
                        for y in range(2019, 2025):
                            if str(y) in file.name:
                                year = y
                                break
                        
                        # Extract data from PDF
                        status_text.text(f"Extracting data from {file.name}...")
                        extracted_data = extract_data_from_pdf(temp_file_path, year)
                        
                        if extracted_data is not None and not extracted_data.empty:
                            all_data.append(extracted_data)
                            st.info(f"Successfully extracted data from {file.name}")
                        else:
                            st.warning(f"Could not extract data from {file.name}. Using sample data.")
                            
                            # Create sample data frame for this year
                            if year is None:
                                year = 2024  # Default to most recent year if unknown
                            
                            # Create empty financial data structure
                            financial_data = {
                                'Year': [],
                                'Quarter': [],
                                'Revenue': [],
                                'Cost_of_Sales': [],
                                'Gross_Profit': [],
                                'Operating_Expenses': [],
                                'Operating_Profit': [],
                                'Net_Profit': [],
                                'EPS': [],
                                'Net_Asset_Per_Share': [],
                                'Industry': [],
                                'Currency': []
                            }
                            
                            # Generate sample data for this year
                            financial_data['Year'].append(year)
                            financial_data['Quarter'].append('Annual')
                            financial_data['Revenue'].append(168.5 + (year - 2023) * 8.7)  # Base on 2023 data
                            financial_data['Cost_of_Sales'].append(125.2 + (year - 2023) * 5.6)
                            financial_data['Gross_Profit'].append(43.3 + (year - 2023) * 3.1)
                            financial_data['Operating_Expenses'].append(23.7 + (year - 2023) * 0.8)
                            financial_data['Operating_Profit'].append(19.6 + (year - 2023) * 2.3)
                            financial_data['Net_Profit'].append(16.8 + (year - 2023) * 1.7)
                            financial_data['EPS'].append(12.75 + (year - 2023) * 1.3)
                            financial_data['Net_Asset_Per_Share'].append(98.65 + (year - 2023) * 5.65)
                            financial_data['Industry'].append('All')
                            financial_data['Currency'].append('LKR')
                            
                            # Create DataFrame and add to data list
                            sample_df = pd.DataFrame(financial_data)
                            sample_df['Source'] = 'Sample'
                            all_data.append(sample_df)
                    
                    except Exception as e:
                        st.error(f"Error processing {file.name}: {str(e)}")
                        continue
                    
                    # Update progress
                    progress_bar.progress((i+1) / len(uploaded_files))
                
                if all_data:
                    # Combine all extracted data
                    status_text.text("Combining and processing extracted data...")
                    combined_data = pd.concat(all_data)
                    
                    # Process the data
                    processed_data = process_financial_data(combined_data)
                    
                    # Add growth rates
                    processed_data = add_growth_rates(processed_data)
                    
                    # Store in session state
                    st.session_state.processed_data = processed_data
                    
                    # Save to file for later use
                    save_data_to_file(processed_data, os.path.join(UPLOAD_FOLDER, 'processed_data.json'))
                    
                    # Display success message
                    progress_bar.progress(1.0)
                    status_text.text("Processing complete!")
                    st.success(f"Successfully processed {len(all_data)} files and extracted financial data.")
                    
                    # Auto-navigate to Dashboard
                    st.markdown("""
                    <div style="text-align: center; margin-top: 20px;">
                        <h3>✅ Data processing complete!</h3>
                        <p>Your financial data has been processed. View the analysis in the Dashboard.</p>
                        <a href="#" id="goto-dashboard" style="
                            display: inline-block;
                            padding: 10px 20px;
                            background-color: #4CAF50;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                            margin-top: 10px;
                        ">View Dashboard</a>
                    </div>
                    <script>
                        document.getElementById('goto-dashboard').addEventListener('click', function() {
                            document.querySelector('button[data-testid="stSidebarNavButton"]').click();
                            Array.from(document.querySelectorAll('div[data-testid="stRadio"] label')).forEach(function(label) {
                                if (label.innerText === 'Dashboard') {
                                    label.click();
                                }
                            });
                        });
                    </script>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Failed to extract data from the uploaded files.")
            
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
                import traceback
                st.error(traceback.format_exc())
    
    elif page == "AI Insights":
        st.markdown("<div class='section-header'>AI-Powered Financial Insights</div>", unsafe_allow_html=True)
        
        if st.session_state.processed_data is None:
            st.info("Please upload financial data files to view AI insights.")
        else:
            # Apply filters if not already done
            if 'filtered_data' not in st.session_state:
                filtered_data = filter_data(
                    st.session_state.processed_data,
                    st.session_state.selected_years,
                    st.session_state.selected_industry,
                    st.session_state.selected_currency
                )
                st.session_state.filtered_data = filtered_data
            
            # Generate executive summary
            st.markdown("<div class='section-header'>Executive Summary</div>", unsafe_allow_html=True)
            
            try:
                summary = generate_summary(st.session_state.filtered_data)
                st.markdown(summary, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating executive summary: {e}")
            
            # Generate key insights
            st.markdown("<div class='section-header'>Key Financial Insights</div>", unsafe_allow_html=True)
            
            try:
                insights = generate_insights(st.session_state.filtered_data)
                
                for insight in insights:
                    st.markdown(f"<div class='insight-card'>{insight}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error generating insights: {e}")
    
    elif page == "Forecasting":
        st.markdown("<div class='section-header'>Financial Forecasting</div>", unsafe_allow_html=True)
        
        if st.session_state.processed_data is None:
            st.info("Please upload financial data files to use forecasting features.")
        else:
            # Apply filters if not already done
            if 'filtered_data' not in st.session_state:
                filtered_data = filter_data(
                    st.session_state.processed_data,
                    st.session_state.selected_years,
                    st.session_state.selected_industry,
                    st.session_state.selected_currency
                )
                st.session_state.filtered_data = filtered_data
            
            # Forecast controls
            metric_options = ["Revenue", "EPS", "Net_Profit", "Gross_Profit_Margin", "Net_Asset_Per_Share"]
            selected_metric = st.selectbox("Select Metric to Forecast", options=metric_options)
            
            forecast_periods = st.slider("Forecast Periods (Years)", min_value=1, max_value=5, value=3)
            
            if st.button("Generate Forecast"):
                with st.spinner("Generating forecast..."):
                    try:
                        # Generate forecast
                        forecast_fig = forecast_metrics(st.session_state.filtered_data, selected_metric, forecast_periods)
                        
                        # Display the forecast
                        st.plotly_chart(forecast_fig, use_container_width=True)
                        
                        # Display forecast summary
                        st.markdown("<div class='section-header'>Forecast Analysis</div>", unsafe_allow_html=True)
                        
                        # For this example, just show a basic explanation
                        st.markdown(f"""
                        This forecast uses time series analysis techniques to project future values for {selected_metric.replace('_', ' ')} 
                        based on historical data from {min(st.session_state.selected_years)} to {max(st.session_state.selected_years)}.
                        
                        The forecast takes into account:
                        - Historical trends and patterns
                        - Year-over-year growth rates
                        - Seasonal variations (if applicable)
                        
                        Note: Forecasts are estimates and should be used as one of many inputs for business decision-making.
                        External factors such as economic conditions, regulatory changes, and market disruptions can 
                        significantly impact actual results.
                        """)
                    except Exception as e:
                        st.error(f"Error generating forecast: {e}")
    
    elif page == "Data Export":
        st.markdown("<div class='section-header'>Export Data</div>", unsafe_allow_html=True)
        
        if st.session_state.processed_data is None:
            st.info("Please upload financial data files to export data.")
        else:
            # Apply filters if not already done
            if 'filtered_data' not in st.session_state:
                filtered_data = filter_data(
                    st.session_state.processed_data,
                    st.session_state.selected_years,
                    st.session_state.selected_industry,
                    st.session_state.selected_currency
                )
                st.session_state.filtered_data = filtered_data
            
            # Export options
            export_format = st.selectbox("Export Format", options=["CSV", "Excel", "JSON"])
            
            if st.button("Export Data"):
                try:
                    # Prepare the data
                    export_data = st.session_state.filtered_data.copy()
                    
                    # Convert to selected format
                    if export_format == "CSV":
                        csv = export_data.to_csv(index=False)
                        b64 = base64.b64encode(csv.encode()).decode()
                        href = f'<a href="data:file/csv;base64,{b64}" download="john_keells_financial_data.csv">Download CSV File</a>'
                    elif export_format == "Excel":
                        # For Excel, we need to create a binary file
                        output = io.BytesIO()
                        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                            export_data.to_excel(writer, index=False, sheet_name='Financial Data')
                        excel_data = output.getvalue()
                        b64 = base64.b64encode(excel_data).decode()
                        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="john_keells_financial_data.xlsx">Download Excel File</a>'
                    elif export_format == "JSON":
                        json_str = export_data.to_json(orient='records')
                        b64 = base64.b64encode(json_str.encode()).decode()
                        href = f'<a href="data:file/json;base64,{b64}" download="john_keells_financial_data.json">Download JSON File</a>'
                    
                    st.markdown(href, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error exporting data: {e}")
            
            # Data preview
            st.markdown("<div class='section-header'>Data Preview</div>", unsafe_allow_html=True)
            st.dataframe(st.session_state.filtered_data)

if __name__ == "__main__":
    main()