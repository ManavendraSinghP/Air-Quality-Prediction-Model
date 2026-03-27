from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the machine_learning directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'machine_learning'))

# Import our custom modules
try:
    from model import AQIPredictor
    from data_processing import fetch_current_aqi
except ImportError as e:
    print(f"Import error: {e}")
    # We'll define placeholder functions for now
    def fetch_current_aqi(location):
        # Placeholder function - will be implemented later
        return {"aqi": 50, "pm25": 12, "pm10": 25}

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the model (will load trained model)
predictor = None

@app.route('/')
def home():
    return jsonify({"message": "AQI Prediction API is running!"})

@app.route('/predict', methods=['POST'])
def predict_aqi():
    """
    Predict AQI based on input features
    Expected JSON: {
        "location": "city_name",
        "pm25": 12.5,
        "pm10": 25.0,
        "no2": 15.0,
        "so2": 5.0,
        "co": 0.8,
        "o3": 30.0
    }
    """
    try:
        data = request.get_json()

        # Extract features
        location = data.get('location', '')
        pm25 = data.get('pm25', 0)
        pm10 = data.get('pm10', 0)
        no2 = data.get('no2', 0)
        so2 = data.get('so2', 0)
        co = data.get('co', 0)
        o3 = data.get('o3', 0)

        # Make prediction (placeholder)
        if predictor:
            predicted_aqi = predictor.predict([pm25, pm10, no2, so2, co, o3])
        else:
            # Placeholder prediction
            predicted_aqi = (pm25 * 0.5 + pm10 * 0.3 + no2 * 0.1 + so2 * 0.05 + co * 0.03 + o3 * 0.02)

        # Fetch current AQI
        current_data = fetch_current_aqi(location)
        current_aqi = current_data.get('aqi', 0)

        # Compare predicted vs actual
        comparison = {
            "predicted_aqi": predicted_aqi,
            "current_aqi": current_aqi,
            "difference": abs(predicted_aqi - current_aqi),
            "accuracy": f"{100 - (abs(predicted_aqi - current_aqi) / current_aqi * 100)}%" if current_aqi > 0 else "N/A"
        }

        return jsonify({
            "success": True,
            "location": location,
            "comparison": comparison
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/current_aqi', methods=['GET'])
def get_current_aqi():
    """
    Fetch current AQI for a given location
    Query param: location=city_name
    """
    try:
        location = request.args.get('location', '')
        if not location:
            return jsonify({"success": False, "error": "Location parameter is required"}), 400

        current_data = fetch_current_aqi(location)

        return jsonify({
            "success": True,
            "location": location,
            "aqi_data": current_data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)