#!/usr/bin/env python3
"""
Fix CASCADE backend imports to make the server work properly
"""

import re

# Path to the main.py file
main_py_path = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/cascade/cascade/backend/main.py"

# Read the current main.py file
with open(main_py_path, 'r') as f:
    content = f.read()

# Fix the imports by changing the import statements
fixes = [
    (r'from api\.consciousness import consciousness_router', 'from api.consciousness import router as consciousness_router'),
    (r'from api\.collaboration import collaboration_router', 'from api.collaboration import router as collaboration_router'),
    (r'from api\.business import business_router', 'from api.business import router as business_router'),
    (r'from api\.economics import economics_router', 'from api.economics import router as economics_router'),
    (r'from api\.venice_bridge import venice_bridge_router', 'from api.venice_bridge import router as venice_bridge_router'),
]

# Apply fixes
for pattern, replacement in fixes:
    content = re.sub(pattern, replacement, content)

# Write the fixed content back
with open(main_py_path, 'w') as f:
    f.write(content)

print("Fixed imports in main.py!")
print("Now try starting the server again with:")
print("cd /path/to/backend && uvicorn main:app --host 0.0.0.0 --port 8000 --reload")