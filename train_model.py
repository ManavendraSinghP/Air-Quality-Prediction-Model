import pandas as pd
import numpy as np
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pickle
import warnings
warnings.filterwarnings('ignore')

def train_aqi_model(use_sample=False):
    """
    Train an XGBoost model to predict AQI based on pollutant levels
    """
    print("Loading dataset...")
    # Load the dataset
    if use_sample:
        dataset_file = 'delhi_aqi_sample.csv'
    else:
        dataset_file = 'delhi_aqi_data.csv'

    if not os.path.exists(dataset_file):
        raise FileNotFoundError(f"Dataset file '{dataset_file}' not found. "
                                "Please run prepare_dataset.py first.")

    df = pd.read_csv(dataset_file)

    # Filter for Delhi data only if the column exists
    if 'location_name' in df.columns:
        df_delhi = df[df['location_name'] == 'Delhi'].copy()
    else:
        # If no location column, assume all data is Delhi data
        df_delhi = df.copy()

    print(f"Dataset shape: {df_delhi.shape}")
    print(f"Columns: {list(df_delhi.columns)}")

    # Select features (lowercase as required)
    features = ['pm25', 'pm10', 'so2', 'no2', 'co', 'o3']
    target = 'aqi'

    # Check if required columns exist
    missing_features = [f for f in features if f not in df_delhi.columns]
    if missing_features:
        raise ValueError(f"Missing required feature columns: {missing_features}")

    if target not in df_delhi.columns:
        raise ValueError(f"Missing target column: {target}")

    # Check for missing values
    print("\nMissing values in features:")
    print(df_delhi[features].isnull().sum())

    # Remove rows with missing values
    df_clean = df_delhi.dropna(subset=features + [target])
    print(f"\nDataset shape after cleaning: {df_clean.shape}")

    # Prepare features and target
    X = df_clean[features]
    y = df_clean[target]

    # Split the data (80/20 split)
    print("\nSplitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    # Hyperparameter tuning for XGBoost
    print("\nPerforming hyperparameter tuning...")
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2]
    }

    xgb_model = XGBRegressor(random_state=42)

    # Grid search with cross-validation
    grid_search = GridSearchCV(
        estimator=xgb_model,
        param_grid=param_grid,
        cv=3,
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        verbose=1
    )

    grid_search.fit(X_train, y_train)

    # Best model
    best_model = grid_search.best_estimator_
    print(f"\nBest parameters: {grid_search.best_params_}")

    # Evaluate on test set
    print("\nEvaluating model...")
    y_pred = best_model.predict(X_test)

    # Calculate metrics
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Root Mean Square Error (RMSE): {rmse:.2f}")
    print(f"R² Score: {r2:.4f}")

    # Save the model
    print("\nSaving model...")
    with open('xgboost_aqi_model.pkl', 'wb') as f:
        pickle.dump(best_model, f)

    print("Model saved as 'xgboost_aqi_model.pkl'")

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)

    print("\nFeature Importance:")
    print(feature_importance)

    return best_model

if __name__ == "__main__":
    train_aqi_model()