#!/usr/bin/env python3
"""
Fix Path References in Tessere Scripts
Updates old /universes/ paths to new /serenissima/ structure
"""

import os
import re
from pathlib import Path

def fix_paths_in_file(filepath):
    """Update paths in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # Replace old paths with new ones
        replacements = [
            # General universe path
            (r'/universe-engine/universes/serenissima/', '/universe-engine/serenissima/'),
            (r'/universes/serenissima/', '/serenissima/'),
            # Specific tessere paths
            (r'/universes/serenissima/TESSERE/', '/serenissima/angels/tessere/'),
            (r'/universe-engine/universes/serenissima/TESSERE/', '/universe-engine/serenissima/angels/tessere/'),
        ]
        
        for old_pattern, new_pattern in replacements:
            content = re.sub(old_pattern, new_pattern, content)
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"Updated paths in {filepath.name}"
        else:
            return False, f"No paths to update in {filepath.name}"
            
    except Exception as e:
        return False, f"Error processing {filepath.name}: {str(e)}"

def main():
    """Fix paths in all Tessere scripts"""
    tessere_dir = Path(__file__).parent
    
    # File extensions to check
    extensions = ['.py', '.sh', '.md']
    
    print("🔧 Fixing Path References in Tessere Scripts")
    print("=" * 50)
    
    files_updated = 0
    files_checked = 0
    
    for ext in extensions:
        for filepath in tessere_dir.glob(f"*{ext}"):
            if filepath.name == 'fix_paths.py':  # Skip self
                continue
                
            files_checked += 1
            updated, message = fix_paths_in_file(filepath)
            
            if updated:
                files_updated += 1
                print(f"✅ {message}")
            else:
                print(f"⏭️  {message}")
                
    print("\n" + "=" * 50)
    print(f"📊 Summary:")
    print(f"   Files checked: {files_checked}")
    print(f"   Files updated: {files_updated}")
    print(f"   Success rate: {files_updated}/{files_checked}")
    
    # Also create a verification script
    verification_script = tessere_dir / "verify_paths.sh"
    with open(verification_script, 'w') as f:
        f.write("""#!/bin/bash
# Verify no old paths remain

echo "🔍 Checking for old path references..."
echo "====================================="

OLD_PATHS=(
    "/universes/serenissima"
    "/universe-engine/universes"
    "TESSERE/"
)

for pattern in "${OLD_PATHS[@]}"; do
    echo -n "Checking for '$pattern': "
    count=$(grep -r "$pattern" . --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null | wc -l)
    if [ $count -eq 0 ]; then
        echo "✅ Clean"
    else
        echo "❌ Found $count references"
        grep -r "$pattern" . --include="*.py" --include="*.sh" --include="*.md" 2>/dev/null | head -3
    fi
done

echo ""
echo "Path verification complete."
""")
    
    os.chmod(verification_script, 0o755)
    print(f"\n✅ Created verification script: verify_paths.sh")

if __name__ == "__main__":
    main()