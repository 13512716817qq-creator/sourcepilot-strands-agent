# AgentCore Deployment Runbook

This repository contains a Strands multi-agent implementation plus `app/agentcore_entry.py` using `BedrockAgentCoreApp`.

## Prerequisites
- AWS account and credentials configured locally.
- Python 3.10+.
- Node.js 20+ and npm.
- Permission to create/deploy AgentCore resources and invoke a Bedrock model.

## Recommended current CLI path
```bash
npm install -g @aws/agentcore
agentcore --version
```

Create/configure a code-based Python agent using **Strands** + **Bedrock**, then place this repository's SourcePilot code in the generated app and deploy:

```bash
agentcore create \
  --project-name SourcePilot \
  --name SourcePilotAgent \
  --language Python \
  --framework Strands \
  --model-provider Bedrock \
  --memory none \
  --build CodeZip

agentcore dev
agentcore deploy --dry-run
agentcore deploy
agentcore status
agentcore invoke --prompt "Analyze the Ghana women's footwear test-order request."
```

Do not state that SourcePilot is deployed to AgentCore until `agentcore status` confirms a working runtime and an invocation succeeds.
