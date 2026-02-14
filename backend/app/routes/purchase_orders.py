"""Purchase Order and Epicor integration routes"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.epicor_service import epicor_service
from app.models.database import PurchaseOrder
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/purchase-orders", tags=["purchase-orders"])

def get_db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.config import settings
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/sync-from-epicor")
def sync_purchase_orders_from_epicor(db: Session = Depends(get_db)):
    """Fetch and sync purchase orders from Epicor BAQ"""
    try:
        # Fetch POs from Epicor
        epicor_pos = epicor_service.get_purchase_orders()
        
        if not epicor_pos:
            return {"message": "No purchase orders found in Epicor"}
        
        # Upsert POs in database
        synced_count = 0
        for po_data in epicor_pos:
            po_key = f"{po_data['po_number']}-{po_data['po_line']}"
            
            # Check if PO exists
            existing_po = db.query(PurchaseOrder).filter(
                PurchaseOrder.po_number == po_data['po_number'],
                PurchaseOrder.po_line == po_data['po_line']
            ).first()
            
            remaining_amount = po_data['line_amount'] - po_data['received_amount']
            
            if existing_po:
                # Update
                existing_po.line_amount = po_data['line_amount']
                existing_po.received_amount = po_data['received_amount']
                existing_po.remaining_amount = remaining_amount
            else:
                # Create new
                new_po = PurchaseOrder(
                    po_number=po_data['po_number'],
                    po_line=po_data['po_line'],
                    vendor_id=po_data['vendor_id'],
                    vendor_name=po_data['vendor_name'],
                    line_description=po_data['line_description'],
                    line_amount=po_data['line_amount'],
                    received_amount=po_data['received_amount'],
                    remaining_amount=remaining_amount,
                    due_date=po_data['due_date']
                )
                db.add(new_po)
            
            synced_count += 1
        
        db.commit()
        logger.info(f"Synced {synced_count} purchase orders from Epicor")
        
        return {
            "synced_count": synced_count,
            "message": f"Successfully synced {synced_count} purchase orders"
        }
        
    except Exception as e:
        logger.error(f"Error syncing POs from Epicor: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_purchase_orders(db: Session = Depends(get_db)):
    """Get all purchase orders"""
    try:
        pos = db.query(PurchaseOrder).all()
        
        results = []
        for po in pos:
            results.append({
                "po_id": po.id,
                "po_number": po.po_number,
                "po_line": po.po_line,
                "vendor_name": po.vendor_name,
                "description": po.line_description,
                "line_amount": po.line_amount,
                "remaining_amount": po.remaining_amount,
                "due_date": po.due_date
            })
        
        return results
    except Exception as e:
        logger.error(f"Error fetching purchase orders: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{po_id}")
async def get_purchase_order(po_id: int, db: Session = Depends(get_db)):
    """Get a specific purchase order with its invoices"""
    try:
        po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
        
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        
        return {
            "po_id": po.id,
            "po_number": po.po_number,
            "po_line": po.po_line,
            "vendor_name": po.vendor_name,
            "description": po.line_description,
            "line_amount": po.line_amount,
            "received_amount": po.received_amount,
            "remaining_amount": po.remaining_amount,
            "due_date": po.due_date,
            "invoices": [
                {
                    "invoice_id": inv.id,
                    "invoice_number": inv.invoice_number,
                    "amount": inv.invoice_amount
                }
                for inv in po.invoices
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching purchase order: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
