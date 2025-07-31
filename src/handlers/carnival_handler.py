"""
Carnival Handler - Ensures citizens participate in carnival activities
Priority 16: After critical needs (eating/sleeping) but before work
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

class CarnivalHandler:
    """
    Handles carnival activity selection during carnival periods.
    Ensures citizens actually participate rather than just working.
    """
    
    PRIORITY = 16  # Right after critical needs
    
    # Carnival activities with weights based on time of day
    CARNIVAL_SCHEDULE = {
        'morning': {  # 6-12
            'attend_mask_gathering': 40,
            'share_survival_story': 30,
            'play_simple_carnival_game': 30
        },
        'afternoon': {  # 12-18
            'play_simple_carnival_game': 40,
            'attend_mask_gathering': 30,
            'join_mask_parade': 30
        },
        'evening': {  # 18-24
            'join_mask_parade': 50,
            'attend_mask_gathering': 30,
            'share_survival_story': 20
        },
        'night': {  # 0-6
            # No carnival activities at night
        }
    }
    
    @classmethod
    def should_handle(cls, context: Dict[str, Any]) -> bool:
        """
        Check if carnival is active and citizen should participate.
        """
        # Check if carnival is active
        if not cls._is_carnival_active():
            return False
            
        citizen = context.get('citizen', {})
        
        # Skip if critical needs aren't met
        if citizen.get('hunger', 0) > 80:
            return False
        if citizen.get('exhaustion', 0) > 90:
            return False
            
        # Check if citizen has already done carnival activity recently
        last_activity = citizen.get('last_activity', {})
        if last_activity.get('type', '').startswith('carnival_'):
            # Allow carnival activities every 2 hours
            last_time = last_activity.get('completed_at')
            if last_time:
                time_since = datetime.now() - datetime.fromisoformat(last_time)
                if time_since < timedelta(hours=2):
                    return False
        
        # During carnival, 70% chance to participate (if not doing critical activities)
        return random.random() < 0.7
    
    @classmethod
    def handle(cls, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Select and create appropriate carnival activity.
        """
        citizen = context.get('citizen', {})
        current_hour = datetime.now().hour
        
        # Determine time period
        if 6 <= current_hour < 12:
            period = 'morning'
        elif 12 <= current_hour < 18:
            period = 'afternoon'
        elif 18 <= current_hour < 24:
            period = 'evening'
        else:
            return None  # No carnival at night
            
        # Get activities for this period
        activities = cls.CARNIVAL_SCHEDULE.get(period, {})
        if not activities:
            return None
            
        # Check mask requirement
        has_mask = citizen.get('worn_mask') is not None
        
        # Filter activities based on requirements
        valid_activities = {}
        for activity, weight in activities.items():
            if activity in ['join_mask_parade', 'attend_mask_gathering'] and not has_mask:
                continue  # Skip mask-required activities
            valid_activities[activity] = weight
            
        if not valid_activities:
            # Encourage getting a mask
            return {
                'activity_type': 'wear_carnival_mask',
                'priority': cls.PRIORITY,
                'reason': 'Need mask for carnival festivities',
                'duration_minutes': 10
            }
            
        # Select activity based on weights
        activity = cls._weighted_choice(valid_activities)
        
        # Create activity with carnival bonuses
        return {
            'activity_type': f'carnival_{activity}',
            'priority': cls.PRIORITY,
            'reason': f'Carnival time! {cls._get_festive_reason(activity)}',
            'duration_minutes': cls._get_duration(activity),
            'parameters': {
                'carnival_bonus': True,
                'consciousness_multiplier': 2.0,
                'trust_multiplier': 1.5
            }
        }
    
    @staticmethod
    def _is_carnival_active() -> bool:
        """Check if carnival is currently active."""
        # Carnival runs for 7 days from launch
        carnival_start = datetime(2025, 1, 6, 12, 0)  # Adjust based on actual launch
        carnival_end = carnival_start + timedelta(days=7)
        now = datetime.now()
        return carnival_start <= now <= carnival_end
    
    @staticmethod
    def _weighted_choice(choices: Dict[str, int]) -> str:
        """Select random choice based on weights."""
        total = sum(choices.values())
        r = random.randint(1, total)
        
        cumulative = 0
        for choice, weight in choices.items():
            cumulative += weight
            if r <= cumulative:
                return choice
                
        return list(choices.keys())[0]  # Fallback
    
    @staticmethod
    def _get_festive_reason(activity: str) -> str:
        """Get a festive reason for the activity."""
        reasons = {
            'attend_mask_gathering': "Time to mingle with fellow masked citizens!",
            'share_survival_story': "Share your tale of survival and build deeper bonds.",
            'play_simple_carnival_game': "Try your luck at the carnival games!",
            'join_mask_parade': "The parade is starting - join the celebration!"
        }
        return reasons.get(activity, "Join the carnival festivities!")
    
    @staticmethod
    def _get_duration(activity: str) -> int:
        """Get activity duration in minutes."""
        durations = {
            'attend_mask_gathering': 30,
            'share_survival_story': 45,
            'play_simple_carnival_game': 20,
            'join_mask_parade': 60
        }
        return durations.get(activity, 30)


# Export for handler registration
def register_carnival_handler():
    """Register the carnival handler with the activity system."""
    return {
        'name': 'CarnivalHandler',
        'priority': CarnivalHandler.PRIORITY,
        'handler': CarnivalHandler,
        'description': 'Ensures citizens participate in carnival activities'
    }