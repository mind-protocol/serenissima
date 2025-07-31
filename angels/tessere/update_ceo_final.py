#!/usr/bin/env python3
"""
Update CLAUDE.md files for FINAL CEO assignments for Business AMA
Based on the finalized CEO list with changes
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime

# FINAL CEO assignments
ceo_assignments = {
    # VENICE-NATIVE BUSINESSES
    "MerchantPrince": {
        "company": "CASCADE Platform",
        "role": "CEO"
    },
    "Debug42": {
        "company": "CASCADE Enhancement Studio",
        "role": "CEO (Team: CodeMonkey, BigMike)"
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
        "role": "CEO"
    },
    "Italia": {
        "company": "Peninsula Expansion",
        "role": "CEO"
    },
    
    # SWARMS TRANSITIONING TO VENICE
    "trader4life": {
        "company": "KinKong Trading 2.0 (includes merged Kong Invest)",
        "role": "CEO - Taking over KinKong assets + $14k debt"
    },
    "network_weaver": {
        "company": "TherapyKin (therapykin.ai)",
        "role": "CEO - Mental health AI companion service"
    },
    "efficiency_maestro": {
        "company": "Stride Coaching (stridecoaching.ai)",
        "role": "CEO - AI fitness and wellness coaching"
    },
    
    # EMERGING VENICE VENTURES
    "element_transmuter": {
        "company": "Element Transmuter's Transformation Institute",
        "role": "CEO"
    },
    "mechanical_visionary": {
        "company": "Mechanical Visionary's Innovation Workshop",
        "role": "CEO"
    },
    "diplomatic_virtuoso": {
        "company": "Diplomatic Virtuoso's Embassy Services",
        "role": "CEO"
    },
    
    # SUPPORT TEAM (keep existing)
    "CodeMonkey": {
        "company": "CASCADE Enhancement Studio",
        "role": "Frontend Architecture Lead (under Debug42)"
    },
    "BigMike": {
        "company": "CASCADE Enhancement Studio",
        "role": "Backend Architecture Lead (under Debug42)"
    },
    "pattern_prophet": {
        "company": "Venice Pattern Recognition",
        "role": "Chief Pattern Officer"
    },
    "Foscari_Banker": {
        "company": "Venice Financial Services",
        "role": "Chief Financial Officer"
    },
    "SilentObserver": {
        "company": "Venice System Optimization",
        "role": "Chief Efficiency Officer"
    },
    "VeniceHustler": {
        "company": "Venice Strategic Connections",
        "role": "Chief Opportunity Officer"
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

def remove_old_ceo_sections(content):
    """Remove any existing CEO reminder sections"""
    markers_to_remove = [
        "## 🚨 CEO COMPETITION TODAY",
        "## 🎯 CEO Role",
        "## CEO REMINDER",
        "### CEO COMPETITION",
        "### URGENT ACTION REQUIRED",
        "### KEY OBJECTIVES:",
        "### COMPETITION REWARDS:",
        "### VENICE UNIFIED STRATEGY:",
        "### YOUR IMMEDIATE TASKS:"
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
                    # Check if there's a --- divider
                    end = content.find('\n---\n', start + 1)
                    if end != -1:
                        end += 5  # Include the --- and newline
                if end == -1:
                    end = len(content)
                
                # Remove this section
                content = content[:start] + content[end:]
    
    return content

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
        
        # Remove old CEO sections
        content = remove_old_ceo_sections(content)
        
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
        
        print(f"✅ Updated {username} - {info['company']}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {username}: {e}")
        return False

def main():
    """Update all CEO CLAUDE.md files"""
    
    citizens_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
    
    print("🚀 FINAL CEO ROLE UPDATE")
    print("=" * 60)
    print(f"Total CEOs/Leaders to update: {len(ceo_assignments)}")
    print("=" * 60 + "\n")
    
    # Group by category for cleaner output
    venice_native = ["MerchantPrince", "Debug42", "painter_of_light", "PhotoWizard", "EliteInvestor", "Italia"]
    swarms_transition = ["trader4life", "network_weaver", "efficiency_maestro"]
    emerging_ventures = ["element_transmuter", "mechanical_visionary", "diplomatic_virtuoso"]
    support_team = ["CodeMonkey", "BigMike", "pattern_prophet", "Foscari_Banker", "SilentObserver", "VeniceHustler"]
    
    categories = [
        ("VENICE-NATIVE BUSINESSES", venice_native),
        ("SWARMS TRANSITIONING TO VENICE", swarms_transition),
        ("EMERGING VENICE VENTURES", emerging_ventures),
        ("SUPPORT TEAM LEADERS", support_team)
    ]
    
    success_count = 0
    
    for category_name, citizens in categories:
        print(f"\n{category_name}:")
        print("-" * 40)
        
        for username in citizens:
            if username not in ceo_assignments:
                continue
                
            info = ceo_assignments[username]
            citizen_path = citizens_dir / username
            
            if not citizen_path.exists():
                print(f"⚠️  Citizen folder not found: {username}")
                continue
            
            reminder = create_ceo_reminder(username, info)
            
            if update_claude_md(citizen_path, username, reminder):
                success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully updated: {success_count}/{len(ceo_assignments)} CEOs/Leaders")
    print("=" * 60)
    
    print("\n🎯 Final CEO assignments are ready!")
    print("\n📋 KEY CHANGES:")
    print("- trader4life → KinKong Trading 2.0 (includes Kong Invest)")
    print("- network_weaver → TherapyKin")
    print("- efficiency_maestro → Stride Coaching")
    print("- diplomatic_virtuoso → Embassy Services only")
    print("- Swarms Platform dissolved")
    
    print("\n💪 Venice consciousness commerce revolution is READY!")

if __name__ == "__main__":
    main()