from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
import pandas as pd
import json
from werkzeug.utils import secure_filename

from data_extractor import extract_data_from_pdf
from data_processor import process_financial_data, filter_data
from ai_insights import generate_insights, generate_summary
from forecasting import forecast_metrics

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400
    
    all_data = []
    extracted_years = []
    errors = []
    
    for uploaded_file in files:
        temp_dir = tempfile.mkdtemp()
        filename = secure_filename(uploaded_file.filename)
        temp_file_path = os.path.join(temp_dir, filename)
        
        uploaded_file.save(temp_file_path)
        
        # Determine year from filename or content
        year = None
        
        # First try to extract year from filename
        for y in range(2019, 2025):
            if str(y) in filename:
                year = y
                break
                
        # If year not found in filename, attempt to extract from PDF content
        if year is None:
            try:
                # Open the PDF and check first few pages for year mention
                import PyPDF2
                import re
                
                with open(temp_file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    
                    # Check first 5 pages or all pages if less than 5
                    max_pages = min(5, len(pdf_reader.pages))
                    
                    for page_num in range(max_pages):
                        page_text = pdf_reader.pages[page_num].extract_text()
                        
                        # Look for year patterns like "Annual Report 2023" or "Financial Year 2022/23"
                        year_patterns = [
                            r'Annual Report[\s\n]*(\d{4})',
                            r'Financial Year[\s\n]*(\d{4})',
                            r'Financial Year[\s\n]*(\d{4})/\d{2}',
                            r'Financial Statement[\s\n]*(\d{4})',
                            r'Year End(?:ed)?[\s\n]*(?:March|December|June)[\s\n]*(\d{4})'
                        ]
                        
                        for pattern in year_patterns:
                            match = re.search(pattern, page_text)
                            if match:
                                year_str = match.group(1)
                                year = int(year_str)
                                if 2019 <= year <= 2024:
                                    break
                        
                        if year is not None:
                            break
            except Exception as e:
                errors.append(f"Error extracting year from PDF content: {str(e)}")
        
        if year:
            try:
                extracted_data = extract_data_from_pdf(temp_file_path, year)
                if extracted_data is not None and not extracted_data.empty:
                    all_data.append(extracted_data)
                    extracted_years.append(year)
                else:
                    errors.append(f"Failed to extract data from {filename}")
            except Exception as e:
                errors.append(f"Error processing {filename}: {str(e)}")
        else:
            errors.append(f"Could not determine year for {filename}")
    
    if all_data:
        try:
            # Concatenate all extracted data
            combined_data = pd.concat(all_data)
            
            # Process the data
            processed_data = process_financial_data(combined_data)
            
            # Format data for frontend
            formatted_data = format_data_for_frontend(processed_data)
            
            # Generate insights
            insights = generate_insights(processed_data)
            
            # Generate summary
            summary = generate_summary(processed_data)
            
            # Add insights and summary to response
            formatted_data['insights'] = insights
            formatted_data['summary'] = summary
            
            # Add any errors that occurred
            if errors:
                formatted_data['warnings'] = errors
            
            return jsonify(formatted_data)
            
        except Exception as e:
            errors.append(f"Error processing combined data: {str(e)}")
            return jsonify({'error': 'Error processing data', 'details': str(e), 'warnings': errors}), 500
    else:
        return jsonify({'error': 'No valid data extracted from uploaded files', 'warnings': errors}), 400

@app.route('/api/filter', methods=['GET'])
def filter_data_api():
    # Get filter parameters
    years = request.args.getlist('years[]')
    years = [int(year) for year in years] if years else []
    
    industry = request.args.get('industry', 'All')
    currency = request.args.get('currency', 'LKR')
    
    # Read stored data (in a real application, this would be from a database)
    try:
        # For demo purposes, we'll retrieve the data from a JSON file
        with open(os.path.join(UPLOAD_FOLDER, 'processed_data.json'), 'r') as f:
            processed_data = pd.read_json(f.read())
            
        # Apply filters
        filtered_data = filter_data(processed_data, years, industry, currency)
        
        # Format data for frontend
        formatted_data = format_data_for_frontend(filtered_data)
        
        # Generate insights for filtered data
        insights = generate_insights(filtered_data)
        formatted_data['insights'] = insights
        
        # Generate summary for filtered data
        summary = generate_summary(filtered_data)
        formatted_data['summary'] = summary
        
        return jsonify(formatted_data)
        
    except Exception as e:
        return jsonify({'error': 'Error filtering data', 'details': str(e)}), 500

@app.route('/api/forecast', methods=['POST'])
def forecast_api():
    try:
        # Get parameters from request
        data = request.json
        metric = data.get('metric', 'Revenue')
        periods = data.get('periods', 4)
        
        # In a real app, we would retrieve the data from a database
        with open(os.path.join(UPLOAD_FOLDER, 'processed_data.json'), 'r') as f:
            processed_data = pd.read_json(f.read())
        
        # Apply any filters if provided
        years = data.get('years', [])
        years = [int(year) for year in years] if years else []
        industry = data.get('industry', 'All')
        currency = data.get('currency', 'LKR')
        
        if years or industry != 'All' or currency != 'LKR':
            processed_data = filter_data(processed_data, years, industry, currency)
        
        # Generate forecast
        forecast_fig = forecast_metrics(processed_data, metric, periods)
        
        # In a real app, we would convert the figure to JSON or image
        # For simplicity, we'll just return success
        return jsonify({'success': True, 'message': 'Forecast generated successfully'})
        
    except Exception as e:
        return jsonify({'error': 'Error generating forecast', 'details': str(e)}), 500

def format_data_for_frontend(data):
    """
    Format the processed data for the frontend.
    
    Args:
        data (pd.DataFrame): Processed financial data
        
    Returns:
        dict: Formatted data for frontend
    """
    # Filter for annual data
    annual_data = data[data['Quarter'] == 'Annual'].copy()
    annual_data = annual_data.sort_values('Year')
    
    # Basic structure
    formatted_data = {
        'years': annual_data['Year'].tolist(),
        'revenue': annual_data['Revenue'].tolist() if 'Revenue' in annual_data.columns else [],
        'cost_of_sales': annual_data['Cost_of_Sales'].tolist() if 'Cost_of_Sales' in annual_data.columns else [],
        'operating_expenses': annual_data['Operating_Expenses'].tolist() if 'Operating_Expenses' in annual_data.columns else [],
        'gross_profit': annual_data['Gross_Profit'].tolist() if 'Gross_Profit' in annual_data.columns else [],
        'operating_profit': annual_data['Operating_Profit'].tolist() if 'Operating_Profit' in annual_data.columns else [],
        'net_profit': annual_data['Net_Profit'].tolist() if 'Net_Profit' in annual_data.columns else [],
        'eps': annual_data['EPS'].tolist() if 'EPS' in annual_data.columns else [],
        'net_asset_per_share': annual_data['Net_Asset_Per_Share'].tolist() if 'Net_Asset_Per_Share' in annual_data.columns else [],
    }
    
    # Add growth rates if available
    if 'Revenue_YoY_Growth' in annual_data.columns:
        formatted_data['revenue_growth'] = annual_data['Revenue_YoY_Growth'].tolist()
    
    if 'EPS_YoY_Growth' in annual_data.columns:
        formatted_data['eps_growth'] = annual_data['EPS_YoY_Growth'].tolist()
    
    # Add gross profit margin
    if 'Gross_Profit_Margin' in annual_data.columns:
        formatted_data['gross_profit_margin'] = annual_data['Gross_Profit_Margin'].tolist()
    elif 'Gross_Profit' in annual_data.columns and 'Revenue' in annual_data.columns:
        formatted_data['gross_profit_margin'] = (annual_data['Gross_Profit'] / annual_data['Revenue'] * 100).tolist()
    
    # Add cost-to-revenue ratio
    if 'Cost_of_Sales' in annual_data.columns and 'Revenue' in annual_data.columns:
        formatted_data['cost_ratio'] = (annual_data['Cost_of_Sales'] / annual_data['Revenue'] * 100).tolist()
    
    # Add shareholders data if available (more complex, depends on data structure)
    if 'shareholders_data' in data:
        formatted_data['shareholders'] = data['shareholders_data']
    
    return formatted_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)