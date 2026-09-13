from __future__ import annotations
import re
from app.models.schemas import BuyerRequirements

def extract_requirements(message: str) -> BuyerRequirements:
    text=message.lower()
    destination="Ghana" if "ghana" in text else "Unspecified"
    style_match=re.search(r"(\d+)\s*(?:to|[-–])\s*(\d+)\s*(?:design|style)",text)
    smin,smax=(int(style_match.group(1)),int(style_match.group(2))) if style_match else (8,12)
    qty_match=re.search(r"(?:quantity|qty|around|about)\s*(\d{2,5})",text)
    qty=int(qty_match.group(1)) if qty_match else 100
    missing=[]
    if not qty_match: missing.append("exact quantity")
    if "size" not in text: missing.append("size distribution")
    if not re.search(r"\$\s*\d|usd|target price",text): missing.append("target price")
    if not any(x in text for x in [" pu ","leather","pvc","microfiber","material"]): missing.append("material preference")
    if not any(x in text for x in ["sea freight","air freight","shipping"]): missing.append("shipping method")
    assumptions=[]
    if "exact quantity" in missing: assumptions.append("Use 100 pairs as a reversible test-order assumption for ranking; confirm before commitment.")
    if "material preference" in missing: assumptions.append("Use PU as the comparison baseline; flag mismatches rather than asserting a final material choice.")
    return BuyerRequirements(destination=destination,styles_min=smin,styles_max=smax,order_quantity=qty,missing_critical=missing,assumptions=assumptions)

def generate_rfq(req: BuyerRequirements) -> dict:
    return {"product":req.product,"destination":req.destination,"audience":req.audience,"styles":f"{req.styles_min}-{req.styles_max}","test_order_quantity":req.order_quantity,"comparison_material":req.material,"priority":req.priority,"required_quote_fields":["unit price","MOQ","material","sample cost","lead time","packaging","payment terms","domestic freight"]}
