# AQI Prediction Frontend

This is the frontend interface for the AQI Prediction system. It provides a user-friendly web interface for entering locations and viewing AQI predictions compared to actual values.

## Project Structure

```
frontend/
├── css/           # Stylesheets
├── js/            # JavaScript files
├── assets/        # Images and other assets
├── index.html     # Main HTML file
└── README.md      # This file
```

## Features

1. **Location Input**: Users can enter a city name to get AQI data
2. **AQI Comparison**: Shows both predicted and actual AQI values
3. **Category Display**: Displays AQI categories with color coding
4. **Accuracy Metrics**: Shows how accurate the predictions are
5. **Responsive Design**: Works on desktop and mobile devices

## Setup

1. The frontend is a static website that can be served by any web server
2. Make sure the backend API is running on `http://localhost:5000`
3. Update the `API_BASE_URL` in `js/script.js` if your backend is hosted elsewhere

## Technologies Used

- HTML5
- CSS3 (with Flexbox and Grid for layout)
- Vanilla JavaScript (no frameworks)
- Fetch API for HTTP requests

## Customization

You can customize the appearance by modifying:
- `css/style.css` - Colors, fonts, spacing
- `index.html` - Layout and structure
- `js/script.js` - Functionality and interactions

## API Endpoints Used

1. `GET /current_aqi?location=:location` - Get current AQI for a location
2. `POST /predict` - Get AQI prediction based on pollutant data

## Deployment

To deploy this frontend:

1. Upload all files to a web server
2. Configure the web server to serve static files
3. Ensure CORS is configured correctly if hosting frontend and backend separately
4. Update the API base URL in `js/script.js` if needed