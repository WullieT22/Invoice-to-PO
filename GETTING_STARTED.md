# 🚀 Getting Started - Invoice to PO Matching

Welcome! Your AI-powered Invoice-to-PO matching application for Epicor is ready to use.

## ⚡ Quick Start (5 Minutes)

### 1️⃣ Configure Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and set these **required** values:

```env
# Epicor Configuration (Ask your Epicor administrator)
EPICOR_API_URL=http://your-epicor-server:9050/api/v2
EPICOR_USERNAME=your_epicor_username
EPICOR_PASSWORD=your_epicor_password
EPICOR_COMPANY=YOUR_COMPANY_CODE

# OpenAI Configuration (Get from https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-your-api-key-here

# Optional: Database (defaults to SQLite)
DATABASE_URL=sqlite:///./invoice_po.db

# Optional: Secret key for JWT
SECRET_KEY=your-secret-key-123
```

### 2️⃣ Start Backend (Terminal 1)

```bash
./start_backend.sh
```

Or manually:
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

✓ Backend running: **http://localhost:8000**
✓ API Docs: **http://localhost:8000/docs**

### 3️⃣ Start Frontend (Terminal 2)

```bash
./start_frontend.sh
```

Or manually:
```bash
cd frontend
npm install  # First time only
npm run dev
```

✓ Frontend running: **http://localhost:5173**

### 4️⃣ Test It!

1. Open **http://localhost:5173** in your browser
2. Click "Upload Invoice" 
3. Upload a test invoice (see TEST_DATA.md for samples)
4. System extracts data and finds matching PO
5. Review the match on Dashboard
6. Click "Approve" to confirm

---

## 📋 Using the Application

### Dashboard
- View all **pending invoice matches**
- See all **available purchase orders**
- **Approve** matches with one click
- See **match confidence scores**
- Read **AI reasoning** for each match

### Upload Invoice
- **Drag & drop** or **select** a file
- Supports: **PDF**, **TXT**, **CSV**
- Max file size: **50MB**
- Automatic data extraction
- Instant PO matching

### Workflow

```
1. Upload Invoice
   ↓
2. System Extracts Data
   ├─ Invoice number
   ├─ Vendor name
   ├─ Amount
   ├─ Date
   └─ Type (Standard/Credit/Debit)
   ↓
3. AI Matches to PO
   ├─ Finds best matches
   ├─ Calculates confidence
   ├─ Generates reasoning
   └─ Returns alternatives
   ↓
4. Review Match
   ├─ Check confidence score
   ├─ Read AI reasoning
   ├─ See matched PO details
   └─ Verify amounts match
   ↓
5. Approve or Review
   ├─ Click "Approve" if correct
   └─ Or note discrepancies
```

---

## 🔧 Configuration Details

### Required Credentials

#### Epicor Configuration
Get these from your Epicor administrator:
- **API URL**: Usually `http://[server]:9050/api/v2`
- **Username**: Your Epicor login
- **Password**: Your Epicor password
- **Company Code**: Your company code in Epicor

Test connection:
```bash
curl -u "username:password" \
  http://your-epicor-server:9050/api/v2/Erp.BO.POSvc/POHeaders
```

#### OpenAI API Key
1. Go to https://platform.openai.com/account/api-keys
2. Create a new API key
3. Copy and paste into `.env`
4. Ensure account has API credits

Test API:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk-YOUR-API-KEY"
```

### Optional Configuration

| Variable | Default | Notes |
|----------|---------|-------|
| DATABASE_URL | sqlite:///./invoice_po.db | Use PostgreSQL for production |
| SECRET_KEY | dev-secret-key | Change in production |
| DEBUG | True | Set to False in production |
| CORS_ORIGINS | localhost:5173 | Add production URLs |
| MAX_FILE_SIZE | 50MB | Maximum upload size |
| UPLOAD_DIR | ./uploads | Where to store files |

---

## 📚 Key Features Explained

### AI Matching Algorithm

The system considers multiple factors:

1. **Vendor Name** (40% weight)
   - Exact match: +0.9
   - Partial match: +0.5

2. **Amount Match** (35% weight)
   - Exact match: +0.6
   - Within 5% tolerance: +0.6
   - Within 10% tolerance: +0.3

3. **PO Reference** (20% weight)
   - Invoice contains PO number: +0.9

4. **Invoice Type** (5% weight)
   - Correct classification: +0.1

**Result**: Confidence score between 0-1
- **0.8-1.0**: High confidence (Auto-approved recommended)
- **0.6-0.8**: Medium confidence (Review recommended)
- **0.0-0.6**: Low confidence (Manual review required)

### Supported Invoice Types

- **Standard Invoice**: Normal PO invoice
- **Credit Memo**: Reduction of amount (negative)
- **Debit Memo**: Additional charge

The system automatically detects the type and handles matching accordingly.

---

## 🧪 Testing Your Setup

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
# Response: {"status": "healthy"}
```

### 2. View API Documentation

Open: **http://localhost:8000/docs**

This shows all available endpoints with test interface.

### 3. Sync POs from Epicor

```bash
curl -X GET http://localhost:8000/api/purchase-orders/sync-from-epicor
```

