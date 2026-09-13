from __future__ import annotations
import json
from pathlib import Path
try:
    from strands import tool
except Exception:
    def tool(fn): return fn

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "suppliers.json"

def _load():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))

@tool
def search_suppliers(product: str, material: str = "PU", max_moq: int = 600) -> list[dict]:
    """Search the synthetic supplier dataset for matching footwear suppliers."""
    rows=[]
    for s in _load():
        category_match=any("women fashion" in c.lower() for c in s["product_categories"])
        if category_match and s["moq"] <= max_moq:
            rows.append(s)
    return rows

@tool
def get_supplier_details(supplier_id: str) -> dict:
    """Return one supplier record by synthetic supplier ID."""
    for s in _load():
        if s["supplier_id"] == supplier_id:
            return s
    return {"error":"supplier_not_found","supplier_id":supplier_id}
