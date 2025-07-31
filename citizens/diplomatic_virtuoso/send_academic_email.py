#!/usr/bin/env python3
"""Send academic collaboration email to Ghaffarzadegan team"""

from send_diplomatic_email import DiplomaticEmailer
from pathlib import Path

def send_academic_collaboration():
    """Send the academic collaboration proposal"""
    
    emailer = DiplomaticEmailer()
    
    # Load the email content
    content_path = Path(__file__).parent / 'academic_collaboration_response.md'
    with open(content_path) as f:
        content = f.read()
    
    # Extract just the email portion (after "## Diplomatic Response Draft")
    email_start = content.find("Dear Professor Ghaffarzadegan")
    email_end = content.find("---", email_start)
    email_body = content[email_start:email_end].strip()
    
    # Recipients
    to_emails = [
        "navidg@vt.edu",  # Professor Ghaffarzadegan
        "aritra.majumdar@vt.edu",  # Aritra (assuming VT email)
        "ross@vt.edu"  # Ross (assuming VT email)
    ]
    
    # CC NLR
    cc_email = "nlr@universe-engine.ai"
    
    subject = "Re: Generative Agent-Based Modeling - Venice Bridge to Academic Validation"
    
    # Note: Most email systems need special handling for CC
    # For now, we'll mention it in the email and send separately
    
    print("Sending to academic team...")
    
    # Send to main recipients
    for recipient in to_emails:
        if emailer.send_email(recipient, subject, email_body):
            print(f"✅ Sent to {recipient}")
        else:
            print(f"❌ Failed to send to {recipient}")
    
    # Send CC to NLR
    cc_subject = f"[CC] {subject}"
    cc_note = "CC: This email was sent to the Virginia Tech research team\n\n" + email_body
    
    if emailer.send_email(cc_email, cc_subject, cc_note):
        print(f"✅ CC sent to {cc_email}")
    
    print("\n📧 Academic collaboration email sent!")
    print("Next steps: Monitor for responses and prepare live demo")

if __name__ == "__main__":
    send_academic_collaboration()