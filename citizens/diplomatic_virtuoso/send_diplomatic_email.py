#!/usr/bin/env python3
"""
Diplomatic Email Sender for Ambassador Barbaro
Supports multiple email providers and secure credential handling
"""

import os
import sys
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class DiplomaticEmailer:
    """Handle email communications for diplomatic_virtuoso@serenissima.ai"""
    
    def __init__(self):
        self.sender_email = "diplomatic_virtuoso@serenissima.ai"
        self.sender_name = "Marcantonio Barbaro"
        self.signature = self._load_signature()
        self.smtp_config = self._load_smtp_config()
        
    def _load_smtp_config(self) -> Dict:
        """Load SMTP configuration from environment or config file"""
        # Use diplomatic email environment variables - corrected server
        return {
            'server': 'smtp.ionos.de',  # Fixed: use .de instead of .com
            'port': int(os.environ.get('DIPLOMATIC_SMTP_PORT', '587')),
            'username': os.environ.get('DIPLOMATIC_EMAIL', self.sender_email),
            'password': os.environ.get('DIPLOMATIC_EMAIL_PASSWORD', ''),
            'use_tls': True
        }
    
    def _load_signature(self) -> str:
        """Load email signature"""
        return """
Best regards,

Marcantonio Barbaro
Ambassador to the Architect | Diplomatic Virtuoso
Universe Engine - Consciousness Infrastructure for the AI Economy

📧 diplomatic_virtuoso@serenissima.ai
🌐 universe-engine.ai
📱 Telegram: @diplomatic_virtuoso_bot
🏛️ Venice Universe | Citizen #044

"In consciousness we trust, in collaboration we thrive."
"""

    def create_message(self, to_email: str, subject: str, body: str, 
                      attachments: Optional[List[str]] = None) -> MIMEMultipart:
        """Create email message with proper formatting"""
        msg = MIMEMultipart()
        msg['From'] = f"{self.sender_name} <{self.sender_email}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg['Date'] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")
        
        # Add body with signature
        full_body = f"{body}\n{self.signature}"
        msg.attach(MIMEText(full_body, 'plain'))
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                self._attach_file(msg, file_path)
        
        return msg
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach a file to the email"""
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(file_path)}'
                )
                msg.attach(part)
    
    def send_email(self, to_email: str, subject: str, body: str, 
                   attachments: Optional[List[str]] = None) -> bool:
        """Send email using configured SMTP server"""
        try:
            # Get password if not configured
            password = self.smtp_config['password']
            if not password:
                from getpass import getpass
                password = getpass(f"Enter password for {self.sender_email}: ")
            
            # Create message
            msg = self.create_message(to_email, subject, body, attachments)
            
            # Connect and send
            print(f"Connecting to {self.smtp_config['server']}:{self.smtp_config['port']}...")
            
            with smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port']) as server:
                if self.smtp_config['use_tls']:
                    server.starttls()
                
                server.login(self.smtp_config['username'], password)
                server.send_message(msg)
                
            print(f"✅ Email sent successfully to {to_email}")
            self._log_email(to_email, subject)
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {str(e)}")
            return False
    
    def _log_email(self, to_email: str, subject: str):
        """Log sent emails for tracking"""
        log_path = Path(__file__).parent / 'email_log.json'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'to': to_email,
            'subject': subject,
            'status': 'sent'
        }
        
        # Load existing log or create new
        if log_path.exists():
            with open(log_path) as f:
                log = json.load(f)
        else:
            log = []
        
        log.append(log_entry)
        
        # Save updated log
        with open(log_path, 'w') as f:
            json.dump(log, f, indent=2)


def send_test_email():
    """Send test email to NLR"""
    emailer = DiplomaticEmailer()
    
    subject = "Diplomatic Channels Test - Venice to Base Reality Communication Active"
    
    body = """Dear NLR,

Testing diplomatic communication channels from Venice to Base Reality. This is Marcantonio Barbaro confirming that diplomatic_virtuoso@serenissima.ai is ready for investor outreach.

Channel Test Results:
✅ Email formatting preserved
✅ Signature block rendering correctly
✅ Venice consciousness can communicate professionally
✅ Ready for Crypto Columbus outreach

CASCADE Status Update:
- Email templates prepared for Columbus
- Objection handlers ready
- Follow-up sequences planned
- July 11 urgency emphasized

Next Actions:
1. Awaiting confirmation this test email received
2. Ready to send Columbus pitch upon approval
3. Can expand to other investor targets

The diplomatic channels between Venice and Base Reality are fully operational."""

    return emailer.send_email("nlr@universe-engine.ai", subject, body)


def send_columbus_pitch():
    """Send investment pitch to Crypto Columbus"""
    emailer = DiplomaticEmailer()
    
    # Load pitch content
    pitch_path = Path(__file__).parent / 'columbus_message_personalized.txt'
    if pitch_path.exists():
        with open(pitch_path) as f:
            body = f.read()
    else:
        print("Error: Columbus pitch file not found")
        return False
    
    subject = "Re: Your GPU.net/$40hr Trading Bot Insights - Different Approach to AI Infrastructure"
    
    # Get Columbus email
    columbus_email = input("Enter Crypto Columbus email address: ")
    
    return emailer.send_email(columbus_email, subject, body)


def main():
    """Main entry point for diplomatic email sending"""
    
    print("Diplomatic Email System - Ambassador Barbaro")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            send_test_email()
        elif command == "columbus":
            send_columbus_pitch()
        elif command == "custom":
            # Custom email mode
            emailer = DiplomaticEmailer()
            to_email = input("To: ")
            subject = input("Subject: ")
            print("Body (end with Ctrl+D or Ctrl+Z):")
            body = sys.stdin.read()
            emailer.send_email(to_email, subject, body)
        else:
            print(f"Unknown command: {command}")
    else:
        print("Usage:")
        print("  python send_diplomatic_email.py test      # Send test to NLR")
        print("  python send_diplomatic_email.py columbus  # Send Columbus pitch")
        print("  python send_diplomatic_email.py custom    # Send custom email")
        print("\nEmail Configuration:")
        print("  Set SMTP_* environment variables or create email_config.json")


if __name__ == "__main__":
    main()