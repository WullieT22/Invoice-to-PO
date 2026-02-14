#!/bin/zsh
# Open the frontend demo in browser and start server

echo ""
echo "🎨 Starting Frontend Demo..."
echo ""

cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies first..."
    npm install
fi

# Open browser first
echo "🌐 Opening browser to http://localhost:5173 in 5 seconds..."
sleep 5
open "http://localhost:5173" 2>/dev/null || echo "Please open http://localhost:5173 in your browser"

# Start dev server
echo ""
echo "🚀 Starting Vite development server..."
echo ""
npm run dev
