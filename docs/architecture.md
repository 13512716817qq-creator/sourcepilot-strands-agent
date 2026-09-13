# Architecture

```mermaid
flowchart TD
  U[Buyer / Sourcing Professional] --> UI[SourcePilot Streamlit UI]
  UI --> S[Strands Supervisor Agent]
  S --> R[Requirements Agent]
  S --> D[Supplier Discovery Tool]
  S --> N[Quote Normalization / Structured Data]
  S --> K[Risk & Verification Tool]
  S --> C[Deterministic Cost Tool]
  S --> Q[Deterministic Scoring Tool]
  Q --> H{Human Approval Gate}
  H -->|Approve| P[Procurement Plan]
  H -->|Alternative| Q
  S -. deployable .-> AC[Amazon Bedrock AgentCore Runtime]
  S -. model .-> BR[Amazon Bedrock]
  D --> DB[(Synthetic suppliers.json)]
```

## Design choices
Strands is the agent interface and tool-orchestration layer. Procurement arithmetic, risk thresholds and ranking are deterministic Python so numerical claims are auditable. The UI surfaces autonomy as a workflow rather than a chat transcript, then interrupts the human only for a material cost/risk trade-off.

AgentCore Runtime is implemented as a deployable entrypoint but is not claimed as deployed until an AWS account is actually configured and deployment succeeds.
