import pandas as pd
import numpy as np
import os
import sys
from model import AQIPredictor
from data_processing import load_aqi_data, clean_and_prepare_data, fetch_historical_aqi

def create_sample_dataset(filename="sample_aqi_data.csv"):
    """
    Create a sample AQI dataset for demonstration
    """
    print("Creating sample AQI dataset...")

    # Generate synthetic data
    np.random.seed(42)  # For reproducible results
    n_samples = 1000

    data = {
        'date': pd.date_range(start='2020-01-01', periods=n_samples, freq='D'),
        'pm25': np.random.uniform(0, 150, n_samples),
        'pm10': np.random.uniform(0, 200, n_samples),
        'no2': np.random.uniform(0, 100, n_samples),
        'so2': np.random.uniform(0, 50, n_samples),
        'co': np.random.uniform(0, 20, n_samples),
        'o3': np.random.uniform(0, 120, n_samples),
    }

    # Create AQI based on a formula with some noise
    data['aqi'] = (
        data['pm25'] * 0.8 +
        data['pm10'] * 0.5 +
        data['no2'] * 0.7 +
        data['so2'] * 0.6 +
        data['co'] * 0.9 +
        data['o3'] * 0.4 +
        np.random.normal(0, 10, n_samples)  # Add some noise
    )

    # Ensure AQI is positive
    data['aqi'] = np.maximum(data['aqi'], 0)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Sample dataset saved to {filename}")
    return df

def main():
    # Add parent directory to path to import modules
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

    # Create data directory if it doesn't exist
    data_dir = "../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Create or load dataset
    dataset_path = os.path.join(data_dir, "aqi_data.csv")

    if not os.path.exists(dataset_path):
        print("Dataset not found. Creating sample dataset...")
        df = create_sample_dataset(dataset_path)
    else:
        print("Loading existing dataset...")
        df = load_aqi_data(dataset_path)

        if df is None:
            print("Failed to load dataset. Creating sample dataset...")
            df = create_sample_dataset(dataset_path)

    # Clean and prepare data
    print("Cleaning and preparing data...")
    df_clean = clean_and_prepare_data(df)
    print(f"Dataset shape after cleaning: {df_clean.shape}")

    # Initialize predictor
    predictor = AQIPredictor()

    # Train model
    print("Training model...")
    metrics = predictor.train(df_clean)
    print(f"Model training completed:")
    print(f"  MSE: {metrics['mse']:.2f}")
    print(f"  RMSE: {metrics['rmse']:.2f}")
    print(f"  R² Score: {metrics['r2_score']:.2f}")

    # Save model
    model_path = os.path.join(data_dir, "aqi_model.pkl")
    predictor.save_model(model_path)
    print(f"Model saved to {model_path}")

    # Test prediction
    print("\nTesting prediction with sample data...")
    sample_features = [
        df_clean['pm25'].mean(),
        df_clean['pm10'].mean(),
        df_clean['no2'].mean(),
        df_clean['so2'].mean(),
        df_clean['co'].mean(),
        df_clean['o3'].mean()
    ]

    predicted_aqi = predictor.predict(sample_features)
    actual_aqi = df_clean['aqi'].mean()

    print(f"Sample prediction:")
    print(f"  Features: {[round(x, 2) for x in sample_features]}")
    print(f"  Predicted AQI: {predicted_aqi:.2f}")
    print(f"  Actual average AQI: {actual_aqi:.2f}")
    print(f"  Difference: {abs(predicted_aqi - actual_aqi):.2f}")

if __name__ == "__main__":
    main()