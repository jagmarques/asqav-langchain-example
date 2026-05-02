<p align="center">
  <a href="https://asqav.com"><img src="https://asqav.com/logo-text-white.png" alt="Asqav" width="150"></a>
</p>

# Asqav + LangChain Example

Add verifiable audit trails to any LangChain agent in 3 lines of code.

## Data handling

This example uses the `asqav` Python SDK. By default, the SDK auto-detects the deployment:

- **Asqav cloud (`*.asqav.com`):** the SDK hashes your action context locally and sends only the hash plus a small metadata bag (action_type, agent_id, session_id, model_name, tool_name). Raw prompts and tool arguments never leave your infrastructure.
- **Self-hosted:** the SDK sends the full context so the server can run policy checks, PII redaction, and richer audit views.

Override per call:

```python
import asqav

asqav.init(api_key="sk_...", base_url="https://api.asqav.com", mode="hash-only")
```

This is GDPR-aware data minimization by default for cloud deployments. See [docs/fingerprint-spec.md](https://github.com/jagmarques/asqav-sdk/blob/main/docs/fingerprint-spec.md) in the SDK repo for the fingerprint spec and conformance vectors.

## What this does

Wraps a LangChain ReAct agent with `AsqavCallbackHandler`. Every LLM call, tool use, and chain execution gets logged to an immutable, linked audit trail - no code changes to your agent logic.

## Quick start

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your keys to .env
python main.py
```

## What you get

After running, you will see normal LangChain agent output plus:

```
[asqav] Session started: a]1f3...
[asqav] Logged: llm_call (gpt-4o) - 847 tokens
[asqav] Logged: tool_use (Wikipedia) - search: "Python programming"
[asqav] Logged: agent_finish - hash chain verified
[asqav] Audit trail: 3 events, chain integrity: valid
```

Every event is linked to the previous one. If anyone tampers with the logs, the chain breaks and you know exactly where.

## How it works

```python
from asqav.extras.langchain import AsqavCallbackHandler

# This is the only line you add to your existing agent
handler = AsqavCallbackHandler()

# Pass it to any LangChain component
agent.invoke({"input": "your prompt"}, config={"callbacks": [handler]})
```

That is it. Your agent works exactly the same, but now you have a complete audit trail.

## Requirements

- Python 3.10+
- OpenAI API key (for the LangChain agent)
- asqav API key (free tier available at [asqav.com](https://asqav.com))
