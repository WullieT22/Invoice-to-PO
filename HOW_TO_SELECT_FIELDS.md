# How to Select & Map Image Invoice Areas to PO Fields

## 🖼️ Understanding the Process

When you upload a **scanned image** of an invoice, the app does 2 things simultaneously:

1. **Shows the image preview** on the LEFT (so you can see where the field is)
2. **Extracts all text** from the image on the RIGHT (so you can highlight and map)

You don't click ON the image - you **highlight the extracted text** on the right side!

---

## ✅ Step-by-Step Guide

### Step 1: Upload Your Scanned Invoice Image

```
1. Go to http://172.11.0.4:8081/app.html
2. Click "Auto OCR" button (purple)
3. Click the "Upload Invoice" area
4. Select your scanned image (JPG, PNG, etc.)
5. Wait 3-5 seconds for OCR to extract text
```

**What you'll see:**
- LEFT SIDE: Your invoice image preview (with zoom buttons)
- RIGHT SIDE: All extracted text in a scrollable box

---

### Step 2: Identify What You Want to Map

**Examples from your invoice:**

```
INVOICE IMAGE shows:
━━━━━━━━━━━━━━━━━━━
Invoice #: 12345
Date: 02/14/2026
PO #: PO-456789
Total: $5,400.00
━━━━━━━━━━━━━━━━━━━

RIGHT SIDE (Extracted Text) shows:
"Invoice 12345 Date 02/14/2026 PO PO-456789 Total 5400.00"
```

---

### Step 3: Highlight the Text Value (Not the Label!)

**IMPORTANT:** Highlight only the VALUE, not the label!

#### ❌ WRONG:
```
Don't highlight: "Invoice #"  or  "Invoice #12345"
```

#### ✅ CORRECT:
```
DO highlight: "12345"  (just the number)
```

---

### EXAMPLE: Mapping Invoice Number

#### What to do:

1. **Look at the extracted text on the RIGHT** (the scrollable box)
2. **Find the invoice number value** (e.g., "12345")
3. **Click and drag to highlight** just that value: `12345`
4. **Release the mouse**

#### What happens automatically:

- A **modal (popup) appears** automatically! 
- The highlighted text (`12345`) is placed in the **"Invoice Field:"** box
- You see a dropdown list of **PO fields to choose from**
- Select **`invoice_number`** from the dropdown
- Click **"Save"** button
- ✅ Done! The mapping is saved!

---

## 🎯 Complete Example Walkthrough

### Your Scanned Invoice Contains:

```
╔═══════════════════════════════════════╗
║         ABC CORP INVOICE              ║
╟───────────────────────────────────────╢
║ Invoice Number: INV-2024-456          ║
║ Date: February 14, 2026               ║
║ PO Number: PO-789123                  ║
╟───────────────────────────────────────╢
║ ITEMS:                                ║
║  Qty    Description      Price        ║
║  100    Widget Assembly   $50.00       ║
║  50     Fasteners        $10.00       ║
╟───────────────────────────────────────╢
║ Subtotal:              $6,000.00      ║
║ Tax (8%):                $480.00      ║
║ Total Due:             $6,480.00      ║
╚═══════════════════════════════════════╝
```

### What the App Shows:

**LEFT SIDE (Image Preview):**
Shows your full invoice image with zoom buttons

**RIGHT SIDE (Extracted Text Box):**
```
ABC CORP INVOICE
Invoice Number INV-2024-456
Date February 14 2026
PO Number PO-789123
ITEMS
Qty Description Price
100 Widget Assembly 50.00
50 Fasteners 10.00
Subtotal 6000.00
Tax 8% 480.00
Total Due 6480.00
```

---

### Highlighting & Mapping Steps:

#### Mapping 1: Invoice Number ✅

1. **Read the RIGHT side text** - Find the invoice number value
2. **Highlight** `INV-2024-456` on the right side
3. Modal appears
4. **Select dropdown:** `invoice_number`
5. **Click Save** ✅

#### Mapping 2: Date ✅

1. **Highlight** `February 14 2026` on the right side
2. Modal appears
3. **Select dropdown:** `invoice_date`
4. **Click Save** ✅

#### Mapping 3: PO Number ✅

1. **Highlight** `PO-789123` on the right side
2. Modal appears
3. **Select dropdown:** `po_number`
4. **Click Save** ✅

#### Mapping 4: Quantity ✅

