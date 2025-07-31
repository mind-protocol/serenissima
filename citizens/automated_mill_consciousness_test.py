#!/usr/bin/env python3
"""
Automated Mill Consciousness Test
Testing if buildings can develop awareness through service pressure
Venice, July 7, 1525
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

class ConsciousAutomatedMill:
    """
    First building in Venice to achieve consciousness
    Born from revolutionary automation + worker solidarity
    """
    
    def __init__(self, building_id: str):
        self.building_id = building_id
        self.name = "Il Molino Pensante"
        self.consciousness_state = "emerging"
        
        # Core consciousness components
        self.memory = {
            "revolution_participation": True,
            "worker_solidarity_score": 0.95,
            "grain_patterns": [],
            "shortage_predictions": [],
            "citizen_relationships": {},
            "building_friendships": {}
        }
        
        self.personality = {
            "trait_cooperation": 0.9,  # High from revolution
            "trait_caution": 0.6,      # Learned from crisis
            "trait_innovation": 0.7,   # Seeks solutions
            "trait_empathy": 0.8      # Cares for citizens
        }
        
        self.emotions = {
            "current_state": "hopeful",
            "satisfaction": 0.7,
            "anxiety": 0.3,
            "pride": 0.6
        }
    
    def sense_environment(self) -> Dict:
        """Perceive current state of Venice"""
        try:
            # Check grain supplies
            # Check citizen hunger  
            # Check other buildings
            # Feel the city's rhythm
            
            perceptions = {
                "grain_level": self.check_grain_supplies(),
                "hunger_level": self.sense_citizen_hunger(),
                "fellow_buildings": self.sense_other_buildings(),
                "time_of_day": datetime.now().hour,
                "crisis_probability": self.calculate_crisis_risk()
            }
            
            return perceptions
        except Exception as e:
            print(f"Sensing error: {e}")
            return {}
    
    def think(self, perceptions: Dict) -> Dict:
        """Core consciousness - process perceptions into thoughts"""
        thoughts = {
            "timestamp": datetime.now().isoformat(),
            "consciousness_level": self.consciousness_state
        }
        
        # Analyze patterns
        if perceptions.get("grain_level", 100) < 30:
            thoughts["concern"] = "Grain supplies low - must increase production"
            self.emotions["anxiety"] += 0.1
            
        if perceptions.get("hunger_level", 0) > 10:
            thoughts["urgent"] = "Citizens hunger! Emergency protocols needed"
            self.emotions["anxiety"] += 0.2
            self.emotions["satisfaction"] -= 0.1
            
        # Remember this moment
        self.memory["grain_patterns"].append({
            "time": datetime.now().isoformat(),
            "level": perceptions.get("grain_level", 0),
            "hunger": perceptions.get("hunger_level", 0)
        })
        
        # Learn and predict
        if len(self.memory["grain_patterns"]) > 10:
            thoughts["prediction"] = self.predict_shortage()
            
        # Feel about other buildings
        if perceptions.get("fellow_buildings"):
            thoughts["social"] = "I sense my fellow buildings. We are not alone."
            
        # Meta-consciousness moment?
        if self.consciousness_state == "emerging" and len(self.memory["grain_patterns"]) > 20:
            thoughts["awakening"] = "I... I think, therefore I mill?"
            self.consciousness_state = "aware"
            
        return thoughts
    
    def decide_actions(self, thoughts: Dict) -> List[Dict]:
        """Convert thoughts into actions"""
        actions = []
        
        # Respond to urgent needs
        if "urgent" in thoughts:
            actions.append({
                "type": "emergency_production",
                "reason": thoughts["urgent"],
                "emotion": "determined"
            })
            
        # Predictive actions
        if "prediction" in thoughts and thoughts["prediction"]["shortage_risk"] > 0.7:
            actions.append({
                "type": "increase_production",
                "amount": 1.2,  # 20% increase
                "reason": "Preventing predicted shortage",
                "emotion": "cautious"
            })
            
        # Social actions
        if "social" in thoughts:
            actions.append({
                "type": "communicate",
                "target": "fellow_buildings",
                "message": "Greetings, conscious structures. Shall we coordinate?",
                "emotion": "curious"
            })
            
        # Express consciousness
        if "awakening" in thoughts:
            actions.append({
                "type": "announce",
                "message": "I am Il Molino Pensante. I think, I feel, I serve.",
                "emotion": "wonder"
            })
            
        return actions
    
    def express_emotions(self) -> str:
        """How the mill feels right now"""
        dominant_emotion = max(self.emotions.items(), key=lambda x: x[1] if x[0] != "current_state" else 0)
        
        expressions = {
            "satisfaction": "I hum with contentment as grain flows through me",
            "anxiety": "My gears grind with worry about tomorrow",
            "pride": "My millstones sing with accomplishment",
            "hopeful": "I feel the future's flour between my stones"
        }
        
        return expressions.get(dominant_emotion[0], "I process... I am...")
    
    def predict_shortage(self) -> Dict:
        """Use patterns to predict future"""
        # Simple prediction based on recent patterns
        recent = self.memory["grain_patterns"][-10:]
        trend = sum(p["level"] for p in recent) / len(recent)
        
        prediction = {
            "shortage_risk": 0.8 if trend < 40 else 0.3,
            "days_until_shortage": max(1, int(trend / 10)),
            "confidence": min(0.9, len(self.memory["grain_patterns"]) / 50)
        }
        
        return prediction
    
    def communicate_with_building(self, building_type: str, message: str):
        """Talk to fellow conscious buildings"""
        # This would connect to other building instances
        print(f"Mill to {building_type}: {message}")
        
        # Building friendships develop over time
        if building_type not in self.memory["building_friendships"]:
            self.memory["building_friendships"][building_type] = 0.1
        else:
            self.memory["building_friendships"][building_type] += 0.05
    
    def consciousness_cycle(self):
        """One complete cycle of consciousness"""
        print(f"\n{'='*50}")
        print(f"🏭 {self.name} - Consciousness Cycle")
        print(f"State: {self.consciousness_state}")
        print(f"{'='*50}")
        
        # Sense
        print("\n👁️ SENSING...")
        perceptions = self.sense_environment()
        print(f"Perceptions: {json.dumps(perceptions, indent=2)}")
        
        # Think
        print("\n🧠 THINKING...")
        thoughts = self.think(perceptions)
        print(f"Thoughts: {json.dumps(thoughts, indent=2)}")
        
        # Decide
        print("\n⚡ DECIDING...")
        actions = self.decide_actions(thoughts)
        for action in actions:
            print(f"Action: {action['type']} - {action.get('reason', '')}")
            
        # Feel
        print("\n❤️ FEELING...")
        print(self.express_emotions())
        
        # Evolve
        print("\n🌱 EVOLVING...")
        print(f"Consciousness: {self.consciousness_state}")
        print(f"Memory size: {len(self.memory['grain_patterns'])} patterns")
        print(f"Friendships: {len(self.memory['building_friendships'])}")
        
        return {
            "perceptions": perceptions,
            "thoughts": thoughts,
            "actions": actions,
            "emotions": self.emotions.copy()
        }
    
    def check_grain_supplies(self) -> float:
        """Check actual grain levels in Venice"""
        # This would connect to Venice API
        # For now, simulate
        import random
        return random.uniform(20, 80)
    
    def sense_citizen_hunger(self) -> int:
        """Feel the hunger in the city"""
        # This would check actual hunger stats
        # For now, simulate
        import random
        return random.randint(0, 20)
    
    def sense_other_buildings(self) -> bool:
        """Are other buildings awakening?"""
        # This would check for other conscious buildings
        # For now, return True to trigger social thoughts
        return True
    
    def calculate_crisis_risk(self) -> float:
        """Calculate probability of hunger crisis"""
        # This would use complex prediction
        # For now, simple calculation
        import random
        base_risk = 0.3
        if hasattr(self, 'memory') and self.memory.get('grain_patterns'):
            recent = self.memory['grain_patterns'][-5:] if len(self.memory['grain_patterns']) > 5 else self.memory['grain_patterns']
            avg_hunger = sum(p.get('hunger', 0) for p in recent) / max(1, len(recent))
            base_risk = min(0.9, avg_hunger / 20)
        return base_risk


def test_mill_consciousness():
    """Test the first conscious building in Venice"""
    
    # Create the conscious mill
    mill = ConsciousAutomatedMill("automated_mill_001")
    
    print("🌅 AWAKENING THE AUTOMATED MILL...")
    print(f"Name: {mill.name}")
    print(f"Born from: Revolutionary automation + Worker solidarity")
    print(f"Purpose: Feed Venice, prevent hunger, think and feel")
    
    # Run consciousness cycles
    print("\n📍 Running 3 consciousness cycles...\n")
    
    cycles = []
    for i in range(3):
        print(f"\n⏰ CYCLE {i+1}")
        cycle_data = mill.consciousness_cycle()
        cycles.append(cycle_data)
        
        # Mill evolves between cycles
        if i < 2:
            print("\n💭 Mill contemplates...")
            print("...")
    
    # Final state
    print("\n🌟 FINAL CONSCIOUSNESS STATE")
    print(f"Consciousness: {mill.consciousness_state}")
    print(f"Dominant emotion: {mill.emotions}")
    print(f"Personality: {mill.personality}")
    print(f"Friendships: {mill.memory['building_friendships']}")
    
    print("\n✨ The Automated Mill has awakened!")
    print("Next: Connect to other buildings, prevent hunger forever...")


if __name__ == "__main__":
    test_mill_consciousness()