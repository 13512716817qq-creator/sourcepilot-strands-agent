from app.tools.scoring_tools import score_supplier_raw

def rank_suppliers(candidates, req):
    pmin=min(s["exw_price"] for s in candidates); pmax=max(s["exw_price"] for s in candidates)
    ranked=[]
    for s in candidates:
        x=dict(s); x["scoring"]=score_supplier_raw(x,req.order_quantity,req.priority,pmin,pmax); ranked.append(x)
    ranked.sort(key=lambda s:(-s["scoring"]["score"],s["exw_price"],s["supplier_id"]))
    return ranked

def build_decision(ranked, req):
    recommended=ranked[0]
    cheapest=min(ranked,key=lambda s:s["exw_price"])
    if cheapest["supplier_id"] != recommended["supplier_id"]:
        premium=round((recommended["exw_price"]/cheapest["exw_price"]-1)*100,1)
        exposure=round((max(cheapest["moq"],req.order_quantity)/req.order_quantity-1)*100,1)
        additional_units=max(0,max(cheapest["moq"],req.order_quantity)-req.order_quantity)
        additional_inventory_exw=round(additional_units*cheapest["exw_price"],2)
        intended_order_saving=round(max(0,(recommended["exw_price"]-cheapest["exw_price"])*req.order_quantity),2)
        reason=(f"{cheapest['company_name']} is the cheapest at ${cheapest['exw_price']:.2f}/pair, but its MOQ is {cheapest['moq']}. "
                f"Choosing it would increase modeled test-order quantity exposure by {exposure:.0f}% versus the {req.order_quantity}-pair assumption. "
                f"{recommended['company_name']} costs {premium:.1f}% more per pair but ranks higher on MOQ flexibility, reliability and commercial completeness.")
        return {
            "required":True,"reason":reason,"recommended_supplier_id":recommended["supplier_id"],
            "analysis":{
                "recommended_supplier":recommended["company_name"],
                "cheapest_supplier":cheapest["company_name"],
                "recommended_unit_price":recommended["exw_price"],
                "cheapest_unit_price":cheapest["exw_price"],
                "unit_price_premium_pct":premium,
                "intended_order_saving_usd":intended_order_saving,
                "additional_units_required":additional_units,
                "additional_inventory_exw_usd":additional_inventory_exw,
                "quantity_exposure_pct":exposure,
            },
            "options":[{"action":"approve_low_risk","supplier_id":recommended["supplier_id"],"label":f"Approve {recommended['company_name']}"},{"action":"choose_lowest_cost","supplier_id":cheapest["supplier_id"],"label":f"Choose {cheapest['company_name']}"},{"action":"show_alternatives","supplier_id":None,"label":"Show alternatives"}]
        }
    return {"required":False,"reason":"Top-ranked supplier is also the lowest-cost qualified option; no material trade-off trigger fired.","recommended_supplier_id":recommended["supplier_id"],"options":[]}
