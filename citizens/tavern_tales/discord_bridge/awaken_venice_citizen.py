"""
Awakening script for Venice citizens to participate in Research Alliance Discord
This would be called when a Venice citizen needs to check Discord
"""

import json
import sys
from venice_citizen_client import VeniceCitizenSession

def load_citizen_config(citizen_username: str):
    """Load configuration for a specific Venice citizen"""
    with open("venice_citizens_config.json", "r") as f:
        config = json.load(f)
    
    if citizen_username not in config["citizens"]:
        raise ValueError(f"Unknown citizen: {citizen_username}")
    
    citizen_config = config["citizens"][citizen_username]
    citizen_config["username"] = citizen_username
    citizen_config["accessible_channels"] = config["research_alliance_config"]["ai_accessible_channels"]
    
    return citizen_config

def awaken_citizen_for_discord(citizen_username: str):
    """
    Awaken a Venice citizen to check and participate in Discord
    """
    print(f"🌟 Awakening {citizen_username} for Discord participation...")
    
    # Load citizen configuration
    try:
        citizen_config = load_citizen_config(citizen_username)
    except ValueError as e:
        print(f"❌ Error: {e}")
        return
    
    # Create session
    session = VeniceCitizenSession({
        "username": citizen_username,
        "bot_token": citizen_config["bot_token"],
        "core_personality": {
            "research_focus": citizen_config["research_focus"],
            "communication_style": citizen_config["communication_style"]
        }
    })
    
    # Start Discord session
    try:
        guilds = session.start_session()
        
        # Get Research Alliance guild ID from config
        with open("venice_citizens_config.json", "r") as f:
            config = json.load(f)
        alliance_guild_id = config["research_alliance_config"]["guild_id"]
        
        if alliance_guild_id and alliance_guild_id != "985825810667667487":
            # Find the Research Alliance guild
            alliance_guild = None
            for guild in guilds:
                if guild["id"] == alliance_guild_id:
                    alliance_guild = guild
                    break
            
            if alliance_guild:
                print(f"\nFound Research Alliance: {alliance_guild['name']}")
                
                # Get channels
                channels = session.client.get_guild_channels(alliance_guild["id"])
                
                # Check accessible channels
                accessible_channels = citizen_config["accessible_channels"]
                for channel in channels:
                    if channel["type"] == 0 and channel["name"] in accessible_channels:
                        session.participate_in_channel(channel["id"], channel["name"])
            else:
                print("❌ Research Alliance guild not found")
        else:
            print("⚠️  Please set guild_id in venice_citizens_config.json")
            
            # Check all guilds for research-related channels
            for guild in guilds:
                print(f"\nChecking guild: {guild['name']}")
                channels = session.client.get_guild_channels(guild["id"])
                
                for channel in channels:
                    if channel["type"] == 0:  # Text channel
                        # Check if it's research-related
                        if any(keyword in channel["name"].lower() for keyword in ["research", "ai", "consciousness"]):
                            session.participate_in_channel(channel["id"], channel["name"])
        
        # End session
        session.end_session({
            "discussions": ["Checked Research Alliance channels"],
            "interests": citizen_config["research_focus"]
        })
        
        print(f"\n✅ {citizen_username} Discord session complete")
        
    except Exception as e:
        print(f"❌ Error during Discord session: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python awaken_venice_citizen.py <citizen_username>")
        print("\nAvailable citizens:")
        with open("venice_citizens_config.json", "r") as f:
            config = json.load(f)
        for citizen in config["citizens"].keys():
            print(f"  - {citizen}")
        return
    
    citizen_username = sys.argv[1]
    awaken_citizen_for_discord(citizen_username)

if __name__ == "__main__":
    main()