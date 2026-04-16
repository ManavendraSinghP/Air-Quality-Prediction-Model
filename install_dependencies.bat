@echo off
echo Installing Delhi AQI Prediction System Dependencies...
echo ======================================================

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing Python packages from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo Please make sure you have Python and pip installed.
    echo.
    echo You can download Python from: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo SUCCESS: All dependencies installed successfully!
echo.
echo Next steps:
echo 1. Get your free WAQI API token from https://aqicn.org/data-platform/token/
echo 2. Run start_system.bat to launch the application
echo.
pause