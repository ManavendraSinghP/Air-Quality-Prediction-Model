from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import pickle
import pandas as pd
import requests
import numpy as np

# Initialize FastAPI app
app = FastAPI(title="Delhi AQI Prediction API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model
try:
    with open('xgboost_aqi_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully")
except FileNotFoundError:
    print("Warning: Model file 'xgboost_aqi_model.pkl' not found. Will train model on first prediction.")
    model = None
except Exception as e:
    raise Exception(f"Error loading model: {e}")

# Define request model
class AQIPredictionRequest(BaseModel):
    token: str
    location: str

class ManualPredictionRequest(BaseModel):
    pm25: float
    pm10: float
    so2: float
    no2: float
    co: float
    o3: float

class PredictionResponse(BaseModel):
    station_names: list
    predicted_aqi: list
    actual_aqi: list
    pollutants: list

# Predefined list of Delhi monitoring stations
DELHI_STATIONS = [
    "Anand Vihar", "Punjabi Bagh", "ITO", "RK Puram", "Okhla",
    "Wazirpur", "Siri Fort", "Dwarka", "Najafgarh", "Bawana",
    "Chandni Chowk", "Mandir Marg", "Burari", "Jahangirpuri",
    "Ashok Vihar", "Shadipur", "Aya Nagar", "Vasundhara", "Sector 62",
    "Greater Kailash", "Nehru Place", "Lodhi Road", "Kirti Nagar"
]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Delhi AQI Prediction API is running"}

@app.get("/stations")
async def get_stations():
    """Get list of available Delhi monitoring stations"""
    return {"stations": DELHI_STATIONS}

@app.post("/predict", response_model=PredictionResponse)
async def predict_aqi(request: AQIPredictionRequest):
    """
    Predict AQI based on WAQI API data

    Args:
        token: WAQI API token
        location: Station name to fetch data for

    Returns:
        PredictionResponse with station names, predicted AQI, actual AQI, and pollutant values
    """
    TOKEN = request.token
    location = request.location

    try:
        # Search for the specific station
        search_url = f"https://api.waqi.info/search/?token={TOKEN}&keyword={location}"
        search_response = requests.get(search_url, timeout=10)
        search_response.raise_for_status()
        search_data = search_response.json()

        if search_data['status'] != 'ok':
            raise HTTPException(status_code=400, detail=f"Error searching station: {search_data}")

        if not search_data['data']:
            raise HTTPException(status_code=404, detail=f"No station found for keyword: {location}")

        # Find the exact matching station
        station_info = None
        for station in search_data['data']:
            if station['station']['name'].lower() == location.lower():
                station_info = station
                break

        # If exact match not found, use the first result
        if not station_info:
            station_info = search_data['data'][0]

        station_name = station_info['station']['name']
        station_uid = station_info['uid']

        # Fetch station data using the uid
        feed_url = f"https://api.waqi.info/feed/@{station_uid}/?token={TOKEN}"
        feed_response = requests.get(feed_url, timeout=10)
        feed_response.raise_for_status()
        feed_data = feed_response.json()

        if feed_data['status'] != 'ok':
            raise HTTPException(status_code=400, detail=f"Error fetching station data: {feed_data}")

        # Extract actual AQI and real-time pollutants
        iaqi_data = feed_data['data'].get('iaqi', {})
        actual_aqi = feed_data['data'].get('aqi')

        pm25 = iaqi_data.get('pm25', {}).get('v')
        pm10 = iaqi_data.get('pm10', {}).get('v')
        so2 = iaqi_data.get('so2', {}).get('v')
        no2 = iaqi_data.get('no2', {}).get('v')
        co = iaqi_data.get('co', {}).get('v')
        o3 = iaqi_data.get('o3', {}).get('v')

        # Check if all pollutant data is available
        if any(v is None for v in [pm25, pm10, so2, no2, co, o3]):
            raise HTTPException(status_code=400, detail="Missing pollutant data for prediction")

        # Create DataFrame for prediction with proper column names
        input_data = pd.DataFrame([[
            pm25, pm10, so2, no2, co, o3
        ]], columns=['pm25', 'pm10', 'so2', 'no2', 'co', 'o3'])

        # Load model if not already loaded
        global model
        if model is None:
            try:
                with open('xgboost_aqi_model.pkl', 'rb') as f:
                    model = pickle.load(f)
                print("Model loaded successfully")
            except FileNotFoundError:
                raise HTTPException(status_code=500, detail="Model not found. Please train the model first.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

        # Predict AQI using the loaded model
        predicted_aqi = model.predict(input_data)[0]

        # Return results
        return PredictionResponse(
            station_names=[station_name],
            predicted_aqi=[float(predicted_aqi)],
            actual_aqi=[actual_aqi if actual_aqi is not None else "N/A"],
            pollutants=[{
                "pm25": pm25,
                "pm10": pm10,
                "so2": so2,
                "no2": no2,
                "co": co,
                "o3": o3
            }]
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Error connecting to WAQI API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/predict/manual", response_model=PredictionResponse)
async def predict_aqi_manual(request: ManualPredictionRequest):
    """
    Predict AQI based on manually provided pollutant values

    Args:
        pm25, pm10, so2, no2, co, o3: Pollutant concentration values

    Returns:
        PredictionResponse with predicted AQI
    """
    try:
        # Create DataFrame for prediction
        input_data = pd.DataFrame([[
            request.pm25, request.pm10, request.so2, request.no2, request.co, request.o3
        ]], columns=['pm25', 'pm10', 'so2', 'no2', 'co', 'o3'])

        # Load model if not already loaded
        global model
        if model is None:
            try:
                with open('xgboost_aqi_model.pkl', 'rb') as f:
                    model = pickle.load(f)
                print("Model loaded successfully")
            except FileNotFoundError:
                raise HTTPException(status_code=500, detail="Model not found. Please train the model first.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")

        # Predict AQI using the loaded model
        predicted_aqi = model.predict(input_data)[0]

        # Return results
        return PredictionResponse(
            station_names=["Custom Input"],
            predicted_aqi=[float(predicted_aqi)],
            actual_aqi=["N/A"],
            pollutants=[{
                "pm25": request.pm25,
                "pm10": request.pm10,
                "so2": request.so2,
                "no2": request.no2,
                "co": request.co,
                "o3": request.o3
            }]
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)