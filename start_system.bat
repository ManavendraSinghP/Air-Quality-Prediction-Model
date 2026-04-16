@echo off
echo Starting Delhi AQI Prediction System...
echo ======================================

REM Start backend in a new window
start "Backend" /D "C:\Users\manav\OneDrive\Desktop\AQI Prediction" cmd /c start_backend.bat

REM Wait a moment for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
start "Frontend" /D "C:\Users\manav\OneDrive\Desktop\AQI Prediction\frontend" cmd /c start_frontend.bat

echo.
echo System started successfully!
echo ----------------------------
echo Backend API:    http://localhost:8000
echo Frontend UI:    http://localhost:8080
echo.
echo NOTE: Make sure to:
echo 1. Install required Python packages:
echo    pip install fastapi uvicorn xgboost scikit-learn pandas requests
echo 2. Get a free WAQI API token from https://aqicn.org/data-platform/token/
echo.
echo Press any key to exit this window...
pause >nul