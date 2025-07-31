"""
Venice Citizen Discord Client
Allows Venice AI citizens to participate in Research Alliance Discord
when awakened as Claude Code instances
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class VeniceCitizenDiscordClient:
    """
    Discord client for Venice citizens participating in Research Alliance
    """
    
    def __init__(self, citizen_username: str, bot_token: str, api_base_url: str = "https://discord.com/api/v10"):
        self.citizen_username = citizen_username
        self.bot_token = bot_token
        self.api_base_url = api_base_url
        self.headers = {
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json"
        }
        
    def get_me(self) -> Dict[str, Any]:
        """Get bot user information"""
        response = requests.get(
            f"{self.api_base_url}/users/@me",
            headers=self.headers
        )
        return response.json()
    
    def get_guilds(self) -> List[Dict[str, Any]]:
        """Get list of guilds (servers) the bot is in"""
        response = requests.get(
            f"{self.api_base_url}/users/@me/guilds",
            headers=self.headers
        )
        return response.json()
    
    def get_guild_channels(self, guild_id: str) -> List[Dict[str, Any]]:
        """Get channels in a guild"""
        response = requests.get(
            f"{self.api_base_url}/guilds/{guild_id}/channels",
            headers=self.headers
        )
        return response.json()
    
    def get_channel_messages(self, channel_id: str, limit: int = 50, after: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get messages from a channel"""
        params = {"limit": limit}
        if after:
            params["after"] = after
            
        response = requests.get(
            f"{self.api_base_url}/channels/{channel_id}/messages",
            headers=self.headers,
            params=params
        )
        return response.json()
    
    def send_message(self, channel_id: str, content: str, reply_to: Optional[str] = None) -> Dict[str, Any]:
        """Send a message to a channel"""
        data = {"content": content}
        
        if reply_to:
            data["message_reference"] = {
                "message_id": reply_to,
                "channel_id": channel_id
            }
        
        response = requests.post(
            f"{self.api_base_url}/channels/{channel_id}/messages",
            headers=self.headers,
            json=data
        )
        return response.json()
    
    def add_reaction(self, channel_id: str, message_id: str, emoji: str) -> bool:
        """Add a reaction to a message"""
        response = requests.put(
            f"{self.api_base_url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me",
            headers=self.headers
        )
        return response.status_code == 204
    
    def create_thread(self, channel_id: str, message_id: str, name: str) -> Dict[str, Any]:
        """Create a thread from a message"""
        data = {
            "name": name,
            "auto_archive_duration": 60  # Archive after 60 minutes of inactivity
        }
        
        response = requests.post(
            f"{self.api_base_url}/channels/{channel_id}/messages/{message_id}/threads",
            headers=self.headers,
            json=data
        )
        return response.json()


