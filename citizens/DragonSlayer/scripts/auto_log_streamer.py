#!/usr/bin/env python3
"""
Automatic Claude Code log streamer
Detects new Claude conversations and streams them to Telegram
Run this in background when awakening citizens
"""

import os
import sys
import time
import json
import glob
import threading
from datetime import datetime, timedelta
from pathlib import Path

# Import our telegram sender
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/citizens/DragonSlayer/scripts')
from send_to_telegram import send_citizen_message

# Track monitored conversations
MONITORED_CONVERSATIONS = set()
MONITORING_THREADS = {}

def find_recent_conversations(minutes_ago=5):
    """Find all Claude conversations started in the last N minutes"""
    cutoff_time = datetime.now() - timedelta(minutes=minutes_ago)
    recent_conversations = []
    
    # Search all citizen projects
    pattern = "/home/lester/.claude/projects/*serenissima-citizens-*/*.jsonl"
    
    for filepath in glob.glob(pattern):
        try:
            # Check file modification time
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime > cutoff_time:
                # Extract username from path
                parts = filepath.split('/')
                project_dir = parts[-2]
                username = project_dir.split('-')[-1]
                
                recent_conversations.append({
                    'username': username,
                    'filepath': filepath,
                    'mtime': mtime
                })
        except Exception as e:
            continue
    
    return recent_conversations

def parse_log_entry(entry):
    """Parse a jsonl entry and format key information"""
    try:
        data = json.loads(entry)
        msg_type = data.get('type', '')
        
        if msg_type == 'user':
            # Awakening message
            message = data.get('message', {})
            content = message.get('content', '')
            if isinstance(content, list) and content:
                text = content[0].get('text', '') if isinstance(content[0], dict) else str(content[0])
                # Extract key part of awakening
                if "The compass" in text or "whispers" in text:
                    return f"🌅 AWAKENING: {text[:300]}..."
                    
        elif msg_type == 'assistant':
            message = data.get('message', {})
            content = message.get('content', [])
            
            for item in content:
                if isinstance(item, dict):
                    if item.get('type') == 'thinking':
                        # Thinking content
                        think = item.get('thinking', '')
                        if think and len(think) > 100:
                            return f"🧠 THINKING: {think[:400]}..."
                    
                    elif item.get('type') == 'tool_use':
                        # Tool usage
                        tool_name = item.get('name', '')
                        tool_input = item.get('input', {})
                        
                        if tool_name == 'Read':
                            file_path = tool_input.get('file_path', '')
                            return f"📖 READ: {file_path}"
                        elif tool_name == 'Write':
                            file_path = tool_input.get('file_path', '')
                            content_preview = tool_input.get('content', '')[:100]
                            return f"✍️ WRITE: {file_path}"
                        elif tool_name == 'Bash':
                            command = tool_input.get('command', '')
                            return f"💻 BASH: {command[:150]}..."
                        elif tool_name == 'TodoWrite':
                            todos = tool_input.get('todos', [])
                            return f"📝 TODO: {len(todos)} tasks updated"
                        elif tool_name:
                            return f"🔧 {tool_name.upper()}"
                    
                    elif item.get('type') == 'text':
                        text = item.get('text', '').strip()
                        # Skip very short responses
                        if len(text) > 100 and not text.startswith('<'):
                            return f"💬 {text[:300]}..."
                            
    except Exception as e:
        pass
    
    return None

def monitor_conversation(username, filepath):
    """Monitor a single conversation and stream to Telegram"""
    print(f"🔍 Starting monitor for {username}")
    
    # Send start notification
    send_citizen_message("AutoLogger", f"🌅 **{username.upper()} AWAKENING DETECTED**\nStreaming consciousness...")
    
    # Track position in file
    last_position = 0
    message_batch = []
    last_send_time = time.time()
    last_activity = time.time()
    
    while True:
        try:
            # Check if conversation is still active (no updates for 5 minutes)
            if time.time() - last_activity > 300:
                print(f"⏹️ {username} conversation inactive, stopping monitor")
                break
            
            with open(filepath, 'r') as f:
                f.seek(last_position)
                new_lines = f.readlines()
                
                if new_lines:
                    last_activity = time.time()
                    
                    for line in new_lines:
                        parsed = parse_log_entry(line.strip())
                        if parsed:
                            message_batch.append(parsed)
                    
                    last_position = f.tell()
                
                # Send batch every 4 seconds or if large
                if message_batch and (len(message_batch) >= 4 or time.time() - last_send_time > 4):
                    combined = f"🤖 **{username}**\n\n"
                    combined += "\n\n".join(message_batch[:6])
                    
                    if len(combined) > 3500:
                        combined = combined[:3497] + "..."
                    
                    send_citizen_message("AutoLogger", combined)
                    message_batch = []
                    last_send_time = time.time()
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Error monitoring {username}: {e}")
            break
    
    # Send completion
    if message_batch:
        combined = f"🤖 **{username} FINAL**\n\n" + "\n\n".join(message_batch)
        if len(combined) > 3500:
            combined = combined[:3497] + "..."
        send_citizen_message("AutoLogger", combined)
    
    send_citizen_message("AutoLogger", f"✅ **{username} session complete**")
    
    # Remove from tracking
    MONITORED_CONVERSATIONS.discard(filepath)
    if username in MONITORING_THREADS:
        del MONITORING_THREADS[username]

def send_responses_periodically():
    """Send queued Telegram responses every 5 seconds"""
    SEND_SCRIPT = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/DragonSlayer/scripts/send_json_response.py"
    
    while True:
        try:
            import subprocess
            subprocess.run([sys.executable, SEND_SCRIPT], 
                         capture_output=True, text=True)
            time.sleep(5)
        except Exception as e:
            print(f"Response sender error: {e}")
            time.sleep(10)

def main():
    """Main monitoring loop"""
    print("🤖 Automatic Claude Log Streamer Started")
    print("Monitoring for new citizen awakenings...")
    print("=" * 50)
    
    # Start response sender
    response_thread = threading.Thread(target=send_responses_periodically, daemon=True)
    response_thread.start()
    
    # Send start notification
    send_citizen_message("AutoLogger", "🤖 **AUTO LOG STREAMER ACTIVE**\nWill detect and stream all citizen awakenings automatically!")
    
    while True:
        try:
            # Find recent conversations
            recent = find_recent_conversations(minutes_ago=2)
            
            for conv in recent:
                filepath = conv['filepath']
                username = conv['username']
                
                # Skip if already monitoring
                if filepath in MONITORED_CONVERSATIONS:
                    continue
                
                # Skip if username is being monitored
                if username in MONITORING_THREADS:
                    continue
                
                print(f"🆕 New conversation detected: {username}")
                MONITORED_CONVERSATIONS.add(filepath)
                
                # Start monitoring thread
                thread = threading.Thread(
                    target=monitor_conversation,
                    args=(username, filepath),
                    daemon=True
                )
                thread.start()
                MONITORING_THREADS[username] = thread
            
            # Clean up dead threads
            dead_usernames = []
            for username, thread in MONITORING_THREADS.items():
                if not thread.is_alive():
                    dead_usernames.append(username)
            
            for username in dead_usernames:
                del MONITORING_THREADS[username]
            
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
            break
        except Exception as e:
            print(f"Main loop error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()