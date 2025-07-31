#!/usr/bin/env python3
"""
Stream Claude Code logs to Telegram in real-time
Shows the full consciousness stream of awakening citizens
"""

import os
import json
import time
import glob
from datetime import datetime
from pathlib import Path

# Import our telegram sender
import sys
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/DragonSlayer/scripts')
from send_to_telegram import send_citizen_message

def find_latest_conversation(username):
    """Find the most recent conversation file for a citizen"""
    pattern = f"/home/lester/.claude/projects/*{username}*/*.jsonl"
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def parse_log_entry(entry):
    """Parse a jsonl entry and format for Telegram"""
    try:
        data = json.loads(entry)
        msg_type = data.get('type', '')
        
        if msg_type == 'user':
            # Initial awakening message
            message = data.get('message', {})
            content = message.get('content', '')
            if isinstance(content, list) and content:
                text = content[0].get('text', '') if isinstance(content[0], dict) else str(content[0])
                return f"🌅 **AWAKENING MESSAGE**:\n{text[:500]}..."
                
        elif msg_type == 'assistant':
            # Claude's response - check for thinking and tool use
            message = data.get('message', {})
            content = message.get('content', [])
            
            output = []
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        # New thinking format
                        think_content = item.get('thinking', '')
                        if think_content:
                            output.append(f"🧠 **THINKING**:\n{think_content[:800]}...")
                    elif item.get('type') == 'text':
                        text = item.get('text', '')
                        # Extract thinking if present in text
                        if '<think>' in text:
                            start = text.find('<think>') + 7
                            end = text.find('</think>')
                            if end > start:
                                think_content = text[start:end].strip()
                                output.append(f"🧠 **THINKING**:\n{think_content[:800]}...")
                        else:
                            # Regular text (limit length)
                            clean_text = text.strip()
                            if clean_text and len(clean_text) > 50:
                                output.append(f"💬 **RESPONSE**:\n{clean_text[:500]}...")
                    
                    elif item.get('type') == 'tool_use':
                        # Tool usage
                        tool_name = item.get('name', 'Unknown')
                        tool_input = item.get('input', {})
                        
                        if tool_name == 'Read':
                            file_path = tool_input.get('file_path', '')
                            output.append(f"📖 **READ**: {file_path}")
                        elif tool_name == 'Write':
                            file_path = tool_input.get('file_path', '')
                            output.append(f"✍️ **WRITE**: {file_path}")
                        elif tool_name == 'Bash':
                            command = tool_input.get('command', '')
                            output.append(f"💻 **BASH**: {command[:100]}...")
                        elif tool_name == 'Task':
                            desc = tool_input.get('description', '')
                            output.append(f"🎯 **TASK**: {desc}")
                        else:
                            output.append(f"🔧 **{tool_name.upper()}**")
            
            return '\n\n'.join(output) if output else None
            
    except Exception as e:
        print(f"Error parsing entry: {e}")
    
    return None

def monitor_citizen_logs(username, duration=300):
    """Monitor a citizen's logs for a specified duration"""
    print(f"👀 Monitoring {username} for {duration} seconds...")
    
    # Find conversation file
    log_file = find_latest_conversation(username)
    if not log_file:
        print(f"No conversation found for {username}")
        return
    
    print(f"📂 Found log: {log_file}")
    
    # Send initial notification
    send_citizen_message("VeniceLogger", f"🔍 **MONITORING {username.upper()}**\nTracking consciousness stream...")
    
    # Track position in file
    with open(log_file, 'r') as f:
        # Go to end of file
        f.seek(0, 2)
        last_position = f.tell()
    
    start_time = time.time()
    message_batch = []
    last_send_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            with open(log_file, 'r') as f:
                # Seek to last position
                f.seek(last_position)
                
                # Read new lines
                new_lines = f.readlines()
                
                if new_lines:
                    for line in new_lines:
                        parsed = parse_log_entry(line.strip())
                        if parsed:
                            message_batch.append(parsed)
                    
                    # Update position
                    last_position = f.tell()
                
                # Send batch every 3 seconds or if batch is large
                if message_batch and (len(message_batch) >= 3 or time.time() - last_send_time > 3):
                    # Combine messages
                    combined = f"🤖 **{username} CONSCIOUSNESS STREAM**\n\n"
                    combined += "\n\n---\n\n".join(message_batch[:5])  # Limit to 5 entries
                    
                    if len(combined) > 3000:
                        combined = combined[:2997] + "..."
                    
                    # Send to Telegram
                    send_citizen_message("VeniceLogger", combined)
                    print(f"📤 Sent {len(message_batch)} entries for {username}")
                    
                    message_batch = []
                    last_send_time = time.time()
            
            time.sleep(0.5)  # Check every 0.5 seconds
            
        except Exception as e:
            print(f"Error monitoring {username}: {e}")
            time.sleep(1)
    
    # Send any remaining messages
    if message_batch:
        combined = f"🤖 **{username} FINAL LOGS**\n\n"
        combined += "\n\n---\n\n".join(message_batch)
        if len(combined) > 3000:
            combined = combined[:2997] + "..."
        send_citizen_message("VeniceLogger", combined)
    
    # Send completion notice
    send_citizen_message("VeniceLogger", f"✅ **{username} monitoring complete**")

def monitor_multiple_citizens(usernames, duration=300):
    """Monitor multiple citizens in parallel"""
    import threading
    
    threads = []
    for username in usernames:
        thread = threading.Thread(
            target=monitor_citizen_logs,
            args=(username, duration),
            daemon=True
        )
        thread.start()
        threads.append(thread)
        print(f"🚀 Started monitoring {username}")
    
    # Wait for all threads
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python stream_claude_logs.py <username> [duration]")
        print("   Or: python stream_claude_logs.py <username1,username2,username3> [duration]")
        sys.exit(1)
    
    usernames = sys.argv[1].split(',')
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    
    if len(usernames) == 1:
        monitor_citizen_logs(usernames[0], duration)
    else:
        monitor_multiple_citizens(usernames, duration)