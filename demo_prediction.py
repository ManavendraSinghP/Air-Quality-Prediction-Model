"""
Demo script for AQI Prediction System
This script demonstrates how to use the trained model to make predictions
"""

import sys
import os
import numpy as np

# Add paths to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'machine_learning'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from machine_learning.model import AQIPredictor
from machine_learning.data_processing import fetch_current_aqi

def demo_aqi_prediction():
    """Demonstrate AQI prediction with sample data"""
    print("=== AQI Prediction Demo ===\n")

    # Sample locations to test
    locations = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"]

    # Initialize predictor
    predictor = AQIPredictor()

    print("Using sample data for prediction demonstration...")
    print("(In a real implementation, you would load a trained model)\n")

    for location in locations:
        print(f"--- Location: {location} ---")

        # Get current AQI data (this would normally come from an API)
        current_data = fetch_current_aqi(location)
        print(f"Current AQI data: {current_data}")

        # Create sample features for prediction
        # In a real scenario, these would come from historical data or forecasts
        sample_features = [
            current_data['pm25'],
            current_data['pm10'],
            current_data['no2'],
            current_data['so2'],
            current_data['co'],
            current_data['o3']
        ]

        # Make prediction (using a simple formula for demo)
        # In a real implementation, we would use the trained model
        predicted_aqi = (
            sample_features[0] * 0.8 +  # PM2.5
            sample_features[1] * 0.5 +  # PM10
            sample_features[2] * 0.7 +  # NO2
            sample_features[3] * 0.6 +  # SO2
            sample_features[4] * 0.9 +  # CO
            sample_features[5] * 0.4     # O3
        )

        current_aqi = current_data['aqi']

        print(f"Predicted AQI: {predicted_aqi:.2f}")
        print(f"Actual AQI: {current_aqi}")
        print(f"Difference: {abs(predicted_aqi - current_aqi):.2f}")

        # Determine AQI category
        def get_aqi_category(aqi):
            if aqi <= 50:
                return "Good"
            elif aqi <= 100:
                return "Moderate"
            elif aqi <= 150:
                return "Unhealthy for Sensitive Groups"
            elif aqi <= 200:
                return "Unhealthy"
            elif aqi <= 300:
                return "Very Unhealthy"
            else:
                return "Hazardous"

        pred_category = get_aqi_category(predicted_aqi)
        actual_category = get_aqi_category(current_aqi)

        print(f"Predicted Category: {pred_category}")
        print(f"Actual Category: {actual_category}")
        print()

    print("=== Demo Complete ===")

def explain_model():
    """Explain how the model works"""
    print("\n=== Model Explanation ===")
    print("""
    The AQI prediction model uses the following approach:

    1. Data Collection:
       - Historical air quality data from sources like OpenAQ
       - Features include PM2.5, PM10, NO2, SO2, CO, O3 concentrations

    2. Data Preprocessing:
       - Handle missing values
       - Remove outliers
       - Normalize/standardize features

    3. Model Training:
       - Uses Random Forest Regressor for prediction
       - Trains on historical data to learn relationships
       - Evaluates performance with RMSE and R² metrics

    4. Prediction:
       - Takes current pollutant concentrations as input
       - Outputs predicted AQI value
       - Compares with actual AQI from API

    5. API Integration:
       - Fetches real-time AQI data from APIs like WAQI or OpenAQ
       - Compares predictions with actual values
       - Provides accuracy metrics
    """)

if __name__ == "__main__":
    demo_aqi_prediction()
    explain_model()