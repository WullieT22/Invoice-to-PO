#!/bin/bash

echo "========================================"
echo "   Epicor Connection Setup              "
echo "========================================"
echo "Configuring for server: 199.5.83.159"
echo "User: WESTS"
echo ""

EPICOR_COMP="EPIC06"
EPICOR_PASS="Westfield"
echo ""

# Write to .env file
cd backend

# Create backup if exists
if [ -f .env ]; then
    cp .env .env.bak
fi

# Update/Create .env
cat > .env <<EOF
EPICOR_API_URL=https://199.5.83.159/EpicorERP/api/v1
EPICOR_USERNAME=WESTS
EPICOR_PASSWORD=$EPICOR_PASS
EPICOR_COMPANY=$EPICOR_COMP
EPICOR_BAQ_ID=PO_Test

# Keep existing OpenAI key if possible, otherwise placeholder
OPENAI_API_KEY=sk-placeholder-key-replace-me
AI_MODEL=gpt-4-turbo-preview
EOF

echo "✅ Configuration saved to backend/.env"
echo "   Running connection test..."
python3 test_connection.py