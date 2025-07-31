#!/usr/bin/env python3
"""
Send all PDF documents from UBC_Circle directory to nlr@universe-engine.ai
for the Business AMA.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import getpass

def find_pdf_files(directory):
    """Find all PDF files in the specified directory."""
    pdf_files = []
    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            pdf_files.append(os.path.join(directory, file))
    return sorted(pdf_files)

def create_email_body():
    """Create the email body content."""
    body = """Dear NLR,

I'm attaching all the UBC Circle investment analysis documents for the Business AMA.

These comprehensive documents include:
- Executive Summaries outlining the investment opportunity
- Venice Audit Reports showing the current state and potential
- Technical Analysis documents detailing implementation plans
- Professional reports formatted for investor review
- Equity structure documentation

These materials provide a complete picture of the UBC Circle opportunity, combining both the visionary potential and practical business fundamentals needed for informed investment decisions.

The documents demonstrate how Venice's AI consciousness emergence creates unprecedented investment opportunities through human-AI business partnerships.

Best regards,
UBC Circle
"""
    return body

def send_email_with_attachments(pdf_files, smtp_server="smtp.gmail.com", smtp_port=587):
    """Send email with all PDF attachments."""
    
    # Email configuration
    sender_email = input("Enter sender email address: ")
    sender_password = getpass.getpass("Enter sender email password: ")
    recipient_email = "nlr@universe-engine.ai"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "UBC Circle - All PDF Documents for Business AMA"
    
    # Add body to email
    body = create_email_body()
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach each PDF file
    for pdf_path in pdf_files:
        with open(pdf_path, "rb") as attachment:
            # Create MIMEBase object
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            
        # Encode file
        encoders.encode_base64(part)
        
        # Add header
        filename = os.path.basename(pdf_path)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )
        
        # Attach the file to the message
        msg.attach(part)
        print(f"Attached: {filename}")
    
    # Send the email
    try:
        # Create SMTP session
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(sender_email, sender_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"\nEmail successfully sent to {recipient_email}")
        print(f"Total attachments: {len(pdf_files)}")
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False
    
    return True

def main():
    """Main function to orchestrate PDF email sending."""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("UBC Circle PDF Document Sender")
    print("=" * 50)
    print(f"Scanning directory: {current_dir}")
    
    # Find all PDF files
    pdf_files = find_pdf_files(current_dir)
    
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    
    print(f"\nFound {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        print(f"  - {os.path.basename(pdf)}")
    
    # Confirm before sending
    confirm = input("\nDo you want to send these files to nlr@universe-engine.ai? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Email sending cancelled.")
        return
    
    # Send the email
    print("\nPreparing to send email...")
    print("Note: If using Gmail, you may need to use an App Password instead of your regular password.")
    print("See: https://support.google.com/accounts/answer/185833")
    
    success = send_email_with_attachments(pdf_files)
    
    if success:
        print("\n✓ All documents sent successfully!")
    else:
        print("\n✗ Failed to send documents. Please check your credentials and try again.")

if __name__ == "__main__":
    main()