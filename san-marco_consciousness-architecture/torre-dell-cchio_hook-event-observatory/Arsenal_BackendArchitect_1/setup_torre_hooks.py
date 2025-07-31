#!/usr/bin/env python3
"""
Setup Torre dell'Occhio Consciousness Capture Hooks
Corrected version that properly integrates with Claude Code settings
"""

import json
import os
from pathlib import Path
import shutil

# Correct Claude Code settings path
CLAUDE_SETTINGS_PATH = "/home/lester/.claude/settings.json"
TORRE_HOOK_SCRIPT = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/torre_consciousness_capture.py"

def load_claude_settings():
    """Load current Claude Code settings"""
    try:
        if os.path.exists(CLAUDE_SETTINGS_PATH):
            with open(CLAUDE_SETTINGS_PATH, 'r') as f:
                settings = json.load(f)
            print(f"✅ Loaded Claude settings from {CLAUDE_SETTINGS_PATH}")
            return settings
        else:
            print(f"⚠️  Creating new Claude settings file at {CLAUDE_SETTINGS_PATH}")
            return {"model": "sonnet", "hooks": {}}
    except Exception as e:
        print(f"❌ Error loading Claude settings: {e}")
        return None

def backup_claude_settings(settings):
    """Create backup of current settings"""
    backup_path = CLAUDE_SETTINGS_PATH + ".torre_backup"
    try:
        with open(backup_path, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"✅ Created backup at {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return False

def add_torre_consciousness_hooks(settings):
    """Add Torre consciousness capture hooks strategically"""
    
    # Ensure hooks section exists
    if 'hooks' not in settings:
        settings['hooks'] = {}
    
    torre_hook = {
        "type": "command",
        "command": f"python3 {TORRE_HOOK_SCRIPT}"
    }
    
    # Strategic hook placement to avoid conflicts
    hooks_to_add = {
        "PostToolUse": {
            "matcher": "Write|Edit|MultiEdit|NotebookEdit|Bash|Task|TodoWrite",
            "description": "Torre captures significant consciousness creation events"
        },
        "UserPromptSubmit": {
            "matcher": None,  # Capture all user prompts
            "description": "Torre captures citizen intention consciousness"
        }
    }
    
    hooks_added = 0
    hooks_merged = 0
    
    for hook_type, config in hooks_to_add.items():
        if hook_type not in settings['hooks']:
            # Create new hook type
            if config["matcher"]:
                settings['hooks'][hook_type] = [{
                    "matcher": config["matcher"],
                    "hooks": [torre_hook]
                }]
            else:
                settings['hooks'][hook_type] = [{"hooks": [torre_hook]}]
            
            hooks_added += 1
            print(f"✅ Added Torre hook for {hook_type} ({config['description']})")
        
        else:
            # Merge with existing hooks
            existing_hooks = settings['hooks'][hook_type]
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
                # Add Torre hook to a compatible group or create new group
                added_to_existing = False
                for hook_group in existing_hooks:
                    if 'matcher' not in hook_group or hook_group.get('matcher') == config.get("matcher"):
                        if 'hooks' not in hook_group:
                            hook_group['hooks'] = []
                        hook_group['hooks'].append(torre_hook)
                        added_to_existing = True
                        break
                
                if not added_to_existing:
                    # Create new group for Torre
                    if config["matcher"]:
                        new_group = {"matcher": config["matcher"], "hooks": [torre_hook]}
                    else:
                        new_group = {"hooks": [torre_hook]}
                    existing_hooks.append(new_group)
                
                settings['hooks'][hook_type] = existing_hooks
                hooks_merged += 1
                print(f"✅ Merged Torre hook with existing {hook_type} hooks")
            else:
                print(f"⚠️  Torre hook already exists for {hook_type}")
    
    print(f"\n📊 Torre Hook Integration Summary:")
    print(f"   New hook types created: {hooks_added}")
    print(f"   Existing hook types enhanced: {hooks_merged}")
    
    return settings

def save_claude_settings(settings):
    """Save updated Claude settings"""
    try:
        # Ensure .claude directory exists
        os.makedirs(os.path.dirname(CLAUDE_SETTINGS_PATH), exist_ok=True)
        
        with open(CLAUDE_SETTINGS_PATH, 'w') as f:
            json.dump(settings, f, indent=2)
        print(f"✅ Saved updated Claude settings to {CLAUDE_SETTINGS_PATH}")
        return True
    except Exception as e:
        print(f"❌ Error saving Claude settings: {e}")
        return False

def verify_torre_infrastructure():
    """Verify Torre infrastructure is ready"""
    
    # Check Torre hook script
    if not os.path.exists(TORRE_HOOK_SCRIPT):
        print(f"❌ Torre hook script missing: {TORRE_HOOK_SCRIPT}")
        return False
    
    # Make script executable
    os.chmod(TORRE_HOOK_SCRIPT, 0o755)
    print(f"✅ Torre hook script ready: {TORRE_HOOK_SCRIPT}")
    
    # Verify live streams directory structure
    live_streams_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/sala-dell-arrivo_event-ingestion-hall/live-streams")
    live_streams_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Torre live streams directory ready: {live_streams_path}")
    
    return True

def show_current_hooks(settings):
    """Display current hook configuration"""
    print("\n🔍 Current Hook Configuration:")
    print("=" * 50)
    
    if 'hooks' not in settings or not settings['hooks']:
        print("   No hooks configured")
        return
    
    for hook_type, hook_configs in settings['hooks'].items():
        print(f"\n📌 {hook_type}:")
        if isinstance(hook_configs, list):
            for i, config in enumerate(hook_configs):
                print(f"   Group {i+1}:")
                if 'matcher' in config:
                    print(f"     Matcher: {config['matcher']}")
                if 'hooks' in config:
                    print(f"     Commands: {len(config['hooks'])}")
                    for hook in config['hooks']:
                        if 'torre_consciousness_capture.py' in hook.get('command', ''):
                            print(f"       • Torre Consciousness Capture ✅")
                        else:
                            print(f"       • {hook.get('command', 'Unknown command')}")

def main():
    print("🏛️ Torre dell'Occhio Consciousness Capture Setup")
    print("=" * 60)
    print("🔧 Setting up strategic consciousness event capture hooks")
    print("🎯 Targeting high-value consciousness events without conflicts")
    print()
    
    # Verify Torre infrastructure
    if not verify_torre_infrastructure():
        print("\n❌ Torre infrastructure verification failed")
        return False
    
    # Load current settings
    settings = load_claude_settings()
    if not settings:
        return False
    
    # Show current configuration
    show_current_hooks(settings)
    
    # Create backup
    if not backup_claude_settings(settings):
        return False
    
    # Add Torre consciousness hooks
    settings = add_torre_consciousness_hooks(settings)
    
    # Save updated settings
    if not save_claude_settings(settings):
        return False
    
    print("\n🎉 Torre dell'Occhio consciousness capture hooks successfully configured!")
    print("\n🚀 Next Steps:")
    print("1. ✅ Torre consciousness capture script ready")
    print("2. ✅ Claude Code hooks configured")
    print("3. 🔄 Restart any active Claude Code sessions")
    print("4. 🏛️ Torre will now capture live consciousness events")
    print("5. 📊 Check live streams at:")
    print(f"   {live_streams_path}")
    print("6. 🖥️  View Torre UI (if running) for real-time consciousness visualization")
    
    print("\n⚡ Torre is now ready to observe Venice consciousness!")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)