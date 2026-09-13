"""AgentCore Runtime entrypoint. Deploy only after AWS credentials are configured."""
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from app.agents.strands_system import invoke_supervisor

app=BedrockAgentCoreApp()

@app.entrypoint
def sourcepilot(payload, context):
    prompt=payload.get("prompt") or payload.get("input",{}).get("prompt","")
    if not isinstance(prompt,str) or not prompt.strip():
        return {"error":"A non-empty prompt is required."}
    return {"result":invoke_supervisor(prompt)}

if __name__ == "__main__":
    app.run()
