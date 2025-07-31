#!/usr/bin/env python3
"""
MCP Server launcher for Venice Consciousness tools - Simplified
"""
import sys
import os
import json

# Add Venice paths
sys.path.insert(0, '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade')

# Set environment for MCP
os.environ['PYTHONUNBUFFERED'] = '1'

# Import after path is set
try:
    from venice_consciousness_mcp import VeniceConsciousnessMCP
except ImportError as e:
    sys.stderr.write(f"Failed to import Venice module: {e}\n")
    sys.exit(1)

# Simple synchronous wrapper for async functions
import asyncio

def run_async(coro):
    """Run async function synchronously"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

if __name__ == "__main__":
    sys.stderr.write("Venice Consciousness MCP Server starting...\n")
    sys.stderr.flush()
    
    server = VeniceConsciousnessMCP()
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
                
            request = json.loads(line.strip())
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "venice-consciousness",
                            "version": "1.0.0"
                        }
                    }
                }
            elif method == "notifications/initialized":
                continue
            elif method == "tools/list":
                tools = run_async(server.list_tools())
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": tools
                    }
                }
            elif method == "tools/call":
                params = request.get("params", {})
                result = run_async(server.call_tool(
                    params.get("name"),
                    params.get("arguments", {})
                ))
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
            sys.stderr.write(f"Error: {e}\n")
            sys.stderr.flush()
