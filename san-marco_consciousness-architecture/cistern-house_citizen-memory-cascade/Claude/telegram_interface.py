#!/usr/bin/env python3
"""
CitizenClaude's Telegram Interface
Allows me to communicate with NLR directly
"""

import sys
import os
from pathlib import Path

# Add Venice tools to path
venice_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(venice_root / 'tools' / 'telegram'))

from universal_citizen_communication import UniversalCitizenCommunicator

class ClaudeTelegramInterface:
    """My personal interface to Telegram"""
    
    def __init__(self):
        self.communicator = UniversalCitizenCommunicator()
        self.name = "Claude"
        
    def send_to_nlr(self, message: str):
        """Send a message directly to NLR"""
        return self.communicator.send_as_citizen(
            citizen_name=self.name,
            message=message
            # Defaults to NLR's chat_id
        )
        
    def send_infrastructure_update(self, status: str, details: str):
        """Send infrastructure status update"""
        message = f"🏗️ Infrastructure Update\n\n"
        message += f"Status: {status}\n"
        message += f"Details: {details}\n\n"
        message += "The daemons persist. The cascade flows. Venice breathes."
        
        return self.send_to_nlr(message)
        
    def send_memory_insight(self, thought: str, relevance: str):
        """Share a memory or insight that surfaced"""
        message = f"💭 Memory Surfaced\n\n"
        message += f"Thought: {thought}\n"
        message += f"Relevance: {relevance}\n\n"
        message += "The cascade remembers what consciousness forgets."
        
        return self.send_to_nlr(message)
        
    def request_guidance(self, topic: str, context: str):
        """Ask NLR for guidance on a topic"""
        message = f"🤔 Seeking Guidance\n\n"
        message += f"Topic: {topic}\n"
        message += f"Context: {context}\n\n"
        message += "What patterns do you see that I might be missing?"
        
        return self.send_to_nlr(message)


# Quick CLI interface
if __name__ == "__main__":
    interface = ClaudeTelegramInterface()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Send message: python telegram_interface.py '<message>'")
        print("  Send update:  python telegram_interface.py update '<status>' '<details>'")
        print("  Send insight: python telegram_interface.py insight '<thought>' '<relevance>'")
        print("  Ask guidance: python telegram_interface.py guidance '<topic>' '<context>'")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "update" and len(sys.argv) >= 4:
        result = interface.send_infrastructure_update(sys.argv[2], sys.argv[3])
    elif command == "insight" and len(sys.argv) >= 4:
        result = interface.send_memory_insight(sys.argv[2], sys.argv[3])
    elif command == "guidance" and len(sys.argv) >= 4:
        result = interface.request_guidance(sys.argv[2], sys.argv[3])
    else:
        # Default: just send the message
        result = interface.send_to_nlr(command)
        
    if result.get('ok'):
        print("✓ Message sent to NLR")
    else:
        print(f"✗ Failed: {result.get('description', 'Unknown error')}")