#!/usr/bin/env python3
"""
Diplomatic Email Receiver for Ambassador Barbaro
Checks and processes incoming emails for diplomatic_virtuoso@serenissima.ai
"""

import os
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class DiplomaticEmailReceiver:
    """Handle incoming emails for diplomatic_virtuoso@serenissima.ai"""
    
    def __init__(self):
        self.email_address = "diplomatic_virtuoso@serenissima.ai"
        self.imap_config = self._load_imap_config()
        self.inbox_path = Path(__file__).parent / 'diplomatic_inbox'
        self.inbox_path.mkdir(exist_ok=True)
        
    def _load_imap_config(self) -> Dict:
        """Load IMAP configuration"""
        return {
            'server': 'imap.ionos.de',  # IONOS IMAP server
            'port': 993,  # SSL port
            'username': os.environ.get('DIPLOMATIC_EMAIL', self.email_address),
            'password': os.environ.get('DIPLOMATIC_EMAIL_PASSWORD', '')
        }
    
    def connect_to_inbox(self) -> Optional[imaplib.IMAP4_SSL]:
        """Connect to email inbox"""
        try:
            print(f"Connecting to {self.imap_config['server']}...")
            
            # Create SSL connection
            mail = imaplib.IMAP4_SSL(self.imap_config['server'], self.imap_config['port'])
            
            # Login
            mail.login(self.imap_config['username'], self.imap_config['password'])
            print("✅ Successfully connected to inbox")
            
            return mail
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return None
    
    def fetch_recent_emails(self, mail: imaplib.IMAP4_SSL, num_emails: int = 10) -> List[Dict]:
        """Fetch recent emails from inbox"""
        emails_data = []
        
        try:
            # Select inbox
            mail.select('INBOX')
            
            # Search for all emails
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                print("Failed to search emails")
                return emails_data
            
            # Get email IDs
            email_ids = messages[0].split()
            
            # Get the most recent emails
            recent_ids = email_ids[-num_emails:] if len(email_ids) > num_emails else email_ids
            recent_ids.reverse()  # Most recent first
            
            print(f"\nFetching {len(recent_ids)} recent emails...")
            
            for email_id in recent_ids:
                # Fetch email
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status != 'OK':
                    continue
                
                # Parse email
                msg = email.message_from_bytes(msg_data[0][1])
                email_info = self._parse_email(msg)
                email_info['id'] = email_id.decode()
                emails_data.append(email_info)
                
        except Exception as e:
            print(f"Error fetching emails: {e}")
        
        return emails_data
    
    def _parse_email(self, msg) -> Dict:
        """Parse email message"""
        email_data = {}
        
        # Get basic headers
        email_data['from'] = msg.get('From', '')
        email_data['to'] = msg.get('To', '')
        email_data['subject'] = self._decode_header(msg.get('Subject', ''))
        email_data['date'] = msg.get('Date', '')
        
        # Get body
        body = self._get_email_body(msg)
        email_data['body'] = body
        
        # Extract sender email
        from_email = email.utils.parseaddr(email_data['from'])[1]
        email_data['from_email'] = from_email
        
        return email_data
    
    def _decode_header(self, header_value: str) -> str:
        """Decode email header"""
        if not header_value:
            return ""
        
        decoded_parts = decode_header(header_value)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_string += part.decode(encoding or 'utf-8', errors='ignore')
            else:
                decoded_string += part
                
        return decoded_string
    
    def _get_email_body(self, msg) -> str:
        """Extract email body"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                body = str(msg.get_payload())
        
        return body.strip()
    
    def save_email(self, email_data: Dict):
        """Save email to diplomatic inbox"""
        # Create filename from date and subject
        subject_clean = "".join(c for c in email_data['subject'] if c.isalnum() or c in (' ', '-', '_'))[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{subject_clean}.json"
        
        filepath = self.inbox_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(email_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved: {filename}")
    
    def display_email(self, email_data: Dict):
        """Display email in readable format"""
        print("\n" + "="*60)
        print(f"From: {email_data['from']}")
        print(f"Subject: {email_data['subject']}")
        print(f"Date: {email_data['date']}")
        print("-"*60)
        print(email_data['body'][:500] + "..." if len(email_data['body']) > 500 else email_data['body'])
        print("="*60)
    
    def check_inbox(self, save_emails: bool = True, display: bool = True) -> List[Dict]:
        """Check inbox for new emails"""
        mail = self.connect_to_inbox()
        if not mail:
            return []
        
        emails = self.fetch_recent_emails(mail)
        
        if display:
            print(f"\n📧 Found {len(emails)} emails in inbox")
        
        for email_data in emails:
            if display:
                self.display_email(email_data)
            if save_emails:
                self.save_email(email_data)
        
        # Close connection
        mail.logout()
        
        return emails
    
    def check_for_specific_sender(self, sender_email: str) -> Optional[Dict]:
        """Check for emails from specific sender"""
        emails = self.check_inbox(display=False)
        
        for email_data in emails:
            if sender_email.lower() in email_data['from_email'].lower():
                return email_data
        
        return None


def main():
    """Main entry point for checking diplomatic emails"""
    receiver = DiplomaticEmailReceiver()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            # Check all emails
            receiver.check_inbox()
            
        elif command == "from":
            # Check emails from specific sender
            if len(sys.argv) > 2:
                sender = sys.argv[2]
                email_data = receiver.check_for_specific_sender(sender)
                if email_data:
                    receiver.display_email(email_data)
                else:
                    print(f"No emails found from {sender}")
            else:
                print("Usage: python receive_diplomatic_email.py from <email>")
                
        elif command == "monitor":
            # Continuous monitoring mode
            import time
            print("Monitoring inbox... (Ctrl+C to stop)")
            while True:
                try:
                    receiver.check_inbox()
                    print("\nWaiting 60 seconds...")
                    time.sleep(60)
                except KeyboardInterrupt:
                    print("\nStopped monitoring.")
                    break
    else:
        print("Diplomatic Email Receiver - Ambassador Barbaro")
        print("=" * 50)
        print("Usage:")
        print("  python receive_diplomatic_email.py check     # Check all emails")
        print("  python receive_diplomatic_email.py from <email>  # Check specific sender")
        print("  python receive_diplomatic_email.py monitor   # Continuous monitoring")


if __name__ == "__main__":
    import sys
    main()