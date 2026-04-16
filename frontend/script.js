// Base URL for the API (adjust as needed)
const BASE_URL = 'http://localhost:8000';

// DOM Elements
const apiForm = document.getElementById('api-form');
const manualForm = document.getElementById('manual-form');
const resultsSection = document.getElementById('results');
const errorMessage = document.getElementById('error-message');
const errorText = document.getElementById('error-text');

// AQI Category helper function
function getAQICategory(aqi) {
    if (aqi <= 50) return { name: 'Good', class: 'good' };
    if (aqi <= 100) return { name: 'Moderate', class: 'moderate' };
    if (aqi <= 150) return { name: 'Unhealthy for Sensitive Groups', class: 'unhealthy-sensitive' };
    if (aqi <= 200) return { name: 'Unhealthy', class: 'unhealthy' };
    if (aqi <= 300) return { name: 'Very Unhealthy', class: 'very-unhealthy' };
    return { name: 'Hazardous', class: 'hazardous' };
}

// Show loading state
function showLoading(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Processing...';
    return () => {
        button.disabled = false;
        button.innerHTML = originalText;
    };
}

// Show error message
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    resultsSection.classList.add('hidden');

    // Auto-hide error after 5 seconds
    setTimeout(() => {
        errorMessage.classList.add('hidden');
    }, 5000);
}

// Show results
function showResults(data) {
    const stationName = data.station_names[0];
    const predictedAQI = data.predicted_aqi[0];
    const actualAQI = data.actual_aqi[0];
    const pollutants = data.pollutants[0];

    // Update station name
    document.getElementById('station-name').textContent = stationName;

    // Update predicted AQI
    document.getElementById('predicted-aqi').textContent = predictedAQI.toFixed(2);
    const predictedCategory = getAQICategory(predictedAQI);
    const predictedCategoryElement = document.getElementById('predicted-category');
    predictedCategoryElement.textContent = predictedCategory.name;
    predictedCategoryElement.className = `category-badge ${predictedCategory.class}`;

    // Update actual AQI
    document.getElementById('actual-aqi').textContent = actualAQI !== "N/A" ? actualAQI : "N/A";
    if (actualAQI !== "N/A") {
        const actualCategory = getAQICategory(actualAQI);
        const actualCategoryElement = document.getElementById('actual-category');
        actualCategoryElement.textContent = actualCategory.name;
        actualCategoryElement.className = `category-badge ${actualCategory.class}`;
        actualCategoryElement.style.display = 'inline-block';
    } else {
        document.getElementById('actual-category').style.display = 'none';
    }

    // Update pollutant values
    document.getElementById('display-pm25').textContent = pollutants.pm25;
    document.getElementById('display-pm10').textContent = pollutants.pm10;
    document.getElementById('display-so2').textContent = pollutants.so2;
    document.getElementById('display-no2').textContent = pollutants.no2;
    document.getElementById('display-co').textContent = pollutants.co;
    document.getElementById('display-o3').textContent = pollutants.o3;

    // Show results section
    resultsSection.classList.remove('hidden');
    errorMessage.classList.add('hidden');
}

// API Form Submission
apiForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const token = document.getElementById('token').value;
    const location = document.getElementById('location').value;

    if (!token || !location) {
        showError('Please fill in all required fields');
        return;
    }

    const resetButton = showLoading(document.querySelector('#api-form .btn'));

    try {
        const response = await fetch(`${BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ token, location })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get prediction');
        }

        const data = await response.json();
        showResults(data);
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        resetButton();
    }
});

// Manual Form Submission
manualForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get values from form
    const pm25 = parseFloat(document.getElementById('pm25').value);
    const pm10 = parseFloat(document.getElementById('pm10').value);
    const so2 = parseFloat(document.getElementById('so2').value);
    const no2 = parseFloat(document.getElementById('no2').value);
    const co = parseFloat(document.getElementById('co').value);
    const o3 = parseFloat(document.getElementById('o3').value);

    // Validate inputs
    if (isNaN(pm25) || isNaN(pm10) || isNaN(so2) || isNaN(no2) || isNaN(co) || isNaN(o3)) {
        showError('Please enter valid numbers for all pollutant fields');
        return;
    }

    const resetButton = showLoading(document.querySelector('#manual-form .btn'));

    try {
        const response = await fetch(`${BASE_URL}/predict/manual`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ pm25, pm10, so2, no2, co, o3 })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to get prediction');
        }

        const data = await response.json();
        showResults(data);
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        resetButton();
    }
});

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    console.log('Delhi AQI Predictor frontend loaded');

    // Add some sample values for testing
    document.getElementById('pm25').value = '50.5';
    document.getElementById('pm10').value = '80.2';
    document.getElementById('so2').value = '4.3';
    document.getElementById('no2').value = '25.7';
    document.getElementById('co').value = '0.8';
    document.getElementById('o3').value = '60.1';
});