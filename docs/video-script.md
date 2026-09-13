# 4:35 Demo Video Script

**0:00–0:22 — Buyer message on screen**
Narration: “Buying from China is not difficult because products are impossible to find. The hard part is turning a vague buyer request into a confident procurement decision. My name is Fenix. I work with international buyers sourcing products from China, and I built SourcePilot around that real workflow.”

**0:22–0:42 — Product home**
“SourcePilot is a procurement decision engine, not another sourcing chatbot. It takes a messy buyer request, performs the repetitive analysis autonomously, and comes back only when a real business decision is required.”

**0:42–0:58 — Architecture image**
“It uses Strands Agents as the orchestration layer, real tools for supplier lookup, risk, cost and scoring, and deterministic Python for arithmetic. The application is also prepared for Amazon Bedrock AgentCore Runtime deployment.”

**0:58–1:25 — Paste Ghana request, click Start Sourcing**
“This buyer wants eight to twelve women’s shoe designs for Ghana, a small test order, limited budget and a reliable supplier. The request is incomplete, so SourcePilot separates safe assumptions from missing information that must be verified.”

**1:25–2:05 — Agent Activity + spec**
“Without asking me to manage every step, the agent structures the requirement, builds the procurement specification, searches candidate suppliers, normalizes commercial data, checks risks, calculates modeled costs and ranks suppliers.”

**2:05–2:45 — Supplier comparison + risks**
“Here the cheapest supplier is not automatically the best. The scoring considers price, MOQ, quality, delivery reliability, lead time, quotation completeness and explicit commercial risk flags. Numerical calculations are deterministic rather than invented by the language model.”

**2:45–3:25 — Human Decision Required**
“This is the important moment. SourcePilot sees a genuine trade-off: the cheapest quote requires a much larger MOQ, increasing initial inventory exposure. Instead of silently committing, the agent asks for human judgment. I choose the low-risk test-order option.”

**3:25–3:55 — Procurement Ready**
“Now the workflow resumes and returns a procurement-ready result: selected supplier, modeled order cost, confidence, explanation and verification steps. I can generate a buyer-facing proposal immediately.”

**3:55–4:20 — Code / tool files / AgentCore entrypoint**
“Under the hood, Strands is central to tool orchestration. The repository includes explicit supplier, risk, cost and scoring tools, automated tests, and an AgentCore Runtime entrypoint. Synthetic supplier data keeps the public demo reproducible and privacy-safe.”

**4:20–4:35 — Closing**
“Search tools find suppliers. Chatbots answer questions. SourcePilot manages the decision workflow between the two — from buyer message to procurement decision.”

## Recording safety
Use demo mode, close unrelated tabs, zoom browser to 100–110%, preload the request, record 1080p, and keep the final video under 5:00. If live Bedrock is slow, record the deterministic demo mode and show the Strands/AgentCore implementation in the code segment rather than waiting on network latency.