Should return:
```json
{
  "synced_count": X,
  "message": "Successfully synced X purchase orders"
}
```

### 4. Upload Test Invoice

Create `test.txt`:
```
Invoice: INV-001
Vendor: ACME Corp
Amount: $1000.00
Date: 01/15/2024
PO: PO-001
```

Upload via UI or API:
```bash
curl -X POST http://localhost:8000/api/invoices/upload \
  -F "file=@test.txt"
```

### 5. View Results on Dashboard

Open http://localhost:5173 and check:
- ✓ Pending matches appear
- ✓ Match scores displayed
- ✓ Can click "Approve"

---

## 🐛 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Install dependencies
```bash
cd backend
source .venv/bin/activate
pip install -r requirements.txt
```

**Error**: `Address already in use :8000`

**Solution**: Use different port or kill existing process
```bash
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
# Or use different port:
uvicorn app.main:app --port 9000
```

### Frontend won't start

**Error**: `npm: command not found`

**Solution**: Install Node.js from https://nodejs.org/

**Error**: `Cannot find module`

**Solution**: Reinstall dependencies
```bash
cd frontend
rm -rf node_modules
npm install
```

### Epicor connection fails

**Error**: `Connection refused`

**Solution**: 
1. Verify server URL is correct
2. Check if server is running: `ping your-epicor-server`
3. Check firewall allows port 9050
4. Test manually: `curl http://server:9050/api/v2`

**Error**: `Authentication failed`

**Solution**:
1. Verify username/password are correct
2. Check if user has API access in Epicor
3. Try basic auth: `curl -u "user:pass" http://server:9050/api/v2`

### OpenAI API errors

**Error**: `Invalid API key`

**Solution**: 
1. Verify key is copied correctly (no spaces)
2. Check key is active at https://platform.openai.com/account/api-keys
3. Ensure account has API credits

**Error**: `Rate limit exceeded`

**Solution**:
1. Wait a few seconds and retry
2. Upgrade plan at https://platform.openai.com/account/billing
3. Implement caching to reduce API calls

### Database errors

**Error**: `Database is locked`

**Solution**: Restart backend (SQLite gets locked sometimes)
```bash
./start_backend.sh
```

**Error**: `Connection refused` (PostgreSQL)

**Solution**: 
1. Start PostgreSQL: `brew services start postgresql`
2. Create database: `createdb invoice_po_matching`
3. Update DATABASE_URL in .env

---

## 💡 Common Tasks

### Upload Sample Invoice

1. Go to http://localhost:5173/upload
2. Click "Choose File" or drag invoice
3. Select sample from TEST_DATA.md
4. Click "Upload and Match"
5. Review results

### Sync Purchase Orders

1. Go to Dashboard
2. Check "Available Purchase Orders" section
3. POs automatically synced on startup
4. Click refresh to manually sync:
   ```bash
   curl http://localhost:8000/api/purchase-orders/sync-from-epicor
   ```

### Approve Matches

1. Go to http://localhost:5173
2. See "Pending Matches" section
3. Review match score and reasoning
4. Click "Approve" button
5. Match marked as approved

### Check API Status

```bash
# Health check
curl http://localhost:8000/health

# Get API version
curl http://localhost:8000/

# View all endpoints
curl http://localhost:8000/docs (open in browser)
```

---

## 🚢 Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

Services:
- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- Database: localhost:5432 (PostgreSQL)

### Manual Deployment

1. **Set up server** (Ubuntu/Debian)
   ```bash
   sudo apt-get update
   sudo apt-get install python3.11 nodejs npm postgresql
   ```

2. **Clone project and install**
   ```bash
   git clone <repo> && cd invoice_to_PO
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

3. **Configure** - Set .env files

4. **Run** - Use systemd/supervisor to keep services running

---

## 📖 Documentation

- **README.md** - Full project documentation
- **QUICKSTART.md** - Quick reference
- **IMPLEMENTATION_GUIDE.md** - Technical details
- **TEST_DATA.md** - Sample data and API examples
- **PROJECT_CHECKLIST.md** - What's included

---

## 🆘 Getting Help

### Check Logs

**Backend logs**: Terminal where backend is running
**Frontend logs**: Browser console (F12)
**API docs**: http://localhost:8000/docs

### Test API Endpoints

Use Swagger UI at http://localhost:8000/docs to test all endpoints.

### Review Examples

See TEST_DATA.md for:
- Sample invoices
- API request examples
- Mock responses
- Testing scenarios

---

## ✅ Checklist Before Going Live

- [ ] Epicor credentials verified and working
- [ ] OpenAI API key added and tested
- [ ] Backend starts without errors
- [ ] Frontend loads correctly
- [ ] Can upload sample invoice
- [ ] AI matching returns results
- [ ] Can approve matches
- [ ] Database is configured
- [ ] Environment variables set
- [ ] Firewall allows ports 8000 and 5173

---

## 🎉 Ready to Go!

Your application is fully set up and ready to use.

**Next steps:**
1. ✅ Configure .env file
2. ✅ Start backend and frontend
3. ✅ Upload test invoice
4. ✅ Test matching
5. ✅ Review results

For issues, check IMPLEMENTATION_GUIDE.md troubleshooting section.

**Happy matching!** 🚀