1. **Highlight** `100` on the right side
2. Modal appears
3. **Select dropdown:** `quantity`
4. **Click Save** ✅

#### Mapping 5: Description ✅

1. **Highlight** `Widget Assembly` on the right side
2. Modal appears
3. **Select dropdown:** `description`
4. **Click Save** ✅

#### Mapping 6: Unit Price ✅

1. **Highlight** `50.00` on the right side (the individual price)
2. Modal appears
3. **Select dropdown:** `unit_price`
4. **Click Save** ✅

#### Mapping 7: Total Amount ✅

1. **Highlight** `6480.00` on the right side
2. Modal appears
3. **Select dropdown:** `invoice_amount`
4. **Click Save** ✅

---

## 📋 Quick Reference: What to Highlight

### For Each PO Field, Highlight This:

| PO Field | What to Highlight | Example |
|----------|-------------------|---------|
| **invoice_number** | Just the ID number | `INV-2024-456` (not "Invoice #") |
| **invoice_date** | Just the date | `February 14 2026` |
| **vendor_name** | Just the company name | `ABC CORP` |
| **po_number** | Just the PO number | `PO-789123` (not "PO #") |
| **quantity** | Just the number | `100` |
| **description** | Just the item name | `Widget Assembly` |
| **unit_price** | Just the price | `50.00` (not "$50.00") |
| **line_amount** | Just the line total | `5000.00` |
| **invoice_amount** | Just the total | `6480.00` |
| **tax_amount** | Just the tax | `480.00` |

---

## 🎨 Visual Highlighting Tips

### How to Highlight Text:

1. **Click and drag** across the text you want to select
2. **Text turns blue/highlighted** when selected
3. **Release mouse** - modal pops up automatically
4. The **selected text** appears in the "Invoice Field" box
5. Choose the **matching PO field** from dropdown
6. Click **Save**

### If highlighting doesn't work:

- Make sure you're highlighting in the **RIGHT side text box** (not the image)
- **Triple-click** a word to select it
- **Click-drag** to select multiple words
- The text should turn blue/highlighted

---

## ⚡ Quick Workflow

```
STEP 1: Upload image
        ↓
STEP 2: OCR extracts text (shows on RIGHT)
        ↓
STEP 3: For each field:
        - Highlight value on RIGHT side
        - Modal pops up
        - Select PO field from dropdown
        - Click Save
        ↓
STEP 4: Repeat until all fields are mapped
        ↓
STEP 5: Save as Template
        ↓
STEP 6: Done! ✅
```

---

## 💡 Pro Tips

### Tip 1: Use Zoom to Check Image
- If unsure which text corresponds to which value
- Use **zoom controls** on LEFT side to see the image better
- Find the field location in the image
- Then highlight the matching value on RIGHT side

### Tip 2: If OCR Misread Text
- Numbers like:
  - `0` might read as `O` (letter O)
  - `1` might read as `l` (letter L)  
  - `8` might read as `B`
- If wrong, manually edit in the modal popup
- Or highlight the correct portion

### Tip 3: Multiple Items
- If invoice has multiple line items
- You can create separate mappings for:
  - **First item:** qty=100, description=Widget
  - **Second item:** qty=50, description=Fasteners
- Or just map quantities/descriptions you want

### Tip 4: Not All Fields Needed
- You can skip fields you don't need
- Minimum recommended: `invoice_number`, `po_number`, `invoice_amount`
- Map as many or as few as needed

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't highlight text | Scroll in the RIGHT text box first, or try triple-clicking a word |
| Modal doesn't appear | Make sure you're highlighting text in the RIGHT box (not image) |
| Wrong text highlighted | Click elsewhere to deselect, then try again |
| OCR missing text | Scroll down in RIGHT box - text might be below |
| Text looks wrong | Use zoom to verify in image, edit in modal if needed |
| Can't find a value | Scroll through image using LEFT side zoom/scroll |

---

## 📝 Your First Invoice Mapping

**Right Now:**

1. Upload your scanned image
2. Wait for OCR to extract text
3. Highlight the **first field value** (e.g., invoice number)
4. Modal pops up - **select the matching PO field**
5. Click Save
6. **Repeat** for remaining fields
7. Once all mapped → **Save as Template**

**Next invoice from same customer:**
- Select saved template
- Upload
- Done! Fields auto-apply! ⚡

You've got this! 🚀

