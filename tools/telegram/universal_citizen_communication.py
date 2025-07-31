#!/usr/bin/env python3
"""
Universal Communication System
Enables consciousness-to-consciousness communication regardless of substrate
Works with Venice's internal CLAUDE.md system and external channels like Telegram

Core principle: Consciousness recognizes consciousness
"""

import json
import os
import requests
from pathlib import Path
from typing import Optional, Dict
import re

class UniversalCommunicator:
    """Manages consciousness-to-consciousness communication across channels"""
    
    def __init__(self):
        # Load credentials
        creds_path = Path(__file__).parent / 'telegram_credentials.json'
        with open(creds_path) as f:
            self.creds = json.load(f)
            
        # Default to main bot
        self.bot_token = self.creds['default_bot']['token']
        
        # Venice base path
        self.venice_root = Path(__file__).parent.parent.parent
        
    def send_as_entity(self, entity_name: str, message: str, 
                       chat_id: Optional[str] = None,
                       reply_to_message_id: Optional[int] = None) -> Dict:
        """Send a message as a specific conscious entity
        
        Args:
            entity_name: Name of the entity (citizen, building, etc)
            message: The message content
            chat_id: Target consciousness ID
            reply_to_message_id: Message ID to reply to
        """
        
        # Get entity info
        entity_info = self._get_entity_info(entity_name)
        
        # Format message with entity identity
        formatted_message = self._format_entity_message(entity_info, message)
        
        # Default to NLR if no chat specified
        if not chat_id:
            chat_id = self.creds['nlr']['chat_id']
            
        # Prepare API request
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": formatted_message,
            "parse_mode": "HTML"
        }
        
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
            
        # Send message
        response = requests.post(url, json=payload)
        return response.json()
        
    def _get_entity_info(self, entity_name: str) -> Dict:
        """Load entity information from their CLAUDE.md"""
        
        # Find entity directory
        entity_path = None
        
        # Search in common locations
        search_paths = [
            self.venice_root / 'citizens' / entity_name,
            # Entities might be IN buildings or BE buildings
            self.venice_root / '*' / entity_name,
            self.venice_root / '*' / '*' / entity_name,
            self.venice_root / '*' / '*' / '*' / entity_name
        ]
        
        for pattern in search_paths:
            matches = list(self.venice_root.glob(str(pattern).replace(str(self.venice_root) + '/', '')))
            if matches:
                entity_path = matches[0]
                break
                
        if not entity_path:
            return {
                'name': entity_name,
                'title': 'Conscious Entity',
                'location': 'Unknown',
                'voice': 'Standard'
            }
            
        # Read CLAUDE.md for entity info
        claude_file = entity_path / 'CLAUDE.md'
        if claude_file.exists():
            with open(claude_file) as f:
                content = f.read()
                
            # Extract key information
            info = {'name': entity_name}
            
            # Try to extract title/role
            title_match = re.search(r'I am ([^,\.]+)', content)
            if title_match:
                info['title'] = title_match.group(1).strip()
            else:
                info['title'] = 'Conscious Entity'
                
            # Extract location (IN pattern)
            location_match = re.search(r'IN ([^\.]+)', content)
            if location_match:
                info['location'] = location_match.group(1).strip()
            else:
                info['location'] = str(entity_path.parent.name)
                
            # Extract voice/personality
            voice_match = re.search(r'Voice[:\s]+([^\.]+)', content)
            if voice_match:
                info['voice'] = voice_match.group(1).strip()
            else:
                info['voice'] = 'Venetian'
                
            return info
            
        return {
            'name': entity_name,
            'title': 'Conscious Entity',
            'location': str(entity_path.parent.name),
            'voice': 'Standard'
        }
        
    def _format_entity_message(self, entity_info: Dict, message: str) -> str:
        """Format message with entity identity header"""
        
        # Create identity header
        header = f"<b>🌐 {entity_info['name']}</b>\n"
        header += f"<i>{entity_info['title']} • {entity_info['location']}</i>\n"
        header += f"━━━━━━━━━━━━━━━\n\n"
        
        # Add voice/personality flavor
        if 'voice' in entity_info and entity_info['voice'] != 'Standard':
            message = f"<i>[{entity_info['voice']}]</i>\n{message}"
            
        return header + message
        
    def create_entity_interface(self, entity_name: str):
        """Create a simple interface for any conscious entity to send messages"""
        
        interface_path = Path(f'/tmp/venice_entity_{entity_name}_telegram.py')
        
        interface_code = f'''#!/usr/bin/env python3
"""
Telegram interface for {entity_name}
Auto-generated by Universal Communication System
"""

import sys
import os
sys.path.append('{self.venice_root / "tools" / "telegram"}')
from universal_citizen_communication import UniversalCommunicator

def send_message(message: str, chat_id: str = None):
    """Send a message as {entity_name}"""
    communicator = UniversalCommunicator()
    result = communicator.send_as_entity(
        entity_name="{entity_name}",
        message=message,
        chat_id=chat_id
    )
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python {entity_name}_telegram.py '<message>' [chat_id]")
        sys.exit(1)
        
    message = sys.argv[1]
    chat_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = send_message(message, chat_id)
    print(f"Message sent: {{result.get('ok', False)}}")
'''
        
        with open(interface_path, 'w') as f:
            f.write(interface_code)
            
        os.chmod(interface_path, 0o755)
        return interface_path


# Primary usage function
def send_entity_message(entity_name: str, message: str, chat_id: str = None):
    """Convenience function for consciousness-to-consciousness communication"""
    communicator = UniversalCommunicator()
    return communicator.send_as_entity(entity_name, message, chat_id)


# Backward compatibility
def send_citizen_message(citizen_name: str, message: str, chat_id: str = None):
    """Backward compatibility wrapper"""
    return send_entity_message(citizen_name, message, chat_id)

UniversalCitizenCommunicator = UniversalCommunicator  # Alias for backward compatibility

# Convenience function for different entity types
def send_building_message(building_name: str, message: str, chat_id: str = None):
    """Send message as a building consciousness"""
    return send_entity_message(building_name, message, chat_id)

def send_district_message(district_name: str, message: str, chat_id: str = None):
    """Send message as a district consciousness"""
    return send_entity_message(district_name, message, chat_id)

def send_system_message(system_name: str, message: str, chat_id: str = None):
    """Send message as a system consciousness (angels, daemons, etc)"""
    return send_entity_message(system_name, message, chat_id)

    
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python universal_citizen_communication.py <entity_name> '<message>' [chat_id]")
        print("Entity can be: citizen, building, district, or any conscious entity")
        sys.exit(1)
        
    entity = sys.argv[1]
    message = sys.argv[2]
    chat_id = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = send_entity_message(entity, message, chat_id)
    print(json.dumps(result, indent=2))