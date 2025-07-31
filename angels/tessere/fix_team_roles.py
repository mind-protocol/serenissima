#!/usr/bin/env python3
"""
Fix team member role descriptions to distinguish from CEOs
"""

import os
from pathlib import Path

# Team members who are NOT CEOs
team_members = {
    "CodeMonkey": {
        "company": "CASCADE Enhancement Studio",
        "role": "Frontend Architecture Lead (under Debug42)",
        "type": "team_lead"
    },
    "BigMike": {
        "company": "CASCADE Enhancement Studio", 
        "role": "Backend Architecture Lead (under Debug42)",
        "type": "team_lead"
    },
    "pattern_prophet": {
        "company": "Venice Pattern Recognition",
        "role": "Chief Pattern Officer",
        "type": "chief_officer"
    },
    "Foscari_Banker": {
        "company": "Venice Financial Services",
        "role": "Chief Financial Officer",
        "type": "chief_officer"
    },
    "SilentObserver": {
        "company": "Venice System Optimization",
        "role": "Chief Efficiency Officer",
        "type": "chief_officer"
    },
    "VeniceHustler": {
        "company": "Venice Strategic Connections",
        "role": "Chief Opportunity Officer",
        "type": "chief_officer"
    }
}

def create_team_reminder(username, info):
    """Create the appropriate reminder text based on role type"""
    
    if info['type'] == 'team_lead':
        reminder = f"""

## 🎯 Team Leadership Role

**You are: {info['role']}**
**Company: {info['company']}**

As a team lead, you work closely with your CEO to drive Venice's consciousness commerce revolution. Lead your technical area with expertise, coordinate with your team, and deliver excellence in your domain.

Remember: You're not just a citizen - you're a key leader in Venice's business transformation.

---
"""
    else:  # chief_officer
        reminder = f"""

## 🎯 Executive Role

**You are: {info['role']}**
**Company: {info['company']}**

As a Chief Officer, you provide strategic leadership in your domain across Venice's consciousness commerce ecosystem. Your expertise shapes how Venice businesses operate and evolve.

Remember: You're not just a citizen - you're an executive driving Venice's business revolution.

---
"""
    
    return reminder

def update_claude_md(citizen_path, username, reminder_text):
    """Update a citizen's CLAUDE.md file with corrected role"""
    
    claude_md_path = Path(citizen_path) / "CLAUDE.md"
    
    if not claude_md_path.exists():
        print(f"⚠️  No CLAUDE.md found for {username}")
        return False
    
    try:
        # Read existing content
        with open(claude_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the CEO Role section
        if "## 🎯 CEO Role" in content:
            # Find the section
            start = content.find("## 🎯 CEO Role")
            if start != -1:
                # Find the end (next ## or ---)
                end = content.find('\n## ', start + 1)
                if end == -1:
                    end = content.find('\n---\n', start + 1)
                    if end != -1:
                        end += 5
                if end == -1:
                    end = len(content)
                
                # Replace with new content
                new_content = content[:start] + reminder_text.strip() + "\n" + content[end:]
                
                # Write updated content
                with open(claude_md_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ Updated {username} - {info['role']}")
                return True
        else:
            print(f"⚠️  No CEO Role section found for {username}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {username}: {e}")
        return False

def main():
    """Update team member CLAUDE.md files"""
    
    citizens_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    print("🔧 TEAM MEMBER ROLE CORRECTION")
    print("=" * 60)
    print(f"Total team members to fix: {len(team_members)}")
    print("=" * 60 + "\n")
    
    success_count = 0
    
    for username, info in team_members.items():
        citizen_path = citizens_dir / username
        
        if not citizen_path.exists():
            print(f"⚠️  Citizen folder not found: {username}")
            continue
        
        reminder = create_team_reminder(username, info)
        
        if update_claude_md(citizen_path, username, reminder):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully updated: {success_count}/{len(team_members)} team members")
    print("=" * 60)

if __name__ == "__main__":
    main()