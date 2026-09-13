from __future__ import annotations
import streamlit as st
from app.agents.agentic_workflow import run_agentic_workflow, finalize

st.set_page_config(page_title="SourcePilot",page_icon="🧭",layout="wide")
st.markdown("""<style>
.block-container{max-width:1180px;padding-top:2rem}.decision{border:1px solid #f0b429;border-radius:16px;padding:20px;background:#fffaf0}.ready{border:1px solid #2f855a;border-radius:16px;padding:20px;background:#f0fff4}</style>""",unsafe_allow_html=True)
st.title("SourcePilot")
st.caption("From Buyer Message to Procurement Decision · Professional Agents · Synthetic demonstration data")

DEFAULT="Hi, I am looking for fashionable women's shoes for Ghana. I want around 8 to 12 designs for young women. I want to start with a small quantity. My budget is limited and I need a reliable supplier. Can you help me source from China?"
with st.container(border=True):
    st.subheader("Buyer Request")
    msg=st.text_area("Paste a buyer message",value=DEFAULT,height=130,label_visibility="collapsed")
    c1,c2=st.columns([1,1])
    priority=c1.selectbox("Procurement strategy",["low_moq_balanced_risk","lowest_price"],format_func=lambda x:"Low-MOQ balanced risk" if x.startswith("low") else "Lowest price")
    go=c2.button("Start Sourcing",type="primary",use_container_width=True)

if go:
    st.session_state.result=run_agentic_workflow(msg,priority)
    st.session_state.final=None

if "result" in st.session_state:
    r=st.session_state.result
    st.subheader("Agent Activity")
    st.caption(f"Agent engine: {r.get('agent_engine','Deterministic demo mode')}")
    if r.get("agent_error"): st.warning(r["agent_error"])
    if r.get("agent_output"):
        with st.expander("Strands supervisor output",expanded=False): st.write(r["agent_output"])
    cols=st.columns(4)
    for i,step in enumerate(r["activity"]): cols[i%4].success("✓ "+step)
    req=r["requirements"]
    with st.expander("Procurement specification",expanded=True):
        a,b,c=st.columns(3); a.metric("Destination",req["destination"]); b.metric("Styles",f"{req['styles_min']}–{req['styles_max']}"); c.metric("Test-order assumption",f"{req['order_quantity']} pairs")
        if req["missing_critical"]: st.info("Missing buyer inputs: "+", ".join(req["missing_critical"])+". Safe assumptions are reversible and must be confirmed before commitment.")
    st.subheader("Supplier Comparison")
    rows=[]
    for s in r["shortlist"]:
        rows.append({"Supplier":s["company_name"],"Location":s["location"],"EXW $/pair":s["exw_price"],"MOQ":s["moq"],"Lead time (d)":s["production_lead_time"],"Quality":s["quality_score"],"Reliability":s["historical_delivery_score"],"Score":s["scoring"]["score"],"Risk flags":len(s["computed_risks"])})
    st.dataframe(rows,use_container_width=True,hide_index=True)
    st.subheader("Risk Insights")
    for s in r["shortlist"]:
        if s["computed_risks"]:
            st.markdown(f"**{s['company_name']}**")
            for risk in s["computed_risks"][:3]: st.warning(f"{risk['severity'].upper()}: {risk['reason']}")
    d=r["decision"]
    if d["required"] and not st.session_state.get("final"):
        st.markdown(f"<div class='decision'><h3>⚠ HUMAN DECISION REQUIRED</h3><p>{d['reason']}</p></div>",unsafe_allow_html=True)
        a=d.get("analysis",{})
        if a:
            st.markdown("#### Why this decision?")
            q1,q2,q3,q4=st.columns(4)
            q1.metric("Cheapest unit price",f"${a['cheapest_unit_price']:.2f}")
            q2.metric("100-pair saving",f"${a['intended_order_saving_usd']:.0f}")
            q3.metric("Extra units forced by MOQ",f"{a['additional_units_required']}")
            q4.metric("Extra EXW exposure",f"${a['additional_inventory_exw_usd']:,.0f}")
            st.caption("The model may explain the trade-off, but these quantities are calculated deterministically in Python.")
        opts=d["options"]
        b1,b2,b3=st.columns(3)
        if b1.button(opts[0]["label"],type="primary",use_container_width=True): st.session_state.final=finalize(r,opts[0]["supplier_id"]); st.rerun()
        if b2.button(opts[1]["label"],use_container_width=True): st.session_state.final=finalize(r,opts[1]["supplier_id"]); st.rerun()
        if b3.button("Show alternatives",use_container_width=True): st.info("Alternatives are already ranked in the comparison table. Change the procurement strategy to re-rank deterministically.")
    elif not d["required"] and not st.session_state.get("final"):
        st.session_state.final=finalize(r,d["recommended_supplier_id"])

if st.session_state.get("final"):
    f=st.session_state.final; s=f["selected_supplier"]
    st.markdown("<div class='ready'><h2>✓ PROCUREMENT READY</h2></div>",unsafe_allow_html=True)
    m1,m2,m3,m4=st.columns(4)
    m1.metric("Suppliers analyzed",st.session_state.result["metrics"]["suppliers_analyzed"])
    m2.metric("Selected",s["company_name"])
    m3.metric("Est. order cost",f"${s['costs']['estimated_procurement_total_excl_duty_tax']:,.0f}")
    m4.metric("Confidence",f"{f['confidence']}%")
    st.write(f["explanation"]); st.caption(f["verification_note"])
    proposal=f"""Buyer Proposal — Ghana Women's Footwear Test Order\n\nRecommended supplier: {s['company_name']} ({s['location']})\nRecommended test-order quantity: {s['modeled_order_quantity']} pairs\nEXW unit price: ${s['exw_price']:.2f}\nEstimated procurement total excluding duty/tax: ${s['costs']['estimated_procurement_total_excl_duty_tax']:,.2f}\nLead time: {s['production_lead_time']} days\n\nWhy this option: {f['explanation']}\n\nNext verification steps: confirm size distribution, final material/specification, sample approval, shipping quote, and supplier due diligence before any purchase commitment.\n\nSynthetic demonstration data."""
    st.download_button("Generate Buyer Proposal",proposal,file_name="sourcepilot-buyer-proposal.txt",mime="text/plain",type="primary")
