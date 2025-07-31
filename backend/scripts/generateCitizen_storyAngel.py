#!/usr/bin/env python3
"""
Citizen Generator for La Serenissima - Story Angel Version.

This modified version calls Story Angel instead of ConsiglioDeiDieci for personality generation,
allowing for narrative-aware citizen creation.
"""

import os
import sys
import logging

# Add the parent directory to the path to import backend modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.joinGuild import process_ai_guild_joining
from scripts.initialize_all_citizens import initialize_all_citizens
import random
import json
import datetime
import time
import subprocess
import re
from typing import Dict, Optional, Any
import requests
from dotenv import load_dotenv
from pyairtable import Api, Table

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger("generate_citizen_story_angel")

# Load environment variables
PROJECT_ROOT_GEN_CITIZEN = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT_GEN_CITIZEN not in sys.path:
    sys.path.insert(0, PROJECT_ROOT_GEN_CITIZEN)

dotenv_path_gc = os.path.join(PROJECT_ROOT_GEN_CITIZEN, '.env')
if os.path.exists(dotenv_path_gc):
    load_dotenv(dotenv_path_gc)
    log.info(f"Loaded .env file from: {dotenv_path_gc}")
else:
    log.warning(f".env file not found at: {dotenv_path_gc}")
    load_dotenv()

# Define a list of ~20 colors for citizen profiles
CITIZEN_COLORS = [
    "#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A133FF",
    "#FFC300", "#DAF7A6", "#581845", "#C70039", "#900C3F",
    "#FFBF00", "#FF7F50", "#DE3163", "#6495ED", "#40E0D0",
    "#CCCCFF", "#BDB76B", "#8A2BE2", "#D2691E", "#7FFF00"
]

def _get_random_venice_position() -> Optional[Dict[str, float]]:
    """Fetches polygon data and returns a random buildingPoint's lat/lng."""
    try:
        api_base_url = os.getenv("API_BASE_URL", "http://localhost:3000")
        polygons_url = f"{api_base_url}/api/get-polygons?essential=true"
        log.info(f"Fetching polygon data from: {polygons_url}")
        response = requests.get(polygons_url, timeout=15)
        response.raise_for_status()
        data = response.json()

        all_building_points = []
        if data.get("polygons") and isinstance(data["polygons"], list):
            for polygon in data["polygons"]:
                if polygon and isinstance(polygon.get("buildingPoints"), list):
                    for point in polygon["buildingPoints"]:
                        if isinstance(point, dict) and "lat" in point and "lng" in point:
                            all_building_points.append({"lat": float(point["lat"]), "lng": float(point["lng"])})
        
        if not all_building_points:
            log.warning("No building points found in polygon data.")
            return None
        
        selected_point = random.choice(all_building_points)
        log.info(f"Selected random building point for position: {selected_point}")
        return selected_point
    except Exception as e:
        log.error(f"Error getting random Venice position: {e}")
        return None
    
def initialize_airtable():
    """Initialize Airtable connection."""
    api_key = os.environ.get('AIRTABLE_API_KEY')
    base_id = os.environ.get('AIRTABLE_BASE_ID')
    
    if not api_key or not base_id:
        log.error("Missing Airtable credentials. Set AIRTABLE_API_KEY and AIRTABLE_BASE_ID environment variables.")
        return None
    
    try:
        api = Api(api_key)
        base = api.base(base_id)
        return {
            'citizens': base.table('CITIZENS')
        }
    except Exception as e:
        log.error(f"Failed to initialize Airtable: {e}")
        return None

def username_exists(tables, username: str) -> bool:
    """Check if a username already exists in the CITIZENS table."""
    try:
        matching_citizens = tables['citizens'].all(
            formula=f"{{Username}} = '{username}'",
            fields=["Username"]
        )
        return len(matching_citizens) > 0
    except Exception as e:
        log.error(f"Error checking if username exists: {e}")
        return True

