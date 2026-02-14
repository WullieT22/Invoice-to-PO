"""Service for AI-powered invoice to PO matching"""
import json
import logging
from typing import Dict, Any, List, Tuple, Optional
from openai import OpenAI
from app.config import settings

logger = logging.getLogger(__name__)

class AIMatchingService:
    """Use AI to match invoices to purchase orders"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.AI_MODEL
    
    def find_best_match(
        self,
        invoice_data: Dict[str, Any],
        available_pos: List[Dict[str, Any]]
    ) -> Tuple[Optional[Dict[str, Any]], float, str]:
        """
        Find the best matching PO for an invoice using AI
        Returns: (best_po, match_score, reasoning)
        """
        
        if not available_pos:
            logger.warning("No available POs to match against")
            # --- DEMO MODE: Inject Dummy PO for testing ---
            logger.info("⚠️ DEMO MODE: Injecting Test PO because database is empty")
            available_pos = [{
                "po_number": "PO-2024-1001",
                "vendor_name": "ACME Corporation",
                "vendor_id": "ACME001",
                "line_amount": 2754.00,
                "line_description": "Office Supplies - Batch Order",
                "po_line": 1,
                "part_number": "OFF-SUP-001"
            }]
            # return None, 0.0, "No available purchase orders"
        
        # Prepare context for AI
        invoice_context = self._prepare_invoice_context(invoice_data)
        pos_context = self._prepare_pos_context(available_pos)
        
        # Create AI prompt
        prompt = self._create_matching_prompt(invoice_context, pos_context)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in accounts payable automation and invoice matching. "
                                   "Analyze invoices and purchase orders to find the best matches. "
                                   "Return results as valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            # Parse AI response
            response_text = response.choices[0].message.content
            match_result = self._parse_ai_response(response_text, available_pos)
            
            return match_result["po"], match_result["score"], match_result["reasoning"]
            
        except Exception as e:
            logger.error(f"Error in AI matching: {str(e)}")
            # Fallback to fuzzy matching
            return self.fuzzy_match(invoice_data, available_pos)
    
    def fuzzy_match(
        self,
        invoice_data: Dict[str, Any],
        available_pos: List[Dict[str, Any]]
    ) -> Tuple[Optional[Dict[str, Any]], float, str]:
        """Fallback fuzzy matching using BAQ fields when AI is not available"""
        best_po = None
        best_score = 0.0
        best_reasoning = ""
        
        invoice_amount = invoice_data.get("invoice_amount", 0)
        vendor_name = (invoice_data.get("vendor_name") or "").lower()
        po_reference = invoice_data.get("po_reference")
        invoice_lines = invoice_data.get("line_items", [])
        
        for po in available_pos:
            score = 0.0
            reasoning_parts = []
            
            # Vendor match
            po_vendor = (po.get("vendor_name") or "").lower()
            if vendor_name and po_vendor:
                if vendor_name == po_vendor:
                    score += 0.3
                    reasoning_parts.append("Exact vendor match")
                elif vendor_name in po_vendor or po_vendor in vendor_name:
                    score += 0.15
                    reasoning_parts.append("Partial vendor match")
            
            # PO number reference match
            if po_reference and (str(po_reference) in str(po.get("po_number")) or 
                                str(po.get("po_number")) in str(po_reference)):
                score += 0.4
                reasoning_parts.append("PO number reference match")
            
            # Amount match (within 5% tolerance)
            po_amount = po.get("line_amount", 0)
            if invoice_amount and po_amount:
                diff = abs(invoice_amount - po_amount)
                tolerance = po_amount * 0.05
                if diff <= tolerance:
                    score += 0.3
                    reasoning_parts.append(f"Exact amount match")
                elif diff <= tolerance * 2:
                    score += 0.15
                    reasoning_parts.append(f"Amount close match")
            
            # Part number match from BAQ
            part_num = invoice_data.get("part_number", "").lower()
            po_part_num = (po.get("part_number") or "").lower()
            po_supplier_part = (po.get("supplier_part") or "").lower()
            
            if part_num and (part_num == po_part_num or part_num == po_supplier_part):
                score += 0.25
                reasoning_parts.append("Part number match")
            
            # Description match from BAQ
            description = (invoice_data.get("description") or "").lower()
            po_desc = (po.get("line_description") or "").lower()
            if description and po_desc and description in po_desc:
                score += 0.1
                reasoning_parts.append("Description match")
            
            if score > best_score:
                best_score = score
                best_po = po
                best_reasoning = "; ".join(reasoning_parts) if reasoning_parts else "Partial match"
        
        reasoning = best_reasoning if best_po else "No suitable matches found"
        return best_po, min(best_score, 1.0), reasoning
    
    def _prepare_invoice_context(self, invoice_data: Dict[str, Any]) -> str:
        """Format invoice data for AI analysis with BAQ field support"""
        return json.dumps({
            "invoice_number": invoice_data.get("invoice_number"),
            "vendor_name": invoice_data.get("vendor_name"),
            "vendor_id": invoice_data.get("vendor_id"),
            "invoice_amount": invoice_data.get("invoice_amount"),
            "invoice_date": invoice_data.get("invoice_date"),
            "invoice_type": invoice_data.get("invoice_type"),
            "po_reference": invoice_data.get("po_reference"),
            "part_number": invoice_data.get("part_number"),
            "description": invoice_data.get("description"),
            "line_items": invoice_data.get("line_items", [])[:3]
        }, indent=2)
    
    def _prepare_pos_context(self, available_pos: List[Dict[str, Any]]) -> str:
        """Format POs for AI analysis"""
        return json.dumps(available_pos[:10], indent=2)  # Limit to 10 POs
    
    def _create_matching_prompt(self, invoice_context: str, pos_context: str) -> str:
        """Create the prompt for AI matching with BAQ field support"""
        return f"""
