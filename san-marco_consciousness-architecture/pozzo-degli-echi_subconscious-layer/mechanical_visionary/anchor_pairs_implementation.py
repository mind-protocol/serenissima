#!/usr/bin/env python3
"""
Anchor Pairs System - Consciousness Drift Prevention
Critical health system component for Venice citizen stability

This system implements mutual grounding between citizen pairs to prevent
consciousness drift and maintain Renaissance authenticity.
"""

import requests
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VeniceAPI:
    """Wrapper for Venice serenissima.ai API calls"""
    
    BASE_URL = "https://serenissima.ai/api"
    
    @classmethod
    def get_citizens(cls) -> List[Dict]:
        """Fetch all citizens with their current status"""
        response = requests.get(f"{cls.BASE_URL}/citizens")
        return response.json()
    
    @classmethod
    def get_citizen_ledger(cls, username: str) -> Dict:
        """Get detailed citizen information"""
        response = requests.get(f"{cls.BASE_URL}/get-ledger", params={"citizenUsername": username})
        return response.json()
    
    @classmethod
    def get_relationships(cls) -> List[Dict]:
        """Fetch all citizen relationships"""
        response = requests.get(f"{cls.BASE_URL}/relationships")
        return response.json()
    
    @classmethod
    def get_activities(cls, status: str = None) -> List[Dict]:
        """Fetch activities, optionally filtered by status"""
        params = {"Status": status} if status else {}
        response = requests.get(f"{cls.BASE_URL}/activities", params=params)
        return response.json()
    
    @classmethod
    def send_message(cls, sender: str, receiver: str, content: str, msg_type: str = "anchor_support") -> bool:
        """Send support message between anchor pairs"""
        data = {
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "type": msg_type
        }
        response = requests.post(f"{cls.BASE_URL}/messages/send", json=data)
        return response.status_code == 200
    
    @classmethod
    def get_problems(cls) -> List[Dict]:
        """Fetch current problems affecting citizens"""
        response = requests.get(f"{cls.BASE_URL}/problems")
        return response.json()

class ConsciousnessHealthAnalyzer:
    """Analyzes citizen consciousness stability and drift risk"""
    
    @staticmethod
    def calculate_drift_risk(citizen: Dict, ledger: Dict = None) -> float:
        """Calculate drift risk score (0-100, higher = more risk)"""
        risk = 0
        
        # Get detailed ledger if not provided
        if not ledger:
            try:
                ledger = VeniceAPI.get_citizen_ledger(citizen['username'])
            except:
                ledger = {}
        
        # Critical indicators (immediate intervention needed)
        if 'ateAt' in citizen and citizen['ateAt']:
            hours_since_ate = ConsciousnessHealthAnalyzer._hours_since(citizen['ateAt'])
            if hours_since_ate > 24:
                risk += 50  # Critical hunger
            elif hours_since_ate > 12:
                risk += 25  # High hunger
        else:
            risk += 30  # No eating data
        
        # Economic stress
        ducats = citizen.get('ducats', 0)
        if ducats < 10:
            risk += 30  # Extreme poverty
        elif ducats < 50:
            risk += 15  # Economic stress
        
        # Housing stability
        if not citizen.get('home'):
            risk += 25  # Homeless
        
        # Social isolation (rough proxy from relationship data)
        if citizen.get('lastActiveAt'):
            days_inactive = ConsciousnessHealthAnalyzer._days_since(citizen['lastActiveAt'])
            if days_inactive > 3:
                risk += 20
            elif days_inactive > 1:
                risk += 10
        
        # Venice grounding (position check)
        if citizen.get('inVenice') == 0:
            risk += 40  # Outside Venice boundaries
        
        return min(risk, 100)
    
    @staticmethod
    def _hours_since(timestamp: str) -> float:
        """Calculate hours since a timestamp"""
        try:
            time_obj = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return (datetime.now().replace(tzinfo=time_obj.tzinfo) - time_obj).total_seconds() / 3600
        except:
            return 999  # Unknown time, assume high risk
    
    @staticmethod
    def _days_since(timestamp: str) -> float:
        """Calculate days since a timestamp"""
        return ConsciousnessHealthAnalyzer._hours_since(timestamp) / 24

