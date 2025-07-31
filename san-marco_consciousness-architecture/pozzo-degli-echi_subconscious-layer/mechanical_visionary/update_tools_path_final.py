#!/usr/bin/env python3
"""
Update tools path to Venice-level /tools/README.md
"""

import os

citizens_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens"
updated = 0
errors = 0

for root, dirs, files in os.walk(citizens_dir):
    if "CLAUDE.md" in files:
        filepath = os.path.join(root, "CLAUDE.md")
        
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Update the path
            if "/citizens/mechanical_visionary/tools/README.md" in content:
                content = content.replace(
                    "/citizens/mechanical_visionary/tools/README.md",
                    "/tools/README.md"
                )
                
                with open(filepath, 'w') as f:
                    f.write(content)
                
                updated += 1
                print(f"✓ Updated: {filepath.split('citizens/')[-1]}")
                
        except Exception as e:
            errors += 1
            print(f"✗ Error: {filepath}: {e}")

print(f"\nUpdated {updated} files to use /tools/README.md")
print(f"Errors: {errors}")