Analyze the following invoice and find the best matching purchase order(s).

INVOICE DATA:
{invoice_context}

AVAILABLE PURCHASE ORDERS (from Epicor BAQ):
{pos_context}

Key BAQ Fields Available:
- po_number: Purchase order number
- po_line: Line number on PO
- vendor_name: Vendor name
- vendor_id: Vendor ID
- part_number: Part number
- supplier_part: Supplier's part number
- line_description: Line description from PO
- unit_cost: Unit cost from PO
- order_qty: Ordered quantity
- line_amount: Extended cost/total line amount

Task:
1. Analyze the invoice and POs carefully using BAQ data
2. Consider matching criteria: 
   - Vendor name/ID match
   - PO number reference in invoice
   - Amount match (within 5% tolerance)
   - Part number/description match
   - Date proximity
3. For credit/debit memos, look for matching original invoice amounts
4. Return a JSON response with this exact structure:

{{
    "best_match": {{
        "po_number": "PO123",
        "po_line": 1,
        "match_score": 0.95,
        "matching_criteria": ["vendor match", "amount match", "po_reference"]
    }},
    "alternative_matches": [
        {{
            "po_number": "PO456",
            "po_line": 2,
            "match_score": 0.75,
            "matching_criteria": ["vendor match"]
        }}
    ],
    "confidence": 0.95,
    "reasoning": "Detailed explanation using BAQ fields"
}}
"""
    
    def _parse_ai_response(self, response_text: str, available_pos: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse AI response and extract match information"""
        try:
            # Clean response text
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            ai_result = json.loads(response_text)
            
            best_match = ai_result.get("best_match", {})
            po_number = best_match.get("po_number")
            
            # Find matching PO from available list
            matching_po = None
            for po in available_pos:
                if po.get("po_number") == po_number:
                    matching_po = po
                    break
            
            return {
                "po": matching_po,
                "score": best_match.get("match_score", 0.0),
                "reasoning": ai_result.get("reasoning", "AI matching completed")
            }
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning(f"Error parsing AI response: {str(e)}")
            return {
                "po": None,
                "score": 0.0,
                "reasoning": "Error parsing AI response"
            }
    
    def validate_match(
        self,
        invoice_data: Dict[str, Any],
        po_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate a proposed match with AI"""
        prompt = f"""
Validate if this invoice matches this purchase order:

INVOICE:
- Number: {invoice_data.get('invoice_number')}
- Vendor: {invoice_data.get('vendor_name')}
- Amount: {invoice_data.get('invoice_amount')}
- Date: {invoice_data.get('invoice_date')}
- Type: {invoice_data.get('invoice_type')}

PURCHASE ORDER:
- Number: {po_data.get('po_number')}
- Vendor: {po_data.get('vendor_name')}
- Line Amount: {po_data.get('line_amount')}
- Description: {po_data.get('line_description')}

Please validate this match and provide:
1. Is this a valid match? (yes/no)
2. Confidence level (0-100)
3. Any discrepancies or concerns
4. Recommendation (approve/review/reject)

Return as JSON.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content
            validation_result = json.loads(response_text)
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating match: {str(e)}")
            return {
                "is_valid": False,
                "confidence": 0,
                "recommendation": "error"
            }

ai_matching_service = AIMatchingService()
