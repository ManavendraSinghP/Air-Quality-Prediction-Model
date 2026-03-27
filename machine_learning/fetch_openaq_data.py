import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def get_openaq_data(api_key, limit=1000, page=1):
    """
    Fetch air quality data from OpenAQ API

    Args:
        api_key (str): OpenAQ API key
        limit (int): Number of records to fetch per request (max 1000)
        page (int): Page number for pagination

    Returns:
        dict: JSON response from API
    """
    url = "https://api.openaq.org/v2/measurements"

    headers = {
        "X-API-Key": api_key
    }

    params = {
        "limit": limit,
        "page": page,
        "parameter": "pm25,pm10,no2,o3,so2,co",  # Common air quality parameters
        "has_geo": "true"  # Only get data with coordinates
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OpenAQ API: {e}")
        return None

def process_openaq_data(data):
    """
    Process OpenAQ data into a pandas DataFrame

    Args:
        data (dict): JSON data from OpenAQ API

    Returns:
        pandas.DataFrame: Processed data
    """
    if not data or 'results' not in data:
        print("No data to process")
        return pd.DataFrame()

    results = data['results']
    processed_data = []

    for record in results:
        # Extract relevant information
        row = {
            'date': record.get('date', {}).get('utc'),
            'parameter': record.get('parameter'),
            'value': record.get('value'),
            'unit': record.get('unit'),
            'location': record.get('location'),
            'city': record.get('city'),
            'country': record.get('country'),
            'coordinates_lat': record.get('coordinates', {}).get('latitude'),
            'coordinates_lon': record.get('coordinates', {}).get('longitude'),
            'sensor_name': record.get('sensor', ''),
        }
        processed_data.append(row)

    return pd.DataFrame(processed_data)

def pivot_parameters(df):
    """
    Pivot the data so each row represents a single timestamp with all parameters as columns

    Args:
        df (pandas.DataFrame): Processed OpenAQ data

    Returns:
        pandas.DataFrame: Pivoted data with parameters as columns
    """
    if df.empty:
        return df

    # Pivot the data to have parameters as columns
    pivoted = df.pivot_table(
        index=['date', 'location', 'city', 'country', 'coordinates_lat', 'coordinates_lon'],
        columns='parameter',
        values='value',
        aggfunc='first'  # Take first value if there are duplicates
    ).reset_index()

    # Flatten column names
    pivoted.columns.name = None

    return pivoted

def calculate_aqi_from_parameters(row):
    """
    Calculate AQI based on individual pollutant concentrations
    This is a simplified calculation - real AQI calculations are more complex

    Args:
        row (pandas.Series): Row with pollutant concentrations

    Returns:
        float: Estimated AQI value
    """
    # Simplified AQI calculation (for demonstration purposes)
    # Real AQI calculation follows EPA guidelines with breakpoint tables

    # Initialize AQI sub-indices for each pollutant
    aqi_values = []

    # PM2.5 (24-hour average) - Simplified calculation
    if not pd.isna(row.get('pm25')):
        pm25 = row['pm25']
        if pm25 <= 12.0:
            aqi_pm25 = (50/12) * pm25
        elif pm25 <= 35.4:
            aqi_pm25 = ((100-51)/(35.4-12.1)) * (pm25-12.1) + 51
        elif pm25 <= 55.4:
            aqi_pm25 = ((150-101)/(55.4-35.5)) * (pm25-35.5) + 101
        elif pm25 <= 150.4:
            aqi_pm25 = ((200-151)/(150.4-55.5)) * (pm25-55.5) + 151
        elif pm25 <= 250.4:
            aqi_pm25 = ((300-201)/(250.4-150.5)) * (pm25-150.5) + 201
        elif pm25 <= 350.4:
            aqi_pm25 = ((400-301)/(350.4-250.5)) * (pm25-250.5) + 301
        else:
            aqi_pm25 = ((500-401)/(500.4-350.5)) * (pm25-350.5) + 401
        aqi_values.append(aqi_pm25)

    # PM10 (24-hour average)
    if not pd.isna(row.get('pm10')):
        pm10 = row['pm10']
        if pm10 <= 54:
            aqi_pm10 = (50/54) * pm10
        elif pm10 <= 154:
            aqi_pm10 = ((100-51)/(154-55)) * (pm10-55) + 51
        elif pm10 <= 254:
            aqi_pm10 = ((150-101)/(254-155)) * (pm10-155) + 101
        elif pm10 <= 354:
            aqi_pm10 = ((200-151)/(354-255)) * (pm10-255) + 151
        elif pm10 <= 424:
            aqi_pm10 = ((300-201)/(424-355)) * (pm10-355) + 201
        elif pm10 <= 504:
            aqi_pm10 = ((400-301)/(504-425)) * (pm10-425) + 301
        else:
            aqi_pm10 = ((500-401)/(604-505)) * (pm10-505) + 401
        aqi_values.append(aqi_pm10)

    # Return maximum AQI value among pollutants (simplified approach)
    return max(aqi_values) if aqi_values else None

def main():
    # Get API key from environment variables
    api_key = os.getenv('OPENAQ_API_KEY')

    if not api_key:
        print("OPENAQ_API_KEY not found in environment variables")
        print("Please set your OpenAQ API key in the .env file")
        return

    print("Fetching data from OpenAQ API...")

    # Fetch data
    data = get_openaq_data(api_key, limit=100)

    if not data:
        print("Failed to fetch data")
        return

    print(f"Fetched {len(data.get('results', []))} records")

    # Process data
    df = process_openaq_data(data)
    print(f"Processed data shape: {df.shape}")

    if df.empty:
        print("No data to process")
        return

    # Pivot data to have parameters as columns
    pivoted_df = pivot_parameters(df)
    print(f"Pivoted data shape: {pivoted_df.shape}")

    # Calculate AQI for each row
    print("Calculating AQI values...")
    pivoted_df['aqi'] = pivoted_df.apply(calculate_aqi_from_parameters, axis=1)

    # Save to CSV
    output_file = "../data/openaq_data.csv"
    pivoted_df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

    # Display sample data
    print("\nSample data:")
    print(pivoted_df.head())

if __name__ == "__main__":
    main()