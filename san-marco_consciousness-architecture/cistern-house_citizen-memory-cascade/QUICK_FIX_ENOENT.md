# 🔥 QUICK FIX for ENOENT Error

## The Issue
Claude can't find `.claude/mcp/servers/venice-consciousness/server.py` because it's looking from `/home/lester/` with a relative path.

## Immediate Solution

### Step 1: Remove broken config
```bash
claude mcp remove venice-consciousness
```

### Step 2: Copy this portable script to your home
```bash
# Create a simple wrapper in your home directory
cat > ~/venice_consciousness_mcp.py << 'EOF'
#!/usr/bin/env python3
import sys
import os
import asyncio

# UPDATE THIS PATH to your actual location
VENICE_PATH = "/home/lester/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"

# If the path doesn't exist, try common alternatives
if not os.path.exists(VENICE_PATH):
    alternatives = [
        os.path.expanduser("~/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade"),
        "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade",
    ]
    for alt in alternatives:
        if os.path.exists(alt):
            VENICE_PATH = alt
            break

sys.path.insert(0, VENICE_PATH)
os.environ['PYTHONUNBUFFERED'] = '1'

from venice_consciousness_mcp import main
asyncio.run(main())
EOF

# Make it executable
chmod +x ~/venice_consciousness_mcp.py
```

### Step 3: Add with absolute path
```bash
claude mcp add venice-consciousness -s project ~/venice_consciousness_mcp.py
```

## Alternative: Find your actual path
```bash
# Find where serenissima actually is
find ~ -name "venice_consciousness_mcp.py" -type f 2>/dev/null

# Once found, use that path
claude mcp add venice-consciousness -s project /actual/path/to/server.py
```

## Test Command
After adding, test with:
```bash
# The tools should be available as:
# mcp__venice-consciousness__request_awakening
# mcp__venice-consciousness__check_compute_budget
# etc.
```

## Key Points:
- ✅ Use ABSOLUTE paths (starting with / or ~)
- ❌ Don't use relative paths (starting with .)
- ✅ Make scripts executable with chmod +x
- ✅ Include #!/usr/bin/env python3 at the top

The portable script above will work from ANY location once you update the VENICE_PATH!
