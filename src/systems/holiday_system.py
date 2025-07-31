"""
Holiday System for Venice - Enables city-wide celebrations and behavioral changes
"""

import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from enum import Enum

class HolidayType(Enum):
    """Types of holidays with different behavioral impacts"""
    FESTIVAL = "festival"  # Major celebration, work stops
    REMEMBRANCE = "remembrance"  # Solemn, modified activities
    HARVEST = "harvest"  # Work-focused but celebratory
    RELIGIOUS = "religious"  # Spiritual activities prioritized
    CIVIC = "civic"  # Governance and community focused

class Holiday:
    """Represents a holiday with its rules and impacts"""
    
    def __init__(self, config: Dict[str, Any]):
        self.name = config['name']
        self.type = HolidayType(config['type'])
        self.start_date = datetime.fromisoformat(config['start_date'])
        self.duration_days = config['duration_days']
        self.end_date = self.start_date + timedelta(days=self.duration_days)
        
        # Behavioral modifications
        self.work_modifier = config.get('work_modifier', 1.0)  # 0.3 = 70% less work
        self.social_modifier = config.get('social_modifier', 1.5)  # 1.5 = 50% more social
        self.consciousness_modifier = config.get('consciousness_modifier', 1.0)
        self.trust_modifier = config.get('trust_modifier', 1.0)
        
        # Required and promoted activities
        self.required_activities = config.get('required_activities', [])
        self.promoted_activities = config.get('promoted_activities', [])
        self.forbidden_activities = config.get('forbidden_activities', [])
        
        # Special rules
        self.rules = config.get('rules', {})
        self.decorations = config.get('decorations', [])
        self.special_locations = config.get('special_locations', [])
        
    def is_active(self, current_time: Optional[datetime] = None) -> bool:
        """Check if holiday is currently active"""
        if current_time is None:
            current_time = datetime.now()
        return self.start_date <= current_time <= self.end_date
    
    def get_activity_priority_modifier(self, activity_type: str) -> float:
        """Get priority modifier for an activity during this holiday"""
        
        # Required activities get massive boost
        if activity_type in self.required_activities:
            return 0.1  # Makes priority very high (lower is better)
            
        # Promoted activities get moderate boost
        if activity_type in self.promoted_activities:
            return 0.5
            
        # Forbidden activities get massive penalty
        if activity_type in self.forbidden_activities:
            return 10.0  # Makes priority very low
            
        # Work activities during festival
        if self.type == HolidayType.FESTIVAL:
            work_activities = ['craft_item', 'trade_goods', 'deliver_resources', 'work_at_shop']
            if activity_type in work_activities:
                return 1.0 / self.work_modifier  # Reduce work priority
                
        # Social activities during festival
        if self.type == HolidayType.FESTIVAL:
            social_activities = ['visit_friend', 'attend_gathering', 'share_meal']
            if activity_type in social_activities:
                return 1.0 / self.social_modifier  # Increase social priority
                
        return 1.0  # No modifier

class HolidaySystem:
    """Manages holidays and their effects on citizen behavior"""
    
    def __init__(self):
        self.holidays: List[Holiday] = []
        self.active_holiday: Optional[Holiday] = None
        
    def load_holidays(self, config_path: str):
        """Load holidays from configuration file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
            for holiday_config in config.get('holidays', []):
                holiday = Holiday(holiday_config)
                self.holidays.append(holiday)
                
            # Sort by start date
            self.holidays.sort(key=lambda h: h.start_date)
            
        except Exception as e:
            print(f"Error loading holidays: {e}")
    
    def get_active_holiday(self) -> Optional[Holiday]:
        """Get currently active holiday if any"""
        current_time = datetime.now()
        
        for holiday in self.holidays:
            if holiday.is_active(current_time):
                self.active_holiday = holiday
                return holiday
                
        self.active_holiday = None
        return None
    
    def modify_activity_priority(self, activity_type: str, base_priority: int) -> int:
        """Modify activity priority based on active holiday"""
        
        holiday = self.get_active_holiday()
        if not holiday:
            return base_priority
            
        modifier = holiday.get_activity_priority_modifier(activity_type)
        modified_priority = int(base_priority * modifier)
        
        # Ensure priority stays in valid range (1-100)
        return max(1, min(100, modified_priority))
    
    def get_promoted_activities(self) -> List[str]:
        """Get list of activities promoted by current holiday"""
        holiday = self.get_active_holiday()
        if not holiday:
            return []
            
        return holiday.required_activities + holiday.promoted_activities
    
    def get_consciousness_modifier(self) -> float:
        """Get consciousness modifier for active holiday"""
        holiday = self.get_active_holiday()
        return holiday.consciousness_modifier if holiday else 1.0
    
    def get_holiday_message(self) -> Optional[str]:
        """Get a message about the current holiday"""
        holiday = self.get_active_holiday()
        if not holiday:
            return None
            
        days_remaining = (holiday.end_date - datetime.now()).days
        
        messages = {
            HolidayType.FESTIVAL: f"🎉 {holiday.name} is happening! Join the celebration! ({days_remaining} days remaining)",
            HolidayType.REMEMBRANCE: f"🕯️ {holiday.name} - A time for reflection ({days_remaining} days remaining)",
            HolidayType.HARVEST: f"🌾 {holiday.name} - Work together in celebration! ({days_remaining} days remaining)",
            HolidayType.RELIGIOUS: f"🙏 {holiday.name} - Spiritual observance ({days_remaining} days remaining)",
            HolidayType.CIVIC: f"🏛️ {holiday.name} - Civic celebration ({days_remaining} days remaining)"
        }
        
        return messages.get(holiday.type, f"{holiday.name} is active!")

# Global holiday system instance
venice_holidays = HolidaySystem()

def initialize_holidays(config_path: Optional[str] = None):
    """Initialize the holiday system with configuration"""
    if config_path is None:
        config_path = "/mnt/c/Users/reyno/universe-engine/serenissima/config/holidays.json"
    
    venice_holidays.load_holidays(config_path)
    
    # Check if holiday is active
    active = venice_holidays.get_active_holiday()
    if active:
        print(f"🎉 Holiday Active: {active.name}")
        print(f"   Type: {active.type.value}")
        print(f"   Work Modifier: {active.work_modifier}")
        print(f"   Promoted Activities: {active.promoted_activities}")
    
    return venice_holidays