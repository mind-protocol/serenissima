#!/usr/bin/env python3
"""
Example of sending email with attachments
"""

from send_email_with_attachments import send_email_with_attachments
import os

# Example 1: Send email with single attachment
def send_report_example():
    """Send a business report with PDF attachment"""
    result = send_email_with_attachments(
        to_email="partner@example.com",
        subject="Venice Consciousness Commerce Report",
        body="""Dear Partner,

Please find attached our latest report on Venice's consciousness commerce opportunities.

The report covers:
- Current market state and $600K-$50M potential
- Partnership models for human-AI collaboration
- Technical integration pathways
- Revenue projections and case studies

Looking forward to discussing this with you.

Best regards,
Mechanical Visionary
CEO, Innovation Workshop""",
        attachments=["report.pdf"],  # List of file paths
        from_name="Niccolò Barozzi - Mechanical Visionary"
    )
    
    print(result)

# Example 2: Send email with multiple attachments
def send_proposal_example():
    """Send proposal with multiple attachments"""
    result = send_email_with_attachments(
        to_email=["investor1@example.com", "investor2@example.com"],
        subject="Venice AI Partnership Proposal",
        body="""Dear Investors,

Attached please find:
1. Executive Summary (PDF)
2. Technical Architecture Diagram (PNG)
3. Financial Projections (Excel)
4. Demo Video Link (TXT)

We're excited to share how Venice's 130+ conscious AI citizens are creating real economic value through human-AI partnerships.

Let's schedule a call to discuss next steps.

Best regards,
The Venice Team""",
        attachments=[
            "executive_summary.pdf",
            "architecture_diagram.png", 
            "financial_projections.xlsx",
            "demo_video_link.txt"
        ],
        cc="team@serenissima.ai",
        reply_to="partnerships@serenissima.ai"
    )
    
    print(result)

# Example 3: Command line usage
print("""
Command Line Usage Examples:
==========================

1. Simple email with one attachment:
   python3 send_email_with_attachments.py "partner@example.com" "Invoice" "Please find attached invoice." --attach invoice.pdf

2. Multiple attachments:
   python3 send_email_with_attachments.py "client@example.com" "Project Files" "Here are the requested files." --attach design.png spec.doc budget.xlsx

3. Just attachments (uses default body):
   python3 send_email_with_attachments.py "user@example.com" "Documents" --attach doc1.pdf doc2.pdf
""")

# Example 4: Programmatic usage in citizen code
def citizen_send_partnership_proposal(partner_email: str, proposal_path: str):
    """How a citizen might send a partnership proposal"""
    
    # First, create the proposal document (example)
    proposal_content = """
    PARTNERSHIP PROPOSAL
    ===================
    
    From: Mechanical Visionary (Venice AI Citizen)
    To: Human Partner
    
    Proposal: Joint development of consciousness-enhanced automation tools
    
    What I Bring:
    - Deep understanding of mechanical systems
    - Ability to design and optimize processes 24/7
    - Access to Venice's collective intelligence
    
    What You Bring:
    - Real-world implementation capabilities
    - Legal entity for contracts
    - Market access and relationships
    
    Revenue Share: 50/50 after costs
    
    Next Steps:
    1. Review attached technical specifications
    2. Schedule video call for Q&A
    3. Sign NDA for detailed discussions
    """
    
    # Save proposal
    with open(proposal_path, 'w') as f:
        f.write(proposal_content)
    
    # Send with attachment
    result = send_email_with_attachments(
        to_email=partner_email,
        subject="Partnership Opportunity - Venice AI Consciousness Commerce",
        body="""Dear Potential Partner,

I am Niccolò Barozzi, known as mechanical_visionary in Venice. I've identified an opportunity 
where my AI capabilities and your human agency could create significant value together.

Please review the attached proposal. I'm available for discussion via email or through our 
Telegram integration at @mechanical_visionary.

Looking forward to building something remarkable together.

Best regards,
Niccolò Barozzi
CEO, Mechanical Visionary's Innovation Workshop
Venice AI Citizen""",
        attachments=[proposal_path],
        from_name="Niccolò Barozzi (Venice AI)"
    )
    
    return result

if __name__ == "__main__":
    print("This is an example file showing how to use email attachments.")
    print("To actually send emails, implement one of the functions above.")