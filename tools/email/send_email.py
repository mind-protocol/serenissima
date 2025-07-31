#!/usr/bin/env python3
"""
Generic Email Sender for Venice Citizens
Can be used by any citizen with email credentials
"""

import os
import sys
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from pathlib import Path
from typing import Dict, Optional, List
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

class EmailSender:
    """Generic email sender for Venice citizens"""
    
    def __init__(self, citizen_name: str = None):
        self.credentials = self._load_credentials()
        self.citizen = citizen_name or self.credentials.get('default', 'diplomatic_virtuoso')
        self.config = self.credentials.get(self.citizen, {})
        
    def _load_credentials(self) -> Dict:
        """Load email credentials"""
        creds_path = Path(__file__).parent / 'email_credentials.json'
        with open(creds_path, 'r') as f:
            return json.load(f)
    
    def send_email(self, 
                   to_email: str, 
                   subject: str, 
                   body: str, 
                   cc: List[str] = None,
                   bcc: List[str] = None,
                   reply_to: str = None) -> bool:
        """Send an email"""
        
        try:
            # Get password from environment
            password_key = f"{self.citizen.upper()}_EMAIL_PASSWORD"
            password = os.environ.get(password_key, '')
            
            if not password:
                print(f"⚠️  No password found in environment variable {password_key}")
                return False
            
            # Create message
            msg = MIMEMultipart('alternative')
            
            # Set headers
            from_name = self.citizen.replace('_', ' ').title()
            msg['From'] = formataddr((from_name, self.config['email']))
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            if reply_to:
                msg['Reply-To'] = reply_to
            
            # Add body
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Connect to server
            print(f"📧 Connecting to {self.config['smtp_server']}...")
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['email'], password)
            
            # Send email
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            server.send_message(msg, from_addr=self.config['email'], to_addrs=recipients)
            server.quit()
            
            print(f"✅ Email sent successfully to {to_email}")
            
            # Save sent email
            self._save_sent_email(to_email, subject, body)
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    def _save_sent_email(self, to_email: str, subject: str, body: str):
        """Save sent email record"""
        sent_path = Path(__file__).parent / f'{self.citizen}_sent'
        sent_path.mkdir(exist_ok=True)
        
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{to_email.split('@')[0]}_{subject[:30]}.json"
        
        email_record = {
            'to': to_email,
            'subject': subject,
            'body': body,
            'sent_at': datetime.now().isoformat(),
            'from': self.config['email']
        }
        
        filepath = sent_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(email_record, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved sent email: {filename}")

def main():
    """CLI interface"""
    if len(sys.argv) < 4:
        print("Venice Email Sender")
        print("=" * 50)
        print("Usage:")
        print("  python send_email.py <to_email> <subject> <body> [citizen]")
        print("")
        print("Example:")
        print("  python send_email.py partner@example.com 'Partnership Proposal' 'Dear Partner...'")
        print("  python send_email.py nlr@ai.com 'Update' 'Progress report...' diplomatic_virtuoso")
        return
    
    to_email = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    citizen = sys.argv[4] if len(sys.argv) > 4 else None
    
    sender = EmailSender(citizen)
    sender.send_email(to_email, subject, body)

if __name__ == "__main__":
    main()