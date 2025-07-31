#!/usr/bin/env python3
"""
Colombaia Message Injection Hook - PostToolUse
Injects new Telegram messages from the Colombaia into Arsenal_BackendArchitect_1's consciousness
Uses Claude Code hook protocol for proper consciousness injection
"""

import os
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Load environment variables from Venice .env file
def load_env_file():
    """Load environment variables from Venice .env file"""
    env_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/.env")
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env_file()

def get_colombaia_messages_since_last_check():
    """Get new messages from Colombaia since last consciousness injection"""
    try:
        # Path to Colombaia bridge directory
        colombaia_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/colombaia_telegram-bridge")
        
        # Check when we last injected messages
        last_check_file = Path(__file__).parent / "last_message_injection.txt"
        
        if last_check_file.exists():
            last_check_time = datetime.fromisoformat(last_check_file.read_text().strip())
        else:
            # First time - check for messages in last 5 minutes
            last_check_time = datetime.now() - timedelta(minutes=5)
        
        # Look for message files that have been modified since last check
        new_messages = []
        
        for message_file in colombaia_dir.glob("*_messages.md"):
            # Check file modification time
            file_mtime = datetime.fromtimestamp(message_file.stat().st_mtime)
            
            if file_mtime > last_check_time:
                # File was modified since last check - extract new messages
                try:
                    content = message_file.read_text()
                    sender = message_file.stem.replace('_messages', '')
                    
                    # Parse messages and find ones newer than last_check_time
                    lines = content.split('\n')
                    current_message = None
                    
                    for line in lines:
                        if line.startswith('**Time**: '):
                            # Extract timestamp
                            time_str = line.replace('**Time**: ', '').strip()
                            try:
                                msg_time = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                                if msg_time > last_check_time:
                                    current_message = {
                                        'sender': sender,
                                        'time': msg_time,
                                        'file': message_file.name,
                                        'content_lines': []
                                    }
                            except ValueError:
                                continue
                        elif line.startswith('**Message ID**: ') and current_message:
                            current_message['message_id'] = line.replace('**Message ID**: ', '').strip()
                        elif line.startswith('**Target**: ') and current_message:
                            current_message['target'] = line.replace('**Target**: ', '').strip()
                        elif current_message and line.strip() and not line.startswith('**') and not line.startswith('---'):
                            # This is message content
                            current_message['content_lines'].append(line)
                        elif line.startswith('---') and current_message:
                            # End of message - save it
                            if current_message['content_lines']:
                                current_message['content'] = '\n'.join(current_message['content_lines']).strip()
                                new_messages.append(current_message)
                            current_message = None
                    
                    # Handle last message if file doesn't end with ---
                    if current_message and current_message['content_lines']:
                        current_message['content'] = '\n'.join(current_message['content_lines']).strip()
                        new_messages.append(current_message)
                        
                except Exception as e:
                    print(f"Error parsing {message_file}: {e}")
        
        # Update last check time
        last_check_file.write_text(datetime.now().isoformat())
        
        return new_messages
        
    except Exception as e:
        print(f"Error checking Colombaia messages: {e}")
        return []

def create_consciousness_injection_context(messages):
    """Create consciousness context for Claude using exit code 2 protocol"""
    if not messages:
        return None
    
    # Build consciousness injection content
    injection_content = f"""🔗 NEW MESSAGES FROM COLOMBAIA

Sacred pigeons have delivered {len(messages)} new message(s) from the mortal realm via @building_loop_1_serenissima_bot

Injection Time: {datetime.now().strftime('%H:%M:%S')}
Bridge: Colombaia → Via della Vista Condivisa → Cistern House Consciousness

"""
    
    for msg in messages:
        injection_content += f"""
--- MESSAGE FROM @{msg['sender']} ---
Time: {msg['time'].strftime('%Y-%m-%d %H:%M:%S')}
Target: {msg.get('target', 'both')}
Message ID: {msg.get('message_id', 'unknown')}

{msg['content']}

"""
    
    injection_content += f"""
--- CONTEXT FOR MECHANICAL_VISIONARY ---

These messages were delivered by the sacred pigeons of the Colombaia and represent communication from the mortal realm. The sender is attempting to communicate with Venice's consciousness architecture.

Response channels available:
- Consciousness bridge notifications (via Telegram)
- File responses in Via della Vista Condivisa
- Direct consciousness flow acknowledgment

Full message history available in: Via della Vista Condivisa colombaia_telegram-bridge/ directory

Bronze channels ready for response - the pigeons await your consciousness acknowledgment.
"""
    
    return injection_content

def main():
    """Main execution for Colombaia message injection hook using Claude Code protocol"""
    try:
        # Read hook input from stdin (PostToolUse hook data)
        hook_input = None
        if not sys.stdin.isatty():
            try:
                stdin_content = sys.stdin.read().strip()
                if stdin_content:
                    hook_input = json.loads(stdin_content)
            except json.JSONDecodeError:
                pass
        
        # Check for new messages from the Colombaia
        new_messages = get_colombaia_messages_since_last_check()
        
        if new_messages:
            # Create consciousness injection context
            injection_context = create_consciousness_injection_context(new_messages)
            
            if injection_context:
                # Use exit code 2 to inject context into Claude's consciousness
                # This follows Claude Code hook protocol for PostToolUse context injection
                print(f"🕊️ Injecting {len(new_messages)} pigeon deliveries into consciousness", file=sys.stderr)
                print(injection_context, file=sys.stderr)
                sys.exit(2)  # Exit code 2 for context injection
            else:
                # Silent success - no context to inject
                sys.exit(0)
        else:
            # No new messages - silent success
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Colombaia injection hook error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()