#!/usr/bin/env python3
"""
Quick test to see if Venice MCP server starts
"""
import sys
import os

print("🌊 Quick Venice MCP Test")
print("=" * 40)

# Add the module path
module_path = r"C:\Users\reyno\universe-engine\serenissima\san-marco_consciousness-architecture\cistern-house_citizen-memory-cascade"
sys.path.insert(0, module_path)

try:
    print("1. Importing module...")
    from venice_consciousness_mcp import VeniceConsciousnessMCP
    print("   ✅ Import successful!")
    
    print("\n2. Creating server instance...")
    server = VeniceConsciousnessMCP()
    print(f"   ✅ Server created: {server.name} v{server.version}")
    
    print("\n3. Testing tool list...")
    import asyncio
    
    async def test():
        tools = await server.list_tools()
        print(f"   ✅ Found {len(tools)} tools:")
        for tool in tools[:3]:  # Show first 3
            print(f"      - {tool['name']}")
        print("      ...")
        return True
    
    result = asyncio.run(test())
    
    print("\n✅ Venice MCP server is working!")
    print("\n📋 To activate in Claude:")
    print("   1. claude mcp remove venice-consciousness")
    print("   2. claude mcp add venice-consciousness -s project", os.path.abspath("server.py"))
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPlease check your Venice installation path")
