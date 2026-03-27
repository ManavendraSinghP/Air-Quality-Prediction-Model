"""
Data preprocessing and exploratory analysis for AQI prediction
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import os

def load_and_explore_data(file_path):
    """
    Load data and perform initial exploration

    Args:
        file_path (str): Path to the CSV file

    Returns:
        pandas.DataFrame: Loaded data
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return None

    try:
        df = pd.read_csv(file_path)
        print("=== Data Overview ===")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("\n=== First 5 Rows ===")
        print(df.head())
        print("\n=== Data Info ===")
        print(df.info())
        print("\n=== Statistical Summary ===")
        print(df.describe())

        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_data(df):
    """
    Preprocess the AQI data

    Args:
        df (pandas.DataFrame): Raw data

    Returns:
        pandas.DataFrame: Preprocessed data
    """
    print("\n=== Data Preprocessing ===")

    # Handle missing values
    print(f"Missing values before preprocessing:")
    print(df.isnull().sum())

    # Drop rows with missing AQI values
    df = df.dropna(subset=['aqi'])

    # Fill other missing values with median
    for col in df.select_dtypes(include=[np.number]).columns:
        if col != 'aqi':
            df[col] = df[col].fillna(df[col].median())

    print(f"\nMissing values after preprocessing:")
    print(df.isnull().sum())

    # Remove outliers using IQR method
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    for col in numeric_columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        print(f"Outliers in {col}: {len(outliers)}")

        # Remove extreme outliers (> 500 for AQI)
        if col == 'aqi':
            df = df[df[col] <= 500]

    print(f"\nData shape after outlier removal: {df.shape}")

    return df

