#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")"

echo "========================================"
echo "   Invoice Processing Suite Launcher    "
echo "========================================"
echo "This tool allows you to create templates"
echo "for different client layouts."
echo "========================================"

# 1. Check if Backend is running
if ! lsof -i :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "🔸 Starting Backend Server..."
    # Start in background
    cd backend
    source .venv/bin/activate
    export BACKEND_CORS_ORIGINS='["*"]'
    nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
    cd ..
    echo "   Waiting for server to initialize..."
    sleep 5
else
    echo "✅ Backend is already running."
fi

# 2. Open the Suite
echo "🚀 Opening Processing Suite..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    open app.html
else
    # Try generic open
    xdg-open app.html || start app.html
fi

echo ""
echo "💡 Tip: In the app, highlight text to map it!"