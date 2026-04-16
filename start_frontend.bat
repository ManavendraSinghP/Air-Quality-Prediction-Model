@echo off
echo Starting Delhi AQI Prediction Frontend...
echo ----------------------------------------

cd /d "C:\Users\manav\OneDrive\Desktop\AQI Prediction\frontend"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Start a simple HTTP server
echo Starting HTTP server on port 8080...
echo Frontend will be available at http://localhost:8080
python -m http.server 8080

pause