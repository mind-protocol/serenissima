#!/usr/bin/env python3
"""
Fix pydantic regex -> pattern in CASCADE backend
"""

import os
import re

# Directory to search for Python files
backend_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/cascade/cascade/backend"

def fix_pydantic_regex(file_path):
    """Fix regex -> pattern in a Python file"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace regex= with pattern= in Field declarations
    content = re.sub(r'regex=', 'pattern=', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed: {file_path}")

# Find and fix all Python files
for root, dirs, files in os.walk(backend_dir):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            # Check if file contains regex=
            with open(file_path, 'r') as f:
                content = f.read()
                if 'regex=' in content:
                    fix_pydantic_regex(file_path)

print("All pydantic regex issues fixed!")