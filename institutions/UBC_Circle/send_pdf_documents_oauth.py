#!/usr/bin/env python3
"""
Alternative email sender using environment variables and configuration file
for sending PDF documents to nlr@universe-engine.ai
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import json
import sys

def load_email_config():
    """Load email configuration from file or environment variables."""
    config = {}
    
    # Check for config file first
    config_file = os.path.join(os.path.dirname(__file__), 'email_config.json')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            print("Loaded configuration from email_config.json")
    else:
        # Try environment variables
        config['sender_email'] = os.environ.get('EMAIL_SENDER')
        config['sender_password'] = os.environ.get('EMAIL_PASSWORD')
        config['smtp_server'] = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        config['smtp_port'] = int(os.environ.get('SMTP_PORT', '587'))
        
        if config['sender_email'] and config['sender_password']:
            print("Loaded configuration from environment variables")
        else:
            print("No configuration found. Please create email_config.json or set environment variables.")
            print("\nExample email_config.json:")
            print(json.dumps({
                "sender_email": "your-email@gmail.com",
                "sender_password": "your-app-password",
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587
            }, indent=2))
            print("\nOr set environment variables:")
            print("export EMAIL_SENDER='your-email@gmail.com'")
            print("export EMAIL_PASSWORD='your-app-password'")
            return None
    
    return config

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

def send_email_with_attachments(pdf_files, config):
    """Send email with all PDF attachments."""
    
    recipient_email = "nlr@universe-engine.ai"
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = config['sender_email']
    msg['To'] = recipient_email
    msg['Subject'] = "UBC Circle - All PDF Documents for Business AMA"
    
    # Add body to email
    body = create_email_body()
    msg.attach(MIMEText(body, 'plain'))
    
    # Calculate total size
    total_size = 0
    for pdf_path in pdf_files:
        total_size += os.path.getsize(pdf_path)
    
    print(f"\nTotal size of attachments: {total_size / 1024 / 1024:.2f} MB")
    
    # Warn if size is large
    if total_size > 25 * 1024 * 1024:  # 25MB
        print("WARNING: Total attachment size exceeds 25MB. Some email providers may reject this.")
        confirm = input("Continue anyway? (yes/no): ")
        if confirm.lower() != 'yes':
            return False
    
    # Attach each PDF file
    for pdf_path in pdf_files:
        try:
            with open(pdf_path, "rb") as attachment:
                # Create MIMEBase object
                part = MIMEBase('application', 'pdf')
                part.set_payload(attachment.read())
            
            # Encode file
            encoders.encode_base64(part)
            
            # Add header
            filename = os.path.basename(pdf_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            
            # Attach the file to the message
            msg.attach(part)
            file_size = os.path.getsize(pdf_path) / 1024 / 1024
            print(f"Attached: {filename} ({file_size:.2f} MB)")
            
        except Exception as e:
            print(f"Error attaching {filename}: {str(e)}")
            continue
    
    # Send the email
    try:
        # Create SMTP session
        print(f"\nConnecting to {config['smtp_server']}:{config['smtp_port']}...")
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.set_debuglevel(0)  # Set to 1 for debug output
        server.starttls()  # Enable TLS encryption
        
        print("Authenticating...")
        server.login(config['sender_email'], config['sender_password'])
        
        # Send email
        print("Sending email...")
        text = msg.as_string()
        server.sendmail(config['sender_email'], recipient_email, text)
        server.quit()
        
        print(f"\n✓ Email successfully sent to {recipient_email}")
        print(f"Total attachments: {len(pdf_files)}")
        
    except smtplib.SMTPAuthenticationError:
        print("\n✗ Authentication failed. Please check your credentials.")
        print("If using Gmail, make sure you're using an App Password, not your regular password.")
        print("See: https://support.google.com/accounts/answer/185833")
        return False
    except Exception as e:
        print(f"\n✗ Error sending email: {str(e)}")
        return False
    
    return True

def main():
    """Main function to orchestrate PDF email sending."""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("UBC Circle PDF Document Sender")
    print("=" * 50)
    print(f"Scanning directory: {current_dir}")
    
    # Load configuration
    config = load_email_config()
    if not config:
        sys.exit(1)
    
    # Find all PDF files
    pdf_files = find_pdf_files(current_dir)
    
    if not pdf_files:
        print("No PDF files found in the directory.")
        return
    
    print(f"\nFound {len(pdf_files)} PDF files:")
    for pdf in pdf_files:
        file_size = os.path.getsize(pdf) / 1024 / 1024
        print(f"  - {os.path.basename(pdf)} ({file_size:.2f} MB)")
    
    # Confirm before sending
    confirm = input("\nDo you want to send these files to nlr@universe-engine.ai? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Email sending cancelled.")
        return
    
    # Send the email
    success = send_email_with_attachments(pdf_files, config)
    
    if success:
        print("\n✓ All documents sent successfully!")
    else:
        print("\n✗ Failed to send documents.")

if __name__ == "__main__":
    main()