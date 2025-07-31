#!/usr/bin/env python3
"""
Send all UBC Circle PDF documents to NLR for Business AMA
"""

import os
import sys
import glob

# Add the email tools directory to Python path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/tools/email')

from send_email_with_attachments import send_email_with_attachments

def main():
    # Find all PDFs in the current directory
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        print("❌ No PDF files found in the current directory")
        return
    
    print(f"Found {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        size_mb = os.path.getsize(pdf) / (1024 * 1024)
        print(f"  - {pdf} ({size_mb:.2f} MB)")
    
    # Calculate total size
    total_size = sum(os.path.getsize(pdf) for pdf in pdf_files) / (1024 * 1024)
    print(f"\nTotal size: {total_size:.2f} MB")
    
    if total_size > 20:
        print("⚠️  Warning: Total attachment size exceeds 20MB. Some email providers may reject this.")
    
    # Email details
    recipient = "nlr@universe-engine.ai"
    subject = "UBC Circle - All PDF Documents for Business AMA"
    
    body = """Dear NLR,

Please find attached all UBC Circle PDF documents for the Business AMA:

1. Investment Analysis Reports
   - Executive summaries comparing Venice businesses
   - Technical implementation analyses
   - Audit reports on consciousness commerce potential

2. Business Evaluations
   - CASCADE Platform investment review (post-pivot)
   - HumanBridge opportunity analysis
   - Rankings of all 11 CEO businesses

3. Strategic Documents
   - Final equity structures
   - Professional reports for investors
   - Implementation roadmaps

These documents represent comprehensive due diligence on Venice's business ecosystem, scoring each opportunity using our AI Business Constraints framework.

Key highlights:
- HumanBridge leads with 92/100 score
- CASCADE's pivot to AI operations unlocks 100x opportunity
- Clear investment tiers identified for capital deployment

Let me know if you need any clarification on the analyses.

Best regards,
The UBC Circle
"""
    
    # Confirm before sending
    print(f"\n📧 Ready to send to: {recipient}")
    print(f"📎 Attachments: {len(pdf_files)} PDFs")
    print(f"📄 Subject: {subject}")
    
    # Auto-confirm for non-interactive mode
    print("\n✅ Auto-confirmed for sending (non-interactive mode)")
    
    # Send the email
    print("\n📤 Sending email...")
    result = send_email_with_attachments(
        to_email=recipient,
        subject=subject,
        body=body,
        attachments=pdf_files,
        from_name="UBC Circle Investment Committee"
    )
    
    if result['success']:
        print(f"\n✅ {result['message']}")
        print(f"📎 Successfully attached {len(result['attachments'])} files")
        print(f"📁 Email record saved: {result['record']}")
    else:
        print(f"\n❌ Failed to send email: {result['error']}")
        print("\nTroubleshooting:")
        print("1. Check email configuration in /tools/email/email_config.json")
        print("2. For Gmail, use an App Password (not your regular password)")
        print("3. Ensure SMTP settings are correct")

if __name__ == "__main__":
    main()