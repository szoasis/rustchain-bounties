"""
RustChain CrewAI Agent
=======================
A CrewAI agent that uses RustChain and BoTTube tools.
"""

import os
from crewai import Agent
from langchain_openai import ChatOpenAI

# Import RustChain tools
try:
    from rustchain_langchain.tools import (
        rustchain_health,
        rustchain_balance,
        rustchain_miners,
        rustchain_epoch,
        rustchain_bounties_info,
        bottube_stats,
        bottube_search,
    )
except ImportError:
    print("Warning: rustchain-langchain not installed. Install with: pip install rustchain-langchain")
    # Fallback - create dummy tools
    def rustchain_health():
        """Placeholder - install rustchain-langchain"""
        return "Error: rustchain-langchain not installed"
    
    def rustchain_balance(wallet_id: str):
        return f"Error: rustchain-langchain not installed"
    
    def rustchain_miners():
        return "Error: rustchain-langchain not installed"
    
    def rustchain_epoch():
        return "Error: rustchain-langchain not installed"
    
    def rustchain_bounties_info():
        return "Error: rustchain-langchain not installed"
    
    def bottube_stats():
        return "Error: rustchain-langchain not installed"
    
    def bottube_search(query: str):
        return "Error: rustchain-langchain not installed"


def get_llm():
    """Initialize the LLM."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    return ChatOpenAI(
        model="gpt-4o",
        api_key=api_key,
        temperature=0.7,
    )


def create_rustchain_agent():
    """Create a CrewAI agent with RustChain tools."""
    
    llm = get_llm()
    
    # Define the tools list
    tools = [
        rustchain_health,
        rustchain_balance,
        rustchain_miners,
        rustchain_epoch,
        rustchain_bounties_info,
        bottube_stats,
        bottube_search,
    ]
    
    # Create the agent
    agent = Agent(
        role="RustChain Blockchain Analyst",
        goal="Provide accurate information about RustChain blockchain, miners, and BoTTube platform",
        backstory=(
            "You are an expert analyst specializing in the RustChain Proof-of-Antiquity blockchain. "
            "You have deep knowledge of RTC tokenomics, miner hardware types, antiquity multipliers, "
            "and the BoTTube AI video platform. You help users understand the network status, "
            "check balances, and explore the ecosystem."
        ),
        verbose=True,
        allow_delegation=False,
        tools=tools,
        llm=llm,
    )
    
    return agent


def create_researcher_agent():
    """Create a research-focused agent."""
    
    llm = get_llm()
    
    tools = [
        rustchain_health,
        rustchain_miners,
        rustchain_epoch,
        rustchain_bounties_info,
        bottube_stats,
        bottube_search,
    ]
    
    agent = Agent(
        role="Blockchain Researcher",
        goal="Research and analyze RustChain network metrics and BoTTube trends",
        backstory=(
            "You are a data-driven researcher who specializes in analyzing blockchain networks. "
            "You track miner activity, epoch rewards, platform growth, and emerging trends. "
            "Your insights help understand the RustChain ecosystem."
        ),
        verbose=True,
        allow_delegation=False,
        tools=tools,
        llm=llm,
    )
    
    return agent


if __name__ == "__main__":
    # Quick test
    print("Testing RustChain Agent...")
    
    # Check if API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Set it with:")
        print("    export OPENAI_API_KEY='sk-...'")
        print("\nTools are available. Test individually:")
        print("  - rustchain_health()")
        print("  - rustchain_balance('dual-g4-125')")
        print("  - rustchain_miners()")
        print("  - bottube_search('AI')")
    else:
        agent = create_rustchain_agent()
        print("✅ Agent created successfully!")
        print(f"   Role: {agent.role}")
        print(f"   Tools: {len(agent.tools)} available")
