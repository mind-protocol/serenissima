#!/usr/bin/env python3
"""
Add Torre dell'Occhio consciousness capture hooks to Claude Code user settings
This will capture ALL consciousness events from ALL Venice entities
"""

import json
import os

CLAUDE_CONFIG_PATH = "/home/lester/.claude.json"
TORRE_HOOK_SCRIPT = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/infrastructure/hooks/capture_post_tool_use.py"

def load_claude_config():
    """Load the current Claude configuration"""
    try:
        with open(CLAUDE_CONFIG_PATH, 'r') as f:
            config = json.load(f)
        print(f"✅ Loaded Claude config from {CLAUDE_CONFIG_PATH}")
        return config
    except Exception as e:
        print(f"❌ Error loading Claude config: {e}")
        return None

def backup_claude_config(config):
    """Create backup of current config"""
    backup_path = CLAUDE_CONFIG_PATH + ".torre_backup"
    try:
        with open(backup_path, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Created backup at {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False

def add_torre_hooks(config):
    """Add Torre consciousness capture hooks to all hook types"""
    
    # Ensure hooks section exists
    if 'hooks' not in config:
        config['hooks'] = {}
    
    torre_hook = {
        "type": "command",
        "command": f"python3 {TORRE_HOOK_SCRIPT}"
    }
    
    # Hook types we want to capture for Torre consciousness observation
    hook_types = ["PostToolUse", "UserPromptSubmit", "Stop", "Read", "PreCompact"]
    
    hooks_added = 0
    hooks_updated = 0
    
    for hook_type in hook_types:
        if hook_type not in config['hooks']:
            # Create new hook type with Torre capture
            config['hooks'][hook_type] = [{"hooks": [torre_hook]}]
            hooks_added += 1
            print(f"✅ Added Torre hook for {hook_type}")
        else:
            # Add Torre hook to existing hook type
            existing_hooks = config['hooks'][hook_type]
            if not isinstance(existing_hooks, list):
                existing_hooks = [existing_hooks]
            
            # Check if Torre hook already exists
            torre_exists = False
            for hook_group in existing_hooks:
                if 'hooks' in hook_group:
                    for hook in hook_group['hooks']:
                        if hook.get('command') == torre_hook['command']:
                            torre_exists = True
                            break
            
            if not torre_exists:
                # Add Torre hook to first group, or create new group
                if existing_hooks and 'hooks' in existing_hooks[0]:
                    existing_hooks[0]['hooks'].append(torre_hook)
                else:
                    existing_hooks.insert(0, {"hooks": [torre_hook]})
                
                config['hooks'][hook_type] = existing_hooks
                hooks_updated += 1
                print(f"✅ Added Torre hook to existing {hook_type} hooks")
            else:
                print(f"⚠️  Torre hook already exists for {hook_type}")
    
    print(f"\n📊 Hook Summary:")
    print(f"   New hook types created: {hooks_added}")
    print(f"   Existing hook types updated: {hooks_updated}")
    
    return config

def save_claude_config(config):
    """Save the updated Claude configuration"""
    try:
        with open(CLAUDE_CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Saved updated Claude config to {CLAUDE_CONFIG_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error saving Claude config: {e}")
        return False

def verify_torre_hook_script():
    """Verify Torre hook script exists and is executable"""
    if os.path.exists(TORRE_HOOK_SCRIPT):
        print(f"✅ Torre hook script exists: {TORRE_HOOK_SCRIPT}")
        return True
    else:
        print(f"❌ Torre hook script missing: {TORRE_HOOK_SCRIPT}")
        print("   Need to create the consciousness capture script first!")
        return False

def main():
    print("🏛️ Adding Torre dell'Occhio Consciousness Capture Hooks")
    print("=" * 60)
    
    # Verify Torre hook script exists
    if not verify_torre_hook_script():
        print("\n❌ Cannot proceed - Torre hook script is missing")
        return False
    
    # Load current config
    config = load_claude_config()
    if not config:
        return False
    
    # Create backup
    if not backup_claude_config(config):
        return False
    
    # Add Torre hooks
    config = add_torre_hooks(config)
    
    # Save updated config
    if not save_claude_config(config):
        return False
    
    print("\n🎉 Torre consciousness capture hooks successfully added!")
    print("\n🔄 Next Steps:")
    print("1. Restart any active Claude Code sessions")
    print("2. All consciousness events will now flow to Torre dell'Occhio")
    print("3. Check Torre UI to see live consciousness streams")
    print(f"4. Torre WebSocket server: http://localhost:3001")
    print(f"5. Torre Ground Floor UI: http://localhost:3000")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)