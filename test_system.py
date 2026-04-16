import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import warnings
warnings.filterwarnings('ignore')

def test_model_loading():
    """Test if the model can be loaded successfully"""
    try:
        with open('xgboost_aqi_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("✓ Model loaded successfully")
        return model
    except FileNotFoundError:
        print("✗ Model file not found. Need to train the model first.")
        return None
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        return None

def test_prediction():
    """Test making a prediction with sample data"""
    model = test_model_loading()
    if model is None:
        return False

    try:
        # Create sample input data
        sample_data = pd.DataFrame([[
            50.5, 80.2, 4.3, 25.7, 0.8, 60.1
        ]], columns=['pm25', 'pm10', 'so2', 'no2', 'co', 'o3'])

        prediction = model.predict(sample_data)
        print(f"✓ Sample prediction successful: {prediction[0]:.2f}")
        return True
    except Exception as e:
        print(f"✗ Error making prediction: {e}")
        return False

def test_data_format():
    """Test if the dataset has the expected format"""
    try:
        # Try to read a sample of the dataset
        df_sample = pd.read_csv('delhi_aqi_data.csv', nrows=5)
        print(f"✓ Dataset loaded successfully. Shape: {df_sample.shape}")

        # Check if required columns exist (case-insensitive)
        columns_lower = [col.lower() for col in df_sample.columns]
        required_columns = ['pm25', 'pm10', 'so2', 'no2', 'co', 'o3', 'aqi']

        missing_columns = []
        for col in required_columns:
            if col not in columns_lower:
                missing_columns.append(col)

        if missing_columns:
            print(f"⚠ Warning: Missing columns: {missing_columns}")
            return False
        else:
            print("✓ All required columns present")
            return True

    except Exception as e:
        print(f"✗ Error reading dataset: {e}")
        return False

if __name__ == "__main__":
    print("Testing Delhi AQI Prediction System...\n")

    # Test data format
    print("1. Testing dataset format:")
    data_ok = test_data_format()

    # Test model loading and prediction
    print("\n2. Testing model:")
    model_ok = test_prediction()

    if data_ok and model_ok:
        print("\n✓ All tests passed! System is ready to use.")
    else:
        print("\n✗ Some tests failed. Please check the issues above.")