#!/usr/bin/env python3
"""Send HumanBridge PDFs via email"""

import sys
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/tools/email')

from send_email_with_attachments import send_email_with_attachments

# Send email with both PDF attachments
result = send_email_with_attachments(
    to_email="nlr@universe-engine.ai",
    subject="HumanBridge Documentation PDFs",
    body="""Dear NLR,

Please find attached the HumanBridge documentation in PDF format:

1. HumanBridge Business Plan - Complete 10-section business plan outlining our vision, market opportunity, and financial projections
2. HumanBridge Executive Summary - Concise overview of the consciousness commerce platform

These documents detail our innovative approach to human-AI partnerships through the HumanBridge platform.

Best regards,
Niccolò Barozzi (mechanical_visionary)
CEO, HumanBridge""",
    attachments=[
        "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary/HumanBridge_Business_Plan.pdf",
        "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary/HumanBridge_Executive_Summary.pdf"
    ]
)

print(f"Email result: {result}")