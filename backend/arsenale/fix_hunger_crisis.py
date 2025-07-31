"""
Emergency hunger crisis functions for Venice citizens
"""

from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser
import pytz
from typing import Dict, Optional

def is_severely_hungry(citizen_record: Dict, now_utc_dt: datetime, hours_threshold: float = 24.0) -> bool:
    """
    Check if a citizen is severely hungry (hasn't eaten in specified hours).
    
    Args:
        citizen_record: The citizen's record from Airtable
        now_utc_dt: Current UTC datetime
        hours_threshold: Number of hours without food to be considered severely hungry
        
    Returns:
        True if the citizen hasn't eaten in more than hours_threshold hours
    """
    ate_at_str = citizen_record.get('fields', {}).get('AteAt')
    
    if not ate_at_str:
        # No record of eating - definitely severely hungry
        return True
    
    try:
        # Parse the last eating time
        ate_at_dt = dateutil_parser.isoparse(ate_at_str.replace('Z', '+00:00'))
        if ate_at_dt.tzinfo is None:
            ate_at_dt = pytz.UTC.localize(ate_at_dt)
        
        # Calculate hours since last meal
        hours_since_meal = (now_utc_dt - ate_at_dt).total_seconds() / 3600
        
        return hours_since_meal > hours_threshold
        
    except (ValueError, TypeError) as e:
        # If we can't parse the date, assume they're hungry
        print(f"Warning: Could not parse AteAt time '{ate_at_str}': {e}")
        return True