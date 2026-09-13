from app.agents.orchestrator import run_workflow, finalize
from app.agents.requirements_agent import extract_requirements
from app.tools.cost_tools import calculate_landed_cost
from app.tools.risk_tools import identify_risks

def hero():
    return "Hi, I am looking for fashionable women's shoes for Ghana. I want around 8 to 12 designs for young women. I want to start with a small quantity. My budget is limited and I need a reliable supplier. Can you help me source from China?"

def test_requirement_extraction():
    r=extract_requirements(hero()); assert r.destination=="Ghana"; assert (r.styles_min,r.styles_max)==(8,12); assert "exact quantity" in r.missing_critical

def test_supplier_filtering_and_ranking():
    r=run_workflow(hero()); assert r["metrics"]["suppliers_analyzed"]>=12; assert len(r["shortlist"])==3; assert r["shortlist"][0]["scoring"]["score"]>=r["shortlist"][1]["scoring"]["score"]

def test_cost_calculation():
    c=calculate_landed_cost(8.4,100,135,480); assert c["exw_total"]==840.0; assert c["estimated_procurement_total_excl_duty_tax"]==1455.0

def test_material_mismatch_risk():
    s={"material":"PVC","moq":100,"documentation_score":90,"quotation_completeness":90,"historical_delivery_score":90,"production_lead_time":15,"exw_price":8,"risk_flags":[]}
    risks=identify_risks(s,"PU",100,8.5); assert any(x["code"]=="material_mismatch" for x in risks)

def test_human_decision_trigger():
    r=run_workflow(hero()); assert r["decision"]["required"] is True; assert len(r["decision"]["options"])==3

def test_lowest_price_case_changes_weights():
    r=run_workflow(hero(),"lowest_price"); assert r["shortlist"][0]["scoring"]["components"]["price"] >= 0

def test_deterministic_ranking():
    a=run_workflow(hero()); b=run_workflow(hero()); assert [x["supplier_id"] for x in a["shortlist"]]==[x["supplier_id"] for x in b["shortlist"]]

def test_malformed_missing_buyer_data():
    r=run_workflow("Need shoes."); assert r["requirements"]["destination"]=="Unspecified"; assert r["metrics"]["suppliers_analyzed"]>0

def test_finalize():
    r=run_workflow(hero()); f=finalize(r,r["decision"]["recommended_supplier_id"]); assert f["status"]=="PROCUREMENT READY"; assert 0<f["confidence"]<=100

def test_decision_explainability_metrics():
    r=run_workflow(hero())
    a=r["decision"]["analysis"]
    assert a["additional_units_required"] >= 0
    assert a["additional_inventory_exw_usd"] >= 0
    assert a["quantity_exposure_pct"] >= 0
