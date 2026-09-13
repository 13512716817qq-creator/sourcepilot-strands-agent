from __future__ import annotations
try:
    from strands import tool
except Exception:
    def tool(fn): return fn

def _clamp(x): return max(0.0,min(100.0,x))

def score_supplier_raw(s: dict, order_qty: int, priority: str, price_min: float, price_max: float) -> dict:
    if price_max == price_min: price_score=100.0
    else: price_score=100*(price_max-s["exw_price"])/(price_max-price_min)
    moq_ratio=max(1,s["moq"])/max(1,order_qty)
    moq_score=_clamp(110-25*moq_ratio)
    lead_score=_clamp(115-3.0*s["production_lead_time"])
    quality=float(s["quality_score"])
    reliability=float(s["historical_delivery_score"])
    completeness=float(s["quotation_completeness"])
    risk_penalty=len(s.get("computed_risks",[]))*8
    if priority=="lowest_price":
        w={"price":.40,"moq":.15,"quality":.12,"reliability":.12,"lead":.08,"complete":.13}
    else:
        w={"price":.20,"moq":.24,"quality":.16,"reliability":.18,"lead":.08,"complete":.14}
    base=price_score*w["price"]+moq_score*w["moq"]+quality*w["quality"]+reliability*w["reliability"]+lead_score*w["lead"]+completeness*w["complete"]
    score=_clamp(base-risk_penalty)
    return {"score":round(score,1),"components":{"price":round(price_score,1),"moq":round(moq_score,1),"quality":quality,"reliability":reliability,"lead_time":round(lead_score,1),"quotation_completeness":completeness,"risk_penalty":risk_penalty}}

@tool
def score_supplier(supplier: dict, order_qty: int = 100, priority: str = "low_moq_balanced_risk", price_min: float = 7.0, price_max: float = 11.0) -> dict:
    """Score a supplier with transparent deterministic weights."""
    return score_supplier_raw(supplier,order_qty,priority,price_min,price_max)
