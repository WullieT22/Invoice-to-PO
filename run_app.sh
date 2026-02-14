#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")"

echo "========================================"
echo "   Invoice to PO - Application Launcher "
echo "========================================"

# 1. Kill any existing server on port 8000
echo "[1/4] Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null

# 2. Prepare Backend
echo "[2/4] Preparing Backend..."
cd backend

# Check for virtual environment
if [ ! -d ".venv" ]; then
    echo "      ❌ .venv not found! Running fix_setup.sh first..."
    cd ..
    ./fix_setup.sh
    cd backend
fi

source .venv/bin/activate

# --- FIX: Set Environment Variables for CORS ---
export BACKEND_CORS_ORIGINS='["*"]'
export CORS_ORIGINS="*"

# 3. Start Server
echo "[3/4] Starting Server..."
# Run in background, save logs to backend.log
nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
SERVER_PID=$!

echo "      ⏳ Waiting 5 seconds for startup..."
sleep 5

# 4. Check if it's running
if ps -p $SERVER_PID > /dev/null; then
   echo "      ✅ Backend is RUNNING (PID: $SERVER_PID)"
   echo "[4/4] Opening Dashboard..."
   cd ..
   open dashboard.html
   
   echo ""
   echo "🎉 App is live! Press Ctrl+C to stop."
   echo "Logs are being written to: backend.log"
   trap "kill $SERVER_PID; exit" INT
   wait $SERVER_PID
else
   echo "      ❌ Backend CRASHED immediately."
   echo "      Here is the error log:"
   echo "----------------------------------------"
   cat ../backend.log
   echo "----------------------------------------"
fi