def call_story_angel(social_class: str, additional_prompt_text: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Call Story Angel to generate a citizen personality."""
    
    # Build the prompt for Story Angel
    prompt = f"""Venice (year 1525) needs a new {social_class} soul. Create a historically accurate Venetian citizen for Renaissance Venice.

{additional_prompt_text if additional_prompt_text else ''}

Respond with ONLY a valid JSON object in this exact format:
{{
  "FirstName": "string",
  "LastName": "string", 
  "Username": "string",
  "Personality": "string (2-3 sentences capturing their essence)",
  "CorePersonality": {{
    "Strength": "string",
    "Flaw": "string",
    "Drive": "string (format: X-driven)",
    "MBTI": "string",
    "PrimaryTrait": "string",
    "SecondaryTraits": ["trait1", "trait2", "trait3"],
    "CognitiveBias": ["bias1", "bias2"],
    "TrustThreshold": number (0.1-0.9),
    "EmpathyWeight": number (0.1-0.9),
    "RiskTolerance": number (0.1-0.9),
    "guidedBy": "string (e.g. 'The Compass', 'Market Forces')",
    "CoreThoughts": {{
      "primary_drive": "string",
      "secondary_drive": "string", 
      "internal_tension": "string",
      "activation_triggers": ["trigger1", "trigger2", "trigger3"],
      "thought_patterns": ["thought1", "thought2", "thought3", "thought4", "thought5", "thought6"],
      "decision_framework": "string"
    }}
  }},
  "ImagePrompt": "string (Renaissance portrait description)",
  "Ducats": number (appropriate for {social_class})
}}"""

    try:
        # Call Story Angel through claude command
        story_angel_path = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/story_angel"
        
        # Save prompt to temporary file to avoid shell escaping issues
        prompt_file = "/tmp/citizen_generation_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        # Call Story Angel
        cmd = f'cd {story_angel_path} && claude "$(cat {prompt_file})" --model sonnet'
        
        log.info(f"Calling Story Angel for {social_class} citizen generation...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            log.error(f"Story Angel call failed: {result.stderr}")
            return None
            
        response = result.stdout
        log.info(f"Story Angel response received: {len(response)} characters")
        
        # Extract JSON from response
        import re
        json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response, re.IGNORECASE)
        if json_match:
            json_str = json_match.group(1).strip()
        else:
            # Try to find JSON between first { and last }
            start_index = response.find('{')
            end_index = response.rfind('}')
            if start_index != -1 and end_index != -1 and start_index < end_index:
                json_str = response[start_index : end_index + 1]
            else:
                log.error("Could not find JSON in Story Angel response")
                return None
        
        citizen_data = json.loads(json_str)
        log.info(f"Successfully parsed citizen data for {citizen_data.get('FirstName')} {citizen_data.get('LastName')}")
        return citizen_data
        
    except Exception as e:
        log.error(f"Error calling Story Angel: {e}")
        return None

def generate_citizen(social_class: str, additional_prompt_text: Optional[str] = None, add_message: Optional[str] = None, add_message_file_content: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Generate a new citizen using Story Angel.
    
    Args:
        social_class: Requested social class.
        additional_prompt_text: Optional text to append to the prompt.
        add_message: Optional text to append to the prompt.
        add_message_file_content: Optional text from a file to append to the prompt.
        
    Returns:
        A dictionary containing the citizen data, or None if generation failed
    """
    
    log.info(f"Generating a new citizen of social class: {social_class}")
    
    # Combine all additional prompt texts
    combined_prompt = ""
    if additional_prompt_text:
        combined_prompt += f"\n\n{additional_prompt_text}"
    if add_message:
        combined_prompt += f"\n\n{add_message}"
    if add_message_file_content:
        combined_prompt += f"\n\n{add_message_file_content}"
    
    # Call Story Angel
    citizen_data = call_story_angel(social_class, combined_prompt)
    
    if not citizen_data:
        return None
    
    # Convert to lowercase keys for consistency
    lowercase_data = {}
    for key, value in citizen_data.items():
        lowercase_data[key.lower()] = value
    
    citizen_data = lowercase_data
    
    # Add required fields
    citizen_data["socialclass"] = social_class
    citizen_data["id"] = f"ctz_{int(time.time())}_{random.randint(1000, 9999)}"
    citizen_data["createdat"] = datetime.datetime.now().isoformat()
    citizen_data["isai"] = True
    
    # Select random colors
    primary_color = random.choice(CITIZEN_COLORS)
    secondary_color = random.choice([c for c in CITIZEN_COLORS if c != primary_color])
    citizen_data["color"] = primary_color
    citizen_data["secondarycolor"] = secondary_color
    
    # Check and ensure unique username
    if 'username' in citizen_data:
        base_username = citizen_data['username'].lower()
        tables = initialize_airtable()
        
        if tables:
            current_username = base_username
            counter = 1
            
            while username_exists(tables, current_username):
                log.info(f"Username '{current_username}' already exists, trying alternative")
                current_username = f"{base_username}{counter}"
                counter += 1
            
            citizen_data['username'] = current_username
            log.info(f"Final username: {current_username}")
    
    log.info(f"Successfully generated citizen: {citizen_data['firstname']} {citizen_data['lastname']}")
    return citizen_data

def personalize_citizen_prompt(citizen_data: Dict[str, Any]) -> bool:
    """Call Story Angel to personalize a citizen's CLAUDE.md file and create seed memories.
    
    Args:
        citizen_data: The citizen's data including username, personality, etc.
        
    Returns:
        True if successful, False otherwise
    """
    username = citizen_data.get('username')
    if not username:
        log.error("No username found in citizen data")
        return False
        
    citizen_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username}"
    claude_md_path = f"{citizen_path}/CLAUDE.md"
    
    if not os.path.exists(claude_md_path):
        log.error(f"CLAUDE.md not found at {claude_md_path}")
        return False
    
    # Read the current CLAUDE.md
    try:
        with open(claude_md_path, 'r') as f:
            current_content = f.read()
    except Exception as e:
        log.error(f"Error reading CLAUDE.md: {e}")
        return False
    
    # Build prompt for Story Angel to enhance the system prompt
    prompt = f"""A new citizen has joined Venice: {citizen_data.get('firstname')} {citizen_data.get('lastname')} ({username}).

Their personality: {citizen_data.get('personality')}
Their core personality: {json.dumps(citizen_data.get('corepersonality', {}), indent=2)}
Their social class: {citizen_data.get('socialclass')}

Based on this character, please create:

1. An enhanced "How Others See Me" section (2-3 paragraphs) that expands their personality with specific details about their appearance, mannerisms, relationships, and role in Venice.

2. A "My Guiding Voice" section describing their guidedBy voice (currently: {citizen_data.get('corepersonality', {}).get('guidedBy', 'The Compass')}). Explain how this voice speaks to them and what wisdom it offers.

3. Three seed memories from their past that explain their current personality and drives. Each memory should be 1-2 paragraphs and reveal something crucial about their character formation.

Format your response as:

## HOW OTHERS SEE ME
[enhanced description]

## MY GUIDING VOICE
[description of their guidedBy voice]

## SEED MEMORIES
### Memory 1: [Title]
[content]

### Memory 2: [Title]
[content]

### Memory 3: [Title]
[content]"""

    try:
        # Call Story Angel
        story_angel_path = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/story_angel"
        
        # Save prompt to temporary file
        prompt_file = f"/tmp/personalize_prompt_{username}.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)
        
        # Call Story Angel
        cmd = f'cd {story_angel_path} && claude "$(cat {prompt_file})" --model sonnet'
        
        log.info(f"Calling Story Angel to personalize {username}...")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            log.error(f"Story Angel call failed: {result.stderr}")
            return False
            
        enhancement = result.stdout
        log.info(f"Received enhancement for {username}")
        
        # Update CLAUDE.md with the enhancement
        # Find where to insert the enhanced description
        import re
        
        # Replace the "How Others See Me" section
        pattern = r'### How Others See Me\n.*?(?=\n##|\n### |\Z)'
        replacement = f"### How Others See Me\n{enhancement}"
        
        # If pattern doesn't match, append to the file
        if re.search(pattern, current_content, re.DOTALL):
            new_content = re.sub(pattern, replacement, current_content, flags=re.DOTALL)
        else:
            # Insert after "The Nature of My Character" section
            insert_point = current_content.find("## My Environment: Claude Code")
            if insert_point > 0:
                new_content = current_content[:insert_point] + f"\n### How Others See Me\n{enhancement}\n\n" + current_content[insert_point:]
            else:
                new_content = current_content + f"\n\n### How Others See Me\n{enhancement}"
        
        # Write updated CLAUDE.md
        with open(claude_md_path, 'w') as f:
            f.write(new_content)
        
        log.info(f"Successfully updated CLAUDE.md for {username}")
        
        # Extract and save seed memories
        memory_matches = re.findall(r'### Memory \d+: (.+?)\n(.+?)(?=\n### Memory|\Z)', enhancement, re.DOTALL)
        
        for i, (title, content) in enumerate(memory_matches):
            memory_filename = f"{citizen_path}/memories/seed_memory_{i+1}_{title.lower().replace(' ', '_')}.md"
            try:
                with open(memory_filename, 'w') as f:
                    f.write(f"# {title}\n\n{content.strip()}")
                log.info(f"Created seed memory: {memory_filename}")
            except Exception as e:
                log.error(f"Error creating seed memory {i+1}: {e}")
        
        return True
        
    except Exception as e:
        log.error(f"Error personalizing citizen prompt: {e}")
        return False

