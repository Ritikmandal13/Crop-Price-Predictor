#!/bin/bash

echo "========================================"
echo " Crop Price Predictor - Setup & Run"
echo "========================================"
echo ""

echo "[1/4] Checking Python installation..."
python3 --version || python --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python is not installed!"
    exit 1
fi

echo ""
echo "[2/4] Installing dependencies..."
pip3 install -r requirements.txt || pip install -r requirements.txt

echo ""
echo "[3/4] Initializing database..."
python3 -c "from auth.database import init_db; init_db()" || python -c "from auth.database import init_db; init_db()"

echo ""
echo "[4/4] Starting application..."
echo ""
echo "Application will start at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python3 app.py || python app.py

