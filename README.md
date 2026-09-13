# SourcePilot

**From Buyer Message to Procurement Decision.**

SourcePilot is an autonomous AI sourcing agent that turns an overseas buyer's messy product request into a decision-ready China procurement plan and only asks the human when a real business decision is required.

> Hackathon: AWS / Devpost **Agents for Humans** · Track: **Professional Agents**
>
> Data: **Synthetic demonstration data**. No real factory is represented or claimed verified.

## Why this problem
International sourcing is not just “find me a factory.” A buyer may send a photo, approximate quantity, budget and destination. A sourcing professional then has to structure requirements, compare inconsistent quotes, analyze MOQ, calculate cost, identify specification risk and explain trade-offs. SourcePilot turns that workflow into an agentic process.

## Why an agent, not a chatbot
A chatbot waits for prompts. SourcePilot executes a workflow: requirements → RFQ → supplier discovery → risk checks → deterministic cost analysis → transparent ranking → human approval gate → procurement plan. It surfaces itself when judgment matters.

## Hero demo
A Ghana buyer wants 8–12 women’s shoe designs, a small test order, limited budget and a reliable supplier. SourcePilot analyzes 16 synthetic suppliers, exposes risks and identifies a cost-vs-MOQ decision before producing a procurement-ready recommendation.

## Architecture
See `docs/architecture.md` and `assets/architecture.svg`.

## Stack
- Python
- **Strands Agents SDK**
- Amazon Bedrock-compatible Strands model path
- Amazon Bedrock AgentCore Runtime entrypoint (deployment requires AWS credentials)
- Streamlit
- Deterministic Python cost/risk/scoring tools
- JSON synthetic supplier dataset
- Pytest

## Strands implementation
`app/agents/strands_system.py` creates a Strands supervisor with explicit tools:
- `search_suppliers`
- `get_supplier_details`
- `calculate_order_cost`
- `calculate_landed_cost`
- `identify_risks`
- `score_supplier`

The language model is not trusted with arithmetic. Cost and procurement scoring are deterministic and auditable.

## Human in the loop
SourcePilot does not make irreversible commercial commitments. When the cheapest quote creates materially higher MOQ exposure, material mismatch, or another meaningful trade-off, the UI enters **HUMAN DECISION REQUIRED** and waits for approval.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

For the stable competition demo, the deterministic workflow works without AWS credentials. To invoke the real Strands/Bedrock supervisor, configure AWS credentials and use `app/agents/strands_system.py`.

## Tests
```bash
pytest -q
```

## AgentCore
Current AWS docs support deploying code-based Strands agents through the AgentCore CLI. This repository includes `app/agentcore_entry.py` for a BedrockAgentCoreApp entrypoint. Deployment is deliberately not claimed until it succeeds in the entrant's AWS account.

## Demo-mode integrity
`DEMO_MODE=true` means synthetic supplier data and deterministic outputs are used for stability. It does not invent functionality: the same procurement functions, risk rules and scoring logic execute.

## Privacy and limitations
- No real customer identities or confidential quotations.
- No claim of factory verification or supplier legitimacy.
- Freight is a modeled estimate in synthetic data.
- Customs duty/tax, certification and legal compliance are not calculated.
- A human must verify critical commercial facts before purchase.

## Repository layout
```text
app/       UI, agents, tools, models
data/      synthetic suppliers
tests/     deterministic workflow tests
docs/      rules, architecture, Devpost copy, video plan, audit
assets/    architecture image
```

## Roadmap
Authorized supplier APIs, quotation-PDF parsing, email/RFQ integration, freight APIs, collaborative procurement, supplier performance history, and purchase-order workflows.

## AI assistance disclosure
AI coding assistance was used to accelerate implementation, documentation and testing. Product concept, sourcing workflow, trade-off design and submission decisions remain the entrant's work.

## License
MIT.
