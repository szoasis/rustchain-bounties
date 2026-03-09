"""
LangGraph Example: RustChain Agent

This example demonstrates how to build an AI agent that can query
the RustChain blockchain using LangGraph and the RustChain tools.
"""

from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from rustchain_tools import RUSTCHAIN_TOOLS

# Initialize the LLM
# Set OPENAI_API_KEY environment variable or use another model
llm = ChatOpenAI(model="gpt-4o-mini")

# Create the agent with RustChain tools
agent = create_react_agent(
    llm,
    tools=RUSTCHAIN_TOOLS,
    state_modifier=(
        "You are a RustChain blockchain expert assistant. "
        "You can query node health, epoch info, miner data, and bounties. "
        "Provide accurate and helpful information about the RustChain ecosystem."
    )
)


def run_agent(query: str):
    """Run the agent with a query."""
    result = agent.invoke({"messages": [("user", query)]})
    return result["messages"][-1].content


if __name__ == "__main__":
    # Example queries
    queries = [
        "What's the current health status of all RustChain nodes?",
        "What is the current epoch and slot?",
        "Show me the top 5 miners by balance.",
        "What open bounties are available?",
    ]
    
    for q in queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        print(f"{'='*60}")
        response = run_agent(q)
        print(response)
