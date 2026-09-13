"""Bridge between the stable procurement engine and the real Strands supervisor.

The deterministic engine remains the source of truth for arithmetic, scoring, and
synthetic supplier records. When SOURCEPILOT_AGENT_MODE=strands, the same buyer
objective is also sent through the Strands supervisor so the demo visibly proves
agent orchestration/tool use without trusting the LLM with numerical truth.
"""
from __future__ import annotations
import os
from app.agents.orchestrator import run_workflow, finalize
from app.agents.strands_system import invoke_supervisor


def run_agentic_workflow(message: str, priority: str = "low_moq_balanced_risk") -> dict:
    result = run_workflow(message, priority)
    mode = os.getenv("SOURCEPILOT_AGENT_MODE", "demo").strip().lower()
    result["agent_engine"] = "Deterministic demo mode"
    result["agent_output"] = None
    result["agent_error"] = None

    if mode in {"strands", "bedrock", "live"}:
        model_id = os.getenv("BEDROCK_MODEL_ID") or None
        prompt = f"""Complete SourcePilot's sourcing-analysis workflow for this buyer objective.
Use specialist agents and deterministic tools. Explain the decisive commercial trade-off,
but do not invent certifications, legitimacy, customs duties, or live freight rates.
Buyer message: {message}
Procurement strategy: {priority}
The deterministic application will separately verify every numeric claim before display."""
        try:
            result["agent_output"] = invoke_supervisor(prompt, model_id=model_id)
            result["agent_engine"] = "Strands Agents + Amazon Bedrock"
        except Exception as exc:
            result["agent_error"] = f"Strands invocation unavailable; deterministic workflow preserved: {exc}"
            result["agent_engine"] = "Deterministic fallback (Strands unavailable)"
    return result


__all__ = ["run_agentic_workflow", "finalize"]
