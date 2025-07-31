#!/usr/bin/env python3
"""
Test email delivery without attachments
"""

import os
import sys
from datetime import datetime

# Add the email tools directory to Python path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/tools/email')

from send_email_with_attachments import send_email_with_attachments

def main():
    recipient = "nlr@universe-engine.ai"
    subject = "TEST: UBC Circle Email Delivery Check"
    
    body = f"""This is a test email from UBC Circle to verify email delivery.

Timestamp: {datetime.now().isoformat()}

If you receive this email, the email system is working correctly.
The issue with the previous email may have been due to:
- Attachment size
- Spam filtering
- Delivery delays

Please confirm receipt so we can proceed with sending the PDF documents.

Best regards,
The UBC Circle
"""
    
    print(f"\n📧 Sending test email to: {recipient}")
    print(f"📄 Subject: {subject}")
    print("\n📤 Sending test email without attachments...")
    
    result = send_email_with_attachments(
        to_email=recipient,
        subject=subject,
        body=body,
        attachments=None,  # No attachments for test
        from_name="UBC Circle Test"
    )
    
    if result['success']:
        print(f"\n✅ {result['message']}")
        print(f"📁 Email record saved: {result['record']}")
        print("\n🔍 Please check if this test email arrives.")
        print("If it does, we'll know the email system works and can troubleshoot attachment delivery.")
    else:
        print(f"\n❌ Failed to send test email: {result['error']}")

if __name__ == "__main__":
    main()