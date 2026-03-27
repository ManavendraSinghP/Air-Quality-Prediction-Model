"""
Test script for AQI Prediction API
This script tests the backend API endpoints
"""

import requests
import json
import time

# API base URL
API_BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("=== Testing Health Check Endpoint ===")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_current_aqi(location="Delhi"):
    """Test the current AQI endpoint"""
    print(f"\n=== Testing Current AQI Endpoint for {location} ===")
    try:
        response = requests.get(f"{API_BASE_URL}/current_aqi?location={location}")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200 and data.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint"""
    print("\n=== Testing Prediction Endpoint ===")

    # Sample data for prediction
    sample_data = {
        "location": "Delhi",
        "pm25": 50.2,
        "pm10": 75.5,
        "no2": 30.1,
        "so2": 15.2,
        "co": 1.2,
        "o3": 45.3
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=sample_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}")
        return response.status_code == 200 and data.get('success')
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function to run all tests"""
    print("AQI Prediction API Test Suite")
    print("=" * 40)

    # Wait a moment for server to start
    time.sleep(2)

    # Test health check
    health_ok = test_health_check()

    if health_ok:
        # Test current AQI
        current_ok = test_current_aqi()

        # Test prediction
        predict_ok = test_prediction()

        print("\n" + "=" * 40)
        print("TEST SUMMARY")
        print("=" * 40)
        print(f"Health Check: {'PASS' if health_ok else 'FAIL'}")
        print(f"Current AQI: {'PASS' if current_ok else 'FAIL'}")
        print(f"Prediction: {'PASS' if predict_ok else 'FAIL'}")

        if health_ok and current_ok and predict_ok:
            print("\nAll tests passed! The API is working correctly.")
        else:
            print("\nSome tests failed. Please check the API implementation.")
    else:
        print("\nHealth check failed. The API server may not be running.")

if __name__ == "__main__":
    main()