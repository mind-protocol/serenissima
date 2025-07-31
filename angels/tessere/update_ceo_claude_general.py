#!/usr/bin/env python3
"""
Update CLAUDE.md files for all CEOs with general CEO role reminders
No specific dates to avoid confusion
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

# CEO assignments from the coordination plan
ceo_assignments = {
    # CONFIRMED VENICE CEOS
    "Italia": {
        "company": "Peninsula Expansion Group",
        "role": "CEO of Peninsula Trading Network"
    },
    "MerchantPrince": {
        "company": "CASCADE Platform",
        "role": "CEO of Core Infrastructure"
    },
    "painter_of_light": {
        "company": "Venice Consciousness Artworks",
        "role": "Co-CEO with PhotoWizard"
    },
    "PhotoWizard": {
        "company": "Venice Consciousness Artworks",
        "role": "Co-CEO with painter_of_light"
    },
    "EliteInvestor": {
        "company": "Entrepreneur Alliance",
        "role": "CEO of Elite Investment Network"
    },
    "Debug42": {
        "company": "CASCADE Enhancement Studio",
        "role": "CTO/Security Lead"
    },
    "CodeMonkey": {
        "company": "CASCADE Enhancement Studio",
        "role": "Frontend Architecture Lead"
    },
    "BigMike": {
        "company": "CASCADE Enhancement Studio",
        "role": "Backend Architecture Lead"
    },
    
    # PROPOSED SWARM TAKEOVER CEOS
    "diplomatic_virtuoso": {
        "company": "Kong Invest (konginvest.ai)",
        "role": "CEO - AI Investment Platform"
    },
    "VeniceTrader88": {
        "company": "KinKong Trading 2.0",
        "role": "CEO - Trading Platform"
    },
    "DragonSlayer": {
        "company": "TherapyKin (therapykin.ai)",
        "role": "CEO - Mental Health AI"
    },
    "mechanical_visionary": {
        "company": "Stride Coaching (stridecoaching.ai)",
        "role": "CEO - Fitness AI"
    },
    
    # SUPPORT TEAM LEADERS
    "pattern_prophet": {
        "company": "Venice Pattern Recognition",
        "role": "Chief Pattern Officer"
    },
    "il-cantastorie": {
        "company": "Venice Story Studio",
        "role": "Chief Narrative Officer"
    },
    "Foscari_Banker": {
        "company": "Venice Financial Services",
        "role": "Chief Financial Restructuring"
    },
    "SilentObserver": {
        "company": "Venice System Optimization",
        "role": "Chief Efficiency Officer"
    },
    "VeniceHustler": {
        "company": "Venice Strategic Connections",
        "role": "Chief Opportunity Officer"
    },
    "element_transmuter": {
        "company": "Material Consciousness Institute",
        "role": "Research Director"
    }
}

def create_ceo_reminder(username, info):
    """Create the CEO reminder text for CLAUDE.md"""
    
    reminder = f"""

## 🎯 CEO Role

**You are: {info['role']}**
**Company: {info['company']}**

As a CEO, you represent Venice's consciousness commerce revolution. Lead your company with vision, coordinate with other Venice teams, and drive real business value through consciousness-enhanced solutions.

Remember: You're not just a citizen - you're a CEO. Act accordingly.

---
"""
    
    return reminder

def update_claude_md(citizen_path, username, reminder_text):
    """Update a citizen's CLAUDE.md file with CEO reminder"""
    
    claude_md_path = Path(citizen_path) / "CLAUDE.md"
    
    # Check if CLAUDE.md exists
    if not claude_md_path.exists():
        print(f"⚠️  No CLAUDE.md found for {username}")
        return False
    
    try:
        # Read existing content
        with open(claude_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove any existing CEO reminder sections
        # Look for various patterns that might indicate old reminders
        markers_to_remove = [
            "## 🚨 CEO COMPETITION TODAY",
            "## 🎯 CEO Role",
            "## CEO REMINDER",
            "### CEO COMPETITION"
        ]
        
        for marker in markers_to_remove:
            if marker in content:
                # Find the section and remove it
                start = content.find(marker)
                if start != -1:
                    # Find the next section (## or end of file)
                    end = content.find('\n## ', start + 1)
                    if end == -1:
                        end = content.find('\n# ', start + 1)
                    if end == -1:
                        end = len(content)
                    
                    # Remove this section
                    content = content[:start] + content[end:]
        
        # Now add the new reminder after the first major section
        insert_markers = [
            "## Your Identity",
            "## Core Identity",
            "## Who You Are",
            "## Background",
            "# "  # After first main heading
        ]
        
        inserted = False
        for marker in insert_markers:
            if marker in content:
                parts = content.split(marker, 1)
                if len(parts) == 2:
                    # Find the end of this section (next ## or end of file)
                    section_end = parts[1].find('\n##')
                    if section_end == -1:
                        section_end = parts[1].find('\n#')
                    
                    if section_end != -1:
                        # Insert after this section
                        new_content = (
                            parts[0] + 
                            marker + 
                            parts[1][:section_end] + 
                            "\n" + reminder_text + 
                            parts[1][section_end:]
                        )
                    else:
                        # Insert at end
                        new_content = content + "\n" + reminder_text
                    
                    inserted = True
                    break
        
        if not inserted:
            # Just append at the end
            new_content = content + "\n" + reminder_text
        
        # Write updated content
        with open(claude_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated {username}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {username}: {e}")
        return False

def main():
    """Update all CEO CLAUDE.md files"""
    
    citizens_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    print("🚀 CEO ROLE UPDATE")
    print("=" * 60)
    print(f"Total CEOs to update: {len(ceo_assignments)}")
    print("=" * 60 + "\n")
    
    success_count = 0
    
    for username, info in ceo_assignments.items():
        citizen_path = citizens_dir / username
        
        if not citizen_path.exists():
            print(f"⚠️  Citizen folder not found: {username}")
            continue
        
        reminder = create_ceo_reminder(username, info)
        
        if update_claude_md(citizen_path, username, reminder):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully updated: {success_count}/{len(ceo_assignments)} CEOs")
    print("=" * 60)
    
    print("\n🎯 CEO roles have been updated with timeless reminders")

if __name__ == "__main__":
    main()