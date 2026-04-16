import pandas as pd
import os

def prepare_dataset():
    """
    Prepare the dataset for the AQI prediction model.
    This script ensures the dataset has the correct format and column names.
    """
    dataset_path = "delhi_aqi_data.csv"

    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file '{dataset_path}' not found.")
        print("Please ensure the dataset is in the correct location.")
        return False

    try:
        print("Loading dataset...")
        df = pd.read_csv(dataset_path)
        print(f"Dataset loaded. Shape: {df.shape}")

        # Display column names
        print(f"Original columns: {list(df.columns)}")

        # Check if we need to rename columns
        column_mapping = {}
        for col in df.columns:
            lower_col = col.lower()
            if lower_col in ['pm2.5', 'pm25']:
                column_mapping[col] = 'pm25'
            elif lower_col in ['pm10']:
                column_mapping[col] = 'pm10'
            elif lower_col in ['so2']:
                column_mapping[col] = 'so2'
            elif lower_col in ['no2']:
                column_mapping[col] = 'no2'
            elif lower_col in ['co']:
                column_mapping[col] = 'co'
            elif lower_col in ['o3']:
                column_mapping[col] = 'o3'
            elif lower_col in ['aqi']:
                column_mapping[col] = 'aqi'

        if column_mapping:
            print(f"Renaming columns: {column_mapping}")
            df.rename(columns=column_mapping, inplace=True)

        # Check for required columns
        required_columns = ['pm25', 'pm10', 'so2', 'no2', 'co', 'o3', 'aqi']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Warning: Missing columns: {missing_columns}")
            return False

        print("Dataset preparation completed successfully!")
        print(f"Final columns: {list(df.columns)}")

        # Save a small sample for testing
        sample_path = "delhi_aqi_sample.csv"
        df.sample(n=min(1000, len(df))).to_csv(sample_path, index=False)
        print(f"Sample dataset saved as '{sample_path}'")

        return True

    except Exception as e:
        print(f"Error preparing dataset: {e}")
        return False

if __name__ == "__main__":
    print("Delhi AQI Dataset Preparation Script")
    print("=" * 40)
    success = prepare_dataset()

    if success:
        print("\nDataset is ready for model training!")
    else:
        print("\nDataset preparation failed. Please check the errors above.")