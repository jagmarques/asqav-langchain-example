"""
asqav + LangChain - Tamper-evident audit trails for LangChain agents.

Run: python main.py
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import PromptTemplate
from asqav.extras.langchain import AsqavCallbackHandler

load_dotenv()

# When pointing at *.asqav.com, the SDK hashes context locally before sending.
# For self-hosted deployments, raw context is sent for richer audit. See docs/fingerprint-spec.md.
# Initialize the asqav callback handler - this is the only addition
handler = AsqavCallbackHandler()

# Standard LangChain setup - nothing asqav-specific below
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
tools = [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(top_k_results=1))]

prompt = PromptTemplate.from_template(
    """Answer the question using available tools.

Tools: {tools}
Tool names: {tool_names}

Question: {input}
{agent_scratchpad}"""
)

agent = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run the agent with asqav auditing enabled via callbacks
result = executor.invoke(
    {"input": "What is Python and who created it?"},
    config={"callbacks": [handler]},
)

print("
--- Result ---")
print(result["output"])

