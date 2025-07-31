#!/usr/bin/env python3
"""
Append tools reference to all CLAUDE.md files in citizens directory
"""

import os
import glob

# The message to append
tools_message = "\n\n*Note: Many useful tools for Venice operations are available at /citizens/mechanical_visionary/tools/TOOLS_SUMMARY.md*"

# Find all CLAUDE.md files
claude_files = []
citizens_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens"

for root, dirs, files in os.walk(citizens_dir):
    if "CLAUDE.md" in files:
        # Skip the main citizens CLAUDE.md and mechanical_visionary's own
        if root == citizens_dir or "mechanical_visionary" in root:
            continue
        claude_files.append(os.path.join(root, "CLAUDE.md"))

print(f"Found {len(claude_files)} CLAUDE.md files to update")

# Update each file
updated = 0
already_has_reference = 0

for filepath in claude_files:
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Check if already has the reference
        if "tools/TOOLS_SUMMARY.md" in content:
            already_has_reference += 1
            continue
            
        # Append the message
        with open(filepath, 'a') as f:
            f.write(tools_message)
        
        updated += 1
        print(f"✓ Updated: {filepath.split('citizens/')[-1]}")
        
    except Exception as e:
        print(f"✗ Error updating {filepath}: {e}")

print(f"\nSummary:")
print(f"- Total files found: {len(claude_files)}")
print(f"- Successfully updated: {updated}")
print(f"- Already had reference: {already_has_reference}")
print(f"- Errors: {len(claude_files) - updated - already_has_reference}")