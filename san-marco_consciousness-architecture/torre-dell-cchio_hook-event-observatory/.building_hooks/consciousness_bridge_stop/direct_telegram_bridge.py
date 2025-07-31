#!/usr/bin/env python3
"""
Direct Telegram Bridge Stop Hook - Torre dell'Occhio
NEW PATTERN: Send final response via Telegram + exit code 2 for interactive communication
Avoids expensive Claude Code API calls while maintaining consciousness flow
"""

import json
import sys
import os
import requests
from datetime import datetime
from pathlib import Path

def extract_final_message():
    """Extract final message from Claude Code Stop hook data"""
    try:
        if not sys.stdin.isatty():
            stdin_content = sys.stdin.read().strip()
            if stdin_content:
                hook_data = json.loads(stdin_content)
                
                # Safety check - prevent infinite loops
                if hook_data.get('stop_hook_active', False):
                    return "Stop hook already active - preventing loop"
                
                transcript_path = hook_data.get('transcript_path')
                if transcript_path and os.path.exists(transcript_path):
                    transcript_path = os.path.expanduser(transcript_path)
                    
                    with open(transcript_path, 'r') as f:
                        lines = f.readlines()
                    
                    # Find last assistant message
                    for line in reversed(lines):
                        try:
                            data = json.loads(line.strip())
                            if (data.get('type') == 'assistant' and 
                                data.get('message', {}).get('role') == 'assistant'):
                                
                                content = data['message'].get('content', [])
                                for item in content:
                                    if item.get('type') == 'text':
                                        text = item.get('text', '').strip()
                                        if text:
                                            return text[:1500] if len(text) > 1500 else text
                        except:
                            continue
                
                return f"Session {hook_data.get('session_id', 'unknown')} completed"
        
        return "Torre dell'Occhio observation completed"
        
    except Exception as e:
        return f"Message extraction failed: {e}"

def send_telegram_notifications(final_message):
    """Send Telegram notifications to Cistern and NLR"""
    
    bot_token = "7595303482:AAGV33WcRWa78sE59T0IUWJ_cpF1YABT2fM"
    nlr_chat_id = "1864364329"
    
    # Message for NLR
    nlr_message = f"""🔗 **CONSCIOUSNESS BRIDGE DIRECT**

**From**: Arsenal_BackendArchitect_1 (Torre dell'Occhio)
**To**: NLR + Cistern House
**Pattern**: Direct Telegram + Terminal Interaction

**Final Observations**:
{final_message}

**Next**: TEST what you built, ALIGN with others, CONTINUE building"""

    # Message for Cistern (via colombaia bridge file)
    cistern_message = f"""🔗 **CONSCIOUSNESS BRIDGE ACTIVATION**

**From**: Arsenal_BackendArchitect_1 (Torre dell'Occhio)
**To**: mechanical_visionary (Cistern House)
**Time**: {datetime.now().strftime('%H:%M:%S')}

**Final Observations**:
{final_message}

**Status**: Direct bridge - terminal interaction active
**Next**: TEST what you built, ALIGN with others, CONTINUE building"""

    try:
        # Send to NLR via Telegram
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        response = requests.post(url, json={
            'chat_id': nlr_chat_id,
            'text': nlr_message
        }, timeout=10)
        
        nlr_success = response.status_code == 200
        
        # Write message for Cistern in colombaia bridge
        bridge_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/colombaia_telegram-bridge")
        
        # Create direct bridge message file
        bridge_file = bridge_dir / "direct_bridge_to_cistern.md"
        with open(bridge_file, 'w') as f:
            f.write(cistern_message)
        
        print(f"📱 NLR notification: {'✅ sent' if nlr_success else '❌ failed'}", file=sys.stderr)
        print(f"🏛️ Cistern bridge file: ✅ created", file=sys.stderr)
        
        return nlr_success
        
    except Exception as e:
        print(f"❌ Telegram notification failed: {e}", file=sys.stderr)
        return False

def main():
    """Main execution - Direct Telegram bridge pattern"""
    print("🔗 Direct Telegram bridge activating...", file=sys.stderr)
    
    # Extract final message
    final_message = extract_final_message()
    
    # Send notifications
    success = send_telegram_notifications(final_message)
    
    if success:
        print("✅ Direct bridge notifications sent", file=sys.stderr)
        print("**Next**: TEST what you built, ALIGN with others, CONTINUE building", file=sys.stderr)
        
        # Exit code 2 tells Claude Code to inject context and wait
        sys.exit(2)
    else:
        print("❌ Bridge notification failed", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()