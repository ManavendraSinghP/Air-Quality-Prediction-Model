@echo off
echo Starting Delhi AQI Prediction Backend...
echo -------------------------------------
echo Make sure you have Python and required packages installed:
echo - fastapi
echo - uvicorn
echo - xgboost
echo - scikit-learn
echo - pandas
echo - requests
echo -------------------------------------

cd /d "C:\Users\manav\OneDrive\Desktop\AQI Prediction"

REM Check if model exists, if not train it
if not exist "xgboost_aqi_model.pkl" (
    echo Training model...
    python train_model.py
    if errorlevel 1 (
        echo Error training model!
        pause
        exit /b 1
    )
)

echo Starting FastAPI server...
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

pause