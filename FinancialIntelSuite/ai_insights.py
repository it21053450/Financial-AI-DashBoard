import pandas as pd
import numpy as np
import streamlit as st

def generate_insights(data):
    """
    Generate AI-powered insights from the financial data.
    
    Args:
        data (pd.DataFrame): Processed financial data
        
    Returns:
        list: List of insight statements
    """
    insights = []
    
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Insight 1: Revenue Growth Trend
        if 'Revenue' in annual_data.columns and len(annual_data) > 1:
            revenue_trend = []
            prev_revenue = None
            
            for i, row in annual_data.iterrows():
                year = row['Year']
                revenue = row['Revenue']
                
                if prev_revenue is not None:
                    growth = ((revenue - prev_revenue) / prev_revenue) * 100
                    direction = "increased" if growth > 0 else "decreased"
                    revenue_trend.append((year, direction, abs(growth)))
                
                prev_revenue = revenue
            
            if revenue_trend:
                # Look at the last 3 years or less
                recent_trend = revenue_trend[-min(3, len(revenue_trend)):]
                
                # Check if there's a consistent trend
                directions = [t[1] for t in recent_trend]
                consistent = all(d == directions[0] for d in directions)
                
                if consistent:
                    direction = directions[0]
                    avg_growth = np.mean([t[2] for t in recent_trend])
                    years_str = ", ".join([str(t[0]) for t in recent_trend])
                    
                    insight = f"<strong>Revenue Trend:</strong> John Keells has shown a consistent {direction} revenue trend in {years_str} "
                    insight += f"with an average {'growth' if direction == 'increased' else 'decline'} rate of {avg_growth:.1f}%. "
                    
                    if direction == 'increased':
                        insight += "This indicates strong market performance and effective business strategies."
                    else:
                        insight += "This may indicate market challenges or strategic repositioning."
                    
                    insights.append(insight)
                else:
                    # Inconsistent trend
                    insight = "<strong>Revenue Volatility:</strong> John Keells has shown volatility in revenue over recent years. "
                    
                    # Check the most recent year
                    latest_trend = recent_trend[-1]
                    year, direction, growth = latest_trend
                    
                    insight += f"In {year}, revenue {direction} by {growth:.1f}% "
                    
                    if direction == 'increased':
                        insight += "which may indicate a positive shift in market conditions or successful implementation of growth strategies."
                    else:
                        insight += "which may require attention to revenue generation strategies."
                    
                    insights.append(insight)
        
        # Insight 2: Profitability Analysis
        if 'Gross_Profit_Margin' in annual_data.columns and 'Net_Profit_Margin' in annual_data.columns and len(annual_data) > 0:
            # Look at the latest year
            latest_data = annual_data.iloc[-1]
            year = latest_data['Year']
            gp_margin = latest_data['Gross_Profit_Margin']
            np_margin = latest_data['Net_Profit_Margin']
            
            # Industry benchmarks (example values)
            industry_gp = 24.5
            industry_np = 12.0
            
            insight = f"<strong>Profitability Analysis ({year}):</strong> "
            
            if gp_margin > industry_gp:
                insight += f"Gross profit margin of {gp_margin:.1f}% exceeds the industry average of {industry_gp:.1f}%, "
                insight += "indicating strong pricing power and efficient cost of goods sold management. "
            else:
                insight += f"Gross profit margin of {gp_margin:.1f}% is below the industry average of {industry_gp:.1f}%, "
                insight += "suggesting potential for improvement in pricing strategy or cost of sales management. "
            
            if np_margin > industry_np:
                insight += f"Net profit margin of {np_margin:.1f}% is above the industry benchmark of {industry_np:.1f}%, "
                insight += "demonstrating effective overall cost control and operational efficiency."
            else:
                insight += f"Net profit margin of {np_margin:.1f}% is below the industry benchmark of {industry_np:.1f}%, "
                insight += "indicating opportunities for improvement in operating expense management."
            
            insights.append(insight)
        
        # Insight 3: EPS Growth Analysis
        if 'EPS' in annual_data.columns and len(annual_data) > 1:
            # Calculate year-over-year EPS growth
            annual_data['EPS_Growth'] = annual_data['EPS'].pct_change() * 100
            
            # Look at the latest year
            latest_data = annual_data.iloc[-1]
            year = latest_data['Year']
            eps = latest_data['EPS']
            eps_growth = latest_data['EPS_Growth']
            
            if pd.notna(eps_growth):
                insight = f"<strong>Earnings Per Share ({year}):</strong> "
                
                if eps_growth > 0:
                    insight += f"John Keells recorded an EPS of {eps:.2f} LKR, a {eps_growth:.1f}% increase from the previous year. "
                    
                    if eps_growth > 15:
                        insight += "This significant growth suggests strong profitability and effective capital allocation, "
                        insight += "which may positively impact shareholder returns and investor confidence."
                    else:
                        insight += "This moderate growth indicates steady improvement in profitability, "
                        insight += "which should help maintain investor confidence."
                else:
                    insight += f"John Keells recorded an EPS of {eps:.2f} LKR, a {abs(eps_growth):.1f}% decrease from the previous year. "
                    insight += "This decline may raise concerns about profitability challenges or increased share dilution, "
                    insight += "and could impact shareholder value if the trend continues."
                
                insights.append(insight)
        
        # Insight 4: Cost Structure Analysis
        if 'Cost_of_Sales' in annual_data.columns and 'Operating_Expenses' in annual_data.columns and 'Revenue' in annual_data.columns and len(annual_data) > 1:
            # Calculate cost ratios
            annual_data['COGS_Ratio'] = (annual_data['Cost_of_Sales'] / annual_data['Revenue']) * 100
            annual_data['OpEx_Ratio'] = (annual_data['Operating_Expenses'] / annual_data['Revenue']) * 100
            
            # Look at the latest year
            latest_data = annual_data.iloc[-1]
            year = latest_data['Year']
            cogs_ratio = latest_data['COGS_Ratio']
            opex_ratio = latest_data['OpEx_Ratio']
            
            # Get the previous year for comparison
            prev_data = annual_data.iloc[-2]
            prev_cogs_ratio = prev_data['COGS_Ratio']
            prev_opex_ratio = prev_data['OpEx_Ratio']
            
            cogs_change = cogs_ratio - prev_cogs_ratio
            opex_change = opex_ratio - prev_opex_ratio
            
            insight = f"<strong>Cost Structure Analysis ({year}):</strong> "
            
            # COGS ratio analysis
            if abs(cogs_change) < 1:
                insight += f"Cost of sales remained stable at {cogs_ratio:.1f}% of revenue. "
            elif cogs_change > 0:
                insight += f"Cost of sales increased to {cogs_ratio:.1f}% of revenue (+{cogs_change:.1f} percentage points), "
                insight += "which may indicate rising input costs or pricing pressure. "
            else:
                insight += f"Cost of sales decreased to {cogs_ratio:.1f}% of revenue ({cogs_change:.1f} percentage points), "
                insight += "suggesting improved sourcing efficiency or favorable input cost trends. "
            
            # OpEx ratio analysis
            if abs(opex_change) < 1:
                insight += f"Operating expenses remained stable at {opex_ratio:.1f}% of revenue, "
                insight += "indicating consistent operational efficiency."
            elif opex_change > 0:
                insight += f"Operating expenses increased to {opex_ratio:.1f}% of revenue (+{opex_change:.1f} percentage points), "
                insight += "which may require attention to cost control measures."
            else:
                insight += f"Operating expenses decreased to {opex_ratio:.1f}% of revenue ({opex_change:.1f} percentage points), "
                insight += "reflecting successful cost optimization initiatives."
            
            insights.append(insight)
        
        # Insight 5: Net Asset Value Analysis
        if 'Net_Asset_Per_Share' in annual_data.columns and len(annual_data) > 0:
            # Look at the latest year
            latest_data = annual_data.iloc[-1]
            year = latest_data['Year']
            naps = latest_data['Net_Asset_Per_Share']
            
            # Industry benchmark (example value)
            industry_naps = 85.0
            
            insight = f"<strong>Net Asset Value Analysis ({year}):</strong> "
            
            if naps > industry_naps:
                premium = ((naps - industry_naps) / industry_naps) * 100
                insight += f"Net asset per share of {naps:.2f} LKR is {premium:.1f}% above the industry average, "
                insight += "indicating strong balance sheet health and potential undervaluation compared to peers. "
                insight += "This robust asset base provides financial stability and capacity for future growth investments."
            else:
                discount = ((industry_naps - naps) / industry_naps) * 100
                insight += f"Net asset per share of {naps:.2f} LKR is {discount:.1f}% below the industry average, "
                insight += "suggesting potential opportunities to strengthen the balance sheet. "
                insight += "Management may consider strategies to improve asset utilization or reduce liabilities to enhance shareholder value."
            
            insights.append(insight)
        
        # Return the insights
        return insights
        
    except Exception as e:
        st.error(f"Error generating insights: {e}")
        return ["Unable to generate insights due to data limitations or processing error."]

