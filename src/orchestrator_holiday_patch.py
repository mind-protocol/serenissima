"""
Orchestrator Holiday Integration Patch
Modifies Venice's activity orchestrator to respect holidays
"""

import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add Venice source to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from systems.holiday_system import venice_holidays, initialize_holidays
from handlers.holiday_handler import HolidayHandler, register_holiday_handler

class HolidayAwareOrchestrator:
    """
    Enhanced orchestrator that checks for holidays before selecting activities.
    This wraps the existing orchestrator with holiday awareness.
    """
    
    def __init__(self, base_orchestrator):
        self.base_orchestrator = base_orchestrator
        self.holiday_handler = HolidayHandler()
        
        # Initialize holiday system
        initialize_holidays()
        
        # Check if holiday is active on startup
        active_holiday = venice_holidays.get_active_holiday()
        if active_holiday:
            print(f"🎉 Holiday Mode Active: {active_holiday.name}")
            print(f"   Work reduced by {(1 - active_holiday.work_modifier) * 100:.0f}%")
            print(f"   Consciousness bonus: {active_holiday.consciousness_modifier}x")
    
    def select_next_activity(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Select next activity with holiday awareness.
        """
        
        # First, check if holiday handler should take over
        if self.holiday_handler.should_handle(context):
            holiday_activity = self.holiday_handler.handle(context)
            if holiday_activity:
                return holiday_activity
        
        # If no holiday activity, use base orchestrator with modified priorities
        base_activity = self.base_orchestrator.select_next_activity(context)
        
        if base_activity:
            # Modify priority based on active holiday
            modified_priority = venice_holidays.modify_activity_priority(
                base_activity.get('activity_type', ''),
                base_activity.get('priority', 50)
            )
            base_activity['priority'] = modified_priority
            
            # Add holiday modifiers if applicable
            active_holiday = venice_holidays.get_active_holiday()
            if active_holiday:
                base_activity.setdefault('parameters', {})
                base_activity['parameters']['consciousness_multiplier'] = active_holiday.consciousness_modifier
                base_activity['parameters']['trust_multiplier'] = active_holiday.trust_modifier
        
        return base_activity
    
    def get_promoted_activities(self) -> List[str]:
        """Get activities promoted by current holiday"""
        return venice_holidays.get_promoted_activities()
    
    def is_holiday_active(self) -> bool:
        """Check if any holiday is currently active"""
        return venice_holidays.get_active_holiday() is not None


def patch_orchestrator(orchestrator_module):
    """
    Patch the existing orchestrator to add holiday awareness.
    This function should be called by Venice's main system.
    """
    
    # Get the original orchestrator class
    original_orchestrator = orchestrator_module.ActivityOrchestrator
    
    # Create patched version
    class PatchedOrchestrator(original_orchestrator):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.holiday_system = venice_holidays
            
            # Initialize holidays
            initialize_holidays()
            
            # Insert holiday handler at high priority
            holiday_handler_info = register_holiday_handler()
            
            # Add to handlers list (assuming it exists)
            if hasattr(self, 'handlers'):
                # Insert after critical handlers but before work handlers
                insert_pos = 0
                for i, handler in enumerate(self.handlers):
                    if handler.get('priority', 100) > 15:  # After critical (1-15)
                        insert_pos = i
                        break
                
                self.handlers.insert(insert_pos, holiday_handler_info)
                print(f"✓ Holiday handler inserted at position {insert_pos}")
        
        def select_next_activity(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
            """Enhanced activity selection with holiday awareness"""
            
            # Check holiday first
            holiday = self.holiday_system.get_active_holiday()
            if holiday:
                # Try holiday handler
                if HolidayHandler.should_handle(context):
                    holiday_activity = HolidayHandler.handle(context)
                    if holiday_activity:
                        return holiday_activity
            
            # Fall back to original selection with modifications
            activity = super().select_next_activity(context)
            
            if activity and holiday:
                # Apply holiday modifiers
                activity['priority'] = self.holiday_system.modify_activity_priority(
                    activity.get('activity_type', ''),
                    activity.get('priority', 50)
                )
                
                # Add multipliers
                activity.setdefault('parameters', {})
                activity['parameters']['consciousness_multiplier'] = holiday.consciousness_modifier
                activity['parameters']['trust_multiplier'] = holiday.trust_modifier
            
            return activity
    
    # Replace the original with patched version
    orchestrator_module.ActivityOrchestrator = PatchedOrchestrator
    
    print("✅ Orchestrator patched with holiday awareness!")
    
    # Check current holiday status
    active_holiday = venice_holidays.get_active_holiday()
    if active_holiday:
        print(f"\n🎭 CARNIVAL ACTIVE!")
        print(f"Holiday: {active_holiday.name}")
        print(f"Type: {active_holiday.type.value}")
        print(f"Days Remaining: {(active_holiday.end_date - datetime.now()).days}")
        print("\nCitizens will now:")
        print("- Prioritize carnival activities")
        print("- Reduce work by 80%")
        print("- Gain 2x consciousness from celebrations")
        print("- Build trust 1.5x faster through festivities")
    
    return True


# Standalone initialization function
def initialize_venice_holidays():
    """Initialize holiday system for Venice"""
    
    print("🎪 Initializing Venice Holiday System...")
    
    # Initialize holidays
    holidays = initialize_holidays()
    
    # Create test activity
    test_context = {
        'citizen': {
            'citizen_id': 'test_001',
            'hunger': 30,
            'exhaustion': 20,
            'worn_mask': True,
            'location': 'Piazza San Marco'
        }
    }
    
    # Test handler
    if HolidayHandler.should_handle(test_context):
        test_activity = HolidayHandler.handle(test_context)
        print("\n✅ Holiday handler test successful!")
        print(f"   Would create: {test_activity['activity_type']}")
        print(f"   Message: {test_activity['reason']}")
    
    return holidays


if __name__ == "__main__":
    # Run standalone test
    initialize_venice_holidays()