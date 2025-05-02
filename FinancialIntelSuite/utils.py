import pandas as pd
import streamlit as st
import base64
import io

def convert_df_to_csv(df):
    """
    Convert a DataFrame to a CSV string.
    
    Args:
        df (pd.DataFrame): DataFrame to convert
        
    Returns:
        str: CSV string
    """
    return df.to_csv(index=False)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """
    Generate a link to download a binary file.
    
    Args:
        bin_file (bytes): Binary file
        file_label (str): Label for the file
        
    Returns:
        str: HTML string with download link
    """
    bin_str = base64.b64encode(bin_file).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{file_label}">Download {file_label}</a>'
    return href

def create_download_link(object_to_download, download_filename, download_link_text):
    """
    Generate a download link for any object that can be serialized to bytes.
    
    Args:
        object_to_download: Object to download
        download_filename (str): Name of the download file
        download_link_text (str): Text for the download link
        
    Returns:
        str: HTML string with download link
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = convert_df_to_csv(object_to_download)
        
    # Try to convert to string (if not already)
    if not isinstance(object_to_download, str):
        try:
            object_to_download = str(object_to_download)
        except:
            pass
    
    try:
        # Create a bytes object for a file download
        if isinstance(object_to_download, str):
            object_to_download = object_to_download.encode()
        
        b64 = base64.b64encode(object_to_download).decode()
        
        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
        
    except Exception as e:
        return f"Error generating download link: {e}"

def format_currency(value, currency='LKR'):
    """
    Format a value as currency.
    
    Args:
        value (float): Value to format
        currency (str): Currency code
        
    Returns:
        str: Formatted currency string
    """
    try:
        # For billions, show with 'B' suffix
        if abs(value) >= 1:
            return f"{value:.2f}"
        # For millions, show with 'M' suffix
        elif abs(value) >= 0.001:
            return f"{value * 1000:.2f}M"
        else:
            return f"{value * 1000000:.2f}K"
    except:
        return str(value)

def format_percentage(value):
    """
    Format a value as percentage.
    
    Args:
        value (float): Value to format
        
    Returns:
        str: Formatted percentage string
    """
    try:
        return f"{value:.1f}%"
    except:
        return str(value)

def get_color_for_trend(value):
    """
    Get color based on trend (positive/negative).
    
    Args:
        value (float): Value determining the trend
        
    Returns:
        str: Color code
    """
    if value > 0:
        return "#10B981"  # Green
    elif value < 0:
        return "#EF4444"  # Red
    else:
        return "#6B7280"  # Gray