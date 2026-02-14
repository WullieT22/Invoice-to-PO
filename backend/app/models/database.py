"""Database models for Invoice and PO"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class PurchaseOrder(Base):
    """Purchase Order model from Epicor BAQ"""
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String, unique=True, index=True)
    po_line = Column(Integer)
    vendor_id = Column(String)
    vendor_name = Column(String)
    line_description = Column(String)
    line_amount = Column(Float)
    received_amount = Column(Float, default=0.0)
    remaining_amount = Column(Float)
    due_date = Column(DateTime)
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    invoices = relationship("Invoice", back_populates="purchase_order")
    matches = relationship("InvoiceMatch", back_populates="purchase_order")

class Invoice(Base):
    """Invoice model"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, index=True)
    vendor_id = Column(String)
    vendor_name = Column(String)
    invoice_date = Column(DateTime)
    invoice_amount = Column(Float)
    invoice_type = Column(String)  # Standard, Credit Memo, Debit Memo
    file_path = Column(String)
    extracted_data = Column(Text)  # JSON string of extracted data
    created_date = Column(DateTime, default=datetime.utcnow)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=True)
    purchase_order = relationship("PurchaseOrder", back_populates="invoices")
    matches = relationship("InvoiceMatch", back_populates="invoice")

class InvoiceMatch(Base):
    """Invoice to PO Match result"""
    __tablename__ = "invoice_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"))
    po_id = Column(Integer, ForeignKey("purchase_orders.id"))
    match_score = Column(Float)  # 0-1 confidence score
    matched_amount = Column(Float)
    match_type = Column(String)  # Exact, Fuzzy, Manual
    ai_reasoning = Column(Text)  # Explanation from AI
    is_approved = Column(Boolean, default=False)
    approved_by = Column(String, nullable=True)
    approved_date = Column(DateTime, nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    invoice = relationship("Invoice", back_populates="matches")
    purchase_order = relationship("PurchaseOrder", back_populates="matches")
