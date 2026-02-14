#!/bin/zsh
# Start both frontend and backend in separate terminal windows

echo "Invoice to PO Matching - Dual Start Script"
echo "=========================================="
echo ""

PROJECT_DIR="$(dirname "$0")"

# Ensure helper scripts are executable
chmod +x "$PROJECT_DIR/start_backend.sh" "$PROJECT_DIR/start_frontend.sh"

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected - opening Terminal windows..."
    
    # Start backend in new terminal
    osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR' && ./start_backend.sh\""
    
    sleep 2
    
    # Start frontend in new terminal
    osascript -e "tell application \"Terminal\" to do script \"cd '$PROJECT_DIR' && ./start_frontend.sh\""
    
    echo ""
    echo "✓ Backend starting on port 8000"
    echo "✓ Frontend starting on port 5173"
    echo ""
    echo "Terminal windows should have opened automatically."
    echo "If not, run these commands manually:"
    echo ""
    echo "Terminal 1: ./start_backend.sh"
    echo "Terminal 2: ./start_frontend.sh"
    
else
    echo "For non-macOS systems, please run in separate terminals:"
    echo ""
    echo "Terminal 1:"
    echo "  cd $PROJECT_DIR"
    echo "  ./start_backend.sh"
    echo ""
    echo "Terminal 2:"
    echo "  cd $PROJECT_DIR"
    echo "  ./start_frontend.sh"
fi

echo ""
echo "Once both are running:"
echo "  Frontend: http://localhost:5173"
echo "  API Docs: http://localhost:8000/docs"
