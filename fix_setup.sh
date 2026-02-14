#!/bin/bash

echo "========================================"
echo "   Invoice to PO - Fix & Setup Script   "
echo "========================================"

# 1. Fix Permissions
echo "[1/4] Making scripts executable..."
chmod +x start_all.sh start_backend.sh start_frontend.sh

# 2. Backend Setup
echo "[2/4] Setting up Backend..."
cd backend

# Create .env if missing
if [ ! -f .env ]; then
    echo "      Creating .env file..."
    cp .env.example .env
fi

# Install Python dependencies
echo "      Installing Python requirements..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Frontend Setup
echo "[3/4] Setting up Frontend..."
cd ../frontend
echo "      Installing Node modules..."
npm install

# Ensure vite is installed and executable
if [ ! -f "node_modules/.bin/vite" ]; then
    echo "      ⚠️  Vite not found. Installing explicitly..."
    npm install vite --save-dev
fi

# Fix postcss.config.js for ES Module support (fixes "module is not defined" error)
echo "      ⚙️  Fixing postcss.config.js..."
cat > postcss.config.js <<EOF
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF

# Fix tailwind.config.js for ES Module support
echo "      ⚙️  Fixing tailwind.config.js..."
cat > tailwind.config.js <<EOF
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
EOF

# 4. Ready
echo "========================================"
echo "   ✅ Setup Complete!                   "
echo "========================================"
echo ""
echo "Now try running the app again:"
echo "  ./start_all.sh"
echo ""
echo "If that still fails, run these commands manually in two separate terminals:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source .venv/bin/activate"
echo "  uvicorn app.main:app --reload"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"