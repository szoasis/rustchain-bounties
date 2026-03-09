"""
RustChain Tools for LangChain/LangGraph Integration

This module provides LangChain tools for interacting with RustChain blockchain.
"""

import requests
from typing import Optional, Dict, Any, List
from langchain_core.tools import tool


# Default RustChain nodes
DEFAULT_NODES = [
    "http://50.28.86.131:8099",
    "http://50.28.86.153:8099",
    "http://76.8.228.245:8099",
]


def get_best_node(nodes: List[str] = None) -> Optional[str]:
    """Find the first healthy node."""
    nodes = nodes or DEFAULT_NODES
    for node in nodes:
        try:
            resp = requests.get(f"{node}/health", timeout=3)
            if resp.status_code == 200 and resp.json().get("ok"):
                return node
        except:
            continue
    return None


@tool
def rustchain_health() -> Dict[str, Any]:
    """
    Check health status of RustChain nodes.
    Returns status, version, uptime for all attestation nodes.
    """
    results = []
    for node in DEFAULT_NODES:
        try:
            resp = requests.get(f"{node}/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                results.append({
                    "node": node.replace("http://", "").replace(":8099", ""),
                    "status": "online" if data.get("ok") else "degraded",
                    "version": data.get("version", "unknown"),
                    "uptime_hours": round(data.get("uptime_s", 0) / 3600, 1),
                    "db_rw": data.get("db_rw", False),
                    "tip_age_slots": data.get("tip_age_slots", 0),
                })
        except Exception as e:
            results.append({
                "node": node.replace("http://", "").replace(":8099", ""),
                "status": "offline",
                "error": str(e),
            })
    return {"nodes": results, "healthy_count": sum(1 for r in results if r["status"] == "online")}


@tool
def rustchain_epoch() -> Dict[str, Any]:
    """
    Get current epoch information from RustChain.
    Returns epoch number, slot, blocks per epoch, and enrolled miners.
    """
    node = get_best_node()
    if not node:
        return {"error": "No healthy nodes available"}
    
    try:
        resp = requests.get(f"{node}/epoch", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "epoch": data.get("epoch"),
                "slot": data.get("slot"),
                "blocks_per_epoch": data.get("blocks_per_epoch"),
                "enrolled_miners": data.get("enrolled_miners"),
                "epoch_pot": data.get("epoch_pot"),
                "progress_percent": min(round(data.get("slot", 0) / data.get("blocks_per_epoch", 144) * 100, 1), 100),
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Failed to fetch epoch"}


@tool
def rustchain_balance(miner_id: str) -> Dict[str, Any]:
    """
    Check RTC balance for a wallet/miner ID.
    
    Args:
        miner_id: The wallet address or miner ID to check
    """
    node = get_best_node()
    if not node:
        return {"error": "No healthy nodes available"}
    
    try:
        # Try balance endpoint
        resp = requests.get(f"{node}/balance/{miner_id}", timeout=5)
        if resp.status_code == 200:
            return resp.json()
        # Try miners endpoint to find the miner
        resp = requests.get(f"{node}/miners", timeout=5)
        if resp.status_code == 200:
            miners = resp.json()
            for m in miners:
                if m.get("miner_id") == miner_id or m.get("address") == miner_id:
                    return {
                        "miner_id": m.get("miner_id"),
                        "address": m.get("address"),
                        "balance": m.get("balance", 0),
                        "stake": m.get("stake", 0),
                        "rewards": m.get("rewards", 0),
                    }
            return {"error": f"Miner {miner_id} not found"}
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Failed to fetch balance"}


@tool
def rustchain_miners(top: int = 10) -> Dict[str, Any]:
    """
    Get list of active miners from RustChain.
    
    Args:
        top: Number of top miners to return (default 10)
    """
    node = get_best_node()
    if not node:
        return {"error": "No healthy nodes available"}
    
    try:
        resp = requests.get(f"{node}/miners", timeout=10)
        if resp.status_code == 200:
            miners = resp.json()
            # Sort by balance/rewards
            sorted_miners = sorted(miners, key=lambda x: x.get("balance", 0) + x.get("rewards", 0), reverse=True)
            return {
                "total_miners": len(miners),
                "top_miners": sorted_miners[:top],
            }
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Failed to fetch miners"}


@tool
def rustchain_bounties(status: str = "open") -> Dict[str, Any]:
    """
    Get RustChain bounties from the ecosystem.
    
    Args:
        status: Filter by status - 'open', 'closed', or 'all' (default: open)
    """
    # Query GitHub API for bounties
    try:
        import os
        headers = {}
        token = os.getenv("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        
        resp = requests.get(
            "https://api.github.com/repos/Scottcjn/rustchain-bounties/issues",
            params={"labels": "bounty", "state": status},
            headers=headers,
            timeout=10
        )
        if resp.status_code == 200:
            issues = resp.json()
            bounties = []
            for issue in issues:
                bounties.append({
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "labels": [l.get("name") for l in issue.get("labels", [])],
                    "url": issue.get("html_url"),
                    "created_at": issue.get("created_at"),
                })
            return {"bounties": bounties, "count": len(bounties)}
    except Exception as e:
        return {"error": str(e)}
    return {"error": "Failed to fetch bounties"}


# Export all tools
RUSTCHAIN_TOOLS = [
    rustchain_health,
    rustchain_epoch,
    rustchain_balance,
    rustchain_miners,
    rustchain_bounties,
]
