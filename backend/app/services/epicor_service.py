"""Service to fetch data from Epicor BAQ"""
import requests
import base64
import os
from typing import List, Dict, Any
from app.config import settings
import urllib3
import logging

logger = logging.getLogger(__name__)

class EpicorService:
    """Handle Epicor API interactions"""
    
    def __init__(self):
        # Disable SSL warnings for IP address connections
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.base_url = settings.EPICOR_API_URL
        self.username = settings.EPICOR_USERNAME
        self.password = settings.EPICOR_PASSWORD
        self.company = settings.EPICOR_COMPANY
        self.session = requests.Session()
        self._setup_auth()
    
    def _setup_auth(self):
        """Setup Basic Auth for Epicor API"""
        credentials = base64.b64encode(
            f"{self.username}:{self.password}".encode()
        ).decode()
        self.session.headers.update({
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        })
    
    def _safe_float(self, value: Any, default: float = 0.0) -> float:
        """Safely convert value to float"""
        try:
            return float(value) if value is not None else default
        except (ValueError, TypeError):
            return default

    def get_purchase_orders(self, baq_id: str = None) -> List[Dict[str, Any]]:
        """
        Fetch purchase orders using BAQ
        Maps BAQ fields to invoice matching requirements
        """
        if baq_id is None:
            baq_id = os.getenv("EPICOR_BAQ_ID", "PO_Test")
            
        try:
            # Construct URL: https://199.5.83.159/EpicorERP/api/v1/BaqSvc/PO_Test
            base = self.base_url.rstrip('/')
            url = f"{base}/BaqSvc/{baq_id}"
            
            logger.info(f"🔌 Connecting to Epicor BAQ: {url}")
            
            # Add Company Header (only if company is set)
            headers = {}
            if self.company:
                headers["CallSettings"] = f'{{"Company":"{self.company}"}}'
            
            # verify=False is CRITICAL for IP address connections
            response = self.session.get(url, headers=headers, verify=False, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            pos = []
            
            items = data.get("value", [])
            if items:
                # --- DEBUG: Print the actual columns found in the BAQ ---
                logger.info(f"✅ Connected! Found {len(items)} records.")
                logger.info(f"🔍 BAQ COLUMNS FOUND: {list(items[0].keys())}")
            else:
                logger.warning(f"⚠️ BAQ returned 0 records. Response keys: {list(data.keys())}")
                logger.debug(f"Raw Response: {data}")

            for po in items:
                pos.append({
                    "po_number": po.get("PODetail_PONUM"),
                    "po_line": po.get("PODetail_POLine"),
                    "vendor_id": po.get("Vendor_VendorID"),
                    "vendor_name": po.get("Vendor_Name"),
                    "part_number": po.get("PODetail_PartNum"),
                    "supplier_part": po.get("PODetail_VenPartNum"),
                    "line_description": po.get("PODetail_LineDesc"),
                    "unit_cost": self._safe_float(po.get("PODetail_UnitCost")),
                    "order_qty": self._safe_float(po.get("PODetail_OrderQty")),
                    "our_qty": self._safe_float(po.get("PODetail_XOrderQty")),
                    "base_uom": po.get("PODetail_BaseUOM"),
                    "line_amount": self._safe_float(po.get("PODetail_DocExitCost")),
                })
            
            logger.info(f"Successfully fetched {len(pos)} purchase orders from Epicor BAQ")
            return pos
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching purchase orders from Epicor BAQ: {str(e)}")
            raise

epicor_service = EpicorService()
