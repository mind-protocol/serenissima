#!/usr/bin/env python3
"""
Send investment pitch to Crypto Columbus
"""

import os
import sys
import requests
from pathlib import Path

def send_pitch_to_columbus(telegram_username="cryptocolombus"):
    """Send investment pitch via Telegram"""
    
    # Read the prepared message
    message_file = Path(__file__).parent / "columbus_telegram_message.txt"
    with open(message_file, 'r') as f:
        message = f.read()
    
    # Using NLR's bot or Universe Engine official bot
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN', '8159027121:AAHdzWfhIOABHY3fiyiOOblfS8Fuzq9IwR8')
    
    print(f"Message prepared for @{telegram_username}:")
    print("-" * 50)
    print(message)
    print("-" * 50)
    print("\nNote: This will need to be sent through the appropriate Telegram channel/DM")
    print("The message has been prepared and saved.")
    
    # Save formatted version for easy copying
    formatted_file = Path(__file__).parent / "columbus_pitch_formatted.txt"
    with open(formatted_file, 'w') as f:
        f.write(f"TO: @{telegram_username}\n")
        f.write(f"FROM: Marcantonio Barbaro (diplomatic_virtuoso)\n")
        f.write(f"RE: Universe Engine Investment Opportunity - Closes July 11\n")
        f.write("="*60 + "\n\n")
        f.write(message)
        f.write("\n\n" + "="*60)
        f.write("\n\nFollow-up responses prepared in: columbus_objection_handlers.md")
    
    print(f"\n✅ Formatted pitch saved to: {formatted_file}")
    print("\n📋 Next steps:")
    print("1. Send this message to Crypto Columbus")
    print("2. Be ready with objection handlers")
    print("3. Emphasize July 11 deadline (tomorrow!)")
    print("4. Start with $1k universe ticket as entry point")
    
    return True

if __name__ == "__main__":
    # Check if custom username provided
    username = sys.argv[1] if len(sys.argv) > 1 else "cryptocolombus"
    send_pitch_to_columbus(username)