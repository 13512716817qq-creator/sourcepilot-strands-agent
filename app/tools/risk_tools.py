from __future__ import annotations
try:
    from strands import tool
except Exception:
    def tool(fn): return fn

@tool
def identify_risks(supplier: dict, requested_material: str = "PU", test_order_qty: int = 100, market_median_price: float | None = None) -> list[dict]:
    """Identify transparent commercial risk flags without alleging fraud."""
    risks=[]
    mat=supplier.get("material","").lower(); req=requested_material.lower()
    if req and req not in mat:
        risks.append({"code":"material_mismatch","severity":"high","reason":f"Quoted material '{supplier.get('material')}' does not match requested '{requested_material}'. Requires verification."})
    if supplier.get("moq",0) > max(test_order_qty*3,300):
        risks.append({"code":"high_moq","severity":"high","reason":f"MOQ {supplier['moq']} materially exceeds the {test_order_qty}-unit test-order assumption."})
    if supplier.get("documentation_score",100)<75:
        risks.append({"code":"weak_documentation","severity":"medium","reason":"Documentation score is below the prototype verification threshold."})
    if supplier.get("quotation_completeness",100)<80:
        risks.append({"code":"incomplete_quote","severity":"medium","reason":"Quotation is missing enough commercial fields to require follow-up."})
    if supplier.get("historical_delivery_score",100)<80:
        risks.append({"code":"delivery_history","severity":"medium","reason":"Synthetic delivery-history score is below 80/100."})
    if supplier.get("production_lead_time",0)<7:
        risks.append({"code":"unrealistic_lead_time","severity":"medium","reason":"Lead time appears unusually short and should be verified."})
    if market_median_price and supplier.get("exw_price",999) < market_median_price*0.88:
        risks.append({"code":"low_price_verification","severity":"medium","reason":"Price is more than 12% below the candidate median; specification completeness should be verified."})
    for flag in supplier.get("risk_flags",[]):
        if not any(r["code"]==flag for r in risks):
            risks.append({"code":flag,"severity":"medium","reason":f"Dataset flag '{flag}' requires commercial verification."})
    return risks
