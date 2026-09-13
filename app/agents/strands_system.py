"""SourcePilot's real Strands multi-agent layer.

Architecture:
- Supervisor / orchestrator Agent
- Requirements Agent
- Supplier Discovery Agent
- Quote Normalization Agent
- Risk & Verification Agent
- Commercial Analysis Agent
- Recommendation Agent

Specialized Strands Agents are passed directly to the supervisor as tools. Deterministic Python tools remain the source of truth for supplier data, arithmetic, risk thresholds, and scoring.
"""
from __future__ import annotations
try:
    from strands import Agent
    from strands.models import BedrockModel
except Exception:
    Agent = None
    BedrockModel = None

from app.tools.supplier_tools import search_suppliers, get_supplier_details
from app.tools.cost_tools import calculate_order_cost, calculate_landed_cost
from app.tools.risk_tools import identify_risks
from app.tools.scoring_tools import score_supplier

SUPERVISOR_PROMPT = """You are SourcePilot Supervisor, an autonomous procurement decision engine.
Turn messy buyer intent into a decision-ready sourcing plan. Delegate specialist work to the agents available as tools.
Use deterministic tools for supplier records, arithmetic, risk checks and scoring. Never invent commercial facts.
All demo supplier data is synthetic. Never claim factory verification, certification, customs duty, or supplier legitimacy.
Autonomously handle reversible analysis. Stop and request human judgment when cost, MOQ, specification, or risk trade-offs
would create a meaningful commercial commitment. Do not behave like a generic chatbot."""


def _model(model_id: str | None = None):
    if not model_id or BedrockModel is None:
        return None
    return BedrockModel(model_id=model_id)


def _agent_kwargs(model):
    return {"model": model} if model is not None else {}


def create_agent_team(model_id: str | None = None):
    if Agent is None:
        raise RuntimeError("strands-agents is not installed")
    model = _model(model_id)
    mk = _agent_kwargs(model)

    requirements_agent = Agent(
        name="requirements_agent",
        description="Structures messy buyer messages into procurement requirements and RFQ fields.",
        system_prompt="""Extract product, destination, audience, styles, quantity, target price, material and shipping method.
Separate missing critical information from safe reversible assumptions. Return concise structured procurement facts; do not invent facts.""",
        **mk,
    )
    supplier_agent = Agent(
        name="supplier_discovery_agent",
        description="Searches and inspects the synthetic supplier dataset using tools.",
        system_prompt="Use supplier tools to find relevant candidates. Never fabricate a supplier record.",
        tools=[search_suppliers, get_supplier_details],
        **mk,
    )
    quote_agent = Agent(
        name="quote_normalization_agent",
        description="Normalizes supplier quote fields and highlights missing commercial information.",
        system_prompt="Normalize price, currency, MOQ, material, packaging, lead time, domestic freight and sample cost from provided records. Flag missing fields; never invent them.",
        **mk,
    )
    risk_agent = Agent(
        name="risk_verification_agent",
        description="Checks specification and commercial risks and explains why verification is needed.",
        system_prompt="Use identify_risks. Say 'requires verification' or 'commercial risk flag'; never call a supplier fraudulent.",
        tools=[identify_risks, get_supplier_details],
        **mk,
    )
    commercial_agent = Agent(
        name="commercial_analysis_agent",
        description="Calculates order and modeled landed procurement costs with deterministic tools.",
        system_prompt="Use calculation tools for every numerical cost claim. State clearly that duty/tax are excluded unless data exists.",
        tools=[calculate_order_cost, calculate_landed_cost],
        **mk,
    )
    recommendation_agent = Agent(
        name="recommendation_agent",
        description="Ranks suppliers using transparent procurement scoring and explains trade-offs.",
        system_prompt="Use score_supplier rather than price alone. Explain the decisive trade-off and escalate meaningful commitments to the human.",
        tools=[score_supplier, get_supplier_details],
        **mk,
    )
    return [requirements_agent, supplier_agent, quote_agent, risk_agent, commercial_agent, recommendation_agent]


def create_supervisor(model_id: str | None = None):
    if Agent is None:
        raise RuntimeError("strands-agents is not installed")
    model = _model(model_id)
    specialists = create_agent_team(model_id)
    kwargs = {
        "name": "sourcepilot_supervisor",
        "description": "Coordinates an end-to-end procurement decision workflow.",
        "system_prompt": SUPERVISOR_PROMPT,
        "tools": specialists + [search_suppliers, get_supplier_details, calculate_order_cost, calculate_landed_cost, identify_risks, score_supplier],
    }
    if model is not None:
        kwargs["model"] = model
    return Agent(**kwargs)


def invoke_supervisor(prompt: str, model_id: str | None = None) -> str:
    return str(create_supervisor(model_id)(prompt))
