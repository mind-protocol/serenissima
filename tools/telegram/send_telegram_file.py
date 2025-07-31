#!/usr/bin/env python3
"""
Send files via Telegram bot
Supports documents, images, and other file types
"""

import requests
import json
import sys
import os
import argparse
from pathlib import Path

def send_telegram_file(file_path, chat_id=None, bot_token=None, caption=None, filename=None):
    """Send a file via Telegram bot
    
    Args:
        file_path: Path to the file to send
        chat_id: Target chat ID (defaults to main TG group if not specified)
        bot_token: Bot token to use (defaults to serenissima_ubc_bot if not specified)
        caption: Optional caption for the file
        filename: Optional custom filename (defaults to actual filename)
    
    Returns:
        Response from Telegram API
    """
    
    # Load credentials
    creds_path = os.path.join(os.path.dirname(__file__), 'telegram_credentials.json')
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    # Use provided values or defaults
    bot_token = bot_token or creds['default_bot']['token']
    chat_id = chat_id or creds['main_group']['chat_id']
    
    # Determine file type and appropriate endpoint
    file_ext = Path(file_path).suffix.lower()
    
    # Choose appropriate method based on file type
    if file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
        method = 'sendPhoto'
        file_param = 'photo'
    elif file_ext in ['.pdf', '.doc', '.docx', '.txt', '.md', '.zip', '.json']:
        method = 'sendDocument'
        file_param = 'document'
    elif file_ext in ['.mp4', '.avi', '.mov', '.mkv']:
        method = 'sendVideo'
        file_param = 'video'
    elif file_ext in ['.mp3', '.wav', '.ogg', '.m4a']:
        method = 'sendAudio'
        file_param = 'audio'
    else:
        # Default to document for unknown types
        method = 'sendDocument'
        file_param = 'document'
    
    url = f"https://api.telegram.org/bot{bot_token}/{method}"
    
    # Prepare the file
    custom_filename = filename or os.path.basename(file_path)
    
    with open(file_path, 'rb') as f:
        files = {file_param: (custom_filename, f)}
        
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        
        response = requests.post(url, files=files, data=data)
    
    return response.json()

def send_multiple_files(file_paths, chat_id=None, bot_token=None, caption=None):
    """Send multiple files as a media group (for images/videos only)
    
    Args:
        file_paths: List of file paths to send
        chat_id: Target chat ID
        bot_token: Bot token to use
        caption: Caption for the media group
    
    Returns:
        Response from Telegram API
    """
    
    # Load credentials
    creds_path = os.path.join(os.path.dirname(__file__), 'telegram_credentials.json')
    with open(creds_path, 'r') as f:
        creds = json.load(f)
    
    bot_token = bot_token or creds['default_bot']['token']
    chat_id = chat_id or creds['main_group']['chat_id']
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMediaGroup"
    
    media = []
    files = {}
    
    for i, file_path in enumerate(file_paths):
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            media_type = 'photo'
        elif file_ext in ['.mp4', '.avi', '.mov']:
            media_type = 'video'
        else:
            print(f"Warning: {file_path} is not a photo/video, skipping for media group")
            continue
        
        attach_name = f"attach_{i}"
        media.append({
            'type': media_type,
            'media': f"attach://{attach_name}",
            'caption': caption if i == 0 else None  # Only first item gets caption
        })
        
        with open(file_path, 'rb') as f:
            files[attach_name] = f.read()
    
    data = {
        'chat_id': chat_id,
        'media': json.dumps(media)
    }
    
    # Convert files dict to proper format
    files_formatted = {k: (f"file_{k}", v) for k, v in files.items()}
    
    response = requests.post(url, data=data, files=files_formatted)
    return response.json()

def main():
    """CLI interface for sending files via Telegram"""
    parser = argparse.ArgumentParser(description='Send files via Telegram bot')
    parser.add_argument('file', help='File path to send')
    parser.add_argument('-c', '--caption', help='Caption for the file')
    parser.add_argument('-i', '--chat-id', help='Chat ID (defaults to main group)')
    parser.add_argument('-t', '--token', help='Bot token (defaults to serenissima_ubc_bot)')
    parser.add_argument('-n', '--filename', help='Custom filename for the upload')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    result = send_telegram_file(
        args.file,
        chat_id=args.chat_id,
        bot_token=args.token,
        caption=args.caption,
        filename=args.filename
    )
    
    if result.get('ok'):
        print(f"✅ File sent successfully!")
        print(f"Message ID: {result.get('result', {}).get('message_id', 'N/A')}")
    else:
        print(f"❌ Error sending file: {result.get('description', 'Unknown error')}")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()