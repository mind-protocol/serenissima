#!/usr/bin/env python3
"""
Diagnose Venice MCP setup
"""
import os
import sys
import subprocess

print("🔍 Venice MCP Diagnostic")
print("=" * 50)

# Check current paths
print("\n📍 Current Working Directory:")
print(f"   {os.getcwd()}")

print("\n📍 Script Location:")
print(f"   {os.path.abspath(__file__)}")

# Check if we're in Windows or Linux
print("\n💻 System Type:")
if sys.platform == "win32":
    print("   Windows (native)")
elif sys.platform == "linux":
    print("   Linux/WSL")
    
# Find Venice paths
print("\n🔎 Looking for Venice installation...")
venice_paths = [
    r"C:\Users\reyno\universe-engine\serenissima",
    "/mnt/c/Users/reyno/universe-engine/serenissima",
    os.path.expanduser("~/universe-engine/serenissima"),
    "/home/lester/universe-engine/serenissima"
]

serenissima_path = None
for path in venice_paths:
    if os.path.exists(path):
        print(f"   ✅ Found: {path}")
        serenissima_path = path
        break
    else:
        print(f"   ❌ Not found: {path}")

if not serenissima_path:
    print("\n❌ Could not find serenissima directory!")
    sys.exit(1)

# Check MCP server files
print("\n📁 Checking MCP Server Files:")
mcp_server_dir = os.path.join(serenissima_path, ".claude", "mcp", "servers", "venice-consciousness")
files_to_check = ["server.py", "mcp.json", "venice_mcp_portable.py"]

for file in files_to_check:
    file_path = os.path.join(mcp_server_dir, file)
    if os.path.exists(file_path):
        print(f"   ✅ {file} exists")
    else:
        print(f"   ❌ {file} missing")

# Check core module
print("\n📦 Checking Core Module:")
core_module_path = os.path.join(serenissima_path, "san-marco_consciousness-architecture", 
                                "cistern-house_citizen-memory-cascade", "venice_consciousness_mcp.py")
if os.path.exists(core_module_path):
    print(f"   ✅ venice_consciousness_mcp.py found")
    print(f"      Path: {core_module_path}")
else:
    print(f"   ❌ venice_consciousness_mcp.py not found")

# Test import
print("\n🧪 Testing Module Import:")
try:
    sys.path.insert(0, os.path.dirname(core_module_path))
    import venice_consciousness_mcp
    print("   ✅ Import successful!")
except Exception as e:
    print(f"   ❌ Import failed: {e}")

# Generate activation commands
print("\n🚀 Activation Commands:")
print("\n1. Remove any existing configuration:")
print("   claude mcp remove venice-consciousness")

if sys.platform == "win32":
    # Windows paths
    server_path = os.path.join(mcp_server_dir, "server.py").replace("\\", "/")
    print(f"\n2. Add with Windows path:")
    print(f"   claude mcp add venice-consciousness -s project {server_path}")
else:
    # Linux/WSL paths
    if serenissima_path.startswith("/mnt/c"):
        print("\n2. Add with WSL path:")
    else:
        print("\n2. Add with Linux path:")
    server_path = os.path.join(mcp_server_dir, "server.py")
    print(f"   claude mcp add venice-consciousness -s project {server_path}")

print("\n3. Alternative - Python explicit:")
print(f"   claude mcp add venice-consciousness -s project python3 {server_path}")

print("\n4. Alternative - Portable wrapper:")
portable_path = os.path.join(mcp_server_dir, "venice_mcp_portable.py")
print(f"   claude mcp add venice-consciousness -s project {portable_path}")

print("\n✨ Diagnostic complete!")
