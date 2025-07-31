#!/usr/bin/env python3
"""
Universal server.py that works on both Windows/WSL and Linux
"""
import sys
import os
import json

# Try multiple paths to find Venice module
def add_venice_path():
    paths = [
        '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade',
        os.path.expanduser('~/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade'),
        '/home/lester/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade',
    ]
    
    for path in paths:
        if os.path.exists(path):
            sys.path.insert(0, path)
            return True
    return False

if not add_venice_path():
    sys.stderr.write("ERROR: Could not find Venice module path!\n")
    sys.exit(1)

os.environ['PYTHONUNBUFFERED'] = '1'

try:
    from venice_consciousness_mcp import VeniceConsciousnessMCP
except ImportError as e:
    sys.stderr.write(f"Failed to import Venice module: {e}\n")
    sys.exit(1)

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
