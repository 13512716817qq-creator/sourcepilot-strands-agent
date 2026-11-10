# Devpost Submission Draft

## Project title
SourcePilot

## Tagline
From Buyer Message to Procurement Decision.

## Inspiration
International buyers often send sourcing requests as a product image, a few messages, an approximate quantity and a destination. The difficult part is not finding a factory; it is turning incomplete intent into a procurement decision. I work with international buyers sourcing from China, so I built SourcePilot around the repetitive, judgment-heavy steps that happen between a buyer message and a confident recommendation.

## What it does
SourcePilot is an autonomous procurement decision engine. It structures a buyer request, identifies missing information, builds an RFQ, searches synthetic supplier data, normalizes commercial fields, detects risks, models procurement cost, ranks suppliers with transparent weighted scoring and stops only when a meaningful human decision is required. After approval it produces a procurement-ready plan and buyer-facing proposal.

## How we built it
The project is built in Python with the Strands Agents SDK. A Strands supervisor can call explicit supplier-search, supplier-detail, risk, cost and scoring tools. Deterministic Python functions handle arithmetic and ranking so the model never invents numerical procurement claims. Streamlit provides the product UI. An Amazon Bedrock AgentCore Runtime entrypoint is included for deployment after AWS credentials are configured. Synthetic supplier data makes the public demo reproducible and privacy-safe.

## Challenges
The main design challenge was deciding which steps should be autonomous and which should interrupt a human. Procurement contains reversible analytical work and irreversible commercial commitments. SourcePilot automates the former and creates an explicit approval gate for the latter. A second challenge was keeping agent reasoning visible without turning the interface into a developer console.

## Accomplishments
- End-to-end sourcing workflow from buyer message to procurement recommendation.
- Real tool calls for supplier search, cost, risk and scoring.
- Transparent deterministic ranking and cost calculations.
- Human-in-the-loop decision state for cost/MOQ/risk trade-offs.
- Stable synthetic-data demo mode and automated tests.

## What we learned
An effective professional agent is not a chatbot with a longer prompt. It needs tools, structured state, explicit autonomy boundaries, auditable calculations and a product experience that tells the user when judgment is actually required.

## What's next
Authorized supplier APIs, quotation PDF parsing, email/RFQ integration, freight APIs, collaborative procurement, supplier performance history and purchase-order workflows. None of these are claimed as implemented in this submission.

## Data & privacy
The public demo uses synthetic demonstration data. SourcePilot does not claim supplier legitimacy, factory inspection, customs duty or legal compliance. Those require external verification before purchase.


---

# PayPal AI Hackathon Update — SourcePilot PayFlow

> Submission status: draft. Do not submit until the PayPal Sandbox checkout and the Strands/Bedrock agent have both been demonstrated end to end and a public YouTube video under three minutes is ready.

## Project title

SourcePilot PayFlow

## Tagline

An AI procurement agent that turns an overseas buyer's request into an evidence-backed China sourcing decision and a human-approved PayPal Sandbox checkout.

## The problem

International buyers sourcing from China often start with incomplete messages, product photos, approximate quantities and unclear specifications. They must manually translate these into RFQs, search multiple marketplaces, compare inconsistent listings and quotations, account for minimum order quantities, assess commercial risks and coordinate payments. Generic chatbots can draft messages, but they rarely provide a traceable, decision-ready procurement workflow.

## The solution

SourcePilot structures buyer requirements, identifies missing information, searches supplier and product evidence, drafts RFQs, normalizes price and MOQ, calculates procurement trade-offs, flags verification gaps and produces a ranked recommendation. It pauses for human approval before material commercial decisions. The PayPal Sandbox module demonstrates a controlled test-payment step after the recommendation.

## What makes it different

SourcePilot is not an unranked supplier directory or a generic chat interface. It preserves source URLs and evidence dates, distinguishes public marketplace listing prices from formal supplier quotations, uses deterministic Python tools for cost calculations and scoring, and makes human approval part of the workflow. Synthetic demo suppliers are clearly labelled; live public-source records are not represented as independently verified factories.

## How PayPal is used

The application uses PayPal Orders v2 in the free Sandbox environment. The user can create a test order, open PayPal's approval page, approve the payment with a Sandbox buyer account, return to SourcePilot and capture the approved Sandbox order. The integration is hard-coded to the Sandbox API and does not process live payments. The demonstration payment is not a payment to a real supplier.

## How AI is used

SourcePilot uses the Strands Agents SDK to coordinate specialist agents for requirements analysis, supplier discovery, quotation normalization, risk review, commercial analysis and recommendations. Deterministic tools remain responsible for numerical calculations, scoring and risk thresholds. The submission demo must run with the Strands/Bedrock path enabled so judges can see the AI orchestration; deterministic-only mode is a fallback, not the AI demonstration.

## Built with

- Python
- Streamlit
- Strands Agents SDK
- Amazon Bedrock-compatible model integration
- PayPal Orders v2 REST API (Sandbox)
- Deterministic Python procurement, cost, scoring and risk tools
- Public B2B marketplace source records from Alibaba.com and Made-in-China.com
- Pytest and GitHub Actions

## Current development stage

Functional prototype. The repository includes a reproducible synthetic-data demo, a live-public-source evidence mode, a human approval gate, a PayPal Sandbox create/approve/capture implementation, tests and setup documentation. The new PayPal integration has unit-test coverage. End-to-end Sandbox payment verification and the final recorded demo remain required before submission.

## Significant update during the hackathon period

The pre-existing SourcePilot procurement prototype was materially extended during the PayPal AI Hackathon submission window. The update adds a PayPal Orders v2 Sandbox integration, a checkout interface inside the procurement-ready workflow, secure environment-variable configuration for credentials, automated tests, CI dependency updates and dedicated setup documentation. This is more than a cosmetic or documentation-only change.

## Demo video plan (maximum 2 minutes 50 seconds)

1. 0:00–0:15 — State the problem: fragmented buyer requests and manual China sourcing decisions.
2. 0:15–0:40 — Paste a buyer request and run SourcePilot's Strands agent workflow.
3. 0:40–1:10 — Show structured requirements, supplier evidence, quotation/listing distinction, MOQ and risk comparison.
4. 1:10–1:30 — Show the human approval gate and procurement recommendation.
5. 1:30–1:55 — Create a PayPal Sandbox order from the procurement result and open the approval page.
6. 1:55–2:20 — Approve using a PayPal Sandbox buyer account and return to SourcePilot.
7. 2:20–2:40 — Capture the Sandbox order and show the completed status.
8. 2:40–2:50 — State limitations: Sandbox only, synthetic demo supplier records, no live supplier payment or commercial traction claimed.

## Integrity and limitations

- Do not claim revenue, paying customers, completed real-world transactions or independently verified factories without evidence.
- Do not describe a marketplace listing price as a supplier quotation.
- Do not claim a successful PayPal end-to-end transaction until the Sandbox buyer approval and capture have been tested.
- Do not expose Client Secret values, AWS credentials or other secrets in the repository or video.
- Keep the demo accessible to judges without a fee or private account access that has not been explained.
