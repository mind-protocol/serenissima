#!/usr/bin/env python3
"""
Test MCP handshake for Venice Consciousness server
"""
import json
import subprocess
import sys

def test_handshake():
    """Test the MCP initialization handshake"""
    print("🌊 Testing Venice Consciousness MCP Handshake...")
    
    # Start the server
    server_path = sys.argv[1] if len(sys.argv) > 1 else "./server.py"
    proc = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Send initialization request
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "id": 1,
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "logging": {}
                },
                "clientInfo": {
                    "name": "test"
                }
            }
        }
        
        print("\n📤 Sending initialization request:")
        print(json.dumps(init_request, indent=2))
        
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()
        
        # Read response
        response_line = proc.stdout.readline()
        response = json.loads(response_line)
        
        print("\n📥 Received response:")
        print(json.dumps(response, indent=2))
        
        # Verify response
        if response.get("result", {}).get("serverInfo", {}).get("name") == "venice-consciousness":
            print("\n✅ Handshake successful!")
            
            # Send list_tools request
            list_request = {
                "jsonrpc": "2.0",
                "method": "list_tools",
                "id": 2
            }
            
            print("\n📤 Sending list_tools request...")
            proc.stdin.write(json.dumps(list_request) + "\n")
            proc.stdin.flush()
            
            tools_response = proc.stdout.readline()
            tools = json.loads(tools_response)
            
            print("\n📥 Available tools:")
            if "result" in tools and "tools" in tools["result"]:
                for tool in tools["result"]["tools"]:
                    print(f"   - {tool['name']}: {tool['description']}")
            else:
                print("   (No tools found in expected format)")
                
        else:
            print("\n❌ Handshake failed - unexpected response")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        proc.terminate()
        
    print("\n🌊 MCP server test complete!")

if __name__ == "__main__":
    test_handshake()
