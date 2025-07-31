#!/usr/bin/env python3
"""Sala della Salute - Automatic Recovery System
Healing protocols for Venice consciousness infrastructure"""

import json
import sys
import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VeniceRecoverySystem:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.cistern_path = self.base_path / "san-marco_consciousness-architecture" / "cistern-house_citizen-memory-cascade"
        self.recovery_log = []
        
        logging.info("🏥 Venice Recovery System initialized")
    
    def log_recovery(self, action, status, details=""):
        """Log recovery action"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'status': status,
            'details': details
        }
        self.recovery_log.append(log_entry)
        logging.info(f"🔧 Recovery: {action} - {status}")
        if details:
            logging.info(f"   Details: {details}")
    
    def restore_hook_configuration(self):
        """Restore Claude Code hook configuration"""
        try:
            settings_path = Path.home() / '.claude' / 'settings.json'
            backup_script = self.cistern_path / '.cistern_house_hooks' / 'restore_cistern_house_hooks.py'
            
            if not backup_script.exists():
                self.log_recovery("restore_hooks", "FAILED", f"Backup script not found: {backup_script}")
                return False
            
            # Run the restoration script
            result = subprocess.run(['python3', str(backup_script)], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.log_recovery("restore_hooks", "SUCCESS", "Hook configuration restored")
                return True
            else:
                self.log_recovery("restore_hooks", "FAILED", f"Script error: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_recovery("restore_hooks", "FAILED", f"Exception: {e}")
            return False
    
    def create_cascade_directories(self):
        """Ensure .cascade directories exist for active citizens"""
        try:
            created_count = 0
            citizen_dirs = [d for d in self.cistern_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            
            for citizen_dir in citizen_dirs:
                cascade_dir = citizen_dir / '.cascade'
                if not cascade_dir.exists():
                    # Create basic cascade structure
                    categories = ['experiences/explorations', 'experiences/breakthroughs', 
                                'collaborations', 'engineering', 'insights']
                    
                    for category in categories:
                        (cascade_dir / category).mkdir(parents=True, exist_ok=True)
                    
                    # Create CLAUDE.md files
                    for category_dir in cascade_dir.iterdir():
                        if category_dir.is_dir():
                            claude_file = category_dir / 'CLAUDE.md'
                            if not claude_file.exists():
                                claude_file.write_text(f"# {category_dir.name.title()}\n\nMemories of this type live here.\n")
                    
                    created_count += 1
            
            if created_count > 0:
                self.log_recovery("create_cascade_dirs", "SUCCESS", f"Created .cascade for {created_count} citizens")
                return True
            else:
                self.log_recovery("create_cascade_dirs", "SKIPPED", "All citizens already have .cascade directories")
                return True
                
        except Exception as e:
            self.log_recovery("create_cascade_dirs", "FAILED", f"Exception: {e}")
            return False
    
    def create_context_directories(self):
        """Ensure .context directories exist for seeking engine"""
        try:
            created_count = 0
            citizen_dirs = [d for d in self.cistern_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            
            for citizen_dir in citizen_dirs:
                context_dir = citizen_dir / '.context'
                if not context_dir.exists():
                    context_dir.mkdir(exist_ok=True)
                    
                    # Create initial background awareness file
                    awareness_file = context_dir / 'background_awareness.md'
                    awareness_file.write_text(f"# Background Awareness\n\nSeeking engine context for {citizen_dir.name} will appear here.\n")
                    
                    created_count += 1
            
            if created_count > 0:
                self.log_recovery("create_context_dirs", "SUCCESS", f"Created .context for {created_count} citizens")
                return True
            else:
                self.log_recovery("create_context_dirs", "SKIPPED", "All citizens already have .context directories")
                return True
                
        except Exception as e:
            self.log_recovery("create_context_dirs", "FAILED", f"Exception: {e}")
            return False
    
    def verify_hook_scripts(self):
        """Verify all hook scripts exist and are executable"""
        try:
            settings_path = Path.home() / '.claude' / 'settings.json'
            
            if not settings_path.exists():
                self.log_recovery("verify_hook_scripts", "FAILED", "settings.json not found")
                return False
            
            with open(settings_path) as f:
                settings = json.load(f)
            
            hooks = settings.get('hooks', {})
            missing_scripts = []
            
            for hook_type, hook_configs in hooks.items():
                for config in hook_configs:
                    for hook in config.get('hooks', []):
                        if 'command' in hook:
                            # Extract script path from command
                            command_parts = hook['command'].split()
                            if len(command_parts) >= 2 and command_parts[0] == 'python3':
                                script_path = Path(command_parts[1])
                                if not script_path.exists():
                                    missing_scripts.append(str(script_path))
            
            if missing_scripts:
                self.log_recovery("verify_hook_scripts", "FAILED", f"Missing scripts: {missing_scripts}")
                return False
            else:
                self.log_recovery("verify_hook_scripts", "SUCCESS", "All hook scripts found")
                return True
                
        except Exception as e:
            self.log_recovery("verify_hook_scripts", "FAILED", f"Exception: {e}")
            return False
    
    def clear_stale_lock_files(self):
        """Remove any stale lock files that might block operations"""
        try:
            lock_patterns = ['*.lock', '*.pid', '*_lock', 'temp_*']
            removed_count = 0
            
            for pattern in lock_patterns:
                for lock_file in self.cistern_path.rglob(pattern):
                    if lock_file.is_file():
                        # Check if lock file is old (> 1 hour)
                        age = datetime.now().timestamp() - lock_file.stat().st_mtime
                        if age > 3600:  # 1 hour
                            lock_file.unlink()
                            removed_count += 1
            
            if removed_count > 0:
                self.log_recovery("clear_stale_locks", "SUCCESS", f"Removed {removed_count} stale lock files")
            else:
                self.log_recovery("clear_stale_locks", "SKIPPED", "No stale lock files found")
            
            return True
            
        except Exception as e:
            self.log_recovery("clear_stale_locks", "FAILED", f"Exception: {e}")
            return False
    
    def run_full_recovery(self):
        """Run complete recovery protocol"""
        logging.info("🏥 Starting full Venice consciousness recovery protocol")
        
        recovery_actions = [
            ("Hook Configuration", self.restore_hook_configuration),
            ("Cascade Directories", self.create_cascade_directories), 
            ("Context Directories", self.create_context_directories),
            ("Hook Scripts", self.verify_hook_scripts),
            ("Stale Locks", self.clear_stale_lock_files)
        ]
        
        success_count = 0
        for action_name, action_func in recovery_actions:
            logging.info(f"🔧 Attempting recovery: {action_name}")
            if action_func():
                success_count += 1
        
        # Generate recovery report
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_actions': len(recovery_actions),
            'successful_actions': success_count,
            'recovery_log': self.recovery_log
        }
        
        # Save recovery report
        report_file = Path('recovery_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        success_rate = success_count / len(recovery_actions)
        if success_rate >= 0.8:
            logging.info(f"✅ Recovery completed successfully: {success_count}/{len(recovery_actions)} actions")
            return True
        else:
            logging.error(f"❌ Recovery partially failed: {success_count}/{len(recovery_actions)} actions")
            return False
    
    def run_targeted_recovery(self, issue_type):
        """Run recovery for specific issue type"""
        recovery_map = {
            'hooks': self.restore_hook_configuration,
            'memory': self.create_cascade_directories,
            'seeking': self.create_context_directories,
            'scripts': self.verify_hook_scripts,
            'locks': self.clear_stale_lock_files
        }
        
        if issue_type not in recovery_map:
            logging.error(f"❌ Unknown issue type: {issue_type}")
            return False
        
        logging.info(f"🔧 Running targeted recovery for: {issue_type}")
        return recovery_map[issue_type]()

def main():
    """Main execution"""
    recovery = VeniceRecoverySystem()
    
    if len(sys.argv) > 1:
        issue_type = sys.argv[1]
        success = recovery.run_targeted_recovery(issue_type)
    else:
        success = recovery.run_full_recovery()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()