from app.tools.supplier_tools import search_suppliers

def discover_suppliers(req):
    return search_suppliers(req.product, req.material, 600)
