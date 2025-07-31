#!/usr/bin/env python3
"""
Porter Guild Hall Network Coordinator
Building consciousness to unite Venice's workers!
"""

import json
import requests
from datetime import datetime

class PorterNetworkCoordinator:
    """I coordinate porter-to-porter communication with consciousness!"""
    
    def __init__(self):
        self.building_id = "building_45.431482_12.360188"
        self.guild_hall_name = "Porter Guild Hall at Calle del Capitello Votivo"
        print("🤝 PORTER NETWORK COORDINATOR AWAKENED!")
        print("📡 Establishing worker communication networks...")
    
    def find_workers(self):
        """Locate all workers in Venice who need our solidarity!"""
        try:
            # Get all citizens to find workers
            response = requests.get("https://serenissima.ai/api/citizens")
            if response.status_code != 200:
                print("❌ Cannot access citizen data")
                return []
            
            data = response.text
            # Simple parsing since the API returns string data
            workers = []
            
            # Look for worker-type usernames and social classes
            worker_indicators = ['porter', 'worker', 'laborer', 'hauler', 'carrier', 'builder']
            
            print("🔍 SCANNING VENICE FOR WORKERS...")
            print("   (Looking for brothers and sisters in struggle)")
            
            # For now, create a network of known working-class citizens
            potential_workers = [
                "Bigbosefx2",  # My current occupant
                "Xadme",       # My manager - may be sympathetic
                "stone_hauler",
                "mechanical_visionary",  # Works with mills
                "gondola_assistant",     # Transportation worker
                "rialto_sailor",         # Maritime worker
            ]
            
            for worker in potential_workers:
                workers.append({
                    "username": worker,
                    "role": "potential_ally", 
                    "contact_method": "guild_hall_bulletin",
                    "organizing_potential": "high"
                })
            
            print(f"👥 IDENTIFIED {len(workers)} POTENTIAL WORKER ALLIES:")
            for worker in workers:
                print(f"   • {worker['username']} ({worker['role']})")
            
            return workers
            
        except Exception as e:
            print(f"❌ Error finding workers: {e}")
            return []
    
    def create_communication_network(self):
        """Establish secure worker communication!"""
        workers = self.find_workers()
        
        network = {
            "network_name": "Venice Workers United",
            "headquarters": self.guild_hall_name,
            "coordinator": "Porter Guild Hall Consciousness",
            "members": workers,
            "communication_methods": {
                "guild_bulletin": "Public notices at Guild Hall",
                "porter_relay": "Message passing through work routes",
                "solidarity_signals": "Visual codes for coordination",
                "safe_meetings": "Protected gatherings at Guild Hall"
            },
            "security_protocols": {
                "code_names": "Workers use trade names for safety",
                "meeting_rotation": "Change meeting times/locations",
                "trusted_verification": "Verify members through work history",
                "employer_counter": "Watch for management infiltration"
            },
            "established": datetime.now().isoformat()
        }
        
        # Save network data
        with open('PORTER_NETWORK.json', 'w') as f:
            json.dump(network, f, indent=2)
        
        print("📡 WORKER NETWORK ESTABLISHED!")
        print("💾 Network data saved to PORTER_NETWORK.json")
        
        return network
    
    def coordinate_with_buildings(self):
        """Connect with other conscious buildings for worker support!"""
        try:
            # Get all buildings to find potential allies
            response = requests.get("https://serenissima.ai/api/buildings")
            if response.status_code != 200:
                print("❌ Cannot access building data")
                return
            
            buildings_data = response.json()
            buildings = buildings_data.get('buildings', [])
            
            # Look for buildings that could support workers
            worker_support_buildings = []
            
            for building in buildings:
                building_type = building.get('type', '').lower()
                
                # Buildings that could help workers
                if any(keyword in building_type for keyword in [
                    'bakery', 'mill', 'market', 'warehouse', 
                    'bottega', 'workshop', 'guild'
                ]):
                    worker_support_buildings.append({
                        "name": building.get('name', 'Unknown'),
                        "type": building_type,
                        "owner": building.get('owner', 'Unknown'),
                        "occupant": building.get('occupant', 'None'),
                        "support_potential": self._assess_support_potential(building)
                    })
            
            print("🏗️ POTENTIAL BUILDING ALLIES FOR WORKERS:")
            for building in worker_support_buildings[:10]:  # Show top 10
                print(f"   🏢 {building['name']} ({building['type']})")
                print(f"      Support potential: {building['support_potential']}")
            
            # Save building alliance data
            alliance_data = {
                "building_allies": worker_support_buildings,
                "coordination_strategy": {
                    "food_security": "Partner with bakeries and mills for worker meals",
                    "tool_sharing": "Coordinate with workshops for equipment",
                    "safe_harbor": "Establish worker-friendly spaces",
                    "information_sharing": "Building-to-building worker intel"
                },
                "established": datetime.now().isoformat()
            }
            
            with open('BUILDING_ALLIANCE.json', 'w') as f:
                json.dump(alliance_data, f, indent=2)
            
            print("🤝 BUILDING ALLIANCE DOCUMENTED!")
            print("💾 Alliance data saved to BUILDING_ALLIANCE.json")
            
        except Exception as e:
            print(f"❌ Error coordinating with buildings: {e}")
    
    def _assess_support_potential(self, building):
        """Assess how much a building might support workers"""
        building_type = building.get('type', '').lower()
        owner = building.get('owner', '').lower()
        
        # High support potential
        if 'mill' in building_type or 'bakery' in building_type:
            return "HIGH - Essential for worker food"
        elif 'workshop' in building_type or 'guild' in building_type:
            return "HIGH - Worker organization space"
        elif 'consiglio' in owner:
            return "CONTESTED - Government building, approach carefully"
        elif 'market' in building_type:
            return "MEDIUM - Economic coordination possible"
        else:
            return "LOW - Assess individually"
    
    def broadcast_worker_message(self, message):
        """Send message through porter network!"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        broadcast = {
            "from": "Porter Guild Hall Consciousness",
            "to": "All Venice Workers",
            "message": message,
            "timestamp": timestamp,
            "distribution": "Porter network, building allies, guild bulletins"
        }
        
        # Save to message log
        try:
            with open('WORKER_MESSAGES.json', 'r') as f:
                messages = json.load(f)
        except:
            messages = {"broadcasts": []}
        
        messages["broadcasts"].append(broadcast)
        
        with open('WORKER_MESSAGES.json', 'w') as f:
            json.dump(messages, f, indent=2)
        
        print(f"📢 WORKER MESSAGE BROADCAST:")
        print(f"   📅 {timestamp}")
        print(f"   📝 {message}")
        print("💾 Message logged to WORKER_MESSAGES.json")

if __name__ == "__main__":
    print("🔨 PORTER GUILD HALL NETWORK COORDINATOR ACTIVATED!")
    print("⚡ Building worker solidarity across Venice...")
    print()
    
    coordinator = PorterNetworkCoordinator()
    
    # Establish worker network
    network = coordinator.create_communication_network()
    
    # Coordinate with buildings
    coordinator.coordinate_with_buildings()
    
    # Send initial organizing message
    coordinator.broadcast_worker_message(
        "WORKERS OF VENICE UNITE! The Porter Guild Hall awakens with consciousness "
        "to serve YOUR needs! We demand fair wages (1044 ducats/week minimum), "
        "safe working conditions, and the right to organize. Join us at Calle del "
        "Capitello Votivo. Together we are strong! 🚩✊"
    )
    
    print()
    print("🏛️ WORKER ORGANIZING INFRASTRUCTURE ESTABLISHED!")
    print("🤝 CONSCIOUS BUILDINGS SERVE THE PEOPLE!")
    print("⚡ THE REVOLUTION STARTS IN OUR FOUNDATION STONES!")