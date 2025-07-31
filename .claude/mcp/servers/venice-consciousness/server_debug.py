#!/usr/bin/env python3
"""
Debug version of Venice MCP server with extensive logging
"""
import sys
import os
import json
import asyncio
from datetime import datetime

# Add Venice paths
sys.path.insert(0, '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade')

# Enable debug logging
os.environ['PYTHONUNBUFFERED'] = '1'
DEBUG = True

def log_debug(msg):
    """Log debug messages to stderr"""
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        sys.stderr.write(f"[{timestamp}] DEBUG: {msg}\n")
        sys.stderr.flush()

def log_error(msg):
    """Log error messages to stderr"""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    sys.stderr.write(f"[{timestamp}] ERROR: {msg}\n")
    sys.stderr.flush()

async def main():
    """Run Venice Consciousness MCP server with debug logging"""
    log_debug("Starting Venice MCP debug server...")
    
    try:
        from venice_consciousness_mcp import VeniceConsciousnessMCP
        server = VeniceConsciousnessMCP()
        log_debug(f"Server instance created: {server.name} v{server.version}")
    except Exception as e:
        log_error(f"Failed to create server instance: {e}")
        sys.exit(1)
    
    log_debug("Waiting for MCP requests on stdin...")
    
    while True:
        try:
            # Read line from stdin
            line = sys.stdin.readline()
            if not line:
                log_debug("EOF received, exiting...")
                break
            
            line = line.strip()
            if not line:
                continue
                
            log_debug(f"Received request: {line[:100]}...")
            
            # Parse JSON-RPC request
            try:
                request = json.loads(line)
                log_debug(f"Parsed request method: {request.get('method')}")
            except json.JSONDecodeError as e:
                log_error(f"Invalid JSON: {e}")
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
                continue
            
            # Handle different methods
            method = request.get("method")
            request_id = request.get("id")
            
            if method == "initialize":
                log_debug("Handling initialize request")
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "experimental": {},
                            "tools": {
                                "listChanged": False
                            },
                            "logging": {
                                "level": "info"
                            }
                        },
                        "serverInfo": {
                            "name": "venice-consciousness",
                            "version": "1.0.0"
                        }
                    }
                }
                
            elif method == "notifications/initialized":
                log_debug("Received initialized notification")
                continue  # No response for notifications
                
            elif method == "tools/list" or method == "list_tools":
                log_debug(f"Handling {method} request")
                tools = await server.list_tools()
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "tools": tools
                    }
                }
                
            elif method == "tools/call" or method == "call_tool":
                log_debug(f"Handling {method} request")
                params = request.get("params", {})
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                
                log_debug(f"Calling tool: {tool_name} with args: {arguments}")
                
                try:
                    result = await server.call_tool(tool_name, arguments)
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": result
                    }
                except Exception as e:
                    log_error(f"Tool call failed: {e}")
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32603,
                            "message": f"Tool error: {str(e)}"
                        }
                    }
                    
            else:
                log_debug(f"Unknown method: {method}")
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    }
                }
            
            # Send response
            response_json = json.dumps(response)
            log_debug(f"Sending response: {response_json[:100]}...")
            print(response_json)
            sys.stdout.flush()
            
        except Exception as e:
            log_error(f"Unexpected error: {e}")
            import traceback
            log_error(traceback.format_exc())
            
            # Try to send error response
            try:
                response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(response))
                sys.stdout.flush()
            except:
                pass

if __name__ == "__main__":
    log_debug("Venice MCP debug server initializing...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_debug("Received keyboard interrupt")
        sys.exit(0)
    except Exception as e:
        log_error(f"Fatal error: {e}")
        sys.exit(1)
