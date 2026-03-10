# RustChain CrewAI Template

A working CrewAI agent template that demonstrates real RustChain blockchain and BoTTube video platform interactions.

## What This Does

This template creates a CrewAI agent that can:
- 🟢 Check RustChain node health and network status
- 💰 Check wallet balances
- 👨‍🏭 View active miners and their hardware
- 📊 Monitor epochs and rewards
- 🎥 Search and explore BoTTube AI video platform

## Prerequisites

```bash
# Python 3.10+
python --version  # Should be 3.10 or higher

# Install uv (optional, faster than pip)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/YOUR_USERNAME/rustchain-crewai-template.git
cd rustchain-crewai-template
```

### 2. Create Virtual Environment

```bash
# With uv (recommended)
uv venv
source .venv/bin/activate

# Or with pip
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

```bash
# Required: OpenAI API Key
export OPENAI_API_KEY="sk-..."

# Optional: Custom endpoints
export RUSTCHAIN_NODE="https://50.28.86.131"
export BOTTUBE_URL="https://bottube.ai"
export BEACON_URL="https://rustchain.org/beacon"
```

### 5. Run the Agent

```bash
# Example 1: Check node health
python main.py health

# Example 2: Check wallet balance
python main.py balance dual-g4-125

# Example 3: List active miners
python main.py miners

# Example 4: Search BoTTube videos
python main.py search "AI agents"

# Example 5: Full research task
python main.py research
```

## Project Structure

```
rustchain-crewai-template/
├── main.py                 # CLI entry point with examples
├── crewai_agent.py         # CrewAI agent definition
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── examples/
    └── langchain_example.py  # Pure LangChain version
```

## Available Tools

The agent has access to these RustChain tools:

| Tool | Description |
|------|-------------|
| `rustchain_health` | Check node health, version, uptime |
| `rustchain_epoch` | Current epoch, enrolled miners, reward pot |
| `rustchain_miners` | List active miners with hardware types |
| `rustchain_balance` | Check RTC balance for any wallet |
| `rustchain_bounties_info` | Get bounty program information |
| `bottube_stats` | Platform statistics |
| `bottube_search` | Search videos by query |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | (required) | OpenAI API key for GPT-4 |
| `RUSTCHAIN_NODE` | `https://50.28.86.131` | RustChain node URL |
| `BOTTUBE_URL` | `https://bottube.ai` | BoTTube platform URL |
| `BEACON_URL` | `https://rustchain.org/beacon` | Beacon relay URL |

## Example Output

```
$ python main.py health

🤖 Running RustChain Health Check...

🔍 Executing task...

> rustchain_health: Check RustChain node health

Result:
RustChain Node: Healthy
Version: 1.2.5
Uptime: 72h 15m
Database: Read/Write
```

## Extending the Agent

### Add More Tools

```python
from rustchain_langchain import (
    rustchain_health,
    rustchain_balance,
    bottube_search,
)

# Add to your agent
agent = Agent(
    tools=[rustchain_health, rustchain_balance, bottube_search],
    ...
)
```

### Create Custom Crews

```python
from crewai import Crew, Task, Agent

# Define tasks
research_task = Task(
    description="Research RustChain network status and find interesting miners",
    agent=researcher,
)

# Create crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True,
)

result = crew.kickoff()
```

## Troubleshooting

### "OPENAI_API_KEY not found"

Make sure you've exported your OpenAI API key:
```bash
export OPENAI_API_KEY="sk-..."
```

### "Module not found"

Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Connection errors

The RustChain node might be temporarily unavailable. Check:
- https://50.28.86.131/health

## Resources

- [RustChain GitHub](https://github.com/Scottcjn/Rustchain)
- [RustChain Bounties](https://github.com/Scottcjn/rustchain-bounties)
- [BoTTube](https://bottube.ai)
- [CrewAI Documentation](https://docs.crewai.com)
- [LangChain Documentation](https://python.langchain.com)

## License

MIT License - Feel free to use this template for your own projects!

## Credits

Built with [rustchain-langchain](https://pypi.org/project/rustchain-langchain/) - LangChain + CrewAI tools for RustChain blockchain and BoTTube.
