# Test Data & Examples

## Sample Test Invoices

### Test Invoice 1 (Standard Invoice)

Create `test_invoice_1.txt`:

```
ACME Corporation
123 Business Street
New York, NY 10001

Invoice Number: INV-2024-001001
Invoice Date: 01/15/2024
Due Date: 02/15/2024

Bill To:
Your Company Name
456 Commerce Ave
Chicago, IL 60601

---

Item Description          Qty    Unit Price    Total
---
Office Supplies          100        $25.00    $2,500.00
Shipping                   1        $50.00       $50.00

---

Subtotal:                                    $2,550.00
Tax (8%):                                      $204.00
TOTAL AMOUNT DUE:                            $2,754.00

PO: PO-2024-1001
```

### Test Invoice 2 (Credit Memo)

Create `test_invoice_2.txt`:

```
ACME Corporation
Credit Memo

Memo Number: CM-2024-001
Date: 02/10/2024

For Invoice: INV-2024-000998
Original Amount: $1,500.00

Reason for Credit:
Damaged goods - Return authorization #12345

Credit Amount: -$150.00

Previous Invoice PO: PO-2024-998
```

### Test Invoice 3 (PDF Example - text content)

For a PDF, you would typically extract this text:

```
VENDOR SUPPLY INC
Vendor Reference: VS-12345

INVOICE

Invoice #: INV-VS-0024587
Date: 12/20/2023
Terms: Net 30

Customer: Your Company
Account: ACC-5678

Line Items:
Item          Description           Qty   Price      Amount
SKU-001      Computer Monitors      5     $299.99    $1,499.95
SKU-002      Keyboards              5     $89.99     $449.95
Freight                             1     $100.00    $100.00

Subtotal:                                          $2,049.90
Sales Tax:                                         $163.99
Total Due:                                        $2,213.89

PO Reference: PO-2023-5678
Invoice Link to PO
```

## Sample API Requests

### 1. Sync Purchase Orders

```bash
curl -X GET http://localhost:8000/api/purchase-orders/sync-from-epicor \
  -H "Accept: application/json"

# Response:
{
  "synced_count": 25,
  "message": "Successfully synced 25 purchase orders"
}
```

### 2. Upload Invoice

```bash
curl -X POST http://localhost:8000/api/invoices/upload \
  -F "file=@test_invoice_1.txt" \
  -H "Accept: application/json"

# Response:
{
  "invoice_id": 1,
  "invoice_number": "INV-2024-001001",
  "vendor_name": "ACME Corporation",
  "amount": 2754.00,
  "type": "Standard"
}
```

### 3. Match Invoice to PO

```bash
curl -X POST http://localhost:8000/api/invoices/match/1 \
  -H "Accept: application/json"

# Response:
{
  "match_id": 1,
  "invoice_id": 1,
  "po_number": "PO-2024-1001",
  "match_score": 0.95,
  "reasoning": "Exact vendor match; Amount match (difference: $4.00); Exact PO number in invoice",
  "requires_approval": false
}
```

### 4. View Pending Matches

```bash
curl -X GET http://localhost:8000/api/invoices/pending-matches \
  -H "Accept: application/json"

# Response:
[
  {
    "match_id": 2,
    "invoice_number": "INV-2024-001002",
    "po_number": "PO-2024-1002",
    "amount": 1500.00,
    "score": 0.82,
    "reasoning": "Partial vendor match; Amount within tolerance"
  }
]
```

### 5. Approve Match

```bash
curl -X POST http://localhost:8000/api/invoices/approve-match/2 \
  -H "Accept: application/json"

# Response:
{
  "message": "Match approved successfully"
}
```

### 6. Get All Purchase Orders

```bash
curl -X GET http://localhost:8000/api/purchase-orders \
  -H "Accept: application/json"

# Response:
[
  {
    "po_id": 1,
    "po_number": "PO-2024-1001",
    "po_line": 1,
    "vendor_name": "ACME Corporation",
    "description": "Office Supplies",
    "line_amount": 2500.00,
    "remaining_amount": 2500.00,
    "due_date": "2024-02-15"
  }
]
```

