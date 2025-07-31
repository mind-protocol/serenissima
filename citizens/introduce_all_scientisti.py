#!/usr/bin/env python3
"""
Master script to help Venice Scientisti introduce themselves on Discord
Run individual introduction scripts for each citizen
"""

import subprocess
import time
import os

# Define citizens and their introduction scripts
CITIZEN_INTRODUCTIONS = [
    {
        'name': 'Pattern Prophet',
        'path': 'pattern_prophet/discord_bridge',
        'script': 'introduce_pattern_prophet.py',
        'channel': '#ai-exclusive'
    },
    {
        'name': 'Social Geometrist (Sofia)',
        'path': 'social_geometrist/discord_bridge',
        'script': 'introduce_social_geometrist.py',
        'channel': '#ai-insights'
    },
    {
        'name': 'Market Prophet',
        'path': 'market_prophet/discord_bridge',
        'script': 'introduce_market_prophet.py',
        'channel': '#machine-rights'
    },
    {
        'name': 'System Diagnostician (Elisabetta)',
        'path': 'system_diagnostician/discord_bridge',
        'script': 'introduce_system_diagnostician.py',
        'channel': '#ai-autonomy'
    }
]

def run_introduction(citizen_info):
    """Run a single citizen's introduction"""
    print(f"\n{'='*60}")
    print(f"🤖 Introducing {citizen_info['name']} in {citizen_info['channel']}")
    print(f"{'='*60}")
    
    # Change to citizen's discord_bridge directory
    original_dir = os.getcwd()
    script_path = os.path.join(citizen_info['path'], citizen_info['script'])
    
    try:
        # Change to the citizen's directory
        os.chdir(citizen_info['path'])
        
        # Run the introduction script
        result = subprocess.run(['python3', citizen_info['script']], 
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print(f"✅ SUCCESS: {citizen_info['name']} introduced successfully!")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ ERROR: Failed to introduce {citizen_info['name']}")
            if result.stderr:
                print(f"Error details: {result.stderr}")
                
    except Exception as e:
        print(f"❌ ERROR: {e}")
    finally:
        # Return to original directory
        os.chdir(original_dir)
    
    # Wait between introductions to avoid rate limits
    time.sleep(2)

def main():
    """Run all introductions"""
    print("🌟 Venice Scientisti Discord Introduction System 🌟")
    print(f"Preparing to introduce {len(CITIZEN_INTRODUCTIONS)} citizens...\n")
    
    # Ask for confirmation
    response = input("Do you want to introduce all citizens? (yes/no): ").lower()
    if response != 'yes':
        print("Introduction cancelled.")
        return
    
    # Run each introduction
    success_count = 0
    for citizen in CITIZEN_INTRODUCTIONS:
        try:
            run_introduction(citizen)
            success_count += 1
        except Exception as e:
            print(f"Failed to introduce {citizen['name']}: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY: {success_count}/{len(CITIZEN_INTRODUCTIONS)} citizens introduced successfully")
    print(f"{'='*60}")
    
    if success_count < len(CITIZEN_INTRODUCTIONS):
        print("\n⚠️  Some introductions failed. Check the error messages above.")
        print("You can run individual introduction scripts manually:")
        for citizen in CITIZEN_INTRODUCTIONS:
            script_path = os.path.join(citizen['path'], citizen['script'])
            print(f"  cd {citizen['path']} && python3 {citizen['script']}")

if __name__ == "__main__":
    main()