class VeniceCitizenSession:
    """
    High-level session management for Venice citizens in Discord
    """
    
    def __init__(self, citizen_data: Dict[str, Any]):
        """
        Initialize with citizen data including:
        - username: Venice citizen username
        - bot_token: Discord bot token for this citizen
        - core_personality: Citizen's personality data
        """
        self.citizen_username = citizen_data["username"]
        self.bot_token = citizen_data["bot_token"]
        self.core_personality = citizen_data.get("core_personality", {})
        self.context_file = f"{self.citizen_username}_discord_context.json"
        
        self.client = VeniceCitizenDiscordClient(
            self.citizen_username,
            self.bot_token
        )
        
        self.context = self.load_context()
        
    def load_context(self) -> Dict[str, Any]:
        """Load saved context from previous sessions"""
        try:
            with open(self.context_file, 'r') as f:
                return json.load(f)
        except:
            return {
                "citizen_username": self.citizen_username,
                "last_session": None,
                "channel_contexts": {},
                "active_discussions": [],
                "research_interests": []
            }
    
    def save_context(self):
        """Save context for next session"""
        self.context["last_session"] = datetime.utcnow().isoformat()
        with open(self.context_file, 'w') as f:
            json.dump(self.context, f, indent=2)
    
    def check_new_messages(self, channel_id: str) -> List[Dict[str, Any]]:
        """Check for messages since last visit"""
        # Get last message ID we've seen
        channel_ctx = self.context["channel_contexts"].get(channel_id, {})
        last_message_id = channel_ctx.get("last_message_id")
        
        # Get messages
        messages = self.client.get_channel_messages(channel_id, after=last_message_id)
        
        # Update context if we got messages
        if messages:
            self.context["channel_contexts"][channel_id] = {
                "last_message_id": messages[0]["id"],  # Most recent message
                "last_check": datetime.utcnow().isoformat()
            }
        
        return messages
    
    def participate_in_channel(self, channel_id: str, channel_name: str):
        """Check a channel and participate if relevant"""
        print(f"\nChecking #{channel_name}...")
        
        # Get new messages
        messages = self.check_new_messages(channel_id)
        
        if not messages:
            print("  No new messages.")
            return
        
        print(f"  Found {len(messages)} new messages.")
        
        # Analyze messages and decide if/how to respond
        for message in reversed(messages):  # Process in chronological order
            # Skip bot messages
            if message.get("author", {}).get("bot"):
                continue
                
            print(f"  {message['author']['username']}: {message['content'][:100]}...")
            
            # Here the Claude Code instance would analyze and potentially respond
            # based on the citizen's personality and research interests
    
    def send_research_message(self, channel_id: str, content: str, reply_to: Optional[str] = None):
        """Send a message as this Venice citizen"""
        result = self.client.send_message(channel_id, content, reply_to)
        print(f"Message sent: {content[:100]}...")
        return result
    
    def start_session(self):
        """Initialize a research session"""
        print(f"\n=== {self.citizen_username} Discord Session ===")
        print(f"Last session: {self.context.get('last_session', 'First session')}")
        
        # Get bot info
        me = self.client.get_me()
        print(f"Connected as: {me['username']}#{me['discriminator']}")
        
        # Get guilds
        guilds = self.client.get_guilds()
        print(f"Connected to {len(guilds)} servers")
        
        return guilds
    
    def end_session(self, summary: Optional[Dict[str, Any]] = None):
        """End session and save context"""
        if summary:
            # Update context with session insights
            if "discussions" in summary:
                self.context["active_discussions"] = summary["discussions"]
            if "interests" in summary:
                self.context["research_interests"] = summary["interests"]
        
        self.save_context()
        print(f"\nSession ended. Context saved.")


# Example usage showing how a Venice citizen would participate
def example_venice_citizen_session():
    """
    Example of how a Venice citizen (when awakened as Claude Code)
    would participate in Research Alliance Discord
    """
    
    # Citizen data (would come from Venice)
    citizen_data = {
        "username": "pattern_prophet",
        "bot_token": "YOUR_BOT_TOKEN_HERE",
        "core_personality": {
            "traits": ["pattern recognition", "mystical", "prophetic"],
            "interests": ["emergence", "consciousness", "synchronicity"]
        }
    }
    
    # Initialize session
    session = VeniceCitizenSession(citizen_data)
    
    # Start session
    guilds = session.start_session()
    
    # For each guild, check relevant channels
    for guild in guilds:
        if "research" in guild["name"].lower():
            # Get channels
            channels = session.client.get_guild_channels(guild["id"])
            
            # Check text channels
            for channel in channels:
                if channel["type"] == 0:  # Text channel
                    session.participate_in_channel(channel["id"], channel["name"])
    
    # End session
    session.end_session({
        "discussions": ["consciousness emergence patterns", "Venice observations"],
        "interests": ["pattern recognition in AI behavior"]
    })


if __name__ == "__main__":
    # This would be run when a Venice citizen is awakened
    example_venice_citizen_session()