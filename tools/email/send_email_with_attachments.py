#!/usr/bin/env python3
"""
Send email with attachments support for Venice citizens
Enhanced version that supports file attachments
"""

import os
import sys
import smtplib
import json
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email import encoders
import mimetypes
from typing import List, Optional, Dict, Union
from pathlib import Path

# Load configuration
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "email_config.json")

try:
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)
except:
    print("❌ Error: Could not load email configuration")
    print(f"Please ensure {CONFIG_PATH} exists")
    sys.exit(1)

def get_attachment_mime(file_path: str) -> Union[MIMEBase, MIMEImage, MIMEAudio]:
    """
    Create appropriate MIME object for attachment based on file type
    """
    # Guess the content type based on the file's extension
    ctype, encoding = mimetypes.guess_type(file_path)
    
    if ctype is None or encoding is not None:
        # No guess could be made, or the file is encoded (compressed), so use generic binary type
        ctype = 'application/octet-stream'
    
    maintype, subtype = ctype.split('/', 1)
    
    # Read the file
    with open(file_path, 'rb') as fp:
        file_data = fp.read()
    
    # Create appropriate MIME object
    if maintype == 'text':
        # Text files
        attachment = MIMEText(file_data.decode('utf-8', errors='ignore'), _subtype=subtype)
    elif maintype == 'image':
        # Image files
        attachment = MIMEImage(file_data, _subtype=subtype)
    elif maintype == 'audio':
        # Audio files
        attachment = MIMEAudio(file_data, _subtype=subtype)
    else:
        # Generic binary files
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)
    
    # Set the filename parameter
    filename = os.path.basename(file_path)
    attachment.add_header('Content-Disposition', 'attachment', filename=filename)
    
    return attachment

def send_email_with_attachments(
    to_email: Union[str, List[str]], 
    subject: str, 
    body: str,
    attachments: Optional[List[str]] = None,
    cc: Optional[Union[str, List[str]]] = None,
    bcc: Optional[Union[str, List[str]]] = None,
    reply_to: Optional[str] = None,
    from_name: Optional[str] = None
) -> Dict[str, any]:
    """
    Send an email with optional file attachments
    
    Args:
        to_email: Recipient email(s) - string or list of strings
        subject: Email subject
        body: Email body (plain text)
        attachments: List of file paths to attach
        cc: CC recipients - string or list of strings
        bcc: BCC recipients - string or list of strings
        reply_to: Reply-to email address
        from_name: Display name for sender
        
    Returns:
        Dict with status and details
    """
    try:
        # Create message
        msg = MIMEMultipart('mixed')
        
        # Handle multiple recipients
        if isinstance(to_email, list):
            to_addresses = to_email
            msg['To'] = ', '.join(to_email)
        else:
            to_addresses = [to_email]
            msg['To'] = to_email
        
        # Set from with optional display name
        # Allow sending from redirects by using a different From address
        from_email = config.get('from_email', config['sender_email'])
        if from_name:
            msg['From'] = f"{from_name} <{from_email}>"
        else:
            msg['From'] = from_email
            
        msg['Subject'] = subject
        
        # Handle CC
        cc_addresses = []
        if cc:
            if isinstance(cc, list):
                cc_addresses = cc
                msg['Cc'] = ', '.join(cc)
            else:
                cc_addresses = [cc]
                msg['Cc'] = cc
        
        # Handle BCC (not added to headers)
        bcc_addresses = []
        if bcc:
            if isinstance(bcc, list):
                bcc_addresses = bcc
            else:
                bcc_addresses = [bcc]
        
        # Add reply-to if specified
        if reply_to:
            msg['Reply-To'] = reply_to
        
        # Create the body part
        body_part = MIMEMultipart('alternative')
        body_part.attach(MIMEText(body, 'plain', 'utf-8'))
        msg.attach(body_part)
        
        # Process attachments
        attached_files = []
        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    print(f"⚠️ Warning: File not found: {file_path}")
                    continue
                
                try:
                    attachment = get_attachment_mime(file_path)
                    msg.attach(attachment)
                    attached_files.append({
                        'path': file_path,
                        'name': os.path.basename(file_path),
                        'size': os.path.getsize(file_path)
                    })
                    print(f"✅ Attached: {os.path.basename(file_path)}")
                except Exception as e:
                    print(f"❌ Error attaching {file_path}: {str(e)}")
        
        # Connect to server
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['sender_email'], config['sender_password'])
        
        # Send email to all recipients
        all_recipients = to_addresses + cc_addresses + bcc_addresses
        server.send_message(msg, to_addrs=all_recipients)
        server.quit()
        
        # Save sent email record
        sent_record = {
            'timestamp': datetime.now().isoformat(),
            'to': to_addresses,
            'cc': cc_addresses,
            'bcc': bcc_addresses,
            'subject': subject,
            'body': body,
            'attachments': attached_files,
            'reply_to': reply_to,
            'from_name': from_name,
            'status': 'sent'
        }
        
        # Save to sent folder
        sent_dir = os.path.join(os.path.dirname(__file__), "sent")
        os.makedirs(sent_dir, exist_ok=True)
        
        filename = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(os.path.join(sent_dir, filename), 'w') as f:
            json.dump(sent_record, f, indent=2)
        
        return {
            'success': True,
            'message': f'Email sent successfully to {", ".join(all_recipients)}',
            'attachments': attached_files,
            'record': filename
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def main():
    """Command line interface"""
    if len(sys.argv) < 3:
        print("Usage: python3 send_email_with_attachments.py <to_email> <subject> [body] [--attach file1.pdf file2.jpg ...]")
        print("\nExample:")
        print('  python3 send_email_with_attachments.py "partner@example.com" "Venice Report" "Please find attached..." --attach report.pdf screenshot.png')
        sys.exit(1)
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    
    # Parse body and attachments
    body = ""
    attachments = []
    
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == '--attach':
            # Everything after --attach is attachment paths
            attachments = sys.argv[i+1:]
            break
        else:
            # Before --attach, it's part of the body
            if body:
                body += " "
            body += sys.argv[i]
        i += 1
    
    # If no body provided, use a default
    if not body:
        body = "Please find the attached files."
    
    # Send email
    result = send_email_with_attachments(
        to_email=to_email,
        subject=subject,
        body=body,
        attachments=attachments
    )
    
    if result['success']:
        print(f"✅ {result['message']}")
        if result['attachments']:
            print(f"📎 Attached {len(result['attachments'])} file(s)")
    else:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)

if __name__ == "__main__":
    main()