#!/usr/bin/env python3
"""Test the fixed venice_consciousness_mcp module"""
import sys
import os

# Add path
sys.path.insert(0, '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade')

try:
    print("Testing import...")
    from venice_consciousness_mcp import VeniceConsciousnessMCP
    print("✅ Import successful!")
    
    print("\nTesting server initialization...")
    server = VeniceConsciousnessMCP()
    print(f"✅ Server created: {server.name} v{server.version}")
    
    print("\nTesting tool list...")
    import asyncio
    tools = asyncio.run(server.list_tools())
    print(f"✅ Found {len(tools)} tools")
    for tool in tools:
        print(f"   - {tool['name']}")
    
    print("\n✅ All tests passed! Server is ready to use.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
