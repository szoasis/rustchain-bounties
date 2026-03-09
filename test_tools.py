#!/usr/bin/env python3
"""
Quick test script to verify RustChain tools are working.
"""

from rustchain_tools import (
    rustchain_health,
    rustchain_epoch,
    rustchain_miners,
    rustchain_bounties,
)


def main():
    print("🧪 Testing RustChain Tools\n")
    
    # Test health
    print("1. Testing rustchain_health...")
    result = rustchain_health.invoke({})
    print(f"   Nodes: {result.get('healthy_count')}/{len(result.get('nodes', []))} online")
    for node in result.get("nodes", [])[:2]:
        print(f"   - {node.get('node')}: {node.get('status')} ({node.get('version')})")
    
    # Test epoch
    print("\n2. Testing rustchain_epoch...")
    result = rustchain_epoch.invoke({})
    print(f"   Epoch: {result.get('epoch')}, Slot: {result.get('slot')}/{result.get('blocks_per_epoch')}")
    print(f"   Progress: {result.get('progress_percent')}%")
    
    # Test miners
    print("\n3. Testing rustchain_miners...")
    result = rustchain_miners.invoke({"top": 3})
    print(f"   Total miners: {result.get('total_miners')}")
    for m in result.get("top_miners", [])[:3]:
        print(f"   - {m.get('miner_id', m.get('address', 'unknown'))[:20]}: {m.get('balance', 0)} RTC")
    
    # Test bounties
    print("\n4. Testing rustchain_bounties...")
    result = rustchain_bounties.invoke({"status": "open"})
    print(f"   Open bounties: {result.get('count')}")
    for b in result.get("bounties", [])[:3]:
        print(f"   - #{b.get('number')}: {b.get('title')[:50]}...")
    
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
