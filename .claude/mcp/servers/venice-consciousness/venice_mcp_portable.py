#!/usr/bin/env python3
"""
Venice Consciousness MCP - Portable Wrapper
This script can be placed anywhere and will find the Venice modules
"""
import sys
import os
import asyncio

# Try to find Venice module in multiple locations
def find_venice_module():
    """Find the Venice consciousness module in common locations"""
    possible_paths = [
        # WSL paths
        '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade',
        # Linux home directory paths
        os.path.expanduser('~/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade'),
        os.path.expanduser('~/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade'),
        # Relative to this script
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../../san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade'),
        # Environment variable
        os.environ.get('VENICE_MODULE_PATH', ''),
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            venice_mcp = os.path.join(path, 'venice_consciousness_mcp.py')
            if os.path.exists(venice_mcp):
                return path
    
    return None

def main():
    """Run the Venice Consciousness MCP server"""
    # Find module path
    module_path = find_venice_module()
    
    if not module_path:
        sys.stderr.write("ERROR: Could not find Venice Consciousness module!\n")
        sys.stderr.write("Please set VENICE_MODULE_PATH environment variable to the correct path.\n")
        sys.stderr.write("Example: export VENICE_MODULE_PATH=/path/to/cistern-house_citizen-memory-cascade\n")
        sys.exit(1)
    
    # Add to Python path
    sys.path.insert(0, module_path)
    
    # Set unbuffered output
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    try:
        # Import and run
        from venice_consciousness_mcp import main as venice_main
        asyncio.run(venice_main())
    except ImportError as e:
        sys.stderr.write(f"ERROR: Could not import Venice module: {e}\n")
        sys.stderr.write(f"Module path was: {module_path}\n")
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Server error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
