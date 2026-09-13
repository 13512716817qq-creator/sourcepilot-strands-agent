# Demo Plan

1. Load the Ghana women's footwear request.
2. Click **Start Sourcing**.
3. Show seven completed autonomous procurement steps.
4. Show three shortlisted suppliers and visible risks.
5. Pause on **HUMAN DECISION REQUIRED**.
6. Approve the low-risk option.
7. Show **PROCUREMENT READY**, modeled cost, confidence, explanation, and generate the buyer proposal.

Use `SOURCEPILOT_AGENT_MODE=demo` for stable synthetic data. This does not fake capabilities: it executes the same deterministic procurement workflow while avoiding external API latency. Use `SOURCEPILOT_AGENT_MODE=strands` when AWS/Bedrock credentials are available to expose the real Strands supervisor output in the UI.