def visualize_data(df):
    """
    Create visualizations for exploratory analysis

    Args:
        df (pandas.DataFrame): Preprocessed data
    """
    print("\n=== Creating Visualizations ===")

    # Set up the plotting style
    plt.style.use('seaborn-v0_8')
    fig = plt.figure(figsize=(15, 10))

    # 1. AQI Distribution
    plt.subplot(2, 3, 1)
    plt.hist(df['aqi'], bins=50, alpha=0.7, color='skyblue')
    plt.xlabel('AQI')
    plt.ylabel('Frequency')
    plt.title('Distribution of AQI Values')

    # 2. Correlation Matrix
    plt.subplot(2, 3, 2)
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')

    # 3. AQI vs PM2.5
    plt.subplot(2, 3, 3)
    plt.scatter(df['pm25'], df['aqi'], alpha=0.5, color='green')
    plt.xlabel('PM2.5')
    plt.ylabel('AQI')
    plt.title('AQI vs PM2.5')

    # 4. AQI vs PM10
    plt.subplot(2, 3, 4)
    plt.scatter(df['pm10'], df['aqi'], alpha=0.5, color='orange')
    plt.xlabel('PM10')
    plt.ylabel('AQI')
    plt.title('AQI vs PM10')

    # 5. Box plot of pollutants
    plt.subplot(2, 3, 5)
    pollutant_cols = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
    pollutant_data = df[pollutant_cols].dropna()
    plt.boxplot([pollutant_data[col] for col in pollutant_cols], labels=pollutant_cols)
    plt.ylabel('Concentration')
    plt.title('Distribution of Pollutants')
    plt.xticks(rotation=45)

    # 6. Time series of AQI (if date column exists)
    plt.subplot(2, 3, 6)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df_sorted = df.sort_values('date')
        plt.plot(df_sorted['date'], df_sorted['aqi'], alpha=0.7)
        plt.xlabel('Date')
        plt.ylabel('AQI')
        plt.title('AQI Over Time')
        plt.xticks(rotation=45)
    else:
        # If no date column, show AQI categories
        aqi_categories = pd.cut(df['aqi'],
                               bins=[0, 50, 100, 150, 200, 300, 500],
                               labels=['Good', 'Moderate', 'Unhealthy SG', 'Unhealthy', 'Very Unhealthy', 'Hazardous'])
        category_counts = aqi_categories.value_counts()
        plt.bar(category_counts.index, category_counts.values)
        plt.xlabel('AQI Category')
        plt.ylabel('Count')
        plt.title('Distribution of AQI Categories')
        plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig('../data/aqi_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    print("Visualizations saved to ../data/aqi_analysis.png")

def feature_engineering(df):
    """
    Perform feature engineering to create additional features

    Args:
        df (pandas.DataFrame): Preprocessed data

    Returns:
        pandas.DataFrame: Data with engineered features
    """
    print("\n=== Feature Engineering ===")

    # Create pollution ratio features
    if 'pm25' in df.columns and 'pm10' in df.columns:
        df['pm_ratio'] = df['pm25'] / (df['pm10'] + 1)  # Add 1 to avoid division by zero

    # Create composite pollution index
    pollution_cols = ['pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
    available_cols = [col for col in pollution_cols if col in df.columns]
    if available_cols:
        df['pollution_index'] = df[available_cols].mean(axis=1)

    # Create AQI category feature
    def categorize_aqi(aqi):
        if aqi <= 50:
            return 0  # Good
        elif aqi <= 100:
            return 1  # Moderate
        elif aqi <= 150:
            return 2  # Unhealthy for Sensitive Groups
        elif aqi <= 200:
            return 3  # Unhealthy
        elif aqi <= 300:
            return 4  # Very Unhealthy
        else:
            return 5  # Hazardous

    df['aqi_category'] = df['aqi'].apply(categorize_aqi)

    print(f"New features created: {list(set(df.columns) - set(['pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'aqi']))}")

    return df

def main():
    """
    Main function to run data analysis
    """
    # Create data directory if it doesn't exist
    data_dir = "../data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # For demo purposes, let's create sample data if real data doesn't exist
    data_file = os.path.join(data_dir, "aqi_data.csv")

    if not os.path.exists(data_file):
        print("Creating sample data for demonstration...")
        # Create sample data
        np.random.seed(42)
        n_samples = 1000
        dates = pd.date_range(start='2020-01-01', periods=n_samples, freq='D')

        sample_data = {
            'date': dates,
            'pm25': np.random.uniform(0, 150, n_samples),
            'pm10': np.random.uniform(0, 200, n_samples),
            'no2': np.random.uniform(0, 100, n_samples),
            'so2': np.random.uniform(0, 50, n_samples),
            'co': np.random.uniform(0, 20, n_samples),
            'o3': np.random.uniform(0, 120, n_samples),
        }

        # Create AQI based on a formula with some noise
        sample_data['aqi'] = (
            sample_data['pm25'] * 0.8 +
            sample_data['pm10'] * 0.5 +
            sample_data['no2'] * 0.7 +
            sample_data['so2'] * 0.6 +
            sample_data['co'] * 0.9 +
            sample_data['o3'] * 0.4 +
            np.random.normal(0, 10, n_samples)
        )

        # Ensure AQI is positive
        sample_data['aqi'] = np.maximum(sample_data['aqi'], 0)

        df = pd.DataFrame(sample_data)
        df.to_csv(data_file, index=False)
        print(f"Sample data saved to {data_file}")

    # Load and explore data
    df = load_and_explore_data(data_file)

    if df is not None:
        # Preprocess data
        df_processed = preprocess_data(df)

        # Feature engineering
        df_engineered = feature_engineering(df_processed)

        # Save processed data
        processed_file = os.path.join(data_dir, "aqi_data_processed.csv")
        df_engineered.to_csv(processed_file, index=False)
        print(f"\nProcessed data saved to {processed_file}")

        # Visualize data
        visualize_data(df_engineered)

        print("\n=== Analysis Complete ===")
        print(f"Final dataset shape: {df_engineered.shape}")
        print(f"Columns: {list(df_engineered.columns)}")

if __name__ == "__main__":
    main()