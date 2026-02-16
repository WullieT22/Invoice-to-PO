# Manual Selection Tool Guide

## Overview
The Manual Selection Tool allows you to visually select specific areas on your invoice image and extract text from those areas. This is perfect when you have scanned invoices where you need to extract data from specific field regions.

## How to Use Manual Selection (Image Invoices)

### Step 1: Upload Your Invoice Image
1. Click on the upload area or select a file
2. Choose your invoice image (JPG, PNG, WebP, etc.)
3. The image will appear on the left side of the preview

### Step 2: Switch to Manual Mode
1. Look for the mode buttons at the top of the preview area
2. Click on **"Manual Selection"** mode button (shows "✋ Manual Mode")
3. You'll see the system switch to crosshair cursor for drawing

### Step 3: Draw Selection Boxes
1. Move your mouse to the area on the image where the field data is located
2. **Click and drag** to draw a rectangular box around the text you want to extract
3. Release the mouse - the system will automatically:
   - Extract text from that region using OCR
   - Display the extracted text on the right side with label "[SELECTED AREA]"
   - Open a field mapping modal (if needed)

### Step 4: Map Extracted Text to PO Fields
When text is extracted from a selected area:
1. A field mapping dialog appears showing the extracted text
2. Select which PO field this text represents:
   - `invoice_number` - Invoice number/ID
   - `invoice_date` - Invoice date
   - `vendor_name` - Vendor/Supplier name
   - `vendor_id` - Vendor ID code
   - `po_number` - Purchase Order number
   - `invoice_amount` - Total invoice amount
   - `line_amount` - Line item amount
   - `description` - Line item description
   - `line_number` - Line item number
   - `quantity` - Item quantity
   - `unit_price` - Price per unit
   - `tax_amount` - Tax amount

3. Click "Map Field" to save the mapping
4. Repeat for other fields on the invoice

### Step 5: Using Zoom Control (for Large Images)
Since scanned invoices are often larger than the preview box:

- **🔍+ Zoom In** - Enlarge the image to see small text better
- **🔍- Zoom Out** - Reduce the image size
- **↔️ Fit** - Reset zoom to fit entire image
- Zoom level percentage displays in top right

### Step 6: Save Template and Batch Process
1. Once you've mapped all fields, click "Save Template"
2. Give your template a name (e.g., "Acme Corp Invoices")
3. Use this template to process multiple similar invoices without remapping

## Tips for Best Results

### When to Use Manual Selection
- ✅ Scanned image invoices where text is clear
- ✅ Invoices with non-standard layouts
- ✅ When you need precise control over what fields are extracted
- ✅ When OCR mode has issues with specific areas

### When to Use Auto OCR
- ✅ Digital/native PDF invoices
- ✅ When you want to extract all text at once
- ✅ High-quality scans with clear text
- ✅ For quick batch processing with templates

### Selection Tips
1. **Draw clear boxes** - The larger and more clearly you define the box, the better the OCR accuracy
2. **Zoom in first** - For small or dense text, zoom in before drawing
3. **One field per selection** - Select each field separately for best results
4. **Minimum size** - Selection boxes must be at least 10x10 pixels

## Common Issues

### "Selection too small"
- Draw a larger box around the text area
- Make sure the box contains the complete text you want to extract

### "Empty area - no text detected"
- The area you selected doesn't have readable text
- Try zooming in and selecting again with more clear text visible
- Check that the image isn't blurry or too faded

### Text not extracting correctly
- Try zooming in to the area for better OCR accuracy
- Make sure text is right-side-up in the image
- Select only the readable portion (exclude borders/marks)

## Keyboard Shortcuts
- None currently implemented, but you can use:
  - **Mouse scroll** - Scroll through extracted text on the right
  - **Highlight text** - Click and drag on the right side to select text for quick mapping

## Workflow Example

```
1. Upload scanned invoice → 
2. Select Manual mode → 
3. Draw box around "Invoice #" field → 
4. See extracted number on right → 
5. Map to "invoice_number" field → 
6. Draw box around "Date" field → 
7. See extracted date on right → 
8. Map to "invoice_date" field → 
9. Repeat for other fields → 
10. Save template → 
11. Use template for batch processing similar invoices
```

## Next Steps
- Save your template for reuse
- Use batch processing to process multiple similar invoices
- See the [GETTING_STARTED.md](GETTING_STARTED.md) for complete workflow
