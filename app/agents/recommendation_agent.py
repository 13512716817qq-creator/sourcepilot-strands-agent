from app.tools.scoring_tools import score_supplier_raw


def rank_suppliers(candidates, req):
    pmin=min(s["exw_price"] for s in candidates); pmax=max(s["exw_price"] for s in candidates)
    ranked=[]
    for s in candidates:
        x=dict(s)
        x["scoring"]=score_supplier_raw(x,req.order_quantity,req.priority,pmin,pmax)
        ranked.append(x)
    ranked.sort(key=lambda s:(-s["scoring"]["score"],s["exw_price"],s["supplier_id"]))
    return ranked


def build_decision(ranked, req):
    """Build a human decision only from suppliers already visible in the shortlist.

    This avoids introducing a supplier in the approval step that the user has not
    seen in the comparison table. The broader candidate pool still influences the
    deterministic ranking, but the decision card compares only the top 3 shortlist.
    """
    shortlist=ranked[:3]
    recommended=shortlist[0]
    cheapest=min(shortlist,key=lambda s:s["exw_price"])

    if cheapest["supplier_id"] != recommended["supplier_id"]:
        premium=round((recommended["exw_price"]/cheapest["exw_price"]-1)*100,1)
        modeled_qty=req.order_quantity
        cheapest_commit_qty=max(cheapest["moq"],modeled_qty)
        additional_units=max(0,cheapest_commit_qty-modeled_qty)
        exposure=round((cheapest_commit_qty/modeled_qty-1)*100,1)
        additional_inventory_exw=round(additional_units*cheapest["exw_price"],2)
        intended_order_saving=round(max(0,(recommended["exw_price"]-cheapest["exw_price"])*modeled_qty),2)

        reason=(
            f"Within the 3 shortlisted suppliers, {cheapest['company_name']} has the lowest EXW unit price at "
            f"${cheapest['exw_price']:.2f}/pair, but its MOQ is {cheapest['moq']} pairs. "
            f"For the modeled {modeled_qty}-pair test order, that means committing to {additional_units} extra pairs "
            f"({exposure:.0f}% more units). {recommended['company_name']} costs {premium:.1f}% more per pair, "
            f"but requires no extra quantity beyond the modeled test order and scores higher overall on the "
            f"current procurement strategy."
        )
        return {
            "required":True,
            "reason":reason,
            "recommended_supplier_id":recommended["supplier_id"],
            "comparison_scope":"top_3_shortlist",
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
            "options":[
                {"action":"approve_recommended","supplier_id":recommended["supplier_id"],"label":f"Approve {recommended['company_name']}"},
                {"action":"choose_lower_unit_price","supplier_id":cheapest["supplier_id"],"label":f"Choose {cheapest['company_name']}"},
                {"action":"show_alternatives","supplier_id":None,"label":"Review shortlist"},
            ],
        }

    return {
        "required":False,
        "reason":"The top-ranked shortlisted supplier is also the lowest-price option within the shortlist; no material trade-off trigger fired.",
        "recommended_supplier_id":recommended["supplier_id"],
        "comparison_scope":"top_3_shortlist",
        "options":[],
    }
