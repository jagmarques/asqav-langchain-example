# asqav + LangChain Example

Add tamper-evident audit trails to any LangChain agent in 3 lines of code.

## What this does

Wraps a LangChain ReAct agent with `AsqavCallbackHandler`. Every LLM call, tool use, and chain execution gets logged to an immutable, hash-chained audit trail - no code changes to your agent logic.

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

Every event is hash-chained to the previous one. If anyone tampers with the logs, the chain breaks and you know exactly where.

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
