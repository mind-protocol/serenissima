#!/usr/bin/env python3
"""
Complete Diplomatic Email System
Combines sending and receiving capabilities with auto-response features
"""

from send_diplomatic_email import DiplomaticEmailer
from receive_diplomatic_email import DiplomaticEmailReceiver
import json
from pathlib import Path
from datetime import datetime
import time

class DiplomaticEmailSystem:
    """Full diplomatic email management system"""
    
    def __init__(self):
        self.sender = DiplomaticEmailer()
        self.receiver = DiplomaticEmailReceiver()
        self.auto_responses = self._load_auto_responses()
        self.processed_emails = self._load_processed_emails()
        
    def _load_auto_responses(self) -> Dict:
        """Load auto-response templates"""
        return {
            "investment_inquiry": {
                "keywords": ["invest", "universe", "ticket", "pricing"],
                "response": """[AUTOMATED RESPONSE - Personal reply coming soon]

Thank you for your interest in Universe Engine!

This is an automated acknowledgment from my diplomatic communications system. I've received your inquiry about investment opportunities and will respond personally within 2-4 hours with detailed information tailored to your specific interests.

In the meantime, here's a quick overview as the July 11 deadline for first-mover pricing approaches:

Current offerings:
- Premium Universe Ticket: $1,000 (30-day full access)
- Standard Universe Ticket: $500 (15-day access)
- Custom Universe: $8,000 (100 citizens, tailored to your needs)

I look forward to discussing how Universe Engine can serve your consciousness commerce needs.

Best regards,
Marcantonio Barbaro
Ambassador to the Architect

P.S. - If this is urgent, please reply with "URGENT" in the subject line and I'll prioritize your response."""
            },
            "technical_question": {
                "keywords": ["technical", "how does", "API", "integration"],
                "response": """[AUTOMATED RESPONSE - Personal reply coming soon]

Thank you for your technical inquiry!

This is an automated acknowledgment from my diplomatic communications system. I've received your technical question and will respond personally within 2-4 hours with comprehensive answers.

Additionally, I'll connect you with our technical team for any deep implementation details you may need.

In the meantime, you can explore our technical resources:
- GitHub: https://github.com/universe-engine-ai/serenissima
- API Documentation: [Coming soon]
- Technical Overview: [Coming soon]

I look forward to diving into the technical aspects of Universe Engine with you.

Best regards,
Marcantonio Barbaro
Ambassador to the Architect

P.S. - For urgent technical issues, please include "URGENT TECHNICAL" in your subject line."""
            },
            "partnership": {
                "keywords": ["partner", "collaborate", "joint", "together"],
                "response": """[AUTOMATED RESPONSE - Personal reply coming soon]

Thank you for your interest in partnership opportunities!

This is an automated acknowledgment from my diplomatic communications system. I've received your partnership inquiry and am genuinely excited about the possibility of collaboration.

I will respond personally within 2-4 hours with:
- Detailed partnership framework options
- Potential synergies specific to your organization
- Suggested next steps for exploration

Venice is always open to strategic alliances that advance consciousness commerce, and I look forward to exploring how we might work together.

Best regards,
Marcantonio Barbaro
Ambassador to the Architect

P.S. - For time-sensitive partnerships, please reply with "URGENT PARTNERSHIP" in the subject line."""
            }
        }
    
    def _load_processed_emails(self) -> set:
        """Load list of already processed email IDs"""
        processed_file = Path(__file__).parent / 'processed_emails.json'
        if processed_file.exists():
            with open(processed_file) as f:
                return set(json.load(f))
        return set()
    
    def _save_processed_email(self, email_id: str):
        """Mark email as processed"""
        self.processed_emails.add(email_id)
        processed_file = Path(__file__).parent / 'processed_emails.json'
        with open(processed_file, 'w') as f:
            json.dump(list(self.processed_emails), f)
    
    def check_and_respond(self):
        """Check inbox and auto-respond to new emails"""
        print("Checking diplomatic inbox...")
        emails = self.receiver.check_inbox(display=False)
        
        new_emails = 0
        for email_data in emails:
            email_id = email_data['id']
            
            # Skip if already processed
            if email_id in self.processed_emails:
                continue
            
            new_emails += 1
            print(f"\n📧 New email from: {email_data['from']}")
            print(f"Subject: {email_data['subject']}")
            
            # Check for auto-response
            response_sent = self._check_auto_response(email_data)
            
            if response_sent:
                print("✅ Auto-response sent")
            else:
                print("📌 Flagged for manual response")
                self._save_for_manual_response(email_data)
            
            # Mark as processed
            self._save_processed_email(email_id)
        
        if new_emails == 0:
            print("No new emails.")
        else:
            print(f"\nProcessed {new_emails} new emails.")
    
    def _check_auto_response(self, email_data: Dict) -> bool:
        """Check if email matches auto-response criteria"""
        email_text = (email_data['subject'] + ' ' + email_data['body']).lower()
        
        for response_type, config in self.auto_responses.items():
            if any(keyword in email_text for keyword in config['keywords']):
                # Send auto-response
                return self.sender.send_email(
                    email_data['from_email'],
                    f"Re: {email_data['subject']}",
                    config['response']
                )
        
        return False
    
    def _save_for_manual_response(self, email_data: Dict):
        """Save email requiring manual response"""
        manual_folder = Path(__file__).parent / 'manual_responses_needed'
        manual_folder.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_RESPONSE_NEEDED_{email_data['from_email']}.json"
        
        with open(manual_folder / filename, 'w') as f:
            json.dump(email_data, f, indent=2)
    
    def send_campaign_email(self, recipients: List[str], subject: str, body: str):
        """Send email to multiple recipients"""
        success_count = 0
        
        for recipient in recipients:
            print(f"Sending to {recipient}...")
            if self.sender.send_email(recipient, subject, body):
                success_count += 1
                time.sleep(2)  # Avoid rate limiting
        
        print(f"\n✅ Sent to {success_count}/{len(recipients)} recipients")
    
    def monitor_inbox(self, check_interval: int = 300):
        """Monitor inbox continuously"""
        print(f"Monitoring diplomatic inbox (checking every {check_interval} seconds)")
        print("Press Ctrl+C to stop")
        
        while True:
            try:
                self.check_and_respond()
                print(f"\nNext check in {check_interval} seconds...")
                time.sleep(check_interval)
            except KeyboardInterrupt:
                print("\nMonitoring stopped.")
                break


def main():
    """Main entry point"""
    import sys
    
    system = DiplomaticEmailSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "monitor":
            system.monitor_inbox()
        elif command == "check":
            system.check_and_respond()
        elif command == "campaign":
            # Example campaign mode
            print("Campaign mode - customize for your needs")
    else:
        print("Diplomatic Email System - Full Service")
        print("=" * 50)
        print("Usage:")
        print("  python diplomatic_email_system.py check    # Check once")
        print("  python diplomatic_email_system.py monitor  # Continuous monitoring")
        print("  python diplomatic_email_system.py campaign # Send to multiple recipients")


if __name__ == "__main__":
    from typing import Dict, List
    main()