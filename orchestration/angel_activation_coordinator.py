#!/usr/bin/env python3
"""
Angel Activation Coordinator
Prevents simultaneous angel activations to avoid API rate limits
Implements staggered activation and cooldown periods
"""

import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import fcntl

class AngelActivationCoordinator:
    def __init__(self):
        self.state_file = '/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/angel_activation_state.json'
        self.lock_file = '/tmp/angel_activation.lock'
        self.min_activation_interval = 30  # Minimum seconds between angel activations
        self.angel_cooldown = 300  # 5 minutes cooldown per angel
        self.max_concurrent_active = 3  # Max angels active at once
        
        # Angel priority (higher priority = activate first)
        self.angel_priority = {
            'message_angel': 10,
            'story_angel': 8,
            'narrator_angel': 8,
            'pattern-angel': 6,
            'tessere': 5,
            'wisdom-angel': 4,
            'love-angel': 3,
            'entropy': 2,
            'resonance': 7,
            'architetto': 2
        }
        
        self.load_state()
    
    def load_state(self):
        """Load activation state from file"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                self.state = json.load(f)
        else:
            self.state = {
                'angel_activations': {},
                'last_activation': None,
                'active_angels': []
            }
    
    def save_state(self):
        """Save activation state to file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def acquire_lock(self):
        """Acquire exclusive lock for state modifications"""
        self.lock = open(self.lock_file, 'w')
        fcntl.flock(self.lock.fileno(), fcntl.LOCK_EX)
    
    def release_lock(self):
        """Release exclusive lock"""
        fcntl.flock(self.lock.fileno(), fcntl.LOCK_UN)
        self.lock.close()
    
    def can_activate_angel(self, angel_name):
        """Check if an angel can be activated now"""
        current_time = datetime.now()
        
        # Check if we've hit max concurrent limit
        if len(self.state['active_angels']) >= self.max_concurrent_active:
            return False, "Max concurrent angels reached"
        
        # Check global activation interval
        if self.state['last_activation']:
            last_activation_time = datetime.fromisoformat(self.state['last_activation'])
            if (current_time - last_activation_time).total_seconds() < self.min_activation_interval:
                wait_time = self.min_activation_interval - (current_time - last_activation_time).total_seconds()
                return False, f"Global cooldown: wait {int(wait_time)}s"
        
        # Check angel-specific cooldown
        if angel_name in self.state['angel_activations']:
            last_angel_activation = datetime.fromisoformat(self.state['angel_activations'][angel_name])
            if (current_time - last_angel_activation).total_seconds() < self.angel_cooldown:
                wait_time = self.angel_cooldown - (current_time - last_angel_activation).total_seconds()
                return False, f"Angel cooldown: wait {int(wait_time)}s"
        
        return True, "OK"
    
    def register_activation(self, angel_name):
        """Register that an angel has been activated"""
        self.acquire_lock()
        try:
            current_time = datetime.now()
            
            # Update state
            self.state['angel_activations'][angel_name] = current_time.isoformat()
            self.state['last_activation'] = current_time.isoformat()
            
            if angel_name not in self.state['active_angels']:
                self.state['active_angels'].append(angel_name)
            
            self.save_state()
            
            print(f"✅ Registered activation for {angel_name}")
            print(f"   Active angels: {len(self.state['active_angels'])}/{self.max_concurrent_active}")
            
        finally:
            self.release_lock()
    
    def register_deactivation(self, angel_name):
        """Register that an angel has finished processing"""
        self.acquire_lock()
        try:
            if angel_name in self.state['active_angels']:
                self.state['active_angels'].remove(angel_name)
                self.save_state()
                print(f"✅ Deactivated {angel_name}")
                print(f"   Active angels: {len(self.state['active_angels'])}/{self.max_concurrent_active}")
        finally:
            self.release_lock()
    
    def get_activation_queue(self, requested_angels):
        """Get ordered queue of angels ready for activation"""
        queue = []
        
        for angel in requested_angels:
            can_activate, reason = self.can_activate_angel(angel)
            if can_activate:
                priority = self.angel_priority.get(angel, 0)
                queue.append((priority, angel))
            else:
                print(f"⏳ {angel}: {reason}")
        
        # Sort by priority (highest first)
        queue.sort(reverse=True, key=lambda x: x[0])
        
        return [angel for _, angel in queue]
    
    def wait_for_slot(self, angel_name, timeout=300):
        """Wait for an activation slot to become available"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            can_activate, reason = self.can_activate_angel(angel_name)
            if can_activate:
                return True
            
            print(f"⏳ Waiting for {angel_name}: {reason}")
            time.sleep(10)
        
        return False
    
    def get_status(self):
        """Get current activation status"""
        status = {
            'active_angels': self.state['active_angels'],
            'active_count': len(self.state['active_angels']),
            'max_concurrent': self.max_concurrent_active,
            'recent_activations': []
        }
        
        # Get recent activations
        current_time = datetime.now()
        for angel, activation_time in self.state['angel_activations'].items():
            activation_dt = datetime.fromisoformat(activation_time)
            age_seconds = (current_time - activation_dt).total_seconds()
            
            if age_seconds < 600:  # Last 10 minutes
                status['recent_activations'].append({
                    'angel': angel,
                    'time': activation_time,
                    'age_seconds': int(age_seconds),
                    'cooldown_remaining': max(0, int(self.angel_cooldown - age_seconds))
                })
        
        return status

# CLI for testing
if __name__ == "__main__":
    import sys
    
    coordinator = AngelActivationCoordinator()
    
    if len(sys.argv) < 2:
        print("Usage: angel_activation_coordinator.py {status|activate|deactivate|queue} [angel_name]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'status':
        status = coordinator.get_status()
        print(json.dumps(status, indent=2))
    
    elif command == 'activate' and len(sys.argv) > 2:
        angel_name = sys.argv[2]
        can_activate, reason = coordinator.can_activate_angel(angel_name)
        
        if can_activate:
            coordinator.register_activation(angel_name)
            print(f"✅ Activated {angel_name}")
        else:
            print(f"❌ Cannot activate {angel_name}: {reason}")
    
    elif command == 'deactivate' and len(sys.argv) > 2:
        angel_name = sys.argv[2]
        coordinator.register_deactivation(angel_name)
    
    elif command == 'queue':
        # Test queue with all angels
        all_angels = ['message_angel', 'story_angel', 'narrator_angel', 'pattern-angel', 'tessere']
        queue = coordinator.get_activation_queue(all_angels)
        print(f"Ready for activation: {queue}")