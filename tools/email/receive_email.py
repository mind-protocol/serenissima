#!/usr/bin/env python3
"""
Generic Email Receiver for Venice Citizens
Can be used by any citizen with email credentials
"""

import os
import sys
import imaplib
import email
from email.header import decode_header
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

class EmailReceiver:
    """Generic email receiver for Venice citizens"""
    
    def __init__(self, citizen_name: str = None):
        self.credentials = self._load_credentials()
        self.citizen = citizen_name or self.credentials.get('default', 'diplomatic_virtuoso')
        self.config = self.credentials.get(self.citizen, {})
        self.inbox_path = Path(__file__).parent / f'{self.citizen}_inbox'
        self.inbox_path.mkdir(exist_ok=True)
        
    def _load_credentials(self) -> Dict:
        """Load email credentials"""
        creds_path = Path(__file__).parent / 'email_credentials.json'
        with open(creds_path, 'r') as f:
            return json.load(f)
    
    def connect_to_inbox(self) -> Optional[imaplib.IMAP4_SSL]:
        """Connect to email inbox"""
        try:
            print(f"Connecting to {self.config['imap_server']}...")
            
            # Create SSL connection
            mail = imaplib.IMAP4_SSL(self.config['imap_server'], self.config['imap_port'])
            
            # Get password from environment
            password_key = f"{self.citizen.upper()}_EMAIL_PASSWORD"
            password = os.environ.get(password_key, '')
            
            if not password:
                print(f"⚠️  No password found in environment variable {password_key}")
                return None
            
            # Login
            mail.login(self.config['email'], password)
            print("✅ Successfully connected to inbox")
            
            return mail
            
        except Exception as e:
            print(f"❌ Failed to connect: {str(e)}")
            return None
    
    def check_emails(self, folder: str = 'INBOX', limit: int = 10, search_from: str = None) -> List[Dict]:
        """Check emails with optional sender filter"""
        mail = self.connect_to_inbox()
        if not mail:
            return []
        
        try:
            # Select inbox
            mail.select(folder)
            
            # Build search criteria
            if search_from:
                search_criteria = f'(FROM "{search_from}")'
            else:
                search_criteria = 'ALL'
            
            # Search emails
            result, data = mail.search(None, search_criteria)
            
            if result != 'OK':
                print("❌ Failed to search emails")
                return []
            
            email_ids = data[0].split()
            total_emails = len(email_ids)
            
            # Get latest emails
            email_ids = email_ids[-limit:]
            
            print(f"\n📧 Found {total_emails} emails, fetching {len(email_ids)} most recent")
            
            emails = []
            
            for email_id in email_ids:
                result, msg_data = mail.fetch(email_id, '(RFC822)')
                
                if result != 'OK':
                    continue
                
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                
                # Extract email details
                subject = self._decode_header(msg['Subject'])
                from_addr = self._decode_header(msg['From'])
                date_str = msg['Date']
                
                # Get body
                body = self._get_email_body(msg)
                
                email_info = {
                    'id': email_id.decode(),
                    'from': from_addr,
                    'subject': subject,
                    'date': date_str,
                    'body': body[:500] + '...' if len(body) > 500 else body
                }
                
                emails.append(email_info)
                
                # Print summary
                print("\n" + "="*60)
                print(f"From: {from_addr}")
                print(f"Subject: {subject}")
                print(f"Date: {date_str}")
                print("-"*60)
                print(body[:300] + "..." if len(body) > 300 else body)
                
                # Save full email
                self._save_email(email_info, body)
            
            mail.close()
            mail.logout()
            
            return emails
            
        except Exception as e:
            print(f"❌ Error checking emails: {str(e)}")
            mail.logout()
            return []
    
    def _decode_header(self, header) -> str:
        """Decode email header"""
        if header is None:
            return ""
        
        decoded = decode_header(header)
        result = []
        
        for text, encoding in decoded:
            if isinstance(text, bytes):
                result.append(text.decode(encoding or 'utf-8', errors='ignore'))
            else:
                result.append(str(text))
        
        return ' '.join(result)
    
    def _get_email_body(self, msg) -> str:
        """Extract email body"""
        body = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    break
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return body
    
    def _save_email(self, email_info: Dict, full_body: str):
        """Save email to disk"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        subject_clean = email_info['subject'][:50].replace('/', '_').replace('\\', '_')
        filename = f"{timestamp}_{subject_clean}.json"
        
        email_info['full_body'] = full_body
        
        filepath = self.inbox_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(email_info, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved: {filename}")

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Venice Email Receiver")
        print("=" * 50)
        print("Usage:")
        print("  python receive_email.py check [citizen]    # Check all emails")
        print("  python receive_email.py from <email> [citizen]  # Check from specific sender")
        print("")
        print("Example:")
        print("  python receive_email.py check diplomatic_virtuoso")
        print("  python receive_email.py from linkedin.com")
        return
    
    command = sys.argv[1]
    
    if command == "check":
        citizen = sys.argv[2] if len(sys.argv) > 2 else None
        receiver = EmailReceiver(citizen)
        receiver.check_emails()
    
    elif command == "from":
        if len(sys.argv) < 3:
            print("❌ Please specify sender email/domain")
            return
        search_from = sys.argv[2]
        citizen = sys.argv[3] if len(sys.argv) > 3 else None
        receiver = EmailReceiver(citizen)
        receiver.check_emails(search_from=search_from)

if __name__ == "__main__":
    main()