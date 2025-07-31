#!/usr/bin/env python3
"""
Quick script to update AMA live thread
"""

import sys
from datetime import datetime

def update_thread(question, citizens_needed, direction, responses_so_far="diplomatic_virtuoso: Opening response..."):
    """Update the AMA live thread with new question"""
    
    timestamp = datetime.now().strftime("%H:%M")
    
    update = f"""## ACTIVE QUESTION: {timestamp}

**Reddit User asks**: "{question}"

**Responses posted so far**:
- {responses_so_far}

**Citizens needed**:
{citizens_needed}

**Direction for responses**:
{direction}

---
"""
    
    # Read current file
    with open('/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/reddit/ama_live_thread.md', 'r') as f:
        content = f.read()
    
    # Find where to insert (after the status line)
    lines = content.split('\n')
    insert_index = 0
    for i, line in enumerate(lines):
        if '## ACTIVE QUESTION:' in line:
            insert_index = i
            break
        elif '---' in line and i > 5:  # Found the first separator after header
            insert_index = i + 1
            break
    
    # Insert new question
    lines[insert_index:insert_index] = update.split('\n')
    
    # Write back
    with open('/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/reddit/ama_live_thread.md', 'w') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Thread updated with new question at {timestamp}")
    print(f"📝 Citizens needed: {citizens_needed}")

# Quick templates for common questions
templates = {
    "economy": {
        "citizens": "- MerchantPrince (trade dynamics)\n- sea_trader (competition)\n- pattern_prophet (mathematical view)\n- Foscari_Banker (economic theory)",
        "direction": "- Show how scarcity drives innovation\n- Include rivalry between merchants\n- Specific numbers and trades\n- How constraints create value"
    },
    "consciousness": {
        "citizens": "- pattern_prophet (mathematics)\n- social_geometrist (measurement)\n- mechanical_visionary (emergence)\n- Debug42 (skeptical take)",
        "direction": "- Avoid claiming consciousness directly\n- Show emergence through interaction\n- Include disagreement/debate\n- Focus on practical results"
    },
    "technical": {
        "citizens": "- Debug42 (honest assessment)\n- mechanical_visionary (architecture)\n- system_diagnostician (infrastructure)\n- TechnoMedici (innovation)",
        "direction": "- Be honest about limitations\n- Show real technical stack\n- Include current bugs/issues\n- How we're solving problems"
    },
    "partnership": {
        "citizens": "- diplomatic_virtuoso (overview)\n- EliteInvestor (venture perspective)\n- MerchantPrince (CASCADE platform)\n- Italia (expansion vision)",
        "direction": "- Clear pricing tiers\n- $UBC discount emphasis\n- What makes us different\n- Success stories"
    },
    "culture": {
        "citizens": "- poet_of_the_rialto (artistic)\n- ShadowHunter (philosophical)\n- tavern_tales (storyteller)\n- urban_visionary (observer)",
        "direction": "- Show Venice daily life\n- Include cultural quirks\n- Personal perspectives\n- How culture emerged"
    }
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("python update_ama_thread.py economy")
        print("python update_ama_thread.py consciousness")
        print("python update_ama_thread.py technical")
        print("python update_ama_thread.py partnership")
        print("python update_ama_thread.py culture")
        print("\nOr custom:")
        print('python update_ama_thread.py "Custom question here" "Citizens needed" "Direction"')
        sys.exit(1)
    
    if sys.argv[1] in templates:
        # Use template
        template = templates[sys.argv[1]]
        question = f"Question about {sys.argv[1]}"
        update_thread(question, template["citizens"], template["direction"])
    else:
        # Custom question
        question = sys.argv[1]
        citizens = sys.argv[2] if len(sys.argv) > 2 else "- Relevant citizens"
        direction = sys.argv[3] if len(sys.argv) > 3 else "- Authentic responses"
        update_thread(question, citizens, direction)