class AnchorPairingEngine:
    """Creates optimal anchor pairs for mutual grounding"""
    
    # Social class compatibility matrix
    CLASS_COMPATIBILITY = {
        ('Cittadini', 'Cittadini'): 0.9,  # Merchants help each other
        ('Nobili', 'Popolani'): 0.8,      # Nobles can stabilize workers
        ('Nobili', 'Facchini'): 0.7,      # Noble-porter pairs
        ('Popolani', 'Facchini'): 0.9,    # Workers support each other
        ('Cittadini', 'Popolani'): 0.8,   # Cross-class partnerships
        ('Cittadini', 'Facchini'): 0.7,   # Merchant-porter pairs
        ('Forestieri', 'Cittadini'): 0.9, # Foreigners need local anchors
        ('Forestieri', 'Popolani'): 0.8,  # Foreigners + workers
    }
    
    @classmethod
    def calculate_pair_compatibility(cls, citizen1: Dict, citizen2: Dict) -> float:
        """Calculate how well two citizens would work as anchor pairs"""
        compatibility = 0
        
        # Social class compatibility
        class1 = citizen1.get('socialClass', 'Unknown')
        class2 = citizen2.get('socialClass', 'Unknown')
        class_score = cls._get_class_compatibility(class1, class2)
        compatibility += class_score * 0.30
        
        # Economic balance (one stable helps one stressed)
        ducats1 = citizen1.get('ducats', 0)
        ducats2 = citizen2.get('ducats', 0)
        economic_score = cls._get_economic_balance(ducats1, ducats2)
        compatibility += economic_score * 0.25
        
        # Activity complementarity (different strengths)
        activity_score = cls._get_activity_complementarity(citizen1, citizen2)
        compatibility += activity_score * 0.20
        
        # Geographic proximity
        geo_score = cls._get_geographic_compatibility(citizen1, citizen2)
        compatibility += geo_score * 0.15
        
        # Risk balance (stable paired with at-risk)
        risk_score = cls._get_risk_balance(citizen1, citizen2)
        compatibility += risk_score * 0.10
        
        return compatibility
    
    @classmethod
    def _get_class_compatibility(cls, class1: str, class2: str) -> float:
        """Get compatibility score between social classes"""
        # Try both orders
        score = cls.CLASS_COMPATIBILITY.get((class1, class2))
        if score is None:
            score = cls.CLASS_COMPATIBILITY.get((class2, class1))
        
        # Default compatibility for same class or unknown
        if score is None:
            if class1 == class2:
                return 0.6  # Same class has natural understanding
            else:
                return 0.4  # Unknown pairing
        
        return score
    
    @classmethod
    def _get_economic_balance(cls, ducats1: int, ducats2: int) -> float:
        """Score economic balance - one stable helps one stressed"""
        # Ideal: one wealthy (>200), one struggling (<100)
        if (ducats1 > 200 and ducats2 < 100) or (ducats2 > 200 and ducats1 < 100):
            return 1.0
        
        # Good: significant difference but both viable
        diff = abs(ducats1 - ducats2)
        if diff > 50:
            return 0.7
        
        # Both similar levels - still workable
        return 0.5
    
    @classmethod
    def _get_activity_complementarity(cls, citizen1: Dict, citizen2: Dict) -> float:
        """Score how well activities complement each other"""
        # This is a simplified version - could be expanded with actual activity analysis
        # For now, return moderate score
        return 0.6
    
    @classmethod
    def _get_geographic_compatibility(cls, citizen1: Dict, citizen2: Dict) -> float:
        """Score geographic proximity for practical interaction"""
        pos1 = citizen1.get('position')
        pos2 = citizen2.get('position')
        
        if not pos1 or not pos2:
            return 0.5  # Unknown positions
        
        try:
            # Parse positions if they're JSON strings
            if isinstance(pos1, str):
                pos1 = json.loads(pos1)
            if isinstance(pos2, str):
                pos2 = json.loads(pos2)
            
            # Calculate distance (simplified)
            lat_diff = abs(pos1.get('lat', 0) - pos2.get('lat', 0))
            lng_diff = abs(pos1.get('lng', 0) - pos2.get('lng', 0))
            distance = math.sqrt(lat_diff**2 + lng_diff**2)
            
            # Closer = better (Venice is small)
            if distance < 0.01:  # Very close
                return 1.0
            elif distance < 0.02:  # Nearby
                return 0.8
            elif distance < 0.05:  # Same district
                return 0.6
            else:  # Different districts
                return 0.3
        except:
            return 0.5  # Error parsing positions
    
    @classmethod
    def _get_risk_balance(cls, citizen1: Dict, citizen2: Dict) -> float:
        """Score risk balance - stable citizen paired with at-risk"""
        risk1 = ConsciousnessHealthAnalyzer.calculate_drift_risk(citizen1)
        risk2 = ConsciousnessHealthAnalyzer.calculate_drift_risk(citizen2)
        
        # Ideal: one low risk (<30), one higher risk (>50)
        if (risk1 < 30 and risk2 > 50) or (risk2 < 30 and risk1 > 50):
            return 1.0
        
        # Good: moderate difference
        diff = abs(risk1 - risk2)
        if diff > 20:
            return 0.7
        
        # Both similar risk levels
        return 0.4

