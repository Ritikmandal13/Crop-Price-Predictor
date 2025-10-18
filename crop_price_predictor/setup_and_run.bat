@echo off
echo ========================================
echo  Crop Price Predictor - Setup & Run
echo ========================================
echo.

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed!
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo [3/4] Initializing database...
python -c "from auth.database import init_db; init_db()"

echo.
echo [4/4] Starting application...
echo.
echo Application will start at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause

