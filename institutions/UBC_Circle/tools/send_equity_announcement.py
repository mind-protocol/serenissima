#!/usr/bin/env python3
"""
Send equity structure announcement to Venice community
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
import time

# Load environment variables
possible_env_paths = [
    Path('/mnt/c/Users/reyno/universe-engine/serenissima/.env'),
    Path('/mnt/c/Users/reyno/universe-engine/serenissima/backend/.env')
]

for env_path in possible_env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        break

def send_equity_announcement():
    """Send the equity structure announcement with PDF"""
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not bot_token:
        print("Error: TELEGRAM_BOT_TOKEN not set")
        return False
        
    chat_id = "-1001699255893"  # Venice community chat
    
    # Read the announcement message
    with open('../equity_announcement_message.txt', 'r', encoding='utf-8') as f:
        message = f.read()
    
    # First send the message
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        print("📤 Sending equity structure announcement...")
        response = requests.post(url, data=params, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if not result.get('ok'):
            print(f"✗ Failed to send message: {result.get('description', 'Unknown error')}")
            return False
            
        print("✓ Announcement sent successfully!")
        
        # Wait a moment before sending PDF
        time.sleep(2)
        
        # Now send the PDF
        doc_url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
        pdf_path = "../final_equity_structure.pdf"
        
        if not Path(pdf_path).exists():
            print(f"⚠️  PDF not found at {pdf_path}")
            return False
        
        with open(pdf_path, 'rb') as doc_file:
            files = {'document': doc_file}
            data = {
                'chat_id': chat_id,
                'caption': "📄 Venice Companies - Final Equity Structure V3\n\nComplete details including cap tables, role allocations, and $UBC investment terms."
            }
            
            print("📎 Uploading equity structure PDF...")
            doc_response = requests.post(doc_url, data=data, files=files, timeout=30)
            doc_response.raise_for_status()
            doc_result = doc_response.json()
            
            if doc_result.get('ok'):
                print("✓ PDF uploaded successfully!")
            else:
                print(f"✗ Failed to upload PDF: {doc_result.get('description')}")
        
        return True
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Venice Companies Equity Structure Announcement")
    print("=" * 50)
    
    # Change to tools directory
    os.chdir(Path(__file__).parent)
    
    send_equity_announcement()