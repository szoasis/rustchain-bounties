"""
CrewAI Example: RustChain Research Crew

This example demonstrates how to build a CrewAI crew that can
research the RustChain blockchain using the RustChain tools.
"""

from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

from rustchain_tools import RUSTCHAIN_TOOLS


# Initialize the LLM
llm = ChatOpenAI(model="gpt-4o-mini")


def create_crew():
    """Create a RustChain research crew."""
    
    # Define the researcher agent
    researcher = Agent(
        role="RustChain Researcher",
        goal="Gather accurate information about the RustChain blockchain",
        backstory=(
            "You are an expert in blockchain technology with deep knowledge "
            "of RustChain, a Proof-of-Antiquity blockchain. You can query "
            "nodes, check miner status, and find bounty opportunities."
        ),
        tools=RUSTCHAIN_TOOLS,
        llm=llm,
        verbose=True,
    )
    
    # Define tasks
    task_health = Task(
        description="Check the health status of all RustChain nodes",
        agent=researcher,
        expected_output="A report on node health, version, and uptime",
    )
    
    task_epoch = Task(
        description="Get current epoch information including slot and block progress",
        agent=researcher,
        expected_output="Epoch number, slot position, and progress percentage",
    )
    
    task_miners = Task(
        description="Find the top 5 miners by balance",
        agent=researcher,
        expected_output="List of top miners with their balances",
    )
    
    task_bounties = Task(
        description="List all open bounties in the RustChain ecosystem",
        agent=researcher,
        expected_output="A list of available bounties with rewards",
    )
    
    # Create the crew
    crew = Crew(
        agents=[researcher],
        tasks=[task_health, task_epoch, task_miners, task_bounties],
        verbose=True,
    )
    
    return crew


def run_research():
    """Run the research crew."""
    crew = create_crew()
    result = crew.kickoff()
    return result


if __name__ == "__main__":
    print("Starting RustChain Research Crew...")
    print("=" * 60)
    result = run_research()
    print("\n" + "=" * 60)
    print("Research Results:")
    print("=" * 60)
    print(result)
