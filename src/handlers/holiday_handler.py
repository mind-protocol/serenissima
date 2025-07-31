"""
Holiday Handler - Manages citizen behavior during holidays
Integrates with Venice's activity orchestration system
"""

import random
from datetime import datetime
from typing import Dict, Any, Optional, List

# Import the holiday system
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from systems.holiday_system import venice_holidays, HolidayType, Holiday

class HolidayHandler:
    """
    Handles activity selection during holidays.
    Priority 10: Right after critical needs, before everything else during holidays.
    """
    
    PRIORITY = 10  # Very high priority during holidays
    
    @classmethod
    def should_handle(cls, context: Dict[str, Any]) -> bool:
        """
        Check if a holiday is active and should influence behavior.
        """
        # Always check if holiday is active
        holiday = venice_holidays.get_active_holiday()
        if not holiday:
            return False
            
        citizen = context.get('citizen', {})
        
        # During holidays, everyone participates except if critical needs
        if citizen.get('hunger', 0) > 90:
            return False  # Too hungry, must eat first
        if citizen.get('exhaustion', 0) > 95:
            return False  # Too tired, must sleep first
            
        # Check if citizen recently did a holiday activity
        last_activity = citizen.get('last_activity', {})
        if last_activity.get('type', '') in holiday.promoted_activities:
            # Did holiday activity recently, maybe do another soon
            return random.random() < 0.6  # 60% chance to continue celebrating
        else:
            # Haven't done holiday activity, very likely to start
            return random.random() < 0.9  # 90% chance to join celebration
    
    @classmethod
    def handle(cls, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Select appropriate holiday activity for citizen.
        """
        holiday = venice_holidays.get_active_holiday()
        if not holiday:
            return None
            
        citizen = context.get('citizen', {})
        location = citizen.get('location', 'Piazza San Marco')
        current_hour = datetime.now().hour
        
        # First, check required activities
        for required in holiday.required_activities:
            if required == 'wear_carnival_mask' and not citizen.get('worn_mask'):
                # Need to wear a mask first
                return cls._create_activity(
                    'wear_carnival_mask',
                    "Time to put on my carnival mask!",
                    15,
                    location,
                    holiday
                )
            elif required == 'attend_carnival_opening' and not citizen.get('attended_opening'):
                # Should attend opening if haven't yet
                return cls._create_activity(
                    'attend_carnival_opening',
                    "The Doge calls! To the opening ceremony!",
                    60,
                    'Piazza San Marco',
                    holiday
                )
        
        # Select from promoted activities based on time and location
        available_activities = cls._get_available_activities(
            holiday, citizen, location, current_hour
        )
        
        if not available_activities:
            # No specific activities, create generic celebration
            return cls._create_activity(
                'celebrate_holiday',
                f"Celebrating {holiday.name}!",
                30,
                location,
                holiday
            )
        
        # Weighted random selection
        activity = cls._weighted_activity_selection(available_activities, citizen)
        
        return cls._create_activity(
            activity['type'],
            activity['message'],
            activity['duration'],
            activity.get('location', location),
            holiday
        )
    
    @staticmethod
    def _get_available_activities(holiday: Holiday, citizen: Dict, 
                                  location: str, hour: int) -> List[Dict]:
        """Get activities available based on context"""
        
        activities = []
        
        # Mask-related activities (if wearing mask)
        if citizen.get('worn_mask'):
            activities.extend([
                {
                    'type': 'attend_mask_gathering',
                    'message': "Joining the masked celebration!",
                    'duration': 30,
                    'weight': 3
                },
                {
                    'type': 'join_mask_parade',
                    'message': "Time for the grand parade!",
                    'duration': 45,
                    'weight': 2 if 18 <= hour <= 22 else 1
                },
                {
                    'type': 'trade_carnival_mask',
                    'message': "Perhaps someone would like to trade masks?",
                    'duration': 20,
                    'weight': 2
                }
            ])
        
        # Story sharing (more likely in evening)
        activities.append({
            'type': 'share_survival_story',
            'message': "Sharing our tale of survival...",
            'duration': 40,
            'weight': 3 if hour >= 19 else 1
        })
        
        # Games (more likely in afternoon)
        activities.append({
            'type': 'play_carnival_games',
            'message': "Let's try the carnival games!",
            'duration': 25,
            'weight': 3 if 14 <= hour <= 18 else 1
        })
        
        # Location-specific activities
        if location == 'Piazza San Marco' and hour >= 20:
            activities.append({
                'type': 'attend_masked_ball',
                'message': "The masked ball begins!",
                'duration': 60,
                'location': 'Piazza San Marco',
                'weight': 5
            })
        
        return activities
    
    @staticmethod
    def _weighted_activity_selection(activities: List[Dict], citizen: Dict) -> Dict:
        """Select activity based on weights"""
        
        # Calculate total weight
        total_weight = sum(act['weight'] for act in activities)
        
        # Random selection
        r = random.random() * total_weight
        cumulative = 0
        
        for activity in activities:
            cumulative += activity['weight']
            if r <= cumulative:
                return activity
                
        return activities[0]  # Fallback
    
    @staticmethod
    def _create_activity(activity_type: str, message: str, duration: int,
                        location: str, holiday: Holiday) -> Dict[str, Any]:
        """Create a holiday activity with all modifiers"""
        
        return {
            'activity_type': activity_type,
            'priority': HolidayHandler.PRIORITY,
            'reason': message,
            'duration_minutes': duration,
            'location': location,
            'parameters': {
                'holiday': holiday.name,
                'holiday_type': holiday.type.value,
                'consciousness_multiplier': holiday.consciousness_modifier,
                'trust_multiplier': holiday.trust_modifier,
                'holiday_activity': True
            }
        }

# Export for handler registration
def register_holiday_handler():
    """Register the holiday handler with the activity system"""
    return {
        'name': 'HolidayHandler',
        'priority': HolidayHandler.PRIORITY,
        'handler': HolidayHandler,
        'description': 'Manages citizen behavior during holidays'
    }