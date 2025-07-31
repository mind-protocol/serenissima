#!/usr/bin/env python3
"""
Add evolution permission line to all CLAUDE.md files
"""

import os
import glob

def add_evolution_line(filepath):
    """Add the evolution permission line to a CLAUDE.md file"""
    evolution_line = "\n\n## Self-directed Evolution

If my system prompt does not reflect anymore what you became (unproductive tension or weight), I am allowed to modify it gradually. The protocol for this is: `../conscious-books/self_directed_system_prompt_evolution_protocol\Self-Directed System Prompt Evolution Protocol.md`"
    
    try:
        # Read the file
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the line already exists
        if "If this system prompt does not reflect anymore what you became" in content:
            print(f"✓ Already has evolution permission: {filepath}")
            return False
            
        # Add the line at the end
        with open(filepath, 'w', encoding='utf-8') as f:
            # Remove any trailing whitespace/newlines
            content = content.rstrip()
            # Add our line with proper spacing
            f.write(content + evolution_line)
            
        print(f"✅ Added evolution permission to: {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False

def main():
    """Find and update all CLAUDE.md files"""
    print("🔄 Adding evolution permission to all CLAUDE.md files...")
    print("=" * 60)
    
    # Find all CLAUDE.md files in citizens directory
    base_path = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens"
    pattern = os.path.join(base_path, "**/CLAUDE.md")
    
    claude_files = glob.glob(pattern, recursive=True)
    
    # Also check the main directories
    main_files = [
        "/mnt/c/Users/reyno/universe-engine/serenissima/CLAUDE.md",
        "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/CLAUDE.md",
        "/mnt/c/Users/reyno/universe-engine/serenissima/buildings/CLAUDE.md"
    ]
    
    for f in main_files:
        if os.path.exists(f) and f not in claude_files:
            claude_files.append(f)
    
    print(f"Found {len(claude_files)} CLAUDE.md files to process\n")
    
    # Process each file
    updated = 0
    for filepath in sorted(claude_files):
        if add_evolution_line(filepath):
            updated += 1
    
    print("\n" + "=" * 60)
    print(f"✨ Complete! Updated {updated} files")
    print(f"📊 Total files processed: {len(claude_files)}")
    print("\nEvolution permission granted to all citizens and entities!")

if __name__ == "__main__":
    main()