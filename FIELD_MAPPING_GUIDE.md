# Invoice to PO Field Mapping Guide

## 🎯 How to Map Invoice Fields to PO Fields

### Step 1: Open the App
Go to: **http://172.11.0.4:8081/app.html**

### Step 2: Select "Manual Mapping" Mode
- Click on the **Manual Mapping** option (the green highlighted button)
- This allows you to manually select fields from the invoice

### Step 3: Upload Your Invoice
- Upload a PDF, image, or text file of your customer invoice
- The app will display the invoice content

### Step 4: Highlight & Map Fields
The app supports **highlight-to-map** workflow:

1. **Highlight text** in the invoice (like "Invoice #", "PO #", "Total Amount")
2. A modal will **automatically pop up**
3. The highlighted text appears in the "Invoice Field" field
4. **Select the matching PO field** from the dropdown
5. **Save the mapping**

### Available PO Fields to Map To:

| PO Field | Description | Example |
|----------|-------------|---------|
| **invoice_number** | Invoice ID | INV-2024-001 |
| **invoice_date** | Invoice date | 02/14/2026 |
| **vendor_name** | Supplier name | ABC Corp |
| **vendor_id** | Supplier ID | VENDOR-123 |
| **po_number** | Purchase order number | PO-456789 |
| **invoice_amount** | Total invoice amount | $5,000.00 |
| **line_amount** | Amount per line item | $1,000.00 |
| **description** | Line item description | Widget Assembly |
| **line_number** | PO line number | 1 |
| **quantity** | Item quantity | 100 |
| **unit_price** | Price per unit | $50.00 |
| **tax_amount** | Tax amount | $400.00 |

### Step 5: Create a Template for This Customer

Once you've mapped all the fields:

1. Enter a **Template Name** (e.g., "ABC Corp Standard Format")
2. Click **💾 Save Template**
3. The template is saved locally on your computer

### Step 6: Use the Template for Future Invoices from the Same Customer

For the **next invoice** from this customer:

1. Go back to app.html
2. Under **"Have an Existing Template?"** section
3. **Select your saved template** (e.g., "ABC Corp Standard Format")
4. **Upload the new invoice file**
5. The system **automatically applies the same field mappings**
6. Skip straight to matching!

---

## 📋 Workflow Example

### First Invoice from ABC Corp
```
1. Upload invoice → Manual Mapping
2. Highlight "Invoice #12345" → Map to invoice_number
3. Highlight "PO-456789" → Map to po_number  
4. Highlight "$5,000" → Map to invoice_amount
5. ... map other fields ...
6. Save as Template "ABC Corp - Standard"
```

### Second Invoice from ABC Corp (Same Format)
```
1. Select Template "ABC Corp - Standard"
2. Upload new PDF
3. Mappings automatically applied ✅
4. Go straight to matching! 🚀
```

---

## 🎨 Field Mapping Tips

### Do:
✅ Create a **separate template for each customer** (each has different invoice format)  
✅ Name templates clearly: "CustomerName - MonthYear" or "Vendor-Format-Type"  
✅ Save templates after mapping **all essential fields** (at minimum: PO#, Amount, Date)  
✅ **Highlight exactly** the value you want to map (not the label)  

### Don't:
❌ Don't try to use same template for different customers  
❌ Don't highlight labels like "Invoice #" - highlight the actual number  
❌ Don't map fields you won't use  

---

## 📝 Fields You Should Always Map

For reliable PO matching, map these 4 fields minimum:

1. **po_number** - Critical for matching invoices to purchase orders
2. **invoice_number** - Identifies the invoice in your system
3. **invoice_amount** - Validates against PO
4. **invoice_date** - Important for aging and reconciliation

---

## 💾 Using Saved Templates

### View All Templates
Templates are saved automatically in your browser's local storage.

### Delete a Template
Templates are stored locally - if you want to remove one, you can clear browser data or contact support.

### Share Templates
To move templates to another computer:
1. Export templates from browser (via Developer Tools → Local Storage)
2. Import on new computer

---

## 🔄 Complete Workflow After Field Mapping

### After Mapping & Matching:

1. **Review Matches** - See which PO each invoice matched to
2. **Approve** - Confirm the match is correct ✅
3. **Reject** - If incorrect, opt for manual PO selection
4. **Auto-Sync to Epicor** - Approved matches sync back to your Epicor system

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Highlight not working | Make sure you're in "Manual Mapping" mode |
| Template not appearing | Refresh the page and check template list |
| Same fields appearing in different places | Create customer-specific template with correct positions |
| Can't select from dropdown | Ensure you've highlighted text first |

---

## 📌 Summary

**For Customer "ABC Corp":**
1. First invoice → Manual highlight & map → Save as template
2. All future invoices → Auto-apply template → Skip to matching
3. Time savings: ~5 mins per invoice → ~30 seconds per invoice!

This method allows you to handle multiple customers with different invoice formats while only setting up once per customer!

