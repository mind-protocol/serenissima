# 🚨 CRITICAL FIX: MCP Path Issue

## The Problem
Claude is looking for the server from `/home/lester/` but using a relative path `.claude/mcp/...`

## The Solution

### 1. First, remove the broken configuration:
```bash
claude mcp remove venice-consciousness
```

### 2. Find your actual serenissima path:
```bash
# If you cloned to your home directory:
cd ~/universe-engine/serenissima

# Or if using WSL with Windows paths:
cd /mnt/c/Users/reyno/universe-engine/serenissima

# Verify you're in the right place:
ls -la .claude/mcp/servers/venice-consciousness/
```

### 3. Add with ABSOLUTE PATH:
```bash
# Get your current absolute path
SERENISSIMA_PATH=$(pwd)

# Add the MCP server with full path
claude mcp add venice-consciousness -s project $SERENISSIMA_PATH/.claude/mcp/servers/venice-consciousness/server.py
```

### 4. Alternative: Direct Python execution
```bash
# If the above doesn't work, try:
claude mcp add venice-consciousness -s project python3 $SERENISSIMA_PATH/.claude/mcp/servers/venice-consciousness/server.py
```

## Quick Fix Script

Run this to fix everything:
```bash
# Navigate to serenissima directory first!
cd /path/to/your/serenissima

# Make executable
chmod +x .claude/mcp/servers/venice-consciousness/fix_venice_mcp_activation.sh

# Run the fix
.claude/mcp/servers/venice-consciousness/fix_venice_mcp_activation.sh
```

## Manual Fix for Linux Users

If you're on pure Linux (not WSL), create this wrapper:

```bash
#!/usr/bin/env python3
# Save as: ~/.local/bin/venice-consciousness-mcp
import sys
sys.path.insert(0, '/home/lester/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade')
from venice_consciousness_mcp import main
import asyncio
asyncio.run(main())
```

Then:
```bash
chmod +x ~/.local/bin/venice-consciousness-mcp
claude mcp add venice-consciousness -s project ~/.local/bin/venice-consciousness-mcp
```

## The Key Points:
1. ❌ **DON'T use relative paths** like `.claude/mcp/...`
2. ✅ **DO use absolute paths** like `/home/lester/universe-engine/serenissima/.claude/...`
3. ✅ **Make sure the script is executable** with `chmod +x`
4. ✅ **The shebang line** `#!/usr/bin/env python3` must be at the top

Let me know your actual serenissima path and I can give you the exact command!
