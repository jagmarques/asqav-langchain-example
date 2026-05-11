"""
asqav + LangChain - Tamper-evident audit trails for LangChain agents.

Run: python main.py
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import PromptTemplate
from asqav.extras.langchain import AsqavCallbackHandler

load_dotenv()

# SDK hashes context client-side when baseUrl is *.asqav.com; see docs/fingerprint-spec.md.
handler = AsqavCallbackHandler()

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

result = executor.invoke(
    {"input": "What is Python and who created it?"},
    config={"callbacks": [handler]},
)

print("\n--- Result ---")
print(result["output"])