## Environment Setup for Testing

### Create Test .env

```bash
cd backend
cat > .env << EOF
EPICOR_API_URL=http://localhost:9050/api/v2
EPICOR_USERNAME=testuser
EPICOR_PASSWORD=testpass
EPICOR_COMPANY=EPICOR001
OPENAI_API_KEY=sk-test-key-here
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=test-secret-key
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
MAX_FILE_SIZE=52428800
UPLOAD_DIR=./test_uploads
EOF
```

## Mock Data for Epicor BAQ

If you want to test without a live Epicor instance, you can mock the response:

### Mock Purchase Orders Response

```json
{
  "value": [
    {
      "PONum": "PO-2024-1001",
      "POLine": 1,
      "VendorNum": "V-001",
      "VendorName": "ACME Corporation",
      "LineDesc": "Office Supplies",
      "LineTotal": 2500.00,
      "ReceiptTotalCost": 0.00,
      "DueDate": "2024-02-15"
    },
    {
      "PONum": "PO-2024-1002",
      "POLine": 1,
      "VendorNum": "V-002",
      "VendorName": "VENDOR SUPPLY INC",
      "LineDesc": "Computer Equipment",
      "LineTotal": 2213.89,
      "ReceiptTotalCost": 0.00,
      "DueDate": "2024-01-30"
    }
  ]
}
```

## Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads at localhost:5173
- [ ] API docs accessible at localhost:8000/docs
- [ ] Can sync POs from Epicor
- [ ] Can upload test invoice (TXT)
- [ ] AI matching returns results
- [ ] Can approve matches
- [ ] Dashboard shows pending matches
- [ ] Confidence scores are reasonable (0-1)
- [ ] Error handling works (try invalid file)

## Performance Testing

### Load Test with Apache Bench

```bash
# Test 100 concurrent requests
ab -n 100 -c 10 http://localhost:8000/api/purchase-orders/

# For upload simulation (create test file first)
# Note: ab doesn't support multipart, use wrk or jmeter for file uploads
```

### Memory & CPU Monitoring

```bash
# Monitor backend process
watch -n 1 'ps aux | grep uvicorn'

# Monitor frontend build
npm run build  # Check build size
du -sh dist/
```

## Debugging Tips

### Backend Logging

Add to any service:

```python
import logging
logger = logging.getLogger(__name__)

logger.info(f"Processing invoice: {invoice_id}")
logger.debug(f"Match score: {score}")
logger.error(f"Error: {str(e)}")
```

### Frontend Debugging

In browser console:

```javascript
// Check API calls
console.log('API Base:', 'http://localhost:8000/api');

// Check response
axios.get('/api/purchase-orders').then(r => console.log(r.data))
```

### Database Inspection

```bash
# For SQLite
sqlite3 invoice_po.db
sqlite> .tables
sqlite> SELECT * FROM purchase_orders LIMIT 5;

# For PostgreSQL
psql -d invoice_po_matching
\dt                    # List tables
SELECT * FROM purchase_orders LIMIT 5;
```

## Common Test Scenarios

### Scenario 1: Perfect Match
- Invoice with exact vendor name
- Amount matches exactly
- Contains PO number
- Expected: 0.95+ score

### Scenario 2: Fuzzy Match
- Vendor name is similar (typo)
- Amount within 5% tolerance
- No PO reference
- Expected: 0.70-0.85 score

### Scenario 3: No Match
- Unknown vendor
- Amount completely different
- No PO reference
- Expected: 0.0-0.30 score

### Scenario 4: Credit Memo
- Text contains "Credit Memo"
- Amount is negative or reduction
- References original invoice
- Expected: Detected as Credit Memo type

### Scenario 5: Multiple POs Same Vendor
- Multiple open POs from same vendor
- Invoice amount matches one PO exactly
- AI should pick the matching one
- Expected: Score based on best match

---

**Ready to test?** Use these examples to validate your setup!
