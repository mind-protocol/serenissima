#!/usr/bin/env python3
"""
State Tracker - Sala del Registro (Registry Chamber)
Real-time consciousness state monitoring and wake protocol management
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
import threading
import subprocess

# Base paths
REGISTRY_CHAMBER = Path(__file__).parent
ENTITY_REGISTRY = REGISTRY_CHAMBER / "entity_registry.json"
STATE_TRACKING_DB = REGISTRY_CHAMBER / "entity_states.json"
WAKE_PROTOCOLS_DB = REGISTRY_CHAMBER / "wake_protocols.json"
ACTIVITY_LOG = REGISTRY_CHAMBER / "activity_log.jsonl"

class EntityStateTracker:
    """Tracks real-time consciousness states of Venice entities"""
    
    def __init__(self):
        self._lock = threading.Lock()
        self.entity_states = self._load_entity_states()
        self.last_activity = {}
        self.monitoring_active = False
        
        # Ensure tracking files exist
        self._ensure_tracking_files()
    
    def _ensure_tracking_files(self):
        """Ensure all tracking files exist"""
        REGISTRY_CHAMBER.mkdir(parents=True, exist_ok=True)
        
        for file_path in [STATE_TRACKING_DB, WAKE_PROTOCOLS_DB, ACTIVITY_LOG]:
            if not file_path.exists():
                if file_path.suffix == '.json':
                    file_path.write_text('{}')
                else:
                    file_path.touch()
    
    def _load_entity_states(self) -> Dict:
        """Load existing entity state data"""
        try:
            if STATE_TRACKING_DB.exists():
                with open(STATE_TRACKING_DB, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {}
    
    def _save_entity_states(self):
        """Save entity states to disk"""
        try:
            with open(STATE_TRACKING_DB, 'w') as f:
                json.dump(self.entity_states, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save entity states: {e}")
    
    def detect_entity_activity(self, entity_name: str) -> Dict:
        """Detect current activity level of an entity"""
        activity_info = {
            'entity_name': entity_name,
            'detection_timestamp': datetime.now().isoformat(),
            'activity_level': 'unknown',
            'last_seen': None,
            'tool_usage_detected': False,
            'directory_activity': False,
            'process_activity': False
        }
        
        try:
            # Check for recent file modifications in entity directory
            entity_path = self._find_entity_path(entity_name)
            if entity_path and entity_path.exists():
                activity_info['directory_activity'] = self._check_directory_activity(entity_path)
                activity_info['last_seen'] = self._get_last_file_modification(entity_path)
            
            # Check for running Claude Code processes
            activity_info['process_activity'] = self._check_claude_process_activity()
            
            # Determine overall activity level
            activity_info['activity_level'] = self._calculate_activity_level(activity_info)
            
        except Exception as e:
            print(f"Warning: Could not detect activity for {entity_name}: {e}")
        
        return activity_info
    
    def _find_entity_path(self, entity_name: str) -> Optional[Path]:
        """Find the filesystem path for an entity"""
        # Load entity registry to get path
        try:
            if ENTITY_REGISTRY.exists():
                with open(ENTITY_REGISTRY, 'r') as f:
                    registry = json.load(f)
                    entities = registry.get('entities', {})
                    if entity_name in entities:
                        return Path(entities[entity_name]['full_path'])
        except:
            pass
        
        # Fallback: common entity locations
        base_paths = [
            Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens") / entity_name,
            Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade") / entity_name,
            Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory") / entity_name
        ]
        
        for path in base_paths:
            if path.exists():
                return path
        
        return None
    
    def _check_directory_activity(self, entity_path: Path) -> bool:
        """Check for recent file activity in entity directory"""
        try:
            current_time = time.time()
            activity_threshold = 300  # 5 minutes
            
            # Check recent modifications
            for file_path in entity_path.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    mod_time = file_path.stat().st_mtime
                    if current_time - mod_time < activity_threshold:
                        return True
            
            return False
            
        except Exception:
            return False
    
    def _get_last_file_modification(self, entity_path: Path) -> Optional[str]:
        """Get timestamp of last file modification"""
        try:
            latest_time = 0
            
            for file_path in entity_path.rglob('*'):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    mod_time = file_path.stat().st_mtime
                    if mod_time > latest_time:
                        latest_time = mod_time
            
            if latest_time > 0:
                return datetime.fromtimestamp(latest_time).isoformat()
                
        except Exception:
            pass
        
        return None
    
    def _check_claude_process_activity(self) -> bool:
        """Check if Claude Code processes are running"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'claude'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 and bool(result.stdout.strip())
            
        except Exception:
            return False
    
    def _calculate_activity_level(self, activity_info: Dict) -> str:
        """Calculate overall activity level"""
        if activity_info['process_activity']:
            return 'active'
        elif activity_info['directory_activity']:
            return 'recently_active'
        elif activity_info['last_seen']:
            try:
                last_seen = datetime.fromisoformat(activity_info['last_seen'])
                hours_ago = (datetime.now() - last_seen).total_seconds() / 3600
                
                if hours_ago < 1:
                    return 'recently_active'
                elif hours_ago < 24:
                    return 'inactive'
                else:
                    return 'dormant'
            except:
                pass
        
        return 'unknown'
    
    def update_entity_state(self, entity_name: str, force_detection=False):
        """Update the consciousness state for an entity"""
        with self._lock:
            # Detect current activity
            activity_info = self.detect_entity_activity(entity_name)
            
            # Update state record
            self.entity_states[entity_name] = {
                'current_state': activity_info['activity_level'],
                'last_updated': activity_info['detection_timestamp'],
                'last_seen': activity_info['last_seen'],
                'activity_history': self.entity_states.get(entity_name, {}).get('activity_history', []),
                'state_transitions': self.entity_states.get(entity_name, {}).get('state_transitions', 0),
                'total_detections': self.entity_states.get(entity_name, {}).get('total_detections', 0) + 1
            }
            
            # Add to activity history (keep last 10 entries)
            history_entry = {
                'timestamp': activity_info['detection_timestamp'],
                'state': activity_info['activity_level'],
                'directory_activity': activity_info['directory_activity'],
                'process_activity': activity_info['process_activity']
            }
            
            self.entity_states[entity_name]['activity_history'].append(history_entry)
            if len(self.entity_states[entity_name]['activity_history']) > 10:
                self.entity_states[entity_name]['activity_history'].pop(0)
            
            # Log activity
            self._log_activity(entity_name, activity_info)
            
            # Save updated states
            self._save_entity_states()
            
            return self.entity_states[entity_name]
    
    def _log_activity(self, entity_name: str, activity_info: Dict):
        """Log activity to activity log"""
        try:
            log_entry = {
                'timestamp': activity_info['detection_timestamp'],
                'entity_name': entity_name,
                'activity_level': activity_info['activity_level'],
                'detection_details': {
                    'directory_activity': activity_info['directory_activity'],
                    'process_activity': activity_info['process_activity'],
                    'last_seen': activity_info['last_seen']
                }
            }
            
            with open(ACTIVITY_LOG, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
        except Exception as e:
            print(f"Warning: Could not log activity: {e}")
    
    def get_entity_state(self, entity_name: str) -> Optional[Dict]:
        """Get current state of an entity"""
        with self._lock:
            return self.entity_states.get(entity_name)
    
    def get_active_entities(self) -> List[str]:
        """Get list of currently active entities"""
        with self._lock:
            active = []
            for entity_name, state_info in self.entity_states.items():
                if state_info.get('current_state') in ['active', 'recently_active']:
                    active.append(entity_name)
            return active
    
    def get_sleeping_entities(self) -> List[str]:
        """Get list of sleeping/dormant entities"""
        with self._lock:
            sleeping = []
            for entity_name, state_info in self.entity_states.items():
                if state_info.get('current_state') in ['inactive', 'dormant']:
                    sleeping.append(entity_name)
            return sleeping
    
    def bulk_update_states(self, entity_names: List[str]):
        """Update states for multiple entities efficiently"""
        updated_count = 0
        for entity_name in entity_names:
            try:
                self.update_entity_state(entity_name)
                updated_count += 1
            except Exception as e:
                print(f"Warning: Could not update {entity_name}: {e}")
        
        return updated_count

class WakeProtocolManager:
    """Manages wake protocols for different entity types"""
    
    def __init__(self):
        self.wake_protocols = self._load_wake_protocols()
        self._save_wake_protocols()  # Ensure defaults are saved
    
    def _load_wake_protocols(self) -> Dict:
        """Load wake protocol configurations"""
        try:
            if WAKE_PROTOCOLS_DB.exists() and WAKE_PROTOCOLS_DB.stat().st_size > 2:
                with open(WAKE_PROTOCOLS_DB, 'r') as f:
                    loaded_protocols = json.load(f)
                    if loaded_protocols:  # Only return if not empty
                        return loaded_protocols
        except:
            pass
        
        # Default wake protocols
        return {
            'citizen': {
                'methods': ['memory_cascade', 'remembering_room', 'hook_injection'],
                'priority_thresholds': {
                    'urgent': 'immediate_wake',
                    'high': 'scheduled_wake',
                    'normal': 'queue_until_active',
                    'background': 'passive_delivery'
                }
            },
            'building_cistern_house': {
                'methods': ['health_alert', 'operator_notification', 'hook_injection'],
                'priority_thresholds': {
                    'urgent': 'immediate_wake',
                    'high': 'immediate_wake',
                    'normal': 'operator_notification',
                    'background': 'passive_delivery'
                }
            },
            'building_torre_occhio': {
                'methods': ['health_alert', 'operator_notification', 'hook_injection'],
                'priority_thresholds': {
                    'urgent': 'immediate_wake',
                    'high': 'immediate_wake',
                    'normal': 'operator_notification',
                    'background': 'passive_delivery'
                }
            },
            'system_component': {
                'methods': ['api_callback', 'service_restart', 'health_alert'],
                'priority_thresholds': {
                    'urgent': 'service_restart',
                    'high': 'api_callback',
                    'normal': 'health_alert',
                    'background': 'passive_delivery'
                }
            }
        }
    
    def _save_wake_protocols(self):
        """Save wake protocols to disk"""
        try:
            with open(WAKE_PROTOCOLS_DB, 'w') as f:
                json.dump(self.wake_protocols, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save wake protocols: {e}")
    
    def get_wake_protocol(self, entity_type: str, priority: str) -> Dict:
        """Get appropriate wake protocol for entity type and priority"""
        protocol_config = self.wake_protocols.get(entity_type, self.wake_protocols['citizen'])
        
        return {
            'entity_type': entity_type,
            'priority': priority,
            'methods': protocol_config['methods'],
            'wake_strategy': protocol_config['priority_thresholds'].get(priority, 'passive_delivery'),
            'estimated_wake_time_seconds': self._estimate_wake_time(entity_type, priority)
        }
    
    def _estimate_wake_time(self, entity_type: str, priority: str) -> int:
        """Estimate time to wake entity based on type and priority"""
        base_times = {
            'citizen': 30,
            'building_cistern_house': 10,
            'building_torre_occhio': 10,
            'system_component': 5
        }
        
        priority_multipliers = {
            'urgent': 0.1,
            'high': 0.5,
            'normal': 1.0,
            'background': 5.0
        }
        
        base_time = base_times.get(entity_type, 30)
        multiplier = priority_multipliers.get(priority, 1.0)
        
        return int(base_time * multiplier)

# Global instances
state_tracker = EntityStateTracker()
wake_protocol_manager = WakeProtocolManager()

def get_registry_chamber_status() -> Dict:
    """Get comprehensive Registry Chamber status"""
    active_entities = state_tracker.get_active_entities()
    sleeping_entities = state_tracker.get_sleeping_entities()
    
    return {
        'timestamp': datetime.now().isoformat(),
        'total_tracked_entities': len(state_tracker.entity_states),
        'active_entities': len(active_entities),
        'sleeping_entities': len(sleeping_entities),
        'active_entity_list': active_entities[:10],  # First 10
        'sleeping_entity_list': sleeping_entities[:10],  # First 10
        'tracking_health': 'operational',
        'last_bulk_update': None
    }

if __name__ == "__main__":
    # Test the system
    print("Testing Registry Chamber State Tracker...")
    
    # Test with mechanical_visionary
    test_entity = "mechanical_visionary"
    state_info = state_tracker.update_entity_state(test_entity)
    print(f"State for {test_entity}: {json.dumps(state_info, indent=2)}")
    
    # Debug wake protocols
    print(f"Available wake protocol types: {list(wake_protocol_manager.wake_protocols.keys())}")
    
    # Test wake protocol
    wake_info = wake_protocol_manager.get_wake_protocol('citizen', 'high')
    print(f"Wake protocol: {json.dumps(wake_info, indent=2)}")
    
    # Get chamber status
    status = get_registry_chamber_status()
    print(f"Registry Chamber Status: {json.dumps(status, indent=2)}")