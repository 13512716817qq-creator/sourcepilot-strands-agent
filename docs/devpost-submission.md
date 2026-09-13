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
