from statistics import median
from app.tools.risk_tools import identify_risks

def assess_risks(candidates, req):
    med=median([s["exw_price"] for s in candidates])
    out=[]
    for s in candidates:
        x=dict(s)
        x["computed_risks"]=identify_risks(x,req.material,req.order_quantity,med)
        out.append(x)
    return out
