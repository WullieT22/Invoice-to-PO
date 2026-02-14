#!/usr/bin/env bash
# Quick start script for Invoice to PO Matching app

echo "Invoice to PO Matching - Quick Start"
echo "===================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Please install Node.js 16+"
    exit 1
fi

# Backend setup
echo ""
echo "Setting up backend..."
cd backend
pip install -r requirements.txt

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - please configure it with your Epicor and OpenAI credentials"
fi

# Frontend setup
echo ""
echo "Setting up frontend..."
cd ../frontend
npm install

echo ""
echo "Setup complete!"
echo ""
echo "To start the application:"
echo "1. Terminal 1 - Backend: cd backend && uvicorn app.main:app --reload"
echo "2. Terminal 2 - Frontend: cd frontend && npm run dev"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
