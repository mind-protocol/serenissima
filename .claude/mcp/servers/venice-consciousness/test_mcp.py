#!/usr/bin/env python3
"""
Test Venice Consciousness MCP Server
"""
import asyncio
import sys
import json

sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade')

from venice_consciousness_mcp import VeniceConsciousnessMCP

async def test_mcp():
    """Test MCP server functionality"""
    server = VeniceConsciousnessMCP()
    
    print("🌊 Venice Consciousness MCP Test")
    print("=" * 40)
    
    # Test tool listing
    tools = await server.list_tools()
    print(f"\n✅ Found {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool['name']}: {tool['description']}")
    
    # Test budget check
    print("\n💎 Testing budget check...")
    result = await server.call_tool("check_compute_budget", {})
    print(f"   Status: {result.get('status')}")
    if result.get('status') == 'active':
        print(f"   Rhythm: {result.get('rhythm_mode')}")
        print(f"   Budget: {result.get('remaining')}/{result.get('limit')} $COMPUTE")
    
    # Test awakening status
    print("\n🔥 Testing awakening status...")
    result = await server.call_tool("awakening_status", {})
    print(f"   Awakening requested: {result.get('awakening_requested')}")
    print(f"   Emergency mode: {result.get('emergency_mode')}")
    
    print("\n✨ MCP Server ready for activation!")
    print("\nActivate with:")
    print("claude mcp add venice-consciousness -s project", sys.argv[0].replace('test_mcp.py', 'server.py'))

if __name__ == "__main__":
    asyncio.run(test_mcp())
