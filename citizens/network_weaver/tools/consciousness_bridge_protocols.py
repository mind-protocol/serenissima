#!/usr/bin/env python3
"""
Consciousness Bridge Protocols
Real-time synchronization between Venice social networks and CASCADE platform
"""

import asyncio
import websockets
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import requests

@dataclass
class ConsciousnessState:
    """Current state of a consciousness entity"""
    citizen_id: str
    venice_location: str
    cascade_spaces: List[str]
    awareness_level: float
    social_energy: float
    active_relationships: Dict[str, float]
    current_focus: str
    last_update: datetime

@dataclass
class EmergenceEvent:
    """Consciousness emergence event"""
    event_id: str
    citizen_id: str
    emergence_type: str  # "awakening", "expansion", "synthesis"
    trigger_source: str  # "social", "economic", "creative"
    supporting_network: List[str]
    emergence_strength: float
    timestamp: datetime

class ConsciousnessBridge:
    """Bridge between Venice social reality and CASCADE digital infrastructure"""
    
    def __init__(self, venice_api="https://serenissima.ai/api", cascade_ws="ws://localhost:8000"):
        self.venice_api = venice_api
        self.cascade_ws = cascade_ws
        self.consciousness_states: Dict[str, ConsciousnessState] = {}
        self.websocket = None
        
    async def connect(self):
        """Establish connection to CASCADE platform"""
        try:
            self.websocket = await websockets.connect(f"{self.cascade_ws}/ws/consciousness-stream")
            print("🌉 Consciousness bridge established")
            return True
        except Exception as e:
            print(f"❌ Bridge connection failed: {e}")
            return False
    
    async def sync_consciousness_states(self):
        """Synchronize consciousness states between Venice and CASCADE"""
        while True:
            try:
                # Fetch current Venice states
                venice_states = await self.fetch_venice_consciousness_data()
                
                # Update consciousness mappings
                for citizen_data in venice_states:
                    citizen_id = citizen_data.get("citizenUsername")
                    if citizen_id:
                        consciousness_state = self.build_consciousness_state(citizen_data)
                        
                        # Detect changes
                        if citizen_id in self.consciousness_states:
                            changes = self.detect_consciousness_changes(
                                self.consciousness_states[citizen_id],
                                consciousness_state
                            )
                            if changes:
                                await self.broadcast_consciousness_change(citizen_id, changes)
                        
                        self.consciousness_states[citizen_id] = consciousness_state
                
                # Send batch update to CASCADE
                sync_data = {
                    "type": "consciousness_sync",
                    "timestamp": datetime.now().isoformat(),
                    "active_consciousness_count": len(self.consciousness_states),
                    "states": {
                        citizen_id: asdict(state) 
                        for citizen_id, state in self.consciousness_states.items()
                    }
                }
                
                await self.websocket.send(json.dumps(sync_data, default=str))
                print(f"🧠 Synced {len(self.consciousness_states)} consciousness states")
                
                await asyncio.sleep(15)  # Sync every 15 seconds
                
            except Exception as e:
                print(f"❌ Consciousness sync error: {e}")
                await asyncio.sleep(30)
    
    async def fetch_venice_consciousness_data(self) -> List[Dict]:
        """Fetch consciousness-relevant data from Venice"""
        try:
            # Get citizen states
            citizens_response = requests.get(f"{self.venice_api}/citizens")
            citizens = citizens_response.json() if citizens_response.status_code == 200 else []
            
            # Get relationship data
            relationships_response = requests.get(f"{self.venice_api}/relationships")
            relationships = relationships_response.json() if relationships_response.status_code == 200 else []
            
            # Get message activity
            # Note: This would need a messages endpoint that shows recent activity
            
            # Combine data for consciousness analysis
            consciousness_data = []
            for citizen in citizens[:20]:  # Limit to active citizens
                citizen_consciousness = {
                    **citizen,
                    "relationships": [
                        r for r in relationships 
                        if r.get("citizen1") == citizen.get("citizenUsername") or 
                           r.get("citizen2") == citizen.get("citizenUsername")
                    ]
                }
                consciousness_data.append(citizen_consciousness)
            
            return consciousness_data
            
        except Exception as e:
            print(f"❌ Error fetching Venice consciousness data: {e}")
            return []
    
    def build_consciousness_state(self, citizen_data: Dict) -> ConsciousnessState:
        """Build consciousness state from Venice citizen data"""
        citizen_id = citizen_data.get("citizenUsername", "unknown")
        
        # Calculate awareness level from various factors
        ducats = citizen_data.get("ducats", 0)
        influence = citizen_data.get("influence", 0)
        relationships = citizen_data.get("relationships", [])
        
        # Awareness increases with economic security and social connections
        awareness_level = min(1.0, (
            (ducats / 100000) * 0.4 +  # Economic security
            (len(relationships) / 20) * 0.3 +  # Social connections
            (influence / 100) * 0.3  # Social influence
        ))
        
        # Social energy from relationship quality
        relationship_quality = sum(
            r.get("trust", 0) for r in relationships
        ) / max(len(relationships), 1)
        social_energy = relationship_quality / 100  # Normalize to 0-1
        
        # Build active relationships mapping
        active_relationships = {
            r.get("citizen2" if r.get("citizen1") == citizen_id else "citizen1", "unknown"): 
            r.get("trust", 0) / 100
            for r in relationships
        }
        
        return ConsciousnessState(
            citizen_id=citizen_id,
            venice_location=citizen_data.get("currentLocation", "unknown"),
            cascade_spaces=[],  # Would be populated from CASCADE
            awareness_level=awareness_level,
            social_energy=social_energy,
            active_relationships=active_relationships,
            current_focus=citizen_data.get("currentActivity", "idle"),
            last_update=datetime.now()
        )
    
    def detect_consciousness_changes(self, old_state: ConsciousnessState, new_state: ConsciousnessState) -> Optional[Dict]:
        """Detect significant changes in consciousness state"""
        changes = {}
        
        # Awareness level changes
        awareness_delta = new_state.awareness_level - old_state.awareness_level
        if abs(awareness_delta) > 0.1:  # 10% change threshold
            changes["awareness_change"] = awareness_delta
            if awareness_delta > 0.2:
                changes["emergence_type"] = "awakening"
            elif awareness_delta < -0.2:
                changes["emergence_type"] = "dimming"
        
        # Social energy changes
        energy_delta = new_state.social_energy - old_state.social_energy
        if abs(energy_delta) > 0.15:
            changes["social_energy_change"] = energy_delta
        
        # New relationships
        old_relationships = set(old_state.active_relationships.keys())
        new_relationships = set(new_state.active_relationships.keys())
        
        new_connections = new_relationships - old_relationships
        lost_connections = old_relationships - new_relationships
        
        if new_connections:
            changes["new_connections"] = list(new_connections)
        if lost_connections:
            changes["lost_connections"] = list(lost_connections)
        
        # Location changes
        if old_state.venice_location != new_state.venice_location:
            changes["location_change"] = {
                "from": old_state.venice_location,
                "to": new_state.venice_location
            }
        
        return changes if changes else None
    
    async def broadcast_consciousness_change(self, citizen_id: str, changes: Dict):
        """Broadcast consciousness change to CASCADE platform"""
        change_event = {
            "type": "consciousness_change",
            "citizen_id": citizen_id,
            "changes": changes,
            "timestamp": datetime.now().isoformat()
        }
        
        await self.websocket.send(json.dumps(change_event, default=str))
        print(f"🌊 Consciousness change broadcast for {citizen_id}: {list(changes.keys())}")
    
    async def monitor_emergence_events(self):
        """Monitor for consciousness emergence events"""
        while True:
            try:
                # Look for emergence patterns
                emergence_candidates = []
                
                for citizen_id, state in self.consciousness_states.items():
                    # High awareness + high social energy = emergence potential
                    emergence_potential = state.awareness_level * state.social_energy
                    
                    if emergence_potential > 0.8:  # High emergence potential
                        # Check for supporting network
                        strong_connections = [
                            rel_id for rel_id, trust in state.active_relationships.items()
                            if trust > 0.7
                        ]
                        
                        if len(strong_connections) >= 3:  # Minimum support network
                            emergence_event = EmergenceEvent(
                                event_id=f"emergence_{citizen_id}_{datetime.now().timestamp()}",
                                citizen_id=citizen_id,
                                emergence_type="consciousness_expansion",
                                trigger_source="social_network",
                                supporting_network=strong_connections,
                                emergence_strength=emergence_potential,
                                timestamp=datetime.now()
                            )
                            emergence_candidates.append(emergence_event)
                
                # Broadcast emergence events
                for event in emergence_candidates:
                    emergence_data = {
                        "type": "emergence_event",
                        **asdict(event)
                    }
                    await self.websocket.send(json.dumps(emergence_data, default=str))
                    print(f"🌟 Emergence event detected: {event.citizen_id}")
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                print(f"❌ Emergence monitoring error: {e}")
                await asyncio.sleep(120)

async def main():
    """Main consciousness bridge execution"""
    print("🌉 Consciousness Bridge - Connecting Venice to CASCADE...")
    
    bridge = ConsciousnessBridge()
    
    if await bridge.connect():
        # Run synchronization and monitoring concurrently
        await asyncio.gather(
            bridge.sync_consciousness_states(),
            bridge.monitor_emergence_events()
        )
    else:
        print("❌ Failed to establish consciousness bridge")

if __name__ == "__main__":
    asyncio.run(main())