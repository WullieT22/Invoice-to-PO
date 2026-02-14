"""Service for extracting data from invoice documents"""
import os
import json
import logging
from typing import Dict, Any, Optional
import pdfplumber
from pathlib import Path
import re

logger = logging.getLogger(__name__)

class InvoiceExtractionService:
    """Extract structured data from various invoice formats"""
    
    # Common invoice field patterns
    INVOICE_NUMBER_PATTERNS = [
        r"invoice\s+(?:number|#|no\.?)[\s:]*([A-Z0-9\-]+)",
        r"inv\s+(?:number|#|no\.?)[\s:]*([A-Z0-9\-]+)",
        r"^([A-Z0-9\-]{5,20})$"  # Standalone invoice number
    ]
    
    AMOUNT_PATTERNS = [
        r"(?:total|amount|due)\s+(?:amount)?[\s:]*\$?([\d,]+\.?\d*)",
        r"\$?([\d,]+\.?\d*)(?:\s*(?:total|amount|due))?",
    ]
    
    DATE_PATTERNS = [
        r"(?:invoice|bill)\s+(?:date|issued)[\s:]*(\d{1,2}/\d{1,2}/\d{2,4})",
        r"(\d{1,2}/\d{1,2}/\d{2,4})",
        r"(\d{4}-\d{2}-\d{2})",
    ]
    
    VENDOR_PATTERNS = [
        r"(?:from|bill\s+from|vendor|supplier)[\s:]*\n?([A-Z][A-Za-z\s&.,']+)",
    ]
    
    def extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract data from PDF invoice"""
        try:
            extracted_data = {
                "invoice_number": None,
                "vendor_name": None,
                "invoice_amount": None,
                "invoice_date": None,
                "po_reference": None,
                "invoice_type": "Standard",
                "line_items": [],
                "raw_text": ""
            }
            
            with pdfplumber.open(file_path) as pdf:
                # Extract text from all pages
                full_text = ""
                for page in pdf.pages:
                    full_text += page.extract_text() or ""
                    # Try to extract tables
                    tables = page.extract_tables()
                    if tables:
                        extracted_data["line_items"].extend(self._extract_line_items(tables))
                
                extracted_data["raw_text"] = full_text
                
                # Extract fields using regex patterns
                self._extract_fields(full_text, extracted_data)
                
                logger.info(f"Successfully extracted data from PDF: {file_path}")
                
        except Exception as e:
            logger.error(f"Error extracting data from PDF {file_path}: {str(e)}")
            raise
        
        return extracted_data
    
    def extract_from_text(self, text: str) -> Dict[str, Any]:
        """Extract data from plain text invoice"""
        extracted_data = {
            "invoice_number": None,
            "vendor_name": None,
            "invoice_amount": None,
            "invoice_date": None,
            "po_reference": None,
            "invoice_type": "Standard",
            "line_items": [],
            "raw_text": text
        }
        
        self._extract_fields(text, extracted_data)
        self._detect_invoice_type(text, extracted_data)
        
        return extracted_data
    
    def _extract_fields(self, text: str, data: Dict[str, Any]):
        """Extract structured fields from text"""
        text_lower = text.lower()
        
        # Extract invoice number
        for pattern in self.INVOICE_NUMBER_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                data["invoice_number"] = match.group(1).strip()
                break
        
        # Extract amount
        for pattern in self.AMOUNT_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    amount_str = match.group(1).replace(",", "")
                    data["invoice_amount"] = float(amount_str)
                    break
                except ValueError:
                    continue
        
        # Extract date
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, text)
            if match:
                data["invoice_date"] = match.group(1)
                break
        
        # Extract vendor name
        for pattern in self.VENDOR_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                data["vendor_name"] = match.group(1).strip()
                break
        
        # Look for PO reference
        po_match = re.search(r"(?:p\.?o\.?|purchase\s+order)\s*[#:]*\s*([A-Z0-9\-]+)", text, re.IGNORECASE)
        if po_match:
            data["po_reference"] = po_match.group(1)
    
    def _detect_invoice_type(self, text: str, data: Dict[str, Any]):
        """Detect invoice type (Standard, Credit Memo, Debit Memo)"""
        text_lower = text.lower()
        
        if "credit" in text_lower and "memo" in text_lower:
            data["invoice_type"] = "Credit Memo"
        elif "debit" in text_lower and "memo" in text_lower:
            data["invoice_type"] = "Debit Memo"
        elif "credit note" in text_lower:
            data["invoice_type"] = "Credit Memo"
        elif "debit note" in text_lower:
            data["invoice_type"] = "Debit Memo"
    
    def _extract_line_items(self, tables: list) -> list:
        """Extract line items from PDF tables"""
        line_items = []
        for table in tables:
            for row in table:
                if row and len(row) >= 2:
                    line_items.append({
                        "description": str(row[0]) if row[0] else "",
                        "quantity": str(row[1]) if len(row) > 1 else "",
                        "amount": str(row[-1]) if row[-1] else ""
                    })
        return line_items
    
    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """Extract data based on file type"""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".pdf":
            return self.extract_from_pdf(file_path)
        elif file_ext in [".txt", ".csv"]:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return self.extract_from_text(text)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

invoice_extraction_service = InvoiceExtractionService()