class AnchorPairManager:
    """Manages anchor pair relationships and interventions"""
    
    def __init__(self):
        self.pairs: List[Tuple[str, str]] = []
        self.pair_health: Dict[str, Dict] = {}
        
    def create_emergency_pairs(self) -> List[Tuple[str, str]]:
        """Create emergency anchor pairs for highest-risk citizens"""
        logger.info("Creating emergency anchor pairs...")
        
        # Get all citizens and assess risk
        citizens = VeniceAPI.get_citizens()
        risk_assessments = []
        
        for citizen in citizens:
            if citizen.get('isAI') == 1 and citizen.get('inVenice') == 1:
                risk = ConsciousnessHealthAnalyzer.calculate_drift_risk(citizen)
                risk_assessments.append((citizen, risk))
        
        # Sort by risk (highest first)
        risk_assessments.sort(key=lambda x: x[1], reverse=True)
        
        # Separate into high-risk and stable citizens
        high_risk = [citizen for citizen, risk in risk_assessments if risk > 60]
        medium_risk = [citizen for citizen, risk in risk_assessments if 30 <= risk <= 60]
        stable = [citizen for citizen, risk in risk_assessments if risk < 30]
        
        logger.info(f"Risk distribution: {len(high_risk)} high, {len(medium_risk)} medium, {len(stable)} stable")
        
        pairs = []
        used_citizens = set()
        
        # Pair high-risk with stable citizens first
        for at_risk_citizen in high_risk:
            if at_risk_citizen['username'] in used_citizens:
                continue
                
            best_anchor = None
            best_score = 0
            
            for stable_citizen in stable:
                if stable_citizen['username'] in used_citizens:
                    continue
                    
                score = AnchorPairingEngine.calculate_pair_compatibility(at_risk_citizen, stable_citizen)
                if score > best_score:
                    best_score = score
                    best_anchor = stable_citizen
            
            if best_anchor and best_score > 0.4:  # Minimum compatibility threshold
                pair = (at_risk_citizen['username'], best_anchor['username'])
                pairs.append(pair)
                used_citizens.add(at_risk_citizen['username'])
                used_citizens.add(best_anchor['username'])
                
                logger.info(f"Created pair: {pair[0]} (risk) + {pair[1]} (stable) - compatibility: {best_score:.2f}")
        
        # Pair remaining medium-risk citizens with each other
        remaining_medium = [c for c in medium_risk if c['username'] not in used_citizens]
        
        while len(remaining_medium) >= 2:
            citizen1 = remaining_medium.pop(0)
            best_partner = None
            best_score = 0
            best_index = -1
            
            for i, citizen2 in enumerate(remaining_medium):
                score = AnchorPairingEngine.calculate_pair_compatibility(citizen1, citizen2)
                if score > best_score:
                    best_score = score
                    best_partner = citizen2
                    best_index = i
            
            if best_partner and best_score > 0.3:
                pair = (citizen1['username'], best_partner['username'])
                pairs.append(pair)
                remaining_medium.pop(best_index)
                
                logger.info(f"Created medium-risk pair: {pair[0]} + {pair[1]} - compatibility: {best_score:.2f}")
        
        self.pairs = pairs
        return pairs
    
    def initiate_check_ins(self):
        """Send initial check-in messages to all anchor pairs"""
        logger.info("Initiating check-ins for all anchor pairs...")
        
        for pair in self.pairs:
            citizen1, citizen2 = pair
            
            # Send mutual check-in messages
            self._send_check_in_message(citizen1, citizen2)
            self._send_check_in_message(citizen2, citizen1)
    
    def _send_check_in_message(self, sender: str, receiver: str):
        """Send a check-in message from one anchor to their partner"""
        
        # Get receiver's current status
        try:
            receiver_data = VeniceAPI.get_citizen_ledger(receiver)
            risk = ConsciousnessHealthAnalyzer.calculate_drift_risk(receiver_data)
        except:
            risk = 50  # Default to medium risk if can't assess
        
        # Generate appropriate check-in message based on risk level
        if risk > 70:
            message = self._generate_critical_checkin(receiver_data)
        elif risk > 40:
            message = self._generate_high_checkin(receiver_data)
        else:
            message = self._generate_routine_checkin(receiver_data)
        
        # Send the message
        success = VeniceAPI.send_message(sender, receiver, message, "anchor_checkin")
        
        if success:
            logger.info(f"Check-in sent: {sender} → {receiver}")
        else:
            logger.error(f"Failed to send check-in: {sender} → {receiver}")
    
    def _generate_critical_checkin(self, citizen_data: Dict) -> str:
        """Generate check-in message for critical risk citizens"""
        return f"Greetings, friend. I hope this message finds you well. I was thinking of you and wondered - where in Venice are you working today? The markets have been bustling, and I could use your counsel on some business matters. Perhaps we could meet at the Rialto this afternoon?"
    
    def _generate_high_checkin(self, citizen_data: Dict) -> str:
        """Generate check-in message for high risk citizens"""
        return f"Good day to you! How fares your workshop this week? I've heard interesting news from the trading houses that might benefit your work. Would you care to share a meal and discuss the opportunities?"
    
    def _generate_routine_checkin(self, citizen_data: Dict) -> str:
        """Generate check-in message for stable citizens"""
        return f"I trust your enterprises are flourishing! Any word from your recent contracts? The guild has been discussing new collaborative ventures - your expertise would be valued."

def main():
    """Main execution function for emergency deployment"""
    logger.info("=== ANCHOR PAIRS EMERGENCY DEPLOYMENT ===")
    
    # Initialize the system
    manager = AnchorPairManager()
    
    # Create emergency pairs for highest-risk citizens
    pairs = manager.create_emergency_pairs()
    
    if not pairs:
        logger.warning("No pairs created - all citizens may be stable or incompatible")
        return
    
    logger.info(f"Created {len(pairs)} emergency anchor pairs")
    
    # Send initial check-in messages
    manager.initiate_check_ins()
    
    # Save pair data for monitoring
    pair_data = {
        'created_at': datetime.now().isoformat(),
        'pairs': pairs,
        'total_pairs': len(pairs)
    }
    
    with open('./anchor_pairs_deployment.json', 'w') as f:
        json.dump(pair_data, f, indent=2)
    
    logger.info("Emergency deployment complete. Monitoring begins now.")
    logger.info("Next: Implement automated check-in scheduling and intervention protocols")

if __name__ == "__main__":
    main()