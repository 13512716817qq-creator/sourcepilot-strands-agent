from __future__ import annotations
from app.agents.requirements_agent import extract_requirements, generate_rfq
from app.agents.supplier_agent import discover_suppliers
from app.agents.risk_agent import assess_risks
from app.agents.cost_agent import add_costs
from app.agents.recommendation_agent import rank_suppliers, build_decision

ACTIVITY=["Understanding request","Building procurement specification","Searching supplier candidates","Normalizing quotations","Checking commercial risks","Calculating estimated costs","Ranking suppliers"]

def run_workflow(message: str, priority: str = "low_moq_balanced_risk") -> dict:
    req=extract_requirements(message); req.priority=priority
    rfq=generate_rfq(req)
    candidates=discover_suppliers(req)
    candidates=assess_risks(candidates,req)
    candidates=add_costs(candidates,req)
    ranked=rank_suppliers(candidates,req)
    decision=build_decision(ranked,req)
    risk_count=sum(len(s["computed_risks"]) for s in ranked)
    return {"requirements":req.to_dict(),"rfq":rfq,"candidates":ranked,"shortlist":ranked[:3],"decision":decision,"activity":ACTIVITY,"metrics":{"suppliers_analyzed":len(ranked),"shortlisted":3,"risk_flags_detected":risk_count,"human_interventions":1 if decision["required"] else 0}}

def finalize(result: dict, supplier_id: str) -> dict:
    selected=next(s for s in result["candidates"] if s["supplier_id"]==supplier_id)
    high=sum(1 for r in selected["computed_risks"] if r["severity"]=="high")
    confidence=max(55,min(96,int(selected["scoring"]["score"] - high*5 + 8)))
    explanation=(f"{selected['company_name']} is selected because its procurement score is {selected['scoring']['score']}/100. "
                 f"For the modeled order quantity of {selected['modeled_order_quantity']} pairs, the estimated procurement total excluding duty/tax is "
                 f"${selected['costs']['estimated_procurement_total_excl_duty_tax']:,.2f}. "
                 f"The recommendation balances price, MOQ, quality, delivery reliability, lead time, quotation completeness and explicit risk flags.")
    return {"status":"PROCUREMENT READY","selected_supplier":selected,"confidence":confidence,"explanation":explanation,"verification_note":"Synthetic demonstration data. Freight is modeled; customs duty/tax and supplier legitimacy are not asserted and require verification."}
