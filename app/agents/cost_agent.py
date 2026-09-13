from app.tools.cost_tools import calculate_landed_cost

def add_costs(candidates, req):
    out=[]
    for s in candidates:
        x=dict(s)
        q=max(req.order_quantity, s["moq"])
        x["modeled_order_quantity"]=q
        x["costs"]=calculate_landed_cost(s["exw_price"],q,s["domestic_freight"],s["estimated_intl_freight"])
        out.append(x)
    return out
