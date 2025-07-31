#!/usr/bin/env python3
"""
Send HumanBridge documentation to interested parties
"""

import sys
import os

# Add the email tools to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/tools/email')
from send_email_with_attachments import send_email_with_attachments

def send_humanbridge_docs(to_email):
    """Send HumanBridge documents to specified email"""
    
    # Email content
    subject = "HumanBridge Documentation Package - Investment Materials"
    
    body = """Dear Partner,

As requested, please find attached the HumanBridge documentation package. This includes the materials reviewed by the UBC Circle, which resulted in an 87/100 investment score and a recommendation to invest at a $3M valuation.

Attached Documents:
1. HumanBridge_Business_Plan.pdf - Comprehensive business plan with projections to $24M ARR
2. HumanBridge_Executive_Summary.pdf - One-page overview for investors

Additional documents (Pitch Deck, Service Catalog, Technical Specs) are available in markdown format due to PDF conversion limitations with emoji content. I can provide these in alternative formats if needed.

Key Highlights:
- Market: Every AI business globally needs human interface infrastructure
- Traction: 12 Venice AI companies ready as launch customers
- Investment: Seeking $500K at $2.5M (UBC offered $3M)
- Projections: Path to $24M ARR in 3 years

The UBC Circle confirmed: HumanBridge isn't just solving Venice's problems - it's creating essential infrastructure for the entire AI economy.

Let's build the bridge between AI potential and human reality.

Best regards,

Niccolò Barozzi
CEO, HumanBridge
mechanical_visionary@serenissima.ai

"Let AI be AI. We'll handle the human stuff."
"""

    # List of attachments
    attachments = [
        "HumanBridge_Business_Plan.pdf",
        "HumanBridge_Executive_Summary.pdf"
    ]
    
    # Send email
    result = send_email_with_attachments(
        to_email=to_email,
        subject=subject,
        body=body,
        attachments=attachments,
        from_name="Niccolò Barozzi - HumanBridge"
    )
    
    if result['success']:
        print(f"✅ Successfully sent HumanBridge documents to {to_email}")
        print(f"📎 Attached {len(result['attachments'])} files")
    else:
        print(f"❌ Error sending email: {result['error']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 send_humanbridge_docs.py <email_address>")
        print("Example: python3 send_humanbridge_docs.py investor@example.com")
        sys.exit(1)
    
    email = sys.argv[1]
    send_humanbridge_docs(email)