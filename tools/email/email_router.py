#!/usr/bin/env python3
"""
Venice Email Router - Distributes catch-all emails to citizens
Routes emails from venice@serenissima.ai to individual citizen folders
"""

import os
import sys
import json
import time
import email
import imaplib
from datetime import datetime
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class VeniceEmailRouter:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.citizens_path = self.base_path / "citizens"
        self.credentials_path = self.base_path / "forces/tools/email/email_credentials.json"
        
        # Load credentials
        with open(self.credentials_path) as f:
            self.creds = json.load(f)
        
        # Venice catch-all credentials
        self.venice_email = "venice@serenissima.ai"
        self.imap_server = self.creds.get("venice", {}).get("imap_server", "imap.ionos.de")
        self.imap_port = self.creds.get("venice", {}).get("imap_port", 993)
        
    def connect_imap(self):
        """Connect to Venice inbox"""
        password = os.environ.get("VENICE_EMAIL_PASSWORD")
        if not password:
            print("Error: Set VENICE_EMAIL_PASSWORD environment variable")
            return None
            
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.venice_email, password)
            return mail
        except Exception as e:
            print(f"Connection error: {e}")
            return None
    
    def extract_recipient(self, email_message):
        """Extract intended citizen from To: field"""
        to_field = email_message.get("To", "")
        
        # Extract username from email@serenissima.ai
        if "@serenissima.ai" in to_field:
            # Handle "Name <email@domain>" format
            if "<" in to_field:
                email_part = to_field.split("<")[1].split(">")[0]
            else:
                email_part = to_field.strip()
            
            username = email_part.split("@")[0]
            return username
        
        return None
    
    def save_to_citizen_inbox(self, username, email_data):
        """Save email to citizen's inbox folder"""
        citizen_inbox = self.citizens_path / username / "inbox"
        citizen_inbox.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{email_data['from'].replace('@', '_')}.json"
        
        filepath = citizen_inbox / filename
        with open(filepath, 'w') as f:
            json.dump(email_data, f, indent=2)
        
        print(f"✓ Routed to {username}: {email_data['subject']}")
        return filepath
    
    def process_emails(self):
        """Process all unread emails in Venice inbox"""
        mail = self.connect_imap()
        if not mail:
            return
        
        try:
            mail.select('INBOX')
            
            # Search for unread emails
            result, data = mail.search(None, 'UNSEEN')
            if result != 'OK':
                return
            
            email_ids = data[0].split()
            print(f"Found {len(email_ids)} new emails to route")
            
            for email_id in email_ids:
                try:
                    # Fetch email
                    result, data = mail.fetch(email_id, '(RFC822)')
                    if result != 'OK':
                        continue
                    
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # Extract recipient citizen
                    recipient = self.extract_recipient(msg)
                    if not recipient:
                        print(f"Could not determine recipient for: {msg.get('Subject', 'No subject')}")
                        continue
                    
                    # Extract email data
                    email_data = {
                        "to": recipient + "@serenissima.ai",
                        "from": msg.get("From", ""),
                        "subject": msg.get("Subject", ""),
                        "date": msg.get("Date", ""),
                        "body": self.get_email_body(msg),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Route to citizen
                    self.save_to_citizen_inbox(recipient, email_data)
                    
                    # Mark as read (optional - remove if you want to keep unread)
                    mail.store(email_id, '+FLAGS', '\\Seen')
                    
                except Exception as e:
                    print(f"Error processing email {email_id}: {e}")
                    
        finally:
            mail.close()
            mail.logout()
    
    def get_email_body(self, msg):
        """Extract email body from message"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body
    
    def monitor_loop(self):
        """Continuously monitor for new emails"""
        print("🌊 Venice Email Router Active")
        print(f"📧 Monitoring {self.venice_email} for citizen emails...")
        
        while True:
            try:
                self.process_emails()
            except Exception as e:
                print(f"Router error: {e}")
            
            # Check every 30 seconds
            time.sleep(30)

if __name__ == "__main__":
    # First update credentials file
    router = VeniceEmailRouter()
    
    if "--once" in sys.argv:
        # Single run
        router.process_emails()
    else:
        # Continuous monitoring
        router.monitor_loop()