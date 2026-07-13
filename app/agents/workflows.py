from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
import operator
from app.core.config import settings

# Initialize Ollama with qwen3 model
llm = ChatOllama(
    model="qwen3",
    base_url=settings.OLLAMA_BASE_URL
)

# Define the state for LangGraph
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

# Define a simple node that uses the LLM
def chat_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", chat_node)
workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# Compile the graph
agent_executor = workflow.compile()

async def run_agent(message: str) -> str:
    # Run the compiled graph
    inputs = {"messages": [HumanMessage(content=message)]}
    result = await agent_executor.ainvoke(inputs)
    return result["messages"][-1].content