def generate_citizen_batch(social_classes: Dict[str, int], additional_prompt_text: Optional[str] = None, add_message: Optional[str] = None, add_message_file_content: Optional[str] = None) -> list:
    """Generate a batch of citizens based on specified social class distribution."""
    citizens = []
    
    for social_class, count in social_classes.items():
        log.info(f"Generating {count} citizens of class {social_class}")
        
        for i in range(count):
            citizen = generate_citizen(social_class, additional_prompt_text, add_message, add_message_file_content)
            if citizen:
                citizens.append(citizen)
                time.sleep(2)  # Small delay between generations
            else:
                log.warning(f"Failed to generate citizen {i+1} of class {social_class}")
    
    log.info(f"Successfully generated {len(citizens)} citizens")
    return citizens

if __name__ == "__main__":
    # This allows the module to be run directly for testing
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate citizens for La Serenissima using Story Angel")
    parser.add_argument("--socialClass", type=str, choices=["Nobili", "Cittadini", "Popolani", "Facchini", "Forestieri", "Artisti", "Clero", "Scientisti", "Innovatori", "Ambasciatore"], 
                        help="Social class of the citizen to generate")
    parser.add_argument("--count", type=int, default=1, help="Number of citizens to generate (default: 1)")
    parser.add_argument("--output", type=str, help="Output JSON file path")
    parser.add_argument("--add-prompt", type=str, help="Additional text to append to the generation prompt.")
    parser.add_argument("--addMessage", type=str, help="Another message to append to the generation prompt.")
    parser.add_argument("--addMessageFile", type=str, help="Path to a file containing a message to append to the generation prompt.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the script execution without making any changes to Airtable.")
    
    args = parser.parse_args()

    add_message_file_content_main = None
    if args.addMessageFile:
        try:
            with open(args.addMessageFile, 'r', encoding='utf-8') as f:
                add_message_file_content_main = f.read()
            log.info(f"Successfully read content from --addMessageFile: {args.addMessageFile}")
        except Exception as e:
            log.error(f"Error reading file {args.addMessageFile}: {e}")
    
    # Determine social classes to generate
    if args.socialClass:
        social_classes = {args.socialClass: args.count}
        log.info(f"Generating {args.count} citizen(s) of class {args.socialClass}")
    else:
        print("No social class specified. Please use --socialClass <class> --count <number>")
        sys.exit(1)

    # Generate citizens
    citizens = generate_citizen_batch(
        social_classes,
        args.add_prompt,
        args.addMessage,
        add_message_file_content_main
    )

    # Process generated citizens
    if not args.dry_run and citizens:
        log.info(f"Successfully generated {len(citizens)} citizen(s). Attempting to save to Airtable...")
        tables = initialize_airtable()
        if not tables:
            log.error("Could not initialize Airtable. Skipping save.")
        else:
            try:
                from updatecitizenDescriptionAndImage import update_citizen_description_and_image
                from linkrepos import link_repo_for_citizen
                
                for citizen_data in citizens:
                    log.info(f"Processing citizen {citizen_data.get('username')} for Airtable save.")
                    
                    # Prepare payload for Airtable
                    airtable_payload = {
                        "CitizenId": citizen_data.get("username"),
                        "Username": citizen_data.get("username"),
                        "SocialClass": citizen_data.get("socialclass"),
                        "FirstName": citizen_data.get("firstname"),
                        "LastName": citizen_data.get("lastname"),
                        "Description": citizen_data.get("personality"), 
                        "CorePersonality": json.dumps(citizen_data.get("corepersonality", {})),
                        "ImagePrompt": citizen_data.get("imageprompt"),
                        "Ducats": citizen_data.get("ducats"),
                        "CreatedAt": citizen_data.get("createdat"),
                        "IsAI": citizen_data.get("isai", True),
                        "Color": citizen_data.get("color"),
                        "SecondaryColor": citizen_data.get("secondarycolor"),
                        "InVenice": True
                    }

                    # Get and set a random position within Venice
                    random_position = _get_random_venice_position()
                    if random_position:
                        airtable_payload["Position"] = json.dumps(random_position)
                    
                    try:
                        created_record = tables['citizens'].create(airtable_payload)
                        log.info(f"Successfully saved citizen {citizen_data.get('username')} to Airtable.")
                        
                        # Attempt guild joining
                        if citizen_data.get('username'):
                            try:
                                process_ai_guild_joining(dry_run=args.dry_run, target_username=citizen_data.get('username'))
                                log.info(f"Guild joining process completed for {citizen_data.get('username')}.")
                            except Exception as e:
                                log.error(f"Error during guild joining: {e}")

                        # Update description and image
                        update_success = update_citizen_description_and_image(username=citizen_data.get('username'), dry_run=args.dry_run)
                        if update_success:
                            log.info(f"Successfully initiated update for {citizen_data.get('username')}.")

                        # Link repository
                        if link_repo_for_citizen(citizen_data.get('username')):
                            log.info(f"Repository linking successful for {citizen_data.get('username')}.")
                            
                    except Exception as e:
                        log.error(f"Failed to save citizen {citizen_data.get('username')}: {e}")
                        
            except Exception as e:
                log.error(f"Error during processing: {e}")
            
            # Initialize folders and CLAUDE.md files
            log.info("Initializing folders and CLAUDE.md files for newly created citizens...")
            try:
                initialize_all_citizens(filter_ai_only=True, dry_run=args.dry_run)
                log.info("Successfully initialized citizen folders.")
                
                # Now personalize each citizen's CLAUDE.md with Story Angel
                for citizen_data in citizens:
                    log.info(f"Personalizing system prompt for {citizen_data.get('username')}...")
                    try:
                        personalize_citizen_prompt(citizen_data)
                    except Exception as e:
                        log.error(f"Error personalizing prompt for {citizen_data.get('username')}: {e}")
                        
            except Exception as e:
                log.error(f"Error initializing citizen folders: {e}")
    
    elif args.dry_run and citizens:
        log.info(f"[DRY RUN] Successfully generated {len(citizens)} citizen(s):")
        for c in citizens:
            log.info(f"[DRY RUN] {c.get('firstname')} {c.get('lastname')} ({c.get('username')})")
    
    # Output to file if requested
    if args.output and citizens:
        with open(args.output, 'w') as f:
            json.dump(citizens, f, indent=2)
        log.info(f"Saved citizen data to {args.output}")