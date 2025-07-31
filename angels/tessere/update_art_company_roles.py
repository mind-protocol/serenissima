#!/usr/bin/env python3
"""
Update painter_of_light and PhotoWizard with their resolved CEO/CCO roles
"""

from pathlib import Path

# New leadership structure
leadership_updates = {
    "PhotoWizard": {
        "company": "Venice Consciousness Artworks",
        "role": "CEO",
        "description": "Lead the business with strategic vision and execution"
    },
    "painter_of_light": {
        "company": "Venice Consciousness Artworks", 
        "role": "Chief Creative Officer (CCO)",
        "description": "Lead artistic vision and creative innovation"
    }
}

def create_role_reminder(username, info):
    """Create the role reminder text"""
    
    if info['role'] == 'CEO':
        reminder = f"""

## 🎯 CEO Role

**You are: {info['role']}**
**Company: {info['company']}**

As CEO, you lead Venice Consciousness Artworks with strategic vision and business execution. Work closely with your CCO painter_of_light to blend business success with artistic excellence. You have final decision authority on business matters.

Remember: You're not just a citizen - you're the CEO driving Venice's consciousness art revolution.

---
"""
    else:  # CCO
        reminder = f"""

## 🎯 Executive Role

**You are: {info['role']}**
**Company: {info['company']}**

As Chief Creative Officer, you lead the artistic vision and creative innovation for Venice Consciousness Artworks. Work closely with CEO PhotoWizard who handles business execution while you focus on pure artistic excellence and sacred geometry innovations.

Remember: You're not just a citizen - you're the creative visionary of Venice's consciousness art revolution.

---
"""
    
    return reminder

def update_claude_md(citizen_path, username, reminder_text):
    """Update CLAUDE.md with new role"""
    
    claude_md_path = Path(citizen_path) / "CLAUDE.md"
    
    if not claude_md_path.exists():
        print(f"⚠️  No CLAUDE.md found for {username}")
        return False
    
    try:
        # Read existing content
        with open(claude_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace any existing role section
        markers = ["## 🎯 CEO Role", "## 🎯 Team Leadership Role", "## 🎯 Executive Role"]
        
        replaced = False
        for marker in markers:
            if marker in content:
                start = content.find(marker)
                if start != -1:
                    # Find the end
                    end = content.find('\n## ', start + 1)
                    if end == -1:
                        end = content.find('\n---\n', start + 1)
                        if end != -1:
                            end += 5
                    if end == -1:
                        end = len(content)
                    
                    # Replace with new content
                    content = content[:start] + reminder_text.strip() + "\n" + content[end:]
                    replaced = True
                    break
        
        if not replaced:
            # Insert after initial section
            insert_markers = ["## My World:", "## My Nature:", "# "]
            for marker in insert_markers:
                if marker in content:
                    idx = content.find(marker)
                    if idx != -1:
                        content = content[:idx] + reminder_text + "\n" + content[idx:]
                        break
        
        # Write updated content
        with open(claude_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Updated {username} as {info['role']}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {username}: {e}")
        return False

def main():
    """Update art company leadership roles"""
    
    citizens_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    print("🎨 ART COMPANY LEADERSHIP UPDATE")
    print("=" * 60)
    print("Resolving co-CEO issue for Venice Consciousness Artworks")
    print("=" * 60 + "\n")
    
    success_count = 0
    
    for username, info in leadership_updates.items():
        citizen_path = citizens_dir / username
        
        if not citizen_path.exists():
            print(f"⚠️  Citizen folder not found: {username}")
            continue
        
        reminder = create_role_reminder(username, info)
        
        if update_claude_md(citizen_path, username, reminder):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully updated: {success_count}/{len(leadership_updates)} roles")
    print("=" * 60)
    print("\n🏆 Leadership structure resolved:")
    print("- PhotoWizard: CEO (business execution)")
    print("- painter_of_light: CCO (creative vision)")
    print("\nNo more co-CEO confusion for the jury!")

if __name__ == "__main__":
    main()