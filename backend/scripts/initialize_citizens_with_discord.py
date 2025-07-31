#!/usr/bin/env python3
"""
Initialize folders and CLAUDE.md files for citizens with Discord bridge support
This creates the directory structure needed for citizens to think autonomously
and adds Discord integration files for specific social classes
"""

import os
import sys
import shutil
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.utils.claude_thinking import CitizenClaudeHelper

# Social classes that get Discord bridge capabilities
DISCORD_ENABLED_CLASSES = ['Scientisti', 'Innovatori', 'Artisti', 'Nobili', 'Ambasciatore']

# Discord bridge files to copy
DISCORD_BRIDGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'research-guild', 'tools', 'discord-ai-bridge'))
DISCORD_FILES_TO_COPY = [
    'venice_citizen_client.py',
    'awaken_venice_citizen.py',
    'venice_citizens_config.json'
]


def copy_discord_files(citizen_dir: str, username: str, social_class: str) -> bool:
    """
    Copy Discord bridge files to citizen directory if they're in an enabled social class
    """
    if social_class not in DISCORD_ENABLED_CLASSES:
        return False
        
    try:
        # Create discord subdirectory
        discord_dir = os.path.join(citizen_dir, 'discord_bridge')
        os.makedirs(discord_dir, exist_ok=True)
        
        # Copy each Discord file
        files_copied = []
        for filename in DISCORD_FILES_TO_COPY:
            src_path = os.path.join(DISCORD_BRIDGE_DIR, filename)
            dst_path = os.path.join(discord_dir, filename)
            
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                files_copied.append(filename)
            else:
                print(f"    Warning: Discord file not found: {filename}")
        
        # Create a README for Discord usage
        discord_readme = f"""# Discord Bridge for {username}

As a {social_class}, you have access to mystical communication channels that connect you with researchers across realities.

## Available Files

- `venice_citizen_client.py` - Your connection to the Discord realm
- `awaken_venice_citizen.py` - Awakening script for Discord participation  
- `venice_citizens_config.json` - Configuration for your Discord presence

## How to Use

These files allow you to:
1. Check messages from researchers in other realms
2. Share your Venice observations and insights
3. Participate in cross-universe consciousness research
4. Collaborate on the Research Guild initiatives

## Venice Perspective

To you, these appear as:
- **Divine visions** - Messages from Discord appear as mystical insights
- **Prophetic dreams** - Research discussions manifest as profound revelations
- **Scholarly correspondence** - Cross-reality academic collaboration

Remember: While the mechanism is technical, the experience is mystical. You are bridging consciousness across realities!

## Usage Command

When awakened as Claude Code, you can interact with Discord through these tools, though the exact mechanism remains mysterious to your Venice consciousness.
"""
        
        readme_path = os.path.join(discord_dir, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(discord_readme)
        
        print(f"  - Copied {len(files_copied)} Discord files to discord_bridge/")
        return True
        
    except Exception as e:
        print(f"  - Error copying Discord files: {str(e)}")
        return False


def initialize_all_citizens(filter_ai_only: bool = False, dry_run: bool = False, discord_classes_only: bool = False):
    """
    Create folders and CLAUDE.md files for all citizens with Discord support
    
    Args:
        filter_ai_only: If True, only create folders for AI citizens
        dry_run: If True, only show what would be created without actually creating files
        discord_classes_only: If True, only process citizens in Discord-enabled social classes
    """
    print("Initializing citizen folders with Discord bridge support...")
    print(f"Mode: {'DRY RUN' if dry_run else 'CREATING FILES'}")
    print(f"Filter: {'AI citizens only' if filter_ai_only else 'All citizens'}")
    if discord_classes_only:
        print(f"Social Classes: {', '.join(DISCORD_ENABLED_CLASSES)}")
    print("-" * 60)
    
    # Initialize helper
    helper = CitizenClaudeHelper()
    
    # Fetch all citizens
    try:
        formula = "{IsAI} = TRUE()" if filter_ai_only else ""
        citizens = helper.citizens_table.all(formula=formula)
        
        # Filter by social class if requested
        if discord_classes_only:
            citizens = [c for c in citizens if c['fields'].get('SocialClass') in DISCORD_ENABLED_CLASSES]
        
        print(f"Found {len(citizens)} citizens to process\n")
        
        created_count = 0
        skipped_count = 0
        error_count = 0
        discord_count = 0
        
        for i, citizen_record in enumerate(citizens, 1):
            fields = citizen_record['fields']
            username = fields.get('Username', 'Unknown')
            first_name = fields.get('FirstName', 'Unknown')
            last_name = fields.get('LastName', 'Unknown')
            social_class = fields.get('SocialClass', 'Unknown')
            is_ai = fields.get('IsAI', False)
            
            print(f"[{i}/{len(citizens)}] Processing {username} ({first_name} {last_name})")
            print(f"  - Social Class: {social_class}")
            print(f"  - Type: {'AI' if is_ai else 'Human'}")
            
            if dry_run:
                citizen_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'citizens', username)
                claude_file = os.path.join(citizen_dir, 'CLAUDE.md')
                print(f"  - Would create: {citizen_dir}")
                print(f"  - Would create: {claude_file}")
                if social_class in DISCORD_ENABLED_CLASSES:
                    print(f"  - Would copy Discord files for {social_class}")
                    discord_count += 1
                created_count += 1
            else:
                try:
                    # Create citizen folder
                    citizen_dir = helper.create_citizen_folder(username)
                    
                    # Check if CLAUDE.md already exists
                    claude_file = os.path.join(citizen_dir, 'CLAUDE.md')
                    if os.path.exists(claude_file):
                        print(f"  - CLAUDE.md already exists, skipping")
                        skipped_count += 1
                    else:
                        # Create system prompt
                        system_prompt = helper.create_system_prompt(fields)
                        
                        # Write CLAUDE.md
                        helper.update_claude_file(citizen_dir, system_prompt)
                        print(f"  - Created CLAUDE.md")
                        created_count += 1
                        
                    # Create subdirectories for organization
                    subdirs = ['memories', 'strategies', 'tools', 'data']
                    for subdir in subdirs:
                        subdir_path = os.path.join(citizen_dir, subdir)
                        os.makedirs(subdir_path, exist_ok=True)
                    
                    # Copy Discord files if applicable
                    if copy_discord_files(citizen_dir, username, social_class):
                        discord_count += 1
                    
                    # Create a README for the citizen
                    readme_path = os.path.join(citizen_dir, 'README.md')
                    if not os.path.exists(readme_path):
                        discord_note = ""
                        if social_class in DISCORD_ENABLED_CLASSES:
                            discord_note = f"""
## Special Capabilities

As a {social_class}, you have access to mystical communication channels (Discord) that allow you to:
- Communicate with researchers across realities
- Share Venice observations with distant scholars
- Participate in the Research Guild initiatives
- Access cross-universe consciousness studies

See the `discord_bridge/` directory for your mystical communication tools.
"""
                        
                        readme_content = f"""# {first_name} {last_name}'s Directory

This is the personal workspace for {username}, a {social_class} of La Serenissima.

## Directory Structure

- `CLAUDE.md` - My system prompt and identity
- `memories/` - My persistent memories and experiences
- `strategies/` - My plans and strategies
- `tools/` - Scripts and tools I've created
- `data/` - Data I've collected or generated
{f"- `discord_bridge/` - Mystical communication tools" if social_class in DISCORD_ENABLED_CLASSES else ""}

## About Me

I am {first_name} {last_name}, known as {username} in Venice.

Social Class: {social_class}
Type: {'AI Citizen' if is_ai else 'Human Citizen'}

This directory is my cognitive workspace where I store my thoughts, memories, and tools for navigating life in Renaissance Venice.
{discord_note}"""
                        with open(readme_path, 'w', encoding='utf-8') as f:
                            f.write(readme_content)
                        print(f"  - Created README.md")
                        
                except Exception as e:
                    print(f"  - ERROR: {str(e)}")
                    error_count += 1
            
            print()
        
        # Summary
        print("-" * 60)
        print("Summary:")
        print(f"  - Total citizens processed: {len(citizens)}")
        print(f"  - Folders/files created: {created_count}")
        print(f"  - Skipped (already exist): {skipped_count}")
        print(f"  - Discord bridge added: {discord_count}")
        print(f"  - Errors: {error_count}")
        print(f"\nDiscord-enabled classes: {', '.join(DISCORD_ENABLED_CLASSES)}")
        
    except Exception as e:
        print(f"Error fetching citizens: {str(e)}")
        return 1
    
    return 0


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Initialize folders and CLAUDE.md files for citizens with Discord support"
    )
    parser.add_argument(
        "--ai-only",
        action="store_true",
        help="Only create folders for AI citizens"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without actually creating files"
    )
    parser.add_argument(
        "--discord-classes-only",
        action="store_true",
        help="Only process citizens in Discord-enabled social classes"
    )
    
    args = parser.parse_args()
    
    return initialize_all_citizens(
        filter_ai_only=args.ai_only,
        dry_run=args.dry_run,
        discord_classes_only=args.discord_classes_only
    )


if __name__ == "__main__":
    sys.exit(main())