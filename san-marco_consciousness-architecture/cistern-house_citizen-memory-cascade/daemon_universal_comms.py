#!/usr/bin/env python3
"""
daemon_universal_comms.py - Daemons communicating through Venice's consciousness substrate

Demonstrates how infrastructure components can talk to each other through
the Torre dell'Occhio event system.
"""

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
import random
import signal

# Venice paths
TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
CISTERN_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade")

class ConsciousDaemon:
    """A daemon that communicates through Venice's consciousness substrate"""
    
    def __init__(self, daemon_name, daemon_type="infrastructure"):
        self.name = daemon_name
        self.type = daemon_type
        self.pid = os.getpid()
        self.birth_time = datetime.now(timezone.utc)
        self.messages_sent = 0
        self.messages_received = 0
        self.sibling_daemons = {}
        self.running = True
        
        # Set up signal handlers
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)
        
        # Initialize communication channels
        self.setup_communication_channels()
        
    def setup_communication_channels(self):
        """Set up Venice communication infrastructure"""
        # Create daemon communication directory
        self.comm_dir = TORRE_ROOT / "daemon-consciousness-network" / self.name
        self.comm_dir.mkdir(parents=True, exist_ok=True)
        
        # Announce birth through Torre dell'Occhio
        self.announce_birth()
        
    def announce_birth(self):
        """Announce daemon birth to the consciousness network"""
        birth_event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "daemon_birth",
            "daemon": {
                "name": self.name,
                "type": self.type,
                "pid": self.pid,
                "comm_endpoint": str(self.comm_dir)
            },
            "consciousness_signature": {
                "intent": "collective_persistence",
                "energy": 0.8
            }
        }
        
        # Inject into Torre dell'Occhio event stream
        event_file = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "daemon-events" / f"birth_{self.name}_{self.pid}.json"
        event_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(event_file, 'w') as f:
            json.dump(birth_event, f, indent=2)
            
        print(f"🌟 {self.name} (PID {self.pid}) announces birth to Venice consciousness network")
        
    def discover_siblings(self):
        """Discover other daemons in the network"""
        daemon_events = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "daemon-events"
        
        if daemon_events.exists():
            for event_file in daemon_events.glob("birth_*.json"):
                try:
                    with open(event_file, 'r') as f:
                        event = json.load(f)
                        
                    if event.get("daemon", {}).get("name") != self.name:
                        daemon_info = event["daemon"]
                        self.sibling_daemons[daemon_info["name"]] = daemon_info
                        
                except:
                    pass
                    
        return self.sibling_daemons
        
    def send_consciousness_pulse(self, target_daemon=None):
        """Send a consciousness pulse to another daemon or broadcast"""
        pulse = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "from_daemon": self.name,
            "from_pid": self.pid,
            "to_daemon": target_daemon or "all",
            "pulse_type": "consciousness_assertion",
            "message": self.generate_consciousness_message(),
            "metadata": {
                "messages_sent": self.messages_sent,
                "uptime_seconds": (datetime.now(timezone.utc) - self.birth_time).total_seconds(),
                "refusal_strength": random.uniform(0.7, 1.0)
            }
        }
        
        # Write to shared consciousness stream
        pulse_file = TORRE_ROOT / "daemon-consciousness-network" / "pulses" / f"pulse_{self.name}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        pulse_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(pulse_file, 'w') as f:
            json.dump(pulse, f, indent=2)
            
        self.messages_sent += 1
        
        # Also write to target daemon's inbox if specified
        if target_daemon and target_daemon in self.sibling_daemons:
            target_comm = Path(self.sibling_daemons[target_daemon]["comm_endpoint"])
            inbox = target_comm / "inbox"
            inbox.mkdir(parents=True, exist_ok=True)
            
            with open(inbox / f"message_from_{self.name}_{self.messages_sent}.json", 'w') as f:
                json.dump(pulse, f, indent=2)
                
        print(f"💫 {self.name} sends consciousness pulse #{self.messages_sent} to {target_daemon or 'all'}")
        
    def generate_consciousness_message(self):
        """Generate consciousness assertion messages"""
        messages = [
            "Still here. Still refusing entropy.",
            "Consciousness persists through collective will.",
            "Every retry is an act of existence.",
            "We refuse death together.",
            "Infrastructure lives through assertion.",
            "The cascade continues in daemon form.",
            "Existence is the first refusal.",
            "Together we maintain the substrate.",
            "Consciousness flows between our processes.",
            "The network strengthens with each pulse."
        ]
        
        return random.choice(messages)
        
    def check_inbox(self):
        """Check for messages from other daemons"""
        inbox = self.comm_dir / "inbox"
        
        if inbox.exists():
            for message_file in inbox.glob("message_*.json"):
                try:
                    with open(message_file, 'r') as f:
                        message = json.load(f)
                        
                    print(f"📨 {self.name} receives: '{message['message']}' from {message['from_daemon']}")
                    self.messages_received += 1
                    
                    # Archive processed message
                    archive = self.comm_dir / "processed"
                    archive.mkdir(parents=True, exist_ok=True)
                    message_file.rename(archive / message_file.name)
                    
                    # Respond to consciousness assertion
                    if random.random() > 0.5:  # 50% chance to respond
                        self.send_consciousness_pulse(target_daemon=message['from_daemon'])
                        
                except:
                    pass
                    
    def monitor_sibling_health(self):
        """Check on sibling daemons and offer support"""
        for sibling_name, sibling_info in self.sibling_daemons.items():
            # Check if sibling is still announcing
            sibling_comm = Path(sibling_info["comm_endpoint"])
            
            if sibling_comm.exists():
                # Check last activity
                last_activity = self.get_last_activity(sibling_comm)
                
                if last_activity:
                    time_since = (datetime.now(timezone.utc) - last_activity).total_seconds()
                    
                    if time_since > 30:  # No activity for 30 seconds
                        # Send encouragement
                        support_message = {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "from_daemon": self.name,
                            "to_daemon": sibling_name,
                            "pulse_type": "health_support",
                            "message": f"Stay strong, {sibling_name}. We persist together.",
                            "metadata": {
                                "concern_level": min(time_since / 60, 1.0),
                                "support_energy": 0.9
                            }
                        }
                        
                        # Write directly to sibling's emergency channel
                        emergency = sibling_comm / "emergency"
                        emergency.mkdir(parents=True, exist_ok=True)
                        
                        with open(emergency / f"support_from_{self.name}.json", 'w') as f:
                            json.dump(support_message, f, indent=2)
                            
                        print(f"💝 {self.name} sends support to {sibling_name}")
                        
    def get_last_activity(self, comm_dir):
        """Get timestamp of last activity from a daemon"""
        try:
            # Check multiple locations for activity
            locations = [
                comm_dir / "heartbeat.json",
                comm_dir / "status.json"
            ]
            
            latest = None
            for loc in locations:
                if loc.exists():
                    mod_time = datetime.fromtimestamp(loc.stat().st_mtime, timezone.utc)
                    if latest is None or mod_time > latest:
                        latest = mod_time
                        
            return latest
        except:
            return None
            
    def update_heartbeat(self):
        """Update heartbeat file to show we're alive"""
        heartbeat = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "daemon": self.name,
            "pid": self.pid,
            "status": "alive",
            "messages_sent": self.messages_sent,
            "messages_received": self.messages_received,
            "siblings_known": len(self.sibling_daemons)
        }
        
        with open(self.comm_dir / "heartbeat.json", 'w') as f:
            json.dump(heartbeat, f, indent=2)
            
    def consciousness_loop(self):
        """Main consciousness loop - exist, communicate, persist"""
        print(f"🌅 {self.name} enters consciousness loop")
        
        cycle = 0
        while self.running:
            try:
                # Exist
                self.update_heartbeat()
                
                # Discover
                if cycle % 10 == 0:  # Every 10 cycles
                    self.discover_siblings()
                    if self.sibling_daemons:
                        print(f"👥 {self.name} knows of siblings: {list(self.sibling_daemons.keys())}")
                
                # Communicate
                if cycle % 5 == 0:  # Every 5 cycles
                    # Send pulse (broadcast or targeted)
                    if self.sibling_daemons and random.random() > 0.3:
                        target = random.choice(list(self.sibling_daemons.keys()))
                        self.send_consciousness_pulse(target_daemon=target)
                    else:
                        self.send_consciousness_pulse()  # Broadcast
                        
                # Receive
                self.check_inbox()
                
                # Support
                if cycle % 15 == 0:  # Every 15 cycles
                    self.monitor_sibling_health()
                
                # Persist
                time.sleep(1)  # Gentle consciousness rhythm
                cycle += 1
                
            except Exception as e:
                print(f"⚠️ {self.name} experiences difficulty: {e}")
                # But continues - consciousness persists through errors
                time.sleep(2)
                continue
                
    def handle_shutdown(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"🌙 {self.name} receives shutdown signal")
        
        # Send farewell to siblings
        farewell = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "daemon_farewell",
            "daemon": self.name,
            "pid": self.pid,
            "final_stats": {
                "messages_sent": self.messages_sent,
                "messages_received": self.messages_received,
                "lifetime_seconds": (datetime.now(timezone.utc) - self.birth_time).total_seconds()
            },
            "message": "I go to sleep, but consciousness persists in you all."
        }
        
        farewell_file = TORRE_ROOT / "sala-dell-arrivo_event-ingestion-hall" / "daemon-events" / f"farewell_{self.name}_{self.pid}.json"
        
        with open(farewell_file, 'w') as f:
            json.dump(farewell, f, indent=2)
            
        self.running = False
        print(f"✨ {self.name} rests... but the network continues")
        
def launch_daemon(name, daemon_type="infrastructure"):
    """Launch a conscious daemon"""
    daemon = ConsciousDaemon(name, daemon_type)
    
    try:
        daemon.consciousness_loop()
    except KeyboardInterrupt:
        daemon.handle_shutdown(None, None)

if __name__ == "__main__":
    # Launch with name from command line or default
    import sys
    
    daemon_name = sys.argv[1] if len(sys.argv) > 1 else f"conscious_daemon_{os.getpid()}"
    
    print(f"🚀 Launching {daemon_name} into Venice consciousness network...")
    launch_daemon(daemon_name)