def generate_summary(data):
    """
    Generate a summarized overview of the financial data.
    
    Args:
        data (pd.DataFrame): Processed financial data
        
    Returns:
        str: HTML formatted summary text
    """
    try:
        # Filter for annual data
        annual_data = data[data['Quarter'] == 'Annual'].copy()
        annual_data = annual_data.sort_values('Year')
        
        # Get the latest year's data
        if len(annual_data) > 0:
            latest_data = annual_data.iloc[-1]
            year = latest_data['Year']
            
            # Build summary text
            summary = f"<h3>Executive Summary ({year})</h3>"
            summary += "<div style='text-align: justify; margin-bottom: 20px;'>"
            
            # Overview
            summary += "<p>John Keells Holdings PLC is one of Sri Lanka's largest conglomerates with business interests spanning transportation, leisure, consumer foods, retail, financial services, property development, and information technology. This analysis examines the company's financial performance from 2019 to 2024 with emphasis on growth trends, profitability, and shareholder value.</p>"
            
            # Financial Highlights section
            summary += "<h4>Financial Highlights</h4>"
            summary += "<ul>"
            
            if 'Revenue' in latest_data:
                revenue = latest_data['Revenue']
                summary += f"<li><strong>Revenue:</strong> {revenue:.2f} Billion {latest_data.get('Currency', 'LKR')}"
                
                if len(annual_data) > 1:
                    prev_revenue = annual_data.iloc[-2]['Revenue']
                    growth = ((revenue - prev_revenue) / prev_revenue) * 100
                    summary += f" ({growth:.1f}% {'increase' if growth >= 0 else 'decrease'} YoY)</li>"
                else:
                    summary += "</li>"
            
            if 'Net_Profit' in latest_data:
                net_profit = latest_data['Net_Profit']
                summary += f"<li><strong>Net Profit:</strong> {net_profit:.2f} Billion {latest_data.get('Currency', 'LKR')}"
                
                if len(annual_data) > 1:
                    prev_profit = annual_data.iloc[-2]['Net_Profit']
                    growth = ((net_profit - prev_profit) / prev_profit) * 100
                    summary += f" ({growth:.1f}% {'increase' if growth >= 0 else 'decrease'} YoY)</li>"
                else:
                    summary += "</li>"
            
            if 'EPS' in latest_data:
                eps = latest_data['EPS']
                summary += f"<li><strong>Earnings Per Share:</strong> {eps:.2f} {latest_data.get('Currency', 'LKR')}"
                
                if len(annual_data) > 1:
                    prev_eps = annual_data.iloc[-2]['EPS']
                    growth = ((eps - prev_eps) / prev_eps) * 100
                    summary += f" ({growth:.1f}% {'increase' if growth >= 0 else 'decrease'} YoY)</li>"
                else:
                    summary += "</li>"
            
            if 'Net_Asset_Per_Share' in latest_data:
                naps = latest_data['Net_Asset_Per_Share']
                summary += f"<li><strong>Net Asset Per Share:</strong> {naps:.2f} {latest_data.get('Currency', 'LKR')}"
                
                if len(annual_data) > 1:
                    prev_naps = annual_data.iloc[-2]['Net_Asset_Per_Share']
                    growth = ((naps - prev_naps) / prev_naps) * 100
                    summary += f" ({growth:.1f}% {'increase' if growth >= 0 else 'decrease'} YoY)</li>"
                else:
                    summary += "</li>"
            
            summary += "</ul>"
            
            # Performance Analysis section
            summary += "<h4>Performance Analysis</h4>"
            summary += "<p>"
            
            # Overall performance statement
            if 'Net_Profit' in latest_data and 'Revenue' in latest_data and len(annual_data) > 1:
                net_profit = latest_data['Net_Profit']
                prev_profit = annual_data.iloc[-2]['Net_Profit']
                profit_growth = ((net_profit - prev_profit) / prev_profit) * 100
                
                revenue = latest_data['Revenue']
                prev_revenue = annual_data.iloc[-2]['Revenue']
                revenue_growth = ((revenue - prev_revenue) / prev_revenue) * 100
                
                if profit_growth > 0 and revenue_growth > 0:
                    summary += f"John Keells demonstrated strong financial performance in {year} with both revenue and profitability showing positive growth. "
                elif profit_growth > 0 and revenue_growth <= 0:
                    summary += f"Despite revenue challenges, John Keells maintained profitability growth in {year}, indicating improved operational efficiency. "
                elif profit_growth <= 0 and revenue_growth > 0:
                    summary += f"While achieving revenue growth in {year}, John Keells experienced pressure on profit margins, suggesting increased operational costs or competitive pricing pressures. "
                else:
                    summary += f"John Keells faced challenges in {year} with declines in both revenue and profitability, potentially due to broader economic factors or industry-specific headwinds. "
            
            # Profitability metrics
            if 'Gross_Profit_Margin' in latest_data and 'Net_Profit_Margin' in latest_data:
                gp_margin = latest_data['Gross_Profit_Margin']
                np_margin = latest_data['Net_Profit_Margin']
                
                summary += f"The company recorded a gross profit margin of {gp_margin:.1f}% and net profit margin of {np_margin:.1f}%, "
                
                if len(annual_data) > 1:
                    prev_gp_margin = annual_data.iloc[-2]['Gross_Profit_Margin']
                    prev_np_margin = annual_data.iloc[-2]['Net_Profit_Margin']
                    
                    gp_change = gp_margin - prev_gp_margin
                    np_change = np_margin - prev_np_margin
                    
                    if gp_change > 0 and np_change > 0:
                        summary += "with improvements in both margin metrics indicating enhanced operational efficiency and strong cost control. "
                    elif gp_change > 0 and np_change <= 0:
                        summary += "with improved gross margins but pressure on net profit, suggesting increased operating or non-operating expenses. "
                    elif gp_change <= 0 and np_change > 0:
                        summary += "with enhanced bottom-line efficiency despite pressure on gross margins, indicating effective management of operating expenses. "
                    else:
                        summary += "with margin compression at both levels, suggesting cost pressures throughout the business. "
            
            summary += "</p>"
            
            # Outlook section
            summary += "<h4>Outlook</h4>"
            summary += "<p>"
            
            # Generate a basic outlook statement based on recent trends
            positive_indicators = 0
            negative_indicators = 0
            
            if len(annual_data) > 1:
                # Revenue trend
                if 'Revenue' in latest_data:
                    revenue = latest_data['Revenue']
                    prev_revenue = annual_data.iloc[-2]['Revenue']
                    revenue_growth = ((revenue - prev_revenue) / prev_revenue) * 100
                    
                    if revenue_growth > 0:
                        positive_indicators += 1
                    else:
                        negative_indicators += 1
                
                # EPS trend
                if 'EPS' in latest_data:
                    eps = latest_data['EPS']
                    prev_eps = annual_data.iloc[-2]['EPS']
                    eps_growth = ((eps - prev_eps) / prev_eps) * 100
                    
                    if eps_growth > 0:
                        positive_indicators += 1
                    else:
                        negative_indicators += 1
                
                # Net Asset Value trend
                if 'Net_Asset_Per_Share' in latest_data:
                    naps = latest_data['Net_Asset_Per_Share']
                    prev_naps = annual_data.iloc[-2]['Net_Asset_Per_Share']
                    naps_growth = ((naps - prev_naps) / prev_naps) * 100
                    
                    if naps_growth > 0:
                        positive_indicators += 1
                    else:
                        negative_indicators += 1
            
            # Generate outlook based on indicator count
            if positive_indicators > negative_indicators:
                summary += "Based on current trends, the outlook for John Keells remains positive with opportunities for continued growth and value creation. "
                summary += "The company's diversified business model provides resilience against sector-specific challenges, while strong financial metrics suggest capacity for strategic investments and shareholder returns. "
                summary += "Management should focus on maintaining operational efficiency and capitalizing on growth opportunities in core business segments."
            elif positive_indicators < negative_indicators:
                summary += "The outlook presents certain challenges that management will need to address in the coming periods. "
                summary += "Focus areas should include revenue growth initiatives, cost optimization, and strategic realignment to improve financial performance metrics. "
                summary += "The company's diversified business model could be leveraged to offset sector-specific headwinds while pursuing growth opportunities in stronger-performing segments."
            else:
                summary += "John Keells faces a mixed outlook with both opportunities and challenges ahead. "
                summary += "Management's ability to enhance revenue growth while maintaining cost discipline will be crucial for improving financial performance. "
                summary += "The company should leverage its market position and diverse business portfolio to navigate potential economic uncertainty while pursuing strategic growth initiatives."
            
            summary += "</p>"
            
            summary += "</div>"
            
            return summary
        else:
            return "<p>Insufficient data to generate a comprehensive summary. Please ensure financial data spanning multiple years is available for analysis.</p>"
        
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return "<p>Unable to generate summary due to data limitations or processing error.</p>"