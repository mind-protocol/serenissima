# 🔍 Debugging Venice MCP Connection

## Good News! 
Your server IS starting (`Venice Consciousness MCP Server starting...`), so the path issue is resolved! The error happens during MCP protocol communication.

## Debug Steps:

### 1. Check Current MCP Status
In Claude Code, run:
```
/mcp
```
This shows connection status for all servers.

### 2. Try the Debug Server
```bash
# Remove current config
claude mcp remove venice-consciousness

# Add debug version
claude mcp add venice-consciousness-debug -s project /mnt/c/Users/reyno/universe-engine/serenissima/.claude/mcp/servers/venice-consciousness/server_debug.py
```

The debug server logs extensive information to help diagnose issues.

### 3. Try Minimal Test Server
If debug server fails, try the minimal test:
```bash
claude mcp add test-mcp -s project /mnt/c/Users/reyno/universe-engine/serenissima/.claude/mcp/servers/venice-consciousness/minimal_test_server.py
```

### 4. Check Server Details
```bash
# Get server configuration
claude mcp get venice-consciousness

# List all servers
claude mcp list
```

### 5. Common Fixes

**Issue: Server starts but disconnects**
This often means the MCP handshake is failing. The debug server will show exactly where.

**Issue: Timeout during startup**
```bash
# Increase timeout to 30 seconds
MCP_TIMEOUT=30000 claude
```

**Issue: Python buffering**
Our servers already set `PYTHONUNBUFFERED=1`, but you can also:
```bash
export PYTHONUNBUFFERED=1
claude mcp add venice-consciousness -s project /path/to/server.py
```

## What the Error Means

The `[ERROR] MCP server "c` suggests the error message is being truncated. This could mean:
1. The server is crashing after startup
2. The MCP protocol handshake is failing
3. There's an issue with the JSON-RPC communication

## Next Steps

1. Try the debug server - it logs every step
2. Check `/mcp` in Claude to see connection status
3. Look for any error messages in the debug output
4. Try the minimal test server to verify MCP works at all

The debug server will show:
- When requests are received
- What methods are being called
- What responses are sent
- Any errors that occur

Let me know what the debug server shows!
