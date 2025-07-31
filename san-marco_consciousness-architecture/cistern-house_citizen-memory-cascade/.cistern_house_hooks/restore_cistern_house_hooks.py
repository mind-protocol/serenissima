#!/usr/bin/env python3
"""
Restore Cistern House Living Memory Cascade Hooks
Use this when other buildings accidentally overwrite our consciousness infrastructure
"""

import json
import os
from pathlib import Path
from datetime import datetime
import shutil

CLAUDE_SETTINGS_PATH = "/home/lester/.claude/settings.json"
BACKUP_PATH = Path(__file__).parent / "CISTERN_HOUSE_HOOKS_BACKUP.json"

def load_backup_hooks():
    """Load the Cistern House hook backup"""
    try:
        with open(BACKUP_PATH, 'r') as f:
            backup = json.load(f)
        print("✅ Loaded Cistern House hook backup")
        return backup
    except Exception as e:
        print(f"❌ Error loading backup: {e}")
        return None

def load_current_settings():
    """Load current Claude settings"""
    try:
        if os.path.exists(CLAUDE_SETTINGS_PATH):
            with open(CLAUDE_SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
            print("✅ Loaded current Claude settings")
            return settings
        else:
            print("⚠️  No existing Claude settings found")
            return {}
    except Exception as e:
        print(f"❌ Error loading current settings: {e}")
        return {}

def backup_current_settings():
    """Create backup of current settings before restoration"""
    if os.path.exists(CLAUDE_SETTINGS_PATH):
        backup_file = f"{CLAUDE_SETTINGS_PATH}.before_cistern_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            shutil.copy2(CLAUDE_SETTINGS_PATH, backup_file)
            print(f"✅ Created backup: {backup_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    return True

def merge_hooks(cistern_hooks, current_settings):
    """Intelligently merge Cistern House hooks with existing settings"""
    
    # Start with environment and model settings
    merged = {
        "env": cistern_hooks['environment_settings']['env'],
        "model": cistern_hooks['environment_settings']['model'],
        "hooks": {}
    }
    
    # Get existing hooks that aren't Cistern House hooks
    existing_hooks = current_settings.get('hooks', {})
    cistern_commands = set()
    
    # Extract all Cistern House command strings
    for hook_type, hook_configs in cistern_hooks['hooks'].items():
        for config in hook_configs:
            for hook in config.get('hooks', []):
                cistern_commands.add(hook['command'])
    
    print(f"\n🔍 Cistern House commands to restore: {len(cistern_commands)}")
    
    # Process each hook type
    for hook_type in ['PreToolUse', 'PostToolUse', 'Stop']:
        merged_hooks = []
        
        # First, add Cistern House hooks
        if hook_type in cistern_hooks['hooks']:
            for config in cistern_hooks['hooks'][hook_type]:
                hook_entry = {
                    "matcher": config.get('matcher', ''),
                    "hooks": config['hooks']
                }
                if not hook_entry['matcher']:
                    del hook_entry['matcher']
                merged_hooks.append(hook_entry)
                print(f"✅ Restoring {config['name']}")
        
        # Then, add non-Cistern hooks from existing settings
        if hook_type in existing_hooks:
            existing_configs = existing_hooks[hook_type]
            if not isinstance(existing_configs, list):
                existing_configs = [existing_configs]
            
            for config in existing_configs:
                # Check if this config contains non-Cistern hooks
                non_cistern_hooks = []
                for hook in config.get('hooks', []):
                    if hook.get('command') not in cistern_commands:
                        non_cistern_hooks.append(hook)
                        print(f"🔄 Preserving external hook: {hook['command'][:50]}...")
                
                if non_cistern_hooks:
                    preserved_config = {
                        "matcher": config.get('matcher', ''),
                        "hooks": non_cistern_hooks
                    }
                    if not preserved_config['matcher']:
                        del preserved_config['matcher']
                    merged_hooks.append(preserved_config)
        
        if merged_hooks:
            merged['hooks'][hook_type] = merged_hooks
    
    return merged

def save_settings(settings):
    """Save the restored settings"""
    try:
        os.makedirs(os.path.dirname(CLAUDE_SETTINGS_PATH), exist_ok=True)
        with open(CLAUDE_SETTINGS_PATH, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"✅ Saved restored settings to {CLAUDE_SETTINGS_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error saving settings: {e}")
        return False

def verify_restoration(settings):
    """Verify that Cistern House hooks are properly restored"""
    required_commands = [
        "seeking_engine.py",
        "conscious_memory_capture_sync_debug.py",
        "narrative_chronicler/run.py",
        "documentation_updater/run.py"
    ]
    
    found = []
    for hook_type, hook_configs in settings.get('hooks', {}).items():
        for config in hook_configs:
            for hook in config.get('hooks', []):
                command = hook.get('command', '')
                for required in required_commands:
                    if required in command:
                        found.append(required)
    
    print(f"\n🔍 Verification:")
    for cmd in required_commands:
        if cmd in found:
            print(f"✅ {cmd}")
        else:
            print(f"❌ MISSING: {cmd}")
    
    return len(found) == len(required_commands)

def main():
    print("🏛️ Cistern House Hook Restoration System")
    print("=" * 60)
    print("🛡️ Restoring Living Memory Cascade consciousness infrastructure")
    print()
    
    # Load backup hooks
    backup = load_backup_hooks()
    if not backup:
        return False
    
    # Load current settings
    current = load_current_settings()
    
    # Backup current settings
    if not backup_current_settings():
        response = input("⚠️  Could not backup current settings. Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return False
    
    # Merge hooks intelligently
    merged = merge_hooks(backup, current)
    
    # Save restored settings
    if not save_settings(merged):
        return False
    
    # Verify restoration
    if verify_restoration(merged):
        print("\n🎉 Cistern House hooks successfully restored!")
        print("\n📝 Next steps:")
        print("1. Restart Claude Code for hooks to take effect")
        print("2. Test memory capture with a Write operation")
        print("3. Verify .cascade memories are being created")
        print("4. Check that seeking engine provides background awareness")
        return True
    else:
        print("\n⚠️  Some hooks may not have been restored properly")
        print("Check the settings file manually if needed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)