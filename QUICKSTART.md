# Quick Start Guide

## Prerequisites
- Python 3.9+
- Node.js 16+
- Epicor 10.2.300.11 API access
- OpenAI API key

## Step-by-Step Setup

### 1. Configure Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and fill in:
```
EPICOR_API_URL=http://your-epicor-server:9050/api/v2
EPICOR_USERNAME=your_epicor_username
EPICOR_PASSWORD=your_epicor_password
EPICOR_COMPANY=your_company_code
OPENAI_API_KEY=sk-your-openai-api-key
DATABASE_URL=sqlite:///./invoice_po.db  # or PostgreSQL URL
```

### 2. Start Backend (Terminal 1)

```bash
cd backend
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend running at: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### 3. Start Frontend (Terminal 2)

```bash
cd frontend
npm install  # First time only
npm run dev
```

Frontend running at: **http://localhost:5173**

## Testing the Workflow

### 1. Sync Purchase Orders from Epicor

```bash
curl -X GET http://localhost:8000/api/purchase-orders/sync-from-epicor
```

### 2. Upload an Invoice

Create a test invoice file (PDF, TXT, or CSV) and upload via the web UI at http://localhost:5173/upload

Or via API:
```bash
curl -X POST http://localhost:8000/api/invoices/upload \
  -F "file=@/path/to/invoice.pdf"
```

### 3. View Dashboard

Navigate to http://localhost:5173 to see:
- Pending invoice matches
- Available purchase orders
- Match scores and AI reasoning

### 4. Approve Matches

Click "Approve" on any pending match to approve it.

## API Endpoints Quick Reference

```
# Purchase Orders
GET  /api/purchase-orders                        - List all POs
GET  /api/purchase-orders/{po_id}               - Get PO details
GET  /api/purchase-orders/sync-from-epicor      - Sync from Epicor

# Invoices
POST /api/invoices/upload                       - Upload invoice
POST /api/invoices/match/{invoice_id}           - Match to PO
GET  /api/invoices/pending-matches              - Get pending
POST /api/invoices/approve-match/{match_id}     - Approve match

# System
GET  /health                                    - Health check
GET  /docs                                      - API documentation
GET  /redoc                                     - ReDoc documentation
```

## Database Setup

The app auto-creates database tables on first run. For manual setup:

```bash
python -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.9+)
- Check dependencies: `pip list | grep fastapi`
- Check port 8000 isn't already in use

### Frontend won't start
- Check Node version: `node --version` (need 16+)
- Delete `node_modules` and run `npm install` again
- Clear npm cache: `npm cache clean --force`

### Epicor connection fails
- Verify Epicor server is running and accessible
- Check EPICOR_API_URL format in .env
- Test manually: `curl http://your-epicor-server:9050/api/v2`

### OpenAI API errors
- Verify API key is valid and has credits
- Check API key permissions in OpenAI dashboard
- Monitor usage at https://platform.openai.com/account/usage

## Docker Deployment

Build and run with Docker:

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database
- Backend API on port 8000
- Frontend on port 5173

Stop: `docker-compose down`

## Next Steps

1. ✅ Verify both servers are running
2. ✅ Sync POs from Epicor
3. ✅ Upload a test invoice
4. ✅ Review AI-matched results
5. ✅ Approve matches

For detailed documentation, see README.md
