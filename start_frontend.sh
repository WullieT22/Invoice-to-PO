#!/bin/zsh
# Start frontend development server
echo "Starting Invoice to PO Matching Frontend..."
echo "=========================================="
echo ""

cd "$(dirname "$0")/frontend"

if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

echo "Starting Vite development server on http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop"
echo ""

npm run dev
