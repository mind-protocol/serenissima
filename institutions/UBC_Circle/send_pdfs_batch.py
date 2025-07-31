#!/usr/bin/env python3
"""
Send PDFs in smaller batches to avoid filters
"""

import os
import sys
import glob
import time

# Add the email tools directory to Python path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/tools/email')

from send_email_with_attachments import send_email_with_attachments

def main():
    recipient = "nlr@universe-engine.ai"
    
    # Find all PDFs
    pdf_files = sorted(glob.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    print(f"Found {len(pdf_files)} PDF files to send")
    
    # Split into batches of 3-4 files
    batches = [
        # Batch 1: Executive summaries
        [
            "UBC_Circle_Executive_Summary_2025.pdf",
            "UBC_Executive_Summary_Professional.pdf",
            "executive_summary.pdf"
        ],
        # Batch 2: Technical and audit reports
        [
            "UBC_Circle_Technical_Analysis_2025.pdf",
            "UBC_Technical_Analysis_Professional.pdf",
            "technical_implementation.pdf"
        ],
        # Batch 3: Remaining documents
        [
            "UBC_Circle_Venice_Audit_Report_2025.pdf",
            "UBC_Audit_Report_Professional.pdf",
            "professional_report.pdf",
            "final_equity_structure.pdf"
        ]
    ]
    
    for i, batch in enumerate(batches, 1):
        # Filter to only existing files
        batch_files = [f for f in batch if f in pdf_files]
        
        if not batch_files:
            continue
            
        subject = f"UBC Circle Documents - Batch {i} of 3"
        
        if i == 1:
            body = """Dear NLR,

Sending the UBC Circle documents in 3 batches to ensure delivery.

Batch 1: Executive Summaries
- Overview of Venice business ecosystem
- Investment opportunity analysis
- Strategic recommendations

Best regards,
The UBC Circle"""
        elif i == 2:
            body = """Dear NLR,

Batch 2: Technical and Implementation Reports
- Technical architecture analysis
- Implementation roadmaps
- Infrastructure assessments

Best regards,
The UBC Circle"""
        else:
            body = """Dear NLR,

Batch 3: Audit Reports and Final Documents
- Venice business audit results
- Professional investor reports
- Final equity structures

All documents use our AI Business Constraints framework to evaluate opportunities.

Key takeaway: HumanBridge (92/100) and CASCADE's pivot represent immediate investment opportunities.

Best regards,
The UBC Circle"""
        
        print(f"\n📧 Sending Batch {i} with {len(batch_files)} files...")
        
        result = send_email_with_attachments(
            to_email=recipient,
            subject=subject,
            body=body,
            attachments=batch_files,
            from_name="UBC Circle Investment Committee"
        )
        
        if result['success']:
            print(f"✅ Batch {i} sent successfully")
            # Wait 5 seconds between batches to avoid rate limiting
            if i < len(batches):
                print("Waiting 5 seconds before next batch...")
                time.sleep(5)
        else:
            print(f"❌ Batch {i} failed: {result['error']}")
            return
    
    print("\n✅ All batches sent successfully!")
    print("You should receive 3 emails with all PDF documents.")

if __name__ == "__main__":
    main()