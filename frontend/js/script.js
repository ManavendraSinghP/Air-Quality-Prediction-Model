// DOM Elements
const form = document.getElementById('aqi-form');
const resultsSection = document.getElementById('results');
const locationInput = document.getElementById('location');

// Result elements
const resultLocation = document.getElementById('result-location');
const predictedAqi = document.getElementById('predicted-aqi');
const actualAqi = document.getElementById('actual-aqi');
const predictedCategory = document.getElementById('predicted-category');
const actualCategory = document.getElementById('actual-category');
const accuracyValue = document.getElementById('accuracy-value');

// API base URL (adjust according to your backend server)
const API_BASE_URL = 'http://localhost:5000';

// Form submission handler
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const location = locationInput.value.trim();

    if (!location) {
        alert('Please enter a location');
        return;
    }

    try {
        // Show loading state
        document.querySelector('button[type="submit"]').textContent = 'Loading...';
        document.querySelector('button[type="submit"]').disabled = true;

        // Fetch current AQI
        const currentResponse = await fetch(`${API_BASE_URL}/current_aqi?location=${encodeURIComponent(location)}`);
        const currentData = await currentResponse.json();

        if (!currentData.success) {
            throw new Error(currentData.error || 'Failed to fetch current AQI');
        }

        // Prepare data for prediction
        const predictionData = {
            location: location,
            pm25: currentData.aqi_data.pm25,
            pm10: currentData.aqi_data.pm10,
            no2: currentData.aqi_data.no2,
            so2: currentData.aqi_data.so2,
            co: currentData.aqi_data.co,
            o3: currentData.aqi_data.o3
        };

        // Make prediction
        const predictResponse = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(predictionData)
        });

        const predictData = await predictResponse.json();

        if (!predictData.success) {
            throw new Error(predictData.error || 'Failed to make prediction');
        }

        // Display results
        displayResults(location, predictData.comparison, currentData.aqi_data);

    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    } finally {
        // Reset loading state
        document.querySelector('button[type="submit"]').textContent = 'Get AQI Data';
        document.querySelector('button[type="submit"]').disabled = false;
    }
});

// Display results function
function displayResults(location, comparison, currentData) {
    // Set location
    resultLocation.textContent = location;

    // Set predicted AQI
    predictedAqi.textContent = Math.round(comparison.predicted_aqi);
    predictedCategory.textContent = getAqiCategory(comparison.predicted_aqi);
    predictedCategory.className = `category ${getAqiCategoryClass(comparison.predicted_aqi)}`;

    // Set actual AQI
    actualAqi.textContent = currentData.aqi;
    actualCategory.textContent = getAqiCategory(currentData.aqi);
    actualCategory.className = `category ${getAqiCategoryClass(currentData.aqi)}`;

    // Set accuracy
    accuracyValue.textContent = comparison.accuracy !== "N/A" ? comparison.accuracy : "N/A";

    // Show results section
    resultsSection.style.display = 'block';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Get AQI category based on value
function getAqiCategory(aqi) {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Very Unhealthy';
    return 'Hazardous';
}

// Get CSS class for AQI category
function getAqiCategoryClass(aqi) {
    if (aqi <= 50) return 'good';
    if (aqi <= 100) return 'moderate';
    if (aqi <= 150) return 'unhealthy-sensitive';
    if (aqi <= 200) return 'unhealthy';
    if (aqi <= 300) return 'very-unhealthy';
    return 'hazardous';
}

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    console.log('AQI Prediction Frontend Loaded');

    // You can add any initialization code here
    // For example, you could check if the backend API is reachable
});