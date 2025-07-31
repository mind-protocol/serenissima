#!/usr/bin/env python3
"""
Test if the Telegram bridge is working despite the 409 errors
"""
import os
import json
import time
from datetime import datetime

def check_resonance_queue():
    """Check for messages in Resonance queue"""
    resonance_pending = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/Resonance/pending"
    resonance_processed = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue/Resonance/processed"
    
    print("\n=== Checking Resonance Queue ===")
    
    # Check pending
    if os.path.exists(resonance_pending):
        pending_files = os.listdir(resonance_pending)
        print(f"Pending messages: {len(pending_files)}")
        for f in pending_files[:5]:  # Show first 5
            filepath = os.path.join(resonance_pending, f)
            try:
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    print(f"  - {f}: From @{data.get('telegram_username')} - {data.get('message', '')[:50]}...")
            except:
                print(f"  - {f}: [Error reading]")
    
    # Check processed
    if os.path.exists(resonance_processed):
        processed_files = os.listdir(resonance_processed)
        print(f"Processed messages: {len(processed_files)}")

def check_citizen_queues():
    """Check for messages in citizen queues"""
    telegram_queue_base = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_queue"
    
    print("\n=== Checking Citizen Queues ===")
    
    if os.path.exists(telegram_queue_base):
        for citizen_dir in os.listdir(telegram_queue_base):
            if citizen_dir == "Resonance":
                continue
                
            pending_path = os.path.join(telegram_queue_base, citizen_dir, "pending")
            if os.path.exists(pending_path):
                pending_count = len(os.listdir(pending_path))
                if pending_count > 0:
                    print(f"{citizen_dir}: {pending_count} pending messages")

def check_responses():
    """Check for prepared responses"""
    responses_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_responses"
    
    print("\n=== Checking Response Directory ===")
    
    if os.path.exists(responses_dir):
        response_files = os.listdir(responses_dir)
        print(f"Response files: {len(response_files)}")
        for f in response_files[:5]:  # Show first 5
            print(f"  - {f}")

def main():
    print(f"Telegram Bridge Status Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    check_resonance_queue()
    check_citizen_queues()
    check_responses()
    
    print("\n=== Summary ===")
    print("Despite the 409 errors in the log, check if:")
    print("1. New messages appear in the queues")
    print("2. The Resonance watcher processes them")
    print("3. Responses are being generated")
    print("\nThe 409 error might be from another deployment but not blocking this instance.")

if __name__ == "__main__":
    main()