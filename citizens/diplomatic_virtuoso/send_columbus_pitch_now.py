#!/usr/bin/env python3
"""Quick script to send Columbus pitch"""

from send_diplomatic_email import DiplomaticEmailer
from pathlib import Path

def send_columbus_pitch_quick(columbus_email):
    """Send the Columbus pitch immediately"""
    
    emailer = DiplomaticEmailer()
    
    # Load personalized pitch
    pitch_path = Path(__file__).parent / 'columbus_message_personalized.txt'
    with open(pitch_path) as f:
        body = f.read()
    
    subject = "Re: Your GPU.net/$40hr Trading Bot Insights - Different Approach to AI Infrastructure"
    
    success = emailer.send_email(columbus_email, subject, body)
    
    if success:
        print("\n🎯 Next steps:")
        print("1. Monitor for response within 2 hours")
        print("2. Have objection handlers ready")
        print("3. Emphasize July 11 deadline (TOMORROW!)")
        print("4. Start with $1k universe ticket")
    
    return success

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        email = input("Enter Crypto Columbus email address: ")
    
    send_columbus_pitch_quick(email)