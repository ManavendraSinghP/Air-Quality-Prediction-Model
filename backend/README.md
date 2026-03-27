# AQI Prediction Backend API

This is the backend API for the AQI Prediction system. It provides endpoints for predicting Air Quality Index values based on environmental data and comparing predictions with actual AQI readings.

## Project Structure

```
backend/
├── api/           # API route handlers
├── models/        # Data models
├── utils/         # Utility functions
├── config/        # Configuration files
├── app.py         # Main Flask application
├── requirements.txt # Python dependencies
└── .env          # Environment variables
```

## Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in `.env` file

## Running the API

```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### GET /
Health check endpoint

Response:
```json
{
  "message": "AQI Prediction API is running!"
}
```

### POST /predict
Predict AQI based on input features

Request:
```json
{
  "location": "Delhi",
  "pm25": 50.2,
  "pm10": 75.5,
  "no2": 30.1,
  "so2": 15.2,
  "co": 1.2,
  "o3": 45.3
}
```

Response:
```json
{
  "success": true,
  "location": "Delhi",
  "comparison": {
    "predicted_aqi": 120.5,
    "current_aqi": 115.2,
    "difference": 5.3,
    "accuracy": "95.4%"
  }
}
```

### GET /current_aqi
Fetch current AQI for a location

Query Parameter: `location=city_name`

Response:
```json
{
  "success": true,
  "location": "Delhi",
  "aqi_data": {
    "aqi": 115,
    "pm25": 50.2,
    "pm10": 75.5,
    "no2": 30.1,
    "so2": 15.2,
    "co": 1.2,
    "o3": 45.3
  }
}
```

## Dependencies

- Flask: Web framework
- Flask-CORS: Cross-Origin Resource Sharing support
- Requests: HTTP library for API calls
- Pandas: Data manipulation
- NumPy: Numerical computing
- Scikit-learn: Machine learning library
- Joblib: Model persistence
- python-dotenv: Environment variable management