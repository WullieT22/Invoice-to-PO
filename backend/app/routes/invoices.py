"""Invoice upload and matching routes"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import os
from app.models.database import Invoice, InvoiceMatch, PurchaseOrder, Base
from app.services.invoice_extraction_service import invoice_extraction_service
from app.services.ai_matching_service import ai_matching_service
from app.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/invoices", tags=["invoices"])

# Dependency to get database session (placeholder - configure with actual DB)
def get_db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and process an invoice document"""
    try:
        # Validate file
        if file.size > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large")
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Extract invoice data
        extracted_data = invoice_extraction_service.extract_from_file(file_path)
        
        # Create invoice record
        from datetime import datetime
        invoice_date = extracted_data.get("invoice_date")
        # Parse date if it's a string
        if isinstance(invoice_date, str):
            try:
                invoice_date = datetime.strptime(invoice_date, "%m/%d/%Y")
            except:
                invoice_date = None
        
        invoice = Invoice(
            invoice_number=extracted_data.get("invoice_number"),
            vendor_name=extracted_data.get("vendor_name"),
            invoice_date=invoice_date,
            invoice_amount=extracted_data.get("invoice_amount"),
            invoice_type=extracted_data.get("invoice_type"),
            file_path=file_path,
            extracted_data=str(extracted_data)
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        
        logger.info(f"Invoice uploaded: {invoice.id}")
        
        return {
            "invoice_id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "vendor_name": invoice.vendor_name,
            "amount": invoice.invoice_amount,
            "type": invoice.invoice_type
        }
        
    except Exception as e:
        logger.error(f"Error uploading invoice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/match/{invoice_id}")
async def match_invoice_to_po(invoice_id: int, db: Session = Depends(get_db)):
    """Match an invoice to a purchase order using AI"""
    try:
        # Get invoice
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        # Get available POs
        available_pos = db.query(PurchaseOrder).filter(
            PurchaseOrder.remaining_amount > 0
        ).all()
        
        if not available_pos:
            raise HTTPException(status_code=404, detail="No available purchase orders")
        
        # Prepare PO data
        pos_data = [
            {
                "po_number": po.po_number,
                "po_line": po.po_line,
                "vendor_name": po.vendor_name,
                "line_amount": po.line_amount,
                "remaining_amount": po.remaining_amount,
                "line_description": po.line_description
            }
            for po in available_pos
        ]
        
        # Parse invoice data
        import json
        invoice_data = json.loads(invoice.extracted_data)
        
        # Find best match
        best_po, match_score, reasoning = ai_matching_service.find_best_match(
            invoice_data, pos_data
        )
        
        if not best_po:
            return {
                "invoice_id": invoice_id,
                "match_found": False,
                "message": "No suitable purchase order found"
            }
        
        # Find PO record
        po_record = db.query(PurchaseOrder).filter(
            PurchaseOrder.po_number == best_po.get("po_number")
        ).first()
        
        # Create match record
        match = InvoiceMatch(
            invoice_id=invoice_id,
            po_id=po_record.id if po_record else None,
            match_score=match_score,
            matched_amount=invoice.invoice_amount,
            match_type="AI",
            ai_reasoning=reasoning
        )
        db.add(match)
        db.commit()
        db.refresh(match)
        
        logger.info(f"Match created: Invoice {invoice_id} to PO {best_po.get('po_number')}")
        
        return {
            "match_id": match.id,
            "invoice_id": invoice_id,
            "po_number": best_po.get("po_number"),
            "match_score": match_score,
            "reasoning": reasoning,
            "requires_approval": match_score < 0.8
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error matching invoice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pending-matches")
async def get_pending_matches(db: Session = Depends(get_db)):
    """Get all invoices waiting for approval"""
    try:
        pending = db.query(InvoiceMatch).filter(
            InvoiceMatch.is_approved == False
        ).all()
        
        results = []
        for match in pending:
            results.append({
                "match_id": match.id,
                "invoice_number": match.invoice.invoice_number,
                "po_number": match.purchase_order.po_number if match.purchase_order else None,
                "amount": match.matched_amount,
                "score": match.match_score,
                "reasoning": match.ai_reasoning
            })
        
        return results
    except Exception as e:
        logger.error(f"Error fetching pending matches: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/approve-match/{match_id}")
async def approve_match(match_id: int, db: Session = Depends(get_db)):
    """Approve an invoice-to-PO match"""
    try:
        match = db.query(InvoiceMatch).filter(InvoiceMatch.id == match_id).first()
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        
        match.is_approved = True
        db.commit()
        
        logger.info(f"Match approved: {match_id}")
        
        return {"message": "Match approved successfully"}
    except Exception as e:
        logger.error(f"Error approving match: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
