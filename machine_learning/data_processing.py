import pandas as pd
import numpy as np
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_aqi_data(filepath):
    """
    Load AQI data from a CSV file
    Expected columns: date, pm25, pm10, no2, so2, co, o3, aqi
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"File {filepath} not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def fetch_historical_aqi(city, days=30):
    """
    Fetch historical AQI data for a city
    This is a placeholder - you would integrate with a real API
    """
    # In a real implementation, you would use an API like WAQI or OpenWeatherMap

    # Generate synthetic data for demonstration
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq='D')
    data = []

    for date in dates:
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'pm25': np.random.uniform(0, 100),
            'pm10': np.random.uniform(0, 150),
            'no2': np.random.uniform(0, 50),
            'so2': np.random.uniform(0, 20),
            'co': np.random.uniform(0, 10),
            'o3': np.random.uniform(0, 80),
            'aqi': np.random.randint(0, 200)
        })

    return pd.DataFrame(data)

def fetch_current_aqi(location):
    """
    Fetch current AQI data for a location using an API
    """
    try:
        # Example with WAQI API (you would need an API key in .env file)
        api_key = os.getenv('WAQI_API_KEY')

        if not api_key:
            # Return sample data if no API key
            print("No API key found. Returning sample data.")
            return {
                "aqi": np.random.randint(0, 150),
                "pm25": np.random.uniform(0, 50),
                "pm10": np.random.uniform(0, 80),
                "no2": np.random.uniform(0, 30),
                "so2": np.random.uniform(0, 10),
                "co": np.random.uniform(0, 5),
                "o3": np.random.uniform(0, 40)
            }

        # Uncomment below for real API usage
        # url = f"http://api.waqi.info/feed/{location}/?token={api_key}"
        # response = requests.get(url)
        # data = response.json()
        #
        # if data['status'] == 'ok':
        #     iaqi = data['data']['iaqi']
        #     return {
        #         "aqi": data['data']['aqi'],
        #         "pm25": iaqi.get('pm25', {}).get('v', 0) if 'pm25' in iaqi else 0,
        #         "pm10": iaqi.get('pm10', {}).get('v', 0) if 'pm10' in iaqi else 0,
        #         "no2": iaqi.get('no2', {}).get('v', 0) if 'no2' in iaqi else 0,
        #         "so2": iaqi.get('so2', {}).get('v', 0) if 'so2' in iaqi else 0,
        #         "co": iaqi.get('co', {}).get('v', 0) if 'co' in iaqi else 0,
        #         "o3": iaqi.get('o3', {}).get('v', 0) if 'o3' in iaqi else 0
        #     }
        # else:
        #     raise Exception(f"API Error: {data.get('data', 'Unknown error')}")

        # Placeholder return for now
        return {
            "aqi": np.random.randint(0, 150),
            "pm25": np.random.uniform(0, 50),
            "pm10": np.random.uniform(0, 80),
            "no2": np.random.uniform(0, 30),
            "so2": np.random.uniform(0, 10),
            "co": np.random.uniform(0, 5),
            "o3": np.random.uniform(0, 40)
        }

    except Exception as e:
        print(f"Error fetching current AQI: {e}")
        # Return sample data on error
        return {
            "aqi": np.random.randint(0, 150),
            "pm25": np.random.uniform(0, 50),
            "pm10": np.random.uniform(0, 80),
            "no2": np.random.uniform(0, 30),
            "so2": np.random.uniform(0, 10),
            "co": np.random.uniform(0, 5),
            "o3": np.random.uniform(0, 40)
        }

def clean_and_prepare_data(df):
    """
    Clean and prepare data for modeling
    """
    # Convert date column to datetime if it exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # Sort by date if it exists
    if 'date' in df.columns:
        df = df.sort_values('date')

    # Handle missing values
    df = df.ffill().bfill()

    # Remove rows with missing AQI values
    df = df.dropna(subset=['aqi'])

    # Remove outliers
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return df.reset_index(drop=True)