# Invoice to PO Matching Application

AI-powered web application for matching invoices to purchase orders in Epicor 10.2.300.11.

## Features

- **Invoice Upload & Extraction**: Support for PDF, TXT, and CSV invoice formats
- **AI-Powered Matching**: Uses OpenAI GPT-4 to intelligently match invoices to POs
- **Epicor BAQ Integration**: Fetches open purchase orders directly from Epicor
- **Multiple Invoice Types**: Handles Standard invoices, Credit Memos, and Debit Memos
- **Confidence Scoring**: AI-generated match scores with explainable reasoning
- **Manual Approval Workflow**: Review and approve matches before posting
- **Real-time Sync**: Sync purchase orders from Epicor on demand

## Architecture

```
invoice_to_PO/
├── backend/                          # FastAPI Python backend
│   ├── app/
│   │   ├── models/                   # Database models
│   │   ├── services/                 # Business logic
│   │   │   ├── epicor_service.py     # Epicor API integration
│   │   │   ├── invoice_extraction_service.py  # Invoice parsing
│   │   │   └── ai_matching_service.py         # AI matching logic
│   │   ├── routes/                   # API endpoints
│   │   │   ├── invoices.py           # Invoice endpoints
│   │   │   └── purchase_orders.py    # PO endpoints
│   │   ├── config.py                 # Configuration
│   │   └── main.py                   # FastAPI app
│   ├── requirements.txt              # Python dependencies
│   └── .env.example                  # Environment variables template
│
├── frontend/                         # React + Vite frontend
│   ├── src/
│   │   ├── pages/                    # Page components
│   │   │   ├── Dashboard.jsx         # Main dashboard
│   │   │   └── InvoiceUpload.jsx     # Upload interface
│   │   ├── components/               # Reusable components
│   │   └── App.jsx                   # Root component
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── docker-compose.yml                # (Optional) Docker setup
```

## Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database
- OpenAI API - GPT-4 for intelligent matching
- pdfplumber - PDF extraction
- requests - Epicor API client

**Frontend:**
- React 18
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - HTTP client
- React Router - Navigation

**Integration:**
- Epicor 10.2.300.11 (via REST API & BAQ)
- PostgreSQL/SQLite - Database

## Installation & Setup

### Prerequisites

- Python 3.9+
- Node.js 16+
- Epicor 10.2.300.11 instance with API access
- OpenAI API key

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   - `EPICOR_API_URL`: Your Epicor server URL
   - `EPICOR_USERNAME`: Epicor username
   - `EPICOR_PASSWORD`: Epicor password
   - `EPICOR_COMPANY`: Company code
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: PostgreSQL or SQLite connection string

3. **Initialize database:**
   ```bash
   python -c "from app.models.database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

4. **Run backend server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   API will be available at `http://localhost:8000`
   API docs: `http://localhost:8000/docs`

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```
   
   Frontend will be available at `http://localhost:5173`

## API Endpoints

### Purchase Orders
- `GET /api/purchase-orders` - List all POs
- `GET /api/purchase-orders/{po_id}` - Get PO details
- `GET /api/purchase-orders/sync-from-epicor` - Sync POs from Epicor

### Invoices
- `POST /api/invoices/upload` - Upload invoice file
- `POST /api/invoices/match/{invoice_id}` - Match invoice to PO
- `GET /api/invoices/pending-matches` - Get pending approvals
- `POST /api/invoices/approve-match/{match_id}` - Approve a match

## Workflow

1. **Sync POs**: Fetch purchase orders from Epicor BAQ
2. **Upload Invoice**: User uploads invoice (PDF, TXT, CSV)
3. **Extract Data**: System extracts invoice details (number, vendor, amount, etc.)
4. **AI Matching**: GPT-4 analyzes and matches invoice to best PO
5. **Review & Approve**: User reviews matches and approves
6. **Post to Epicor**: (Future) Automatically post approved matches to Epicor

## Configuration Details

### Epicor Integration

The app connects to Epicor via REST API using Business Activity Queries (BAQ) to:
- Fetch open purchase orders
- Check PO availability and remaining amounts
- Validate vendor information

### AI Matching Algorithm

The AI considers:
- Vendor name matching
- Invoice amount vs. PO line amount (with 5% tolerance)
- PO number references in invoice
- Invoice type (Standard, Credit Memo, Debit Memo)
- Confidence scoring (0-1)

### Database Schema

**purchase_orders**: Stores PO data from Epicor
**invoices**: Stores uploaded invoice data and extracted fields
**invoice_matches**: Records matching results with scores and approvals

## Troubleshooting

### "Connection refused" for Epicor
- Check Epicor server URL in `.env`
- Verify Epicor API is enabled
- Check firewall/network access

### PDF extraction issues
- Ensure PDF is text-based (not scanned image)
- For scanned PDFs, consider OCR integration

### AI matching returning low scores
- Verify vendor names match between invoice and PO
- Check invoice amounts are within tolerance
- Review AI reasoning in UI

## Future Enhancements

- OCR support for scanned invoices
- Batch invoice processing
- Email notification workflow
- Invoice-to-PO posting in Epicor
- Three-way matching (Invoice-PO-Receipt)
- Custom matching rules engine
- Machine learning model for improved matching
- Multi-tenant support

## Support

For issues or questions, check the API documentation at `/docs` or review logs in the backend console.

## License

MIT
