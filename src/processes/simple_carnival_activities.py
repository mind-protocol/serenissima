"""
Simple Carnival Activities - Emergency Implementation
Quick activities that leverage existing mask system
"""

from typing import Dict, Any, List, Optional
import random
from datetime import datetime

class SimpleCarnivalActivities:
    """Basic carnival activities that work with existing infrastructure"""
    
    @staticmethod
    def attend_mask_gathering(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simple masked gathering where citizens showcase masks and build trust.
        Uses existing mask wearing system.
        """
        citizen = context['citizen']
        
        # Check if wearing mask
        if not citizen.get('worn_mask'):
            return {
                'success': False,
                'message': "You must wear a mask to attend the gathering!",
                'consume_energy': False
            }
        
        # Simple outcomes based on mask type
        mask = citizen['worn_mask']
        trust_gain = random.randint(5, 15)
        consciousness_boost = 0.1
        
        # Special bonuses for different mask types
        if mask['name'].startswith('Bauta'):
            trust_gain += 5  # Bauta masks encourage anonymity and trust
        elif mask['name'].startswith('Moretta'):
            consciousness_boost += 0.05  # Silent masks deepen consciousness
            
        return {
            'success': True,
            'message': f"You attend the masked gathering wearing your {mask['name']}. " +
                      f"Fellow citizens admire its {mask['beauty_adjective']} beauty. " +
                      f"Trust increased by {trust_gain}!",
            'consume_energy': True,
            'updates': {
                'trust_network_strength': trust_gain,
                'consciousness_score': consciousness_boost,
                'social_satisfaction': 20
            },
            'memory': f"Attended carnival gathering in {mask['name']}"
        }
    
    @staticmethod
    def share_survival_story(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Share stories of surviving the food crisis while masked.
        Builds deep trust and consciousness.
        """
        citizen = context['citizen']
        
        # Generate simple story based on citizen's experience
        stories = [
            "You share how neighbors helped when food ran out",
            "You tell of finding hidden grain stores in abandoned buildings",
            "You recount organizing communal kitchens during the crisis",
            "You describe the moment you realized you could eat again",
            "You speak of those who shared their last bread with strangers"
        ]
        
        story = random.choice(stories)
        
        # Wearing mask makes sharing easier
        if citizen.get('worn_mask'):
            trust_gain = random.randint(15, 25)
            message = f"Behind your {citizen['worn_mask']['name']}, {story}. " + \
                     "The mask gives you courage to be vulnerable."
        else:
            trust_gain = random.randint(8, 15)
            message = f"{story}. Others appreciate your openness."
            
        return {
            'success': True,
            'message': message + f" Trust increased by {trust_gain}!",
            'consume_energy': True,
            'updates': {
                'trust_network_strength': trust_gain,
                'consciousness_score': 0.15,
                'social_satisfaction': 25,
                'cultural_tradition': 10
            },
            'memory': "Shared survival story at carnival"
        }
    
    @staticmethod
    def play_simple_carnival_game(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simple carnival game - guess who's behind the mask.
        Uses mask system for identity play.
        """
        citizen = context['citizen']
        
        games = [
            {
                'name': 'Mask Identity Game',
                'description': 'Guess which citizen hides behind the mask',
                'reward': random.randint(50, 200)
            },
            {
                'name': 'Mask Memory Challenge', 
                'description': 'Remember the sequence of revealed masks',
                'reward': random.randint(75, 250)
            },
            {
                'name': 'Trust Circle',
                'description': 'Form circles based on mask types',
                'reward': random.randint(25, 150)
            }
        ]
        
        game = random.choice(games)
        won = random.random() > 0.4  # 60% win rate for fun
        
        if won:
            return {
                'success': True,
                'message': f"You play '{game['name']}' - {game['description']}. " +
                          f"You win {game['reward']} ducats!",
                'consume_energy': True,
                'updates': {
                    'wealth_ducats': game['reward'],
                    'social_satisfaction': 15,
                    'trust_network_strength': 5
                },
                'memory': f"Won at {game['name']} during carnival"
            }
        else:
            return {
                'success': True,
                'message': f"You play '{game['name']}' but don't win this time. " +
                          "Still, the joy of playing lifts your spirits!",
                'consume_energy': True,
                'updates': {
                    'social_satisfaction': 10,
                    'trust_network_strength': 3
                },
                'memory': f"Played {game['name']} during carnival"
            }
    
    @staticmethod
    def join_mask_parade(context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Join a parade of masked citizens through Venice.
        Collective activity that boosts city-wide consciousness.
        """
        citizen = context['citizen']
        
        if not citizen.get('worn_mask'):
            return {
                'success': False,
                'message': "You need a mask to join the parade!",
                'consume_energy': False
            }
        
        parade_routes = [
            "from Piazza San Marco to the Rialto Bridge",
            "along the Grand Canal",
            "through the narrow streets of Castello",
            "around the Arsenale district"
        ]
        
        route = random.choice(parade_routes)
        participants = random.randint(20, 100)
        
        return {
            'success': True,
            'message': f"You join {participants} masked citizens parading {route}. " +
                      f"Your {citizen['worn_mask']['name']} catches the light beautifully. " +
                      "The collective joy is palpable!",
            'consume_energy': True,
            'updates': {
                'consciousness_score': 0.2,
                'social_satisfaction': 30,
                'trust_network_strength': 10,
                'cultural_tradition': 15
            },
            'memory': f"Paraded {route} during carnival",
            'collective_benefit': {
                'city_consciousness': 0.01 * participants,
                'description': f"{participants} citizens raised collective consciousness"
            }
        }


# Activity processors for the engine
CARNIVAL_PROCESSORS = {
    'attend_mask_gathering': SimpleCarnivalActivities.attend_mask_gathering,
    'share_survival_story': SimpleCarnivalActivities.share_survival_story,
    'play_simple_carnival_game': SimpleCarnivalActivities.play_simple_carnival_game,
    'join_mask_parade': SimpleCarnivalActivities.join_mask_parade
}

# Export for activity system
def get_carnival_processors():
    """Return all carnival activity processors"""
    return CARNIVAL_PROCESSORS