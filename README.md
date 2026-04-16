# Air-Quality-Prediction-Model
Intel Artificial Intelligence - VUIP111 MAJOR PROJECT

# Delhi AQI Prediction System

An end-to-end Artificial Intelligence system for predicting Delhi's Air Quality Index (AQI) using machine learning and real-time data from the World Air Quality Index (WAQI) API.

## Features

- **Machine Learning Model**: XGBoost regression model trained on historical Delhi AQI data
- **Real-time Prediction**: Fetches live pollutant data from WAQI API
- **Dual Input Methods**: 
  - API integration with predefined Delhi monitoring stations
  - Manual input for custom pollutant values
- **Beautiful Frontend**: Modern, responsive web interface with real-time visualization
- **Batch Execution**: Windows batch files for easy system startup

## Project Structure

```
├── delhi_aqi_data.csv         # Historical AQI dataset
├── train_model.py             # Model training script
├── app.py                     # FastAPI backend
├── requirements.txt           # Python dependencies
├── frontend/
│   ├── index.html             # Main frontend page
│   ├── styles.css             # Styling
│   └── script.js              # Frontend logic
├── start_backend.bat          # Starts backend API
├── start_frontend.bat         # Starts frontend UI
└── start_system.bat           # Starts both components
```

## Installation

1. **Install Python Dependencies**:
   ```bash
   # Run the install_dependencies.bat file or manually install:
   pip install -r requirements.txt
   ```

2. **Get WAQI API Token**:
   - Register at [WAQI Data Platform](https://aqicn.org/data-platform/token/)
   - Copy your API token for use in the application

3. **Train the Model** (if not already done):
   ```bash
   python train_model.py
   ```

## Usage

### Option 1: Start Both Components Together
Double-click `start_system.bat` to launch both the backend and frontend.

### Option 2: Start Components Separately
1. **Backend**: Double-click `start_backend.bat`
2. **Frontend**: Double-click `start_frontend.bat`

### Accessing the Application
- **Frontend**: Open `http://localhost:8080` in your browser
- **Backend API**: Access at `http://localhost:8000`

## Testing

To verify the system is working correctly:
```bash
python test_system.py
```

This will check:
- Dataset format and availability
- Model loading
- Sample prediction

## API Endpoints

- `GET /` - Health check
- `GET /stations` - Get list of Delhi monitoring stations
- `POST /predict` - Predict AQI using WAQI API data
- `POST /predict/manual` - Predict AQI using manual inputs

## Academic Project Compliance

This system meets all requirements for the Major Project:
- Implements machine learning with XGBoost
- Uses the provided dataset with proper preprocessing
- Includes hyperparameter tuning and model evaluation
- Provides RESTful API backend with FastAPI
- Features a beautiful, user-friendly frontend
- Integrates with external APIs (WAQI)
- Fully documented with modular, commented code
- Batch files for seamless execution

## Dataset Information

The system uses `delhi_aqi_data.csv` containing historical air quality data for Delhi with features:
- pm25, pm10, so2, no2, co, o3 (pollutant concentrations)
- aqi (target variable)

## Model Performance

The XGBoost model is evaluated using:
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- R² Score

## License

This project is developed for academic purposes as part of a Major Project submission.