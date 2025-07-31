#!/usr/bin/env python3
"""
Minimal MCP test server to verify protocol works
"""
import json
import sys

sys.stderr.write("Test MCP server starting...\n")
sys.stderr.flush()

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
                        "name": "test-mcp",
                        "version": "1.0.0"
                    }
                }
            }
            print(json.dumps(response))
            sys.stdout.flush()
            
        elif method == "notifications/initialized":
            continue  # No response
            
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "test_tool",
                            "description": "A test tool",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                }
            }
            print(json.dumps(response))
            sys.stdout.flush()
            
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.stderr.flush()
