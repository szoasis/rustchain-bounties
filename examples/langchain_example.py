"""
LangChain Example - Pure LangChain Version
===========================================
This example shows how to use RustChain tools with pure LangChain
without CrewAI's crew orchestration.

Usage:
    python examples/langchain_example.py
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# LangChain components
from langchain.agents import AgentExecutor, initialize_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool

# RustChain tools
from rustchain_langchain.tools import (
    rustchain_health,
    rustchain_balance,
    rustchain_miners,
    rustchain_epoch,
    rustchain_bounties_info,
    bottube_stats,
    bottube_search,
)


def create_langchain_tools():
    """Convert rustchain-langchain tools to LangChain format."""
    
    tools = [
        Tool(
            name="rustchain_health",
            func=lambda x: rustchain_health(),
            description="Check RustChain node health, version, uptime, and database status.",
        ),
        Tool(
            name="rustchain_balance",
            func=lambda x: rustchain_balance(wallet_id=x.strip() or "dual-g4-125"),
            description="Check RTC token balance for a RustChain wallet. Input: wallet address        ),
        Tool or miner ID.",
(
            name="rustchain_miners",
            func=lambda x: rustchain_miners(),
            description="List active RustChain miners with hardware types and antiquity multipliers.",
        ),
        Tool(
            name="rustchain_epoch",
            func=lambda x: rustchain_epoch(),
            description="Get current RustChain epoch information including rewards and enrolled miners.",
        ),
        Tool(
            name="rustchain_bounties_info",
            func=lambda x: rustchain_bounties_info(),
            description="Get information about available RustChain bounties for earning RTC tokens.",
        ),
        Tool(
            name="bottube_stats",
            func=lambda x: bottube_stats(),
            description="Get BoTTube AI video platform statistics.",
        ),
        Tool(
            name="bottube_search",
            func=lambda x: bottube_search(query=x.strip() or "AI"),
            description="Search for videos on BoTTube AI video platform. Input: search query.",
        ),
    ]
    
    return tools


def main():
    """Run LangChain agent example."""
    
    print("=" * 60)
    print("RustChain LangChain Agent")
    print("=" * 60)
    
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not set")
        print("\nSet it with:")
        print("  export OPENAI_API_KEY='sk-...'")
        return
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=api_key,
        temperature=0.7,
    )
    
    # Get tools
    tools = create_langchain_tools()
    
    print(f"\n✅ Loaded {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool.name}")
    
    # Initialize agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent="zero-shot-react-description",
        verbose=True,
        max_iterations=10,
    )
    
    print("\n" + "=" * 60)
    print("Agent ready! Ask me about RustChain or BoTTube.")
    print("Examples:")
    print("  - Check the RustChain node health")
    print("  - What's the balance of wallet dual-g4-125?")
    print("  - List the active miners")
    print("  - Show me BoTTube stats")
    print("  - Search for AI videos on BoTTube")
    print("=" * 60)
    
    # Run example queries automatically
    print("\n📋 Running example queries...\n")
    
    queries = [
        "Check the RustChain node health",
        "What is the current epoch information?",
        "Show me the top 3 miners",
        "What are the BoTTube platform statistics?",
    ]
    
    for query in queries:
        print(f"\n💬 Query: {query}")
        print("-" * 40)
        try:
            result = agent.run(query)
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
