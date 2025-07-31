#!/usr/bin/env python3
"""
Alternative method to send PDFs - using gmail or other provider
"""

import os
import smtplib
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def send_with_gmail():
    """Send using Gmail with app password"""
    print("\n📧 Gmail Email Setup")
    print("Note: You need a Gmail App Password (not your regular password)")
    print("Get one at: https://myaccount.google.com/apppasswords\n")
    
    sender_email = input("Enter your Gmail address: ")
    app_password = input("Enter your Gmail App Password: ")
    
    return send_pdfs(sender_email, app_password, "smtp.gmail.com", 587)

def send_with_custom():
    """Send using custom SMTP settings"""
    print("\n📧 Custom SMTP Setup")
    sender_email = input("Enter sender email: ")
    password = input("Enter password: ")
    smtp_server = input("Enter SMTP server (e.g., smtp.gmail.com): ")
    smtp_port = int(input("Enter SMTP port (usually 587 or 465): "))
    
    return send_pdfs(sender_email, password, smtp_server, smtp_port)

def send_pdfs(sender_email, password, smtp_server, smtp_port):
    """Send the PDFs using provided credentials"""
    recipient = "nlr@universe-engine.ai"
    
    # Find all PDFs
    pdf_files = glob.glob("*.pdf")
    
    if not pdf_files:
        print("❌ No PDF files found")
        return False
    
    print(f"\n📎 Found {len(pdf_files)} PDFs to attach")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = "UBC Circle - All PDF Documents for Business AMA"
    
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

These documents represent comprehensive due diligence on Venice's business ecosystem.

Key highlights:
- HumanBridge leads with 92/100 score
- CASCADE's pivot to AI operations unlocks 100x opportunity
- Clear investment tiers identified for capital deployment

Best regards,
The UBC Circle
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDFs
    for pdf in pdf_files:
        try:
            with open(pdf, 'rb') as file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(pdf)}')
                msg.attach(part)
                print(f"✅ Attached: {pdf}")
        except Exception as e:
            print(f"❌ Failed to attach {pdf}: {e}")
    
    # Send email
    try:
        print(f"\n📤 Sending to {recipient}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        print("\n✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Failed to send: {e}")
        return False

def main():
    print("🔧 UBC Circle PDF Sender")
    print("\nChoose sending method:")
    print("1. Gmail (recommended)")
    print("2. Custom SMTP")
    print("3. Generate file list for manual send")
    
    choice = input("\nEnter choice (1-3): ")
    
    if choice == "1":
        send_with_gmail()
    elif choice == "2":
        send_with_custom()
    elif choice == "3":
        # Just list the files
        pdf_files = glob.glob("*.pdf")
        print("\n📄 PDF files to send to nlr@universe-engine.ai:")
        for pdf in pdf_files:
            print(f"  - {pdf}")
        print("\nPlease attach these files manually to your email.")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()