# SourcePilot

**From Buyer Message to Evidence-Backed Procurement Decision.**

SourcePilot is an autonomous AI sourcing agent that turns an overseas buyer's messy product request into a decision-ready China procurement plan and only asks the human when a real business decision is required.

> Hackathon: AWS / Devpost **Agents for Humans** · Track: **Professional Agents**
>
> SourcePilot now has two data modes: **Stable Demo** (synthetic, fully reproducible) and **Live Public Sources** (real public Alibaba.com / Made-in-China.com supplier and product source records with links, locations, listed prices, MOQ and contact paths).

## Why this problem
International sourcing is not just “find me a factory.” A buyer may send a photo, approximate quantity, budget and destination. A sourcing professional then has to structure requirements, identify possible suppliers, verify where each data point came from, distinguish public listed prices from formal quotations, compare inconsistent offers, analyze MOQ, calculate cost, identify risk and explain trade-offs.

SourcePilot turns that workflow into an agentic process.

## Why an agent, not a chatbot
A chatbot waits for prompts. SourcePilot executes a workflow: requirements → supplier discovery → source evidence → RFQ → quote normalization → risk checks → deterministic cost analysis → transparent ranking → human approval gate → procurement plan.

## Live Public Sources
`app/live_discovery.py` adds a first evidence-backed sourcing layer using real public B2B marketplace records from:

- **Alibaba.com**
- **Made-in-China.com**

The current V1 connector is intentionally conservative: it stores public-source snapshots in `data/live_supplier_sources.json` and preserves the exact product URL, supplier profile URL, public region/address when available, platform contact path, public listed price range, MOQ, verification evidence and source-check date.

It **does not call a marketplace listed price a supplier quotation**. A formal quotation only exists after the supplier receives the buyer's actual RFQ and confirms quantity, specification, packaging, Incoterm and other commercial terms.

The Live Public Sources UI therefore lets a user:

1. Search the connected evidence set.
2. Compare real public supplier/product records.
3. Open the original marketplace product page.
4. Open the supplier profile.
5. Follow the platform contact path.
6. See the public address when the source publishes one; otherwise SourcePilot shows only the verified region rather than guessing.
7. Generate an RFQ draft asking the supplier to confirm a current EXW quotation.

Future connectors can replace snapshot refreshes with authorized marketplace APIs or compliant search/retrieval providers without changing the evidence schema.

## Stable hero demo
A Ghana buyer wants 8–12 women’s shoe designs, a small test order, limited budget and a reliable supplier. SourcePilot analyzes 16 synthetic supplier profiles, exposes risks and identifies a cost-vs-MOQ decision before producing a procurement-ready recommendation.

The synthetic mode remains available because it is deterministic, reproducible and safe for a competition demo even if an external marketplace or model is unavailable.

## Architecture
![SourcePilot architecture](assets/architecture.svg)

See `docs/architecture.md` for the Mermaid version and design rationale.

## Stack
- Python
- **Strands Agents SDK**
- Amazon Bedrock-compatible Strands model path
- Amazon Bedrock AgentCore Runtime entrypoint (deployment requires AWS credentials)
- Streamlit
- Deterministic Python cost/risk/scoring tools
- JSON synthetic supplier dataset
- JSON real public-source evidence records
- Pytest + GitHub Actions

## Strands implementation
`app/agents/strands_system.py` creates a supervisor with specialized agents for requirements, supplier discovery, quote normalization, risk, commercial analysis and recommendation. The supervisor also has explicit tools:
- `search_suppliers`
- `get_supplier_details`
- `calculate_order_cost`
- `calculate_landed_cost`
- `identify_risks`
- `score_supplier`

`app/agents/agentic_workflow.py` bridges the stable procurement engine and the real Strands supervisor. The language model is not trusted with arithmetic: cost, risk thresholds and supplier scoring remain deterministic and auditable.

## Human in the loop
SourcePilot does not make irreversible commercial commitments. When the visible shortlist contains a meaningful price-vs-MOQ trade-off, the UI enters **HUMAN DECISION REQUIRED** and waits for approval.

The decision card explicitly shows *why* the human is being interrupted, including unit-price savings, extra units forced by MOQ and additional EXW inventory exposure.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

### Stable demo mode
```bash
export SOURCEPILOT_AGENT_MODE=demo
python run.py
```

### Real Strands + Bedrock mode
Configure AWS credentials, then:
```bash
export SOURCEPILOT_AGENT_MODE=strands
export BEDROCK_MODEL_ID=<your-bedrock-model-id>
python run.py
```

If Strands/Bedrock invocation is unavailable, SourcePilot preserves the deterministic workflow rather than breaking the demo.

## Tests
```bash
pytest -q
```

The test suite covers the deterministic procurement flow plus Live Public Sources provenance fields and RFQ generation. GitHub Actions runs tests on every push.

## AgentCore
This repository includes `app/agentcore_entry.py` using `BedrockAgentCoreApp`. Deployment is deliberately not claimed until it succeeds in the entrant's AWS account. See `docs/agentcore-deploy.md`.

## Data integrity
### Stable Demo
Synthetic supplier profiles are clearly labelled synthetic. They are used to prove deterministic workflow logic and are never represented as real factories.

### Live Public Sources
Marketplace supplier/product records are real public-source evidence snapshots. SourcePilot preserves source URLs and check dates, but does not assert that a listing is current, that the supplier is suitable for a specific transaction, or that the displayed listed price is a formal quote. Users must verify all critical facts before purchase.

## Privacy and limitations
- No real customer identities or confidential quotations.
- Public marketplace data is used only as source evidence in Live Public Sources mode.
- Marketplace listed prices may change and can depend on SKU, quantity and customization.
- Contact details hidden behind marketplace login are not scraped or bypassed; SourcePilot points users to the platform contact path.
- Freight, customs duty/tax, certification and legal compliance require separate verification.
- A human must verify critical commercial facts before purchase.

## Repository layout
```text
app/       UI, agents, tools, models, live discovery
data/      synthetic suppliers + public-source evidence snapshots
tests/     deterministic workflow + live-source provenance tests
docs/      rules, architecture, Devpost copy, video plan, audit
assets/    architecture + static demo preview
```

## Roadmap
Authorized marketplace APIs, compliant live-search connectors, quotation-PDF parsing, email/RFQ integration, freight APIs, supplier verification, collaborative procurement, supplier performance history, and purchase-order workflows.

## AI assistance disclosure
AI coding assistance was used to accelerate implementation, documentation and testing. Product concept, sourcing workflow, trade-off design and submission decisions remain the entrant's work.

## License
MIT.
