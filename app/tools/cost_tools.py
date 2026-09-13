from __future__ import annotations
try:
    from strands import tool
except Exception:
    def tool(fn): return fn

@tool
def calculate_order_cost(unit_price: float, quantity: int, domestic_freight: float = 0.0) -> dict:
    """Deterministically calculate EXW product total and China-side cost."""
    product_total=round(unit_price*quantity,2)
    return {"product_total":product_total,"domestic_freight":round(domestic_freight,2),"china_side_total":round(product_total+domestic_freight,2)}

@tool
def calculate_landed_cost(unit_price: float, quantity: int, domestic_freight: float, estimated_intl_freight: float) -> dict:
    """Estimate prototype landed procurement cost excluding duty/tax because no customs data is asserted."""
    exw=round(unit_price*quantity,2)
    total=round(exw+domestic_freight+estimated_intl_freight,2)
    return {"exw_total":exw,"domestic_freight":round(domestic_freight,2),"estimated_international_freight":round(estimated_intl_freight,2),"estimated_procurement_total_excl_duty_tax":total,"estimated_unit_cost_excl_duty_tax":round(total/quantity,2)}
