# How to Map IMAGE Invoices (JPG, PNG, etc.)

## 🖼️ Working with Image Invoices

Your app supports image invoices with **OCR (Optical Character Recognition)** - it reads text from images automatically!

---

## Step-by-Step Guide for Image Invoices

### Option 1: **Auto OCR Mode** (Recommended for First Setup)

This mode automatically reads all text from the image.

#### Steps:

1. **Open the app** → http://172.11.0.4:8081/app.html

2. **Select "Auto OCR" mode** (the purple button)
   - This uses AI to automatically extract text from images

3. **Upload your invoice image** (JPG, PNG, WebP)
   - Click on the upload area or drag & drop
   - Wait 3-5 seconds while OCR reads the image

4. **View the extracted text** 
   - All text from the image appears in the text box
   - The OCR reads everything it can see

5. **Highlight fields you need to map**
   - Look for: Invoice Number, PO Number, Amount, Date, etc.
   - **Highlight just that value** (e.g., highlight "12345" not "Invoice #12345")
   - A modal automatically appears
   - Choose the matching PO field
   - Save

6. **Save as Template** once you've mapped the key fields

---

### Option 2: **Manual Mode** (For More Control)

If OCR misreads something or you want more control:

1. **Select "Manual Mapping" mode** (blue button)

2. **Upload your image**

3. **Manually highlight** the exact areas of text you see in the image
   - Highlight the invoice number value
   - Highlight the PO number value
   - Highlight the amount
   - etc.

4. **Map each highlight** to a PO field

5. **Save as Template**

---

## 📝 Example: Processing an Image Invoice

### Your Invoice Image Shows:

```
━━━━━━━━━━━━━━━━━━━━━
     ABC CORP
━━━━━━━━━━━━━━━━━━━━━

INVOICE # 12345
DATE: 02/14/2026
PO # PO-456789

SHIP TO:
Megastore Distribution
123 Main St
City, ST 12345

LINE ITEMS:
Qty: 100
Part: Widget Assembly
Price: $50.00 each
Total: $5,000.00

TAX: $400.00
TOTAL: $5,400.00

━━━━━━━━━━━━━━━━━━━━━
```

### Mapping Steps:

1. **Auto OCR reads the entire image**
   - All the text above appears in the text box

2. **Highlight "12345"** → Map to `invoice_number`

3. **Highlight "02/14/2026"** → Map to `invoice_date`

4. **Highlight "PO-456789"** → Map to `po_number`

5. **Highlight "100"** → Map to `quantity`

6. **Highlight "Widget Assembly"** → Map to `description`

7. **Highlight "50.00"** → Map to `unit_price`

8. **Highlight "5400.00"** → Map to `invoice_amount`

9. **Save as Template "ABC Corp - Image Format"**

### For Next ABC Corp Image Invoice:
- Select template → Upload → Done! ✅

---

## 🎯 Key Tips for Image Invoices

### ✅ DO:

1. **Make sure image is clear** - Good lighting, not blurry
2. **Use JPG or PNG format** - Clearest results
3. **Highlight only the VALUE** - Not the label
4. **Verify OCR accuracy** - Check if numbers were read correctly
   - Sometimes "0" reads as "O" (letter O)
   - Sometimes "1" reads as "l" (letter L)
   - If OCR misread, manually fix in the mapping

### ❌ DON'T:

- Don't use blurry/faded images - OCR won't read them
- Don't use PDF scans - Use image file directly
- Don't highlight labels like "Invoice #" - highlight the number only
- Don't try to map handwritten fields - OCR can't read handwriting well

---

## ⚡ Quick Comparison: Auto OCR vs Manual

| Feature | Auto OCR | Manual |
|---------|----------|--------|
| Speed | Fast (3-5 sec) | Slower (needs each highlight) |
| Accuracy | Good if image is clear | Very accurate |
| Best for | Clear printed invoices | Unclear/faded invoices |
| Learning curve | Easy | Moderate |

**Recommendation:** Start with **Auto OCR** for clear images!

---

## 🔧 If OCR Isn't Reading Your Image

### Problem: Image is too faded/blurry

**Solutions:**
1. Increase brightness in your image editor
2. Increase contrast in your image editor
3. Use a different image file format (JPG → PNG)
4. Re-scan with better lighting
5. Use Manual mode and type the values manually

### Problem: Some numbers are wrong

**Example:** "0" reads as "O" or "1" reads as "l"

**Solution:** 
- After mapping, double-check the extracted text
- If wrong, manually edit in the modal
- The mapping will still work even if OCR slightly misread

---

## 📸 Supported Image Formats

✅ **Works Well:**
- JPG/JPEG
- PNG
- WebP

⚠️ **May Work:**
- BMP
- TIFF (larger file size)

❌ **Won't Work:**
- PDF (use Text or Image export instead)
- DOCX
- Raw camera RAW files

---

## 💡 Pro Tips

### Tip 1: Clean Up Your Image
Before uploading, use a free tool to:
- Increase contrast/brightness
- Crop out unnecessary borders
- Deskew (rotate) if tilted

**Free Tools:**
- Paint (Windows built-in)
- Preview (Mac built-in)
- Gimp (Free, open-source)
- Pixlr (Online)

### Tip 2: Batch Process Similar Invoices
Once template is saved:
1. All invoices from same customer
2. Same format/layout
3. Just upload → Auto apply template → Get PO matches
4. Saves hours of work!

### Tip 3: Create Multiple Templates
If ABC Corp sends invoices in 2 different formats:
- Template 1: "ABC Corp - Format A"
- Template 2: "ABC Corp - Format B"

Just select the right one for each batch!

---

## 🚀 Quick Start for Your First Image

**Right Now:**

1. Go to http://172.11.0.4:8081/app.html
2. Click **"Auto OCR"** button (purple)
3. Upload your image invoice
4. Wait for text to appear
5. Highlight each field value
6. Choose PO field from dropdown
7. Save mapping → Save template
8. Done! ✅

**Next invoice (same customer):**
1. Select saved template
2. Upload new image
3. System applies mappings automatically
4. Get PO matches in seconds!

---

## ❓ FAQs

**Q: Will OCR read handwritten fields?**  
A: No. OCR only reads printed/typed text. Handwritten fields need to be mapped manually.

**Q: Can I mix PDF pages with images in one template?**  
A: Yes, but the template is format-specific. Same layout = same template works.

**Q: What if OCR reads wrong?**  
A: Manually edit the extracted text or type the correct value in the mapping modal.

**Q: How many images can I upload at once?**  
A: Start with 1-5 to test. For batch processing, use the Batch Upload feature (Step 3).

---

## 📞 Need Help?

If OCR struggles with your invoice:
1. Check image quality (not blurry/faded)
2. Try Manual mode instead
3. Increase image brightness/contrast
4. Upload a clearer version

Your invoice image is now ready to map! 🎯

