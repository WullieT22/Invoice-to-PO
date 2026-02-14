#!/bin/zsh
# Start backend server
echo "Starting Invoice to PO Matching Backend..."
echo "=========================================="
echo ""
echo "Activating Python environment..."
cd "$(dirname "$0")/backend"

if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "Virtual environment not found. Run setup.sh first."
    exit 1
fi

echo "Starting FastAPI server on http://localhost:8000"
echo "API Docs will be available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
