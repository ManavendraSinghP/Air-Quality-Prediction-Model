import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AQIPredictor:
    def __init__(self):
        self.model = None
        self.is_trained = False

    def preprocess_data(self, df):
        """
        Preprocess the AQI data
        Expected columns: pm25, pm10, no2, so2, co, o3, aqi
        """
        # Handle missing values
        df = df.dropna()

        # Remove outliers (AQI values that are unrealistic)
        df = df[(df['aqi'] >= 0) & (df['aqi'] <= 500)]

        # Feature selection
        feature_columns = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
        X = df[feature_columns]
        y = df['aqi']

        return X, y

    def train(self, df):
        """
        Train the AQI prediction model
        """
        # Preprocess data
        X, y = self.preprocess_data(df)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # Initialize and train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        self.is_trained = True

        return {
            "mse": mse,
            "rmse": np.sqrt(mse),
            "r2_score": r2
        }

    def predict(self, features):
        """
        Predict AQI based on features
        features: [pm25, pm10, no2, so2, co, o3]
        """
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")

        # Convert to numpy array and reshape for single prediction
        features_array = np.array(features).reshape(1, -1)
        prediction = self.model.predict(features_array)

        return float(prediction[0])

    def save_model(self, filepath):
        """
        Save the trained model to disk
        """
        if not self.is_trained:
            raise ValueError("No trained model to save")

        joblib.dump(self.model, filepath)

    def load_model(self, filepath):
        """
        Load a trained model from disk
        """
        self.model = joblib.load(filepath)
        self.is_trained = True

def fetch_current_aqi(location):
    """
    Fetch current AQI data for a location using an API
    This is a placeholder - you would integrate with a real AQI API
    """
    # For now, return sample data
    # In a real implementation, you would use an API like WAQI or OpenWeatherMap

    # Example with WAQI API (you would need an API key):
    # api_key = os.getenv('WAQI_API_KEY')
    # url = f"http://api.waqi.info/feed/{location}/?token={api_key}"
    # response = requests.get(url)
    # data = response.json()
    # return data['data']['iaqi']

    # Placeholder return
    return {
        "aqi": np.random.randint(0, 150),
        "pm25": np.random.uniform(0, 50),
        "pm10": np.random.uniform(0, 80),
        "no2": np.random.uniform(0, 30),
        "so2": np.random.uniform(0, 10),
        "co": np.random.uniform(0, 5),
        "o3": np.random.uniform(0, 40)
    }