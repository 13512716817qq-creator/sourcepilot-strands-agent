from __future__ import annotations

import sys
from pathlib import Path

# Streamlit executes this file directly on Render. Add the project root so
# absolute imports such as `app.agents...` work consistently in deployment.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from app.agents.agentic_workflow import run_agentic_workflow, finalize

st.set_page_config(page_title="SourcePilot", page_icon="🧭", layout="wide")
st.markdown(
    """
    <style>
    .block-container{max-width:1180px;padding-top:2rem}
    .decision{border:1px solid #f0b429;border-radius:16px;padding:20px;background:#fffaf0}
    .ready{border:1px solid #2f855a;border-radius:16px;padding:20px;background:#f0fff4}
    .provenance{border:1px solid #d7dee8;border-radius:14px;padding:16px;background:#f8fafc}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("SourcePilot")
st.caption("From Buyer Message to Procurement Decision · Professional Agents · Synthetic demonstration data")

DEFAULT = (
    "Hi, I am looking for fashionable women's shoes for Ghana. I want around 8 to 12 designs "
    "for young women. I want to start with a small quantity. My budget is limited and I need a "
    "reliable supplier. Can you help me source from China?"
)

with st.container(border=True):
    st.subheader("Buyer Request")
    msg = st.text_area("Paste a buyer message", value=DEFAULT, height=130, label_visibility="collapsed")
    c1, c2 = st.columns([1, 1])
    priority = c1.selectbox(
        "Procurement strategy",
        ["low_moq_balanced_risk", "lowest_price"],
        format_func=lambda x: "Low-MOQ balanced risk" if x.startswith("low") else "Lowest price",
    )
    go = c2.button("Start Sourcing", type="primary", use_container_width=True)

if go:
    st.session_state.result = run_agentic_workflow(msg, priority)
    st.session_state.final = None

if "result" in st.session_state:
    r = st.session_state.result
    d = r["decision"]

    st.subheader("Agent Activity")
    st.caption(f"Agent engine: {r.get('agent_engine', 'Deterministic demo mode')}")
    if r.get("agent_error"):
        st.warning(r["agent_error"])
    if r.get("agent_output"):
        with st.expander("Strands supervisor output", expanded=False):
            st.write(r["agent_output"])

    cols = st.columns(4)
    for i, step in enumerate(r["activity"]):
        cols[i % 4].success("✓ " + step)

    req = r["requirements"]
    with st.expander("Procurement specification", expanded=True):
        a, b, c = st.columns(3)
        a.metric("Destination", req["destination"])
        b.metric("Styles", f"{req['styles_min']}–{req['styles_max']}")
        c.metric("Modeled test order", f"{req['order_quantity']} pairs")
        if req["missing_critical"]:
            st.info(
                "Missing buyer inputs: " + ", ".join(req["missing_critical"]) +
                ". SourcePilot uses reversible demo assumptions until the buyer confirms them."
            )

    st.subheader("Shortlisted Supplier Comparison")
    st.markdown(
        """
        <div class="provenance">
        <b>Demo data provenance</b><br>
        These supplier names, city/province locations and quoted prices are <b>synthetic test records</b>
        created for this hackathon. They are not live factory quotations and do not represent verified companies.
        The EXW prices below are fixed, reproducible test inputs in <code>data/suppliers.json</code>.
        Quote basis: <b>USD per pair · EXW China · modeled small test order</b>. International freight,
        customs duty and tax are not included in the unit price.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(
        "SourcePilot scored 16 synthetic supplier profiles using price, MOQ, quality, delivery reliability, "
        "lead time, quotation completeness and explicit risk rules. The three highest-ranked profiles are shown below."
    )

    rows = []
    for idx, s in enumerate(r["shortlist"]):
        status = "Recommended" if s["supplier_id"] == d.get("recommended_supplier_id") else f"Alternative #{idx + 1}"
        rows.append(
            {
                "Supplier": s["company_name"],
                "Status": status,
                "City / Province (demo profile)": s["location"],
                "EXW USD/pair": s["exw_price"],
                "MOQ (pairs)": s["moq"],
                "Lead time (days)": s["production_lead_time"],
                "Quality": s["quality_score"],
                "Reliability": s["historical_delivery_score"],
                "Procurement score": s["scoring"]["score"],
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)

    flagged = [s for s in r["shortlist"] if s["computed_risks"]]
    if flagged:
        st.subheader("Shortlist Risk Checks")
        for s in flagged:
            st.markdown(f"**{s['company_name']}**")
            for risk in s["computed_risks"][:3]:
                st.warning(f"{risk['severity'].upper()}: {risk['reason']}")
    else:
        st.caption("No critical rule-based risk flags were triggered for the three shortlisted demo profiles.")

    if d["required"] and not st.session_state.get("final"):
        st.markdown(
            f"<div class='decision'><h3>⚠ HUMAN DECISION REQUIRED</h3><p>{d['reason']}</p></div>",
            unsafe_allow_html=True,
        )
        a = d.get("analysis", {})
        if a:
            st.markdown("#### Why this decision?")
            q1, q2, q3, q4 = st.columns(4)
            q1.metric("Lower-price shortlisted offer", f"${a['cheapest_unit_price']:.2f}/pair")
            q2.metric(f"Saving on {req['order_quantity']} pairs", f"${a['intended_order_saving_usd']:,.0f}")
            q3.metric("Extra units required by MOQ", f"{a['additional_units_required']}")
            q4.metric("Extra EXW commitment", f"${a['additional_inventory_exw_usd']:,.0f}")
            st.caption(
                "All four figures are calculated deterministically from the three visible shortlisted demo profiles; "
                "the language model is not trusted to calculate them."
            )

        opts = d["options"]
        b1, b2, b3 = st.columns(3)
        if b1.button(opts[0]["label"], type="primary", use_container_width=True):
            st.session_state.final = finalize(r, opts[0]["supplier_id"])
            st.rerun()
        if b2.button(opts[1]["label"], use_container_width=True):
            st.session_state.final = finalize(r, opts[1]["supplier_id"])
            st.rerun()
        if b3.button("Review shortlist", use_container_width=True):
            st.info("All suppliers involved in this decision are the three profiles shown in the shortlist above.")

    elif not d["required"] and not st.session_state.get("final"):
        st.session_state.final = finalize(r, d["recommended_supplier_id"])

if st.session_state.get("final"):
    f = st.session_state.final
    s = f["selected_supplier"]
    st.markdown("<div class='ready'><h2>✓ PROCUREMENT READY</h2></div>", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Profiles analyzed", st.session_state.result["metrics"]["suppliers_analyzed"])
    m2.metric("Selected", s["company_name"])
    m3.metric("Est. modeled order cost", f"${s['costs']['estimated_procurement_total_excl_duty_tax']:,.0f}")
    m4.metric("Decision confidence", f"{f['confidence']}%")

    st.write(f["explanation"])
    st.caption(f["verification_note"])

    proposal = f"""Buyer Proposal — Ghana Women's Footwear Test Order

Recommended demo supplier profile: {s['company_name']}
City / Province (synthetic profile): {s['location']}
Modeled order quantity: {s['modeled_order_quantity']} pairs
Synthetic EXW test input: ${s['exw_price']:.2f} per pair
Estimated procurement total excluding duty/tax: ${s['costs']['estimated_procurement_total_excl_duty_tax']:,.2f}
Lead time assumption: {s['production_lead_time']} days

Why this option: {f['explanation']}

Next verification steps for a real transaction: obtain a live supplier quotation, verify company identity and address, confirm product specification and size distribution, approve a sample, verify freight, and complete commercial due diligence before any purchase commitment.

Synthetic demonstration data only. This is not a live supplier quote or supplier verification report."""

    st.download_button(
        "Generate Buyer Proposal",
        proposal,
        file_name="sourcepilot-buyer-proposal.txt",
        mime="text/plain",
        type="primary",
    )
