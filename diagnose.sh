#!/bin/bash

echo "========================================"
echo "   Invoice to PO - Diagnostic Script    "
echo "========================================"
echo ""
echo "Checking the status of required ports..."
echo ""

# --- Check Backend Port 8000 ---
echo "🔎 Checking Backend Port (8000)..."
if lsof -i :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "   ✅ Port 8000 is IN USE. The backend server is likely running."
    echo "      Process using port 8000:"
    lsof -i :8000 -sTCP:LISTEN | grep LISTEN
else
    echo "   ❌ Port 8000 is FREE. The backend server is NOT running."
    echo "      To start it, run this in a new terminal:"
    echo "      ./start_backend.sh"
fi
echo ""

# --- Check Frontend Port 5173 ---
echo "🔎 Checking Frontend Port (5173)..."
if lsof -i :5173 -sTCP:LISTEN -t >/dev/null ; then
    echo "   ✅ Port 5173 is IN USE. The frontend server is likely running."
    echo "      Process using port 5173:"
    lsof -i :5173 -sTCP:LISTEN | grep LISTEN
else
    echo "   ❌ Port 5173 is FREE. The frontend server is NOT running."
    echo "      To start it, run this in a new terminal:"
    echo "      ./start_frontend.sh"
fi
echo ""

# --- Final Advice ---
echo "========================================"
echo "                 Summary                "
echo "========================================"
echo "The 'site cannot be reached' error means your browser cannot connect to http://localhost:5173."
echo ""
echo "Based on the checks above:"
echo "1. If a port is FREE, the server for it is NOT running. You must start it."
echo "2. If a port is IN USE, check the terminal window for that server for any error messages."
echo "3. If you can't find the running process, you can force it to stop with: kill -9 <PID>"