#!/usr/bin/env python3
"""
RustChain CrewAI Template - Main Entry Point
=============================================
CLI tool to run RustChain-powered AI agents.

Usage:
    python main.py health          - Check node health
    python main.py balance <id>   - Check wallet balance
    python main.py miners          - List active miners
    python main.py epoch           - Get epoch info
    python main.py bounties        - Get bounty info
    python main.py bottube         - Get BoTTube stats
    python main.py search <query>  - Search BoTTube videos
    python main.py research        - Full research task
"""

import os
import sys
import argparse
from dotenv import load_dotenv

# Load .env file if exists
load_dotenv()

# Import agent and tools
from crewai import Task, Crew
from crewai_agent import (
    create_rustchain_agent,
    create_researcher_agent,
    get_llm,
)
from rustchain_langchain.tools import (
    rustchain_health,
    rustchain_balance,
    rustchain_miners,
    rustchain_epoch,
    rustchain_bounties_info,
    bottube_stats,
    bottube_search,
)


def check_api_key():
    """Verify OpenAI API key is set."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not set")
        print("\nSet it with:")
        print("  export OPENAI_API_KEY='sk-...'")
        print("\nOr create a .env file:")
        print("  echo 'OPENAI_API_KEY=sk-...' > .env")
        sys.exit(1)


def cmd_health(args):
    """Check RustChain node health."""
    print("🔍 Checking RustChain node health...\n")
    
    result = rustchain_health()
    print(f"✅ Result:\n{result}")
    return result


def cmd_balance(args):
    """Check wallet balance."""
    wallet_id = args.wallet or "dual-g4-125"
    print(f"💰 Checking balance for wallet: {wallet_id}\n")
    
    result = rustchain_balance(wallet_id=wallet_id)
    print(f"✅ Result:\n{result}")
    return result


def cmd_miners(args):
    """List active miners."""
    print("👨‍🏭 Fetching active miners...\n")
    
    result = rustchain_miners()
    print(f"✅ Result:\n{result}")
    return result


def cmd_epoch(args):
    """Get epoch information."""
    print("📊 Fetching epoch information...\n")
    
    result = rustchain_epoch()
    print(f"✅ Result:\n{result}")
    return result


def cmd_bounties(args):
    """Get bounty information."""
    print("🎯 Fetching RustChain bounty info...\n")
    
    result = rustchain_bounties_info()
    print(f"✅ Result:\n{result}")
    return result


def cmd_bottube(args):
    """Get BoTTube platform stats."""
    print("🎥 Fetching BoTTube statistics...\n")
    
    result = bottube_stats()
    print(f"✅ Result:\n{result}")
    return result


def cmd_search(args):
    """Search BoTTube videos."""
    query = args.query or "AI agents"
    print(f"🔎 Searching BoTTube for: '{query}'\n")
    
    result = bottube_search(query=query)
    print(f"✅ Result:\n{result}")
    return result


def cmd_research(args):
    """Run full research task with CrewAI."""
    check_api_key()
    
    print("🤖 Running full research task with CrewAI...\n")
    print("=" * 50)
    
    # Create agents
    researcher = create_researcher_agent()
    
    # Define research task
    research_task = Task(
        description=(
            "Research the current state of RustChain blockchain network:\n"
            "1. Check node health and version\n"
            "2. List top 5 active miners with their hardware and antiquity multipliers\n"
            "3. Get current epoch info (epoch number, enrolled miners, reward pot)\n"
            "4. Check BoTTube platform stats\n"
            "5. Search for trending AI agent videos on BoTTube\n"
            "6. Summarize the RustChain bounty program\n"
            "\n"
            "Provide a comprehensive report of the findings."
        ),
        agent=researcher,
        expected_output=(
            "A comprehensive report covering node health, miner activity, "
            "epoch status, BoTTube stats, and bounty opportunities."
        ),
    )
    
    # Create crew
    crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        verbose=True,
        memory=True,
    )
    
    # Execute
    result = crew.kickoff()
    
    print("\n" + "=" * 50)
    print("📋 FINAL RESEARCH REPORT:")
    print("=" * 50)
    print(result)
    
    return result


def cmd_interactive(args):
    """Run interactive agent session."""
    check_api_key()
    
    print("🤖 Starting interactive RustChain Agent...")
    print("Type 'exit' to quit\n")
    
    agent = create_rustchain_agent()
    
    while True:
        try:
            query = input("💬 You: ").strip()
            
            if query.lower() in ['exit', 'quit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            # Run agent with task
            task = Task(
                description=query,
                agent=agent,
            )
            
            crew = Crew(
                agents=[agent],
                tasks=[task],
                verbose=False,
            )
            
            result = crew.kickoff()
            print(f"\n🤖 Agent: {result}\n")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="RustChain CrewAI Template - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py health              Check node health
  python main.py balance dual-g4-125 Check wallet balance
  python main.py miners              List active miners
  python main.py search "AI agents"  Search BoTTube
  python main.py research            Full research task

Environment:
  OPENAI_API_KEY     Required for AI agents (CLI tools work without it)
  RUSTCHAIN_NODE    RustChain node URL (default: https://50.28.86.131)
  BOTTUBE_URL       BoTTube URL (default: https://bottube.ai)
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Health check
    subparsers.add_parser("health", help="Check RustChain node health")
    
    # Balance check
    balance_parser = subparsers.add_parser("balance", help="Check wallet balance")
    balance_parser.add_argument("wallet", nargs="?", help="Wallet address or miner ID")
    
    # Miners
    subparsers.add_parser("miners", help="List active miners")
    
    # Epoch
    subparsers.add_parser("epoch", help="Get epoch information")
    
    # Bounties
    subparsers.add_parser("bounties", help="Get bounty program info")
    
    # BoTTube
    subparsers.add_parser("bottube", help="Get BoTTube platform stats")
    
    # Search
    search_parser = subparsers.add_parser("search", help="Search BoTTube videos")
    search_parser.add_argument("query", nargs="?", help="Search query")
    
    # Research
    subparsers.add_parser("research", help="Run full research task")
    
    # Interactive
    subparsers.add_parser("interactive", help="Interactive agent session")
    
    args = parser.parse_args()
    
    # Default to health if no command
    if not args.command:
        args.command = "health"
    
    # Route to handler
    handlers = {
        "health": cmd_health,
        "balance": cmd_balance,
        "miners": cmd_miners,
        "epoch": cmd_epoch,
        "bounties": cmd_bounties,
        "bottube": cmd_bottube,
        "search": cmd_search,
        "research": cmd_research,
        "interactive": cmd_interactive,
    }
    
    handler = handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
