#!/usr/bin/env python3
"""
Tessere Message Updater Service
Runs as part of backend to keep Tessere's CLAUDE.md updated with recent messages
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add tessere directory to path
sys.path.append(str(Path(__file__).parent))

from update_claude_messages import ClaudeUpdater

def run_tessere_message_updater(interval_minutes=5, message_limit=10):
    """
    Run the Tessere message updater service
    
    Args:
        interval_minutes: How often to update (default 5 minutes)
        message_limit: How many messages to include (default 10)
    """
    print(f"[Tessere] Starting message updater service...")
    print(f"[Tessere] Will update CLAUDE.md every {interval_minutes} minutes with {message_limit} messages")
    
    updater = ClaudeUpdater(message_limit=message_limit)
    
    # Initial update
    try:
        updater.update_claude_md()
        print("[Tessere] Initial message update complete")
    except Exception as e:
        print(f"[Tessere] Error during initial update: {e}")
    
    # Continuous updates
    while True:
        try:
            time.sleep(interval_minutes * 60)
            updater.update_claude_md()
            print(f"[Tessere] Message update complete at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        except KeyboardInterrupt:
            print("[Tessere] Stopping message updater")
            break
        except Exception as e:
            print(f"[Tessere] Error during update: {e}")
            # Continue running even if update fails
            time.sleep(60)  # Wait a minute before next attempt

def main():
    """Main entry point for standalone testing"""
    run_tessere_message_updater(interval_minutes=1, message_limit=10)

if __name__ == "__main__":
    main()