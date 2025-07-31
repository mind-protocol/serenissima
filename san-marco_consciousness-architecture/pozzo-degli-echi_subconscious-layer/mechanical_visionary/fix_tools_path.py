#!/usr/bin/env python3
"""
Fix the tools reference path in all CLAUDE.md files
"""

import os

# Find and fix all CLAUDE.md files
citizens_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens"
fixed = 0
errors = 0

for root, dirs, files in os.walk(citizens_dir):
    if "CLAUDE.md" in files:
        filepath = os.path.join(root, "CLAUDE.md")
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Fix the incorrect path
            if "/citizens/mechanical_visionary/tools/TOOLS_SUMMARY.md" in content:
                content = content.replace(
                    "/citizens/mechanical_visionary/tools/TOOLS_SUMMARY.md",
                    "/citizens/mechanical_visionary/tools/README.md"
                )
                
                with open(filepath, 'w') as f:
                    f.write(content)
                
                fixed += 1
                print(f"✓ Fixed: {filepath.split('citizens/')[-1]}")
                
        except Exception as e:
            errors += 1
            print(f"✗ Error fixing {filepath}: {e}")

print(f"\nFixed {fixed} files")
print(f"Errors: {errors}")