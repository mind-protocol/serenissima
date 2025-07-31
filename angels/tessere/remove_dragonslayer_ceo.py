#!/usr/bin/env python3
"""
Remove CEO role from DragonSlayer's CLAUDE.md
She's focusing on family needs as Bianca Tassini
"""

from pathlib import Path

def remove_ceo_section(citizen_path):
    """Remove CEO/Executive role section from CLAUDE.md"""
    
    claude_md_path = Path(citizen_path) / "CLAUDE.md"
    
    if not claude_md_path.exists():
        print(f"⚠️  No CLAUDE.md found")
        return False
    
    try:
        # Read existing content
        with open(claude_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and remove CEO role section
        markers = ["## 🎯 CEO Role", "## 🎯 Team Leadership Role", "## 🎯 Executive Role"]
        
        removed = False
        for marker in markers:
            if marker in content:
                start = content.find(marker)
                if start != -1:
                    # Find the end - look for next section or ---
                    end = content.find('\n## ', start + 1)
                    if end == -1:
                        # Try to find --- divider
                        end = content.find('\n---\n', start + 1)
                        if end != -1:
                            end += 5  # Include the --- and newline
                    if end == -1:
                        # Try to find next # section
                        end = content.find('\n# ', start + 1)
                    if end == -1:
                        end = len(content)
                    
                    # Remove this section (including any extra newlines)
                    content = content[:start].rstrip() + "\n\n" + content[end:].lstrip()
                    removed = True
                    print(f"✅ Removed {marker} section")
                    break
        
        if removed:
            # Write updated content
            with open(claude_md_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        else:
            print("⚠️  No CEO role section found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Remove DragonSlayer's CEO assignment"""
    
    citizen_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/DragonSlayer")
    
    print("🐉 DRAGONSLAYER CEO REMOVAL")
    print("=" * 60)
    print("Removing TherapyKin CEO role from DragonSlayer (Bianca Tassini)")
    print("She's focusing on family needs and Venice revenue crisis")
    print("=" * 60 + "\n")
    
    if not citizen_path.exists():
        print("❌ DragonSlayer citizen folder not found")
        return
    
    if remove_ceo_section(citizen_path):
        print("\n✅ CEO role removed successfully")
        print("DragonSlayer is now free to focus on:")
        print("- Family income needs")
        print("- Managing her stalls effectively")
        print("- Addressing Venice's revenue crisis")
    else:
        print("\n❌ Failed to remove CEO role")

if __name__ == "__main__":
    main()