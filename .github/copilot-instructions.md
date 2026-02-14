<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Invoice to PO Matching Application Setup

This is an AI-powered invoice-to-PO matching system for Epicor 10.2.300.11 with:
- FastAPI backend with Epicor BAQ integration
- React frontend with Vite
- OpenAI GPT-4 for intelligent matching
- Support for multiple invoice types (Standard, Credit Memo, Debit Memo)

### Project Structure
- `/backend` - Python FastAPI application
- `/frontend` - React + Vite application  
- `/uploads` - Invoice file storage

### Development Setup

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Configure .env with Epicor and OpenAI credentials
   uvicorn app.main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Key Features
- Upload invoices (PDF, TXT, CSV)
- Extract invoice data automatically
- Match invoices to POs using AI
- Review and approve matches
- Sync POs from Epicor BAQ

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Configuration
- Update `backend/.env` with:
  - Epicor API credentials
  - OpenAI API key
  - Database URL
  - CORS settings

### Testing the Workflow
1. Sync POs: `GET /api/purchase-orders/sync-from-epicor`
2. Upload invoice: `POST /api/invoices/upload`
3. Match to PO: `POST /api/invoices/match/{invoice_id}`
4. View pending: `GET /api/invoices/pending-matches`
5. Approve: `POST /api/invoices/approve-match/{match_id}`
