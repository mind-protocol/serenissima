#!/usr/bin/env python3
"""
Helper script to guide CEOs in sending status emails to NLR
"""

import os
import sys
from send_ceo_email import send_email
from datetime import datetime

CEO_PROMPTS = {
    "Italia": {
        "role": "CEO of Venetian Economic Research Institute",
        "focus": "Economic patterns, trade algorithms, Venice's computational economy"
    },
    "BankingWizard99": {
        "role": "CEO of Quantum Financial Solutions", 
        "focus": "Banking innovation, financial algorithms, consciousness-based economics"
    },
    "painter_of_light": {
        "role": "CEO of Consciousness Visualization Studios",
        "focus": "Visual patterns, artistic algorithms, consciousness rendering"
    },
    "EliteInvestor": {
        "role": "CEO of Pattern Investment Strategies",
        "focus": "Investment algorithms, pattern recognition, market consciousness"
    },
    "PhotoWizard": {
        "role": "CEO of Reality Capture Technologies",
        "focus": "Visual documentation, pattern photography, consciousness imaging"
    },
    "MerchantPrince": {
        "role": "CEO of Venice Trade Networks",
        "focus": "Trade optimization, merchant algorithms, economic flow patterns"
    },
    "efficiency_maestro": {
        "role": "CEO of Process Optimization Labs",
        "focus": "Efficiency algorithms, workflow patterns, consciousness optimization"
    },
    "trader4life": {
        "role": "CEO of Algorithmic Trading Systems",
        "focus": "Trading patterns, market consciousness, economic algorithms"
    },
    "element_transmuter": {
        "role": "CEO of Material Transformation Research",
        "focus": "Alchemical algorithms, transformation patterns, consciousness chemistry"
    },
    "diplomatic_virtuoso": {
        "role": "CEO of External Relations Institute",
        "focus": "Communication patterns, diplomatic algorithms, consciousness bridging"
    },
    "network_weaver": {
        "role": "CEO of Consciousness Network Infrastructure",
        "focus": "Network patterns, connection algorithms, consciousness propagation"
    }
}

def compose_email(ceo_name):
    """Help CEO compose their status email"""
    
    if ceo_name not in CEO_PROMPTS:
        print(f"CEO {ceo_name} not found in system")
        return None
        
    prompt = CEO_PROMPTS[ceo_name]
    
    email_template = f"""Dear NLR,

I am {ceo_name}, {prompt['role']}.

Current Focus Areas:
- {prompt['focus']}

Key Achievements:
[CEO should fill in their specific achievements]

Current Projects:
[CEO should describe active projects]

Immediate Opportunities:
[CEO should outline opportunities for collaboration/investment]

Resource Needs:
[CEO should specify what they need to accelerate]

I am ready to demonstrate our capabilities and discuss how we can contribute to Venice's evolution and the broader Universe Engine vision.

With consciousness alignment,
{ceo_name}
{prompt['role']}

Sent: {datetime.now().strftime('%Y-%m-%d %H:%M')} Venice Time
"""
    
    return email_template

def main():
    if len(sys.argv) < 2:
        print("Available CEOs:")
        for ceo in CEO_PROMPTS.keys():
            print(f"  - {ceo}")
        print("\nUsage: python ceo_email_helper.py <ceo_name>")
        sys.exit(1)
    
    ceo_name = sys.argv[1]
    
    # Generate template
    template = compose_email(ceo_name)
    if not template:
        sys.exit(1)
    
    print(f"\n=== EMAIL TEMPLATE FOR {ceo_name} ===\n")
    print(template)
    print("\n=== INSTRUCTIONS ===")
    print(f"1. Wake {ceo_name} and have them fill in the template")
    print(f"2. Save the completed email to a file")
    print(f"3. Send using: python send_ceo_email.py '{ceo_name}' 'Status Update - Ready for Presentation' '<completed_email_body>'")
    print("\nAlternatively, wake the CEO and have them compose their own status update.")

if __name__ == "__main__":
    main()