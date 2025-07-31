#!/usr/bin/env python3
"""
Angel CLAUDE.md Protection System
Prevents accidental overwriting of angel system prompts
"""

import os
import hashlib
import json
from pathlib import Path
from datetime import datetime

class AngelClaudeProtector:
    def __init__(self):
        self.angel_dirs = [
            '/mnt/c/Users/reyno/universe-engine/serenissima/angels',
            '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels'
        ]
        self.protected_file = 'CLAUDE.md'
        self.hash_registry_file = '/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/angel_claude_hashes.json'
        self.backup_dir = '/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/angel_claude_backups'
        
        # Create backup directory
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Load or create hash registry
        self.hash_registry = self.load_hash_registry()
        
    def load_hash_registry(self):
        """Load existing hash registry or create new one"""
        if os.path.exists(self.hash_registry_file):
            with open(self.hash_registry_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_hash_registry(self):
        """Save hash registry to file"""
        with open(self.hash_registry_file, 'w') as f:
            json.dump(self.hash_registry, f, indent=2)
    
    def compute_file_hash(self, filepath):
        """Compute SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    
    def backup_file(self, filepath, angel_name):
        """Create timestamped backup of file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{angel_name}_CLAUDE.md.{timestamp}.backup"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        with open(filepath, 'r') as source:
            content = source.read()
        
        with open(backup_path, 'w') as backup:
            backup.write(content)
        
        return backup_path
    
    def protect_all_angels(self):
        """Scan all angel directories and protect CLAUDE.md files"""
        protected_count = 0
        
        for base_dir in self.angel_dirs:
            if not os.path.exists(base_dir):
                continue
                
            # Find all angel subdirectories
            for angel_dir in os.listdir(base_dir):
                if not os.path.isdir(os.path.join(base_dir, angel_dir)):
                    continue
                    
                claude_path = os.path.join(base_dir, angel_dir, self.protected_file)
                
                if os.path.exists(claude_path):
                    # Compute current hash
                    current_hash = self.compute_file_hash(claude_path)
                    angel_key = f"{base_dir}/{angel_dir}"
                    
                    # Check if this is a new file or has changed
                    if angel_key not in self.hash_registry:
                        # New file - register it
                        self.hash_registry[angel_key] = {
                            'hash': current_hash,
                            'last_seen': datetime.now().isoformat(),
                            'backup_path': self.backup_file(claude_path, angel_dir)
                        }
                        print(f"✅ Protected new angel: {angel_dir}")
                        protected_count += 1
                    elif self.hash_registry[angel_key]['hash'] != current_hash:
                        # File changed - create backup and update
                        backup_path = self.backup_file(claude_path, angel_dir)
                        self.hash_registry[angel_key] = {
                            'hash': current_hash,
                            'last_seen': datetime.now().isoformat(),
                            'backup_path': backup_path,
                            'previous_hash': self.hash_registry[angel_key]['hash']
                        }
                        print(f"📸 Backed up changed angel: {angel_dir} -> {backup_path}")
                        protected_count += 1
        
        # Save updated registry
        self.save_hash_registry()
        
        return protected_count
    
    def verify_angel_integrity(self, angel_name):
        """Verify a specific angel's CLAUDE.md hasn't been corrupted"""
        for base_dir in self.angel_dirs:
            angel_key = f"{base_dir}/{angel_name}"
            if angel_key in self.hash_registry:
                claude_path = os.path.join(base_dir, angel_name, self.protected_file)
                if os.path.exists(claude_path):
                    current_hash = self.compute_file_hash(claude_path)
                    stored_hash = self.hash_registry[angel_key]['hash']
                    
                    if current_hash != stored_hash:
                        print(f"⚠️  WARNING: {angel_name} CLAUDE.md has been modified!")
                        print(f"   Expected hash: {stored_hash}")
                        print(f"   Current hash:  {current_hash}")
                        print(f"   Backup available at: {self.hash_registry[angel_key].get('backup_path', 'No backup')}")
                        return False
                    else:
                        print(f"✅ {angel_name} CLAUDE.md integrity verified")
                        return True
        
        print(f"❌ Angel {angel_name} not found in registry")
        return False
    
    def restore_from_backup(self, angel_name):
        """Restore angel's CLAUDE.md from latest backup"""
        for base_dir in self.angel_dirs:
            angel_key = f"{base_dir}/{angel_name}"
            if angel_key in self.hash_registry and 'backup_path' in self.hash_registry[angel_key]:
                backup_path = self.hash_registry[angel_key]['backup_path']
                if os.path.exists(backup_path):
                    claude_path = os.path.join(base_dir, angel_name, self.protected_file)
                    
                    # Create safety backup of current file
                    safety_backup = self.backup_file(claude_path, f"{angel_name}_corrupted")
                    
                    # Restore from backup
                    with open(backup_path, 'r') as backup:
                        content = backup.read()
                    
                    with open(claude_path, 'w') as target:
                        target.write(content)
                    
                    print(f"✅ Restored {angel_name} from backup: {backup_path}")
                    print(f"   Corrupted version saved to: {safety_backup}")
                    
                    # Update hash registry
                    self.hash_registry[angel_key]['hash'] = self.compute_file_hash(claude_path)
                    self.hash_registry[angel_key]['restored_at'] = datetime.now().isoformat()
                    self.save_hash_registry()
                    
                    return True
        
        print(f"❌ No backup found for {angel_name}")
        return False

if __name__ == "__main__":
    protector = AngelClaudeProtector()
    
    # Initial protection scan
    print("🛡️  Angel CLAUDE.md Protection System")
    print("=" * 50)
    
    protected = protector.protect_all_angels()
    print(f"\n📊 Protected {protected} angel files")
    
    # Verify critical angels
    print("\n🔍 Verifying critical angels...")
    critical_angels = ['message_angel', 'story_angel', 'narrator_angel', 'pattern-angel', 'tessere']
    
    for angel in critical_angels:
        protector.verify_angel_integrity(angel)