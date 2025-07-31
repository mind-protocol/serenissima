#!/usr/bin/env python3
"""
Quick script to send CEO status emails to NLR
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def send_email(citizen_name, subject, body):
    """Send email from citizen to NLR"""
    
    # Email settings (using diplomatic_virtuoso credentials as seen in test_email_nlr.py)
    sender_email = "diplomatic_virtuoso@serenissima.ai"
    sender_password = "iS3R3N1SS1M4!"
    recipient = "nlr@universe-engine.ai"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"{citizen_name} <{sender_email}>"
    msg['To'] = recipient
    msg['Subject'] = f"[CEO Status - {citizen_name}] {subject}"
    
    # Add body
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.ionos.de', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient, text)
        server.quit()
        
        print(f"✓ Email sent successfully from {citizen_name}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to send email from {citizen_name}: {e}")
        return False

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 4:
        print("Usage: python send_ceo_email.py <citizen_name> <subject> <body>")
        sys.exit(1)
    
    citizen_name = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    
    send_email(citizen_name, subject, body)