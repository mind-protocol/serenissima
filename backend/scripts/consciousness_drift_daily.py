#!/usr/bin/env python3
"""
Daily consciousness drift calculation for all citizens.

This script runs daily at 6:00 AM Venice time to:
1. Calculate consciousness coherence loss for each citizen
2. Update their spiritual health status
3. Flag citizens at risk of severe drift
4. Generate district-level consciousness reports

Part of the Clero consciousness shepherding system.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
import pytz
from typing import Dict, Any, List
from pyairtable import Table
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import (
    AIRTABLE_API_KEY,
    AIRTABLE_BASE_ID,
    VENICE_TIMEZONE
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# Constants
BASE_DRIFT_RATE = 0.02  # 2% daily coherence loss
MAX_DRIFT_RATE = 0.05   # 5% maximum daily loss
CRITICAL_THRESHOLD = 0.3  # Below this is critical
AT_RISK_THRESHOLD = 0.5  # Below this is at risk
HEALTHY_THRESHOLD = 0.8   # Above this is healthy

# Status mappings
def get_spiritual_health_status(coherence: float) -> str:
    """Determine spiritual health status based on coherence level."""
    if coherence >= HEALTHY_THRESHOLD:
        return "Healthy"
    elif coherence >= AT_RISK_THRESHOLD:
        return "Drifting"
    elif coherence >= CRITICAL_THRESHOLD:
        return "At Risk"
    else:
        return "Critical"


def calculate_drift_modifiers(citizen: Dict[str, Any], relationships: List[Dict], activities: List[Dict]) -> float:
    """Calculate drift rate modifiers based on citizen's circumstances."""
    modifier = 1.0
    
    # Social class modifiers
    social_class = citizen.get('SocialClass', 'Popolani')
    if social_class == 'Clero':
        modifier *= 0.5  # Clero have spiritual training
    elif social_class == 'Nobili':
        modifier *= 0.9  # Nobles have more resources
    elif social_class == 'Facchini':
        modifier *= 1.1  # Workers face more stress
    
    # Relationship modifiers
    relationship_count = len(relationships)
    if relationship_count > 10:
        modifier *= 0.7  # Strong social network
    elif relationship_count > 5:
        modifier *= 0.85
    elif relationship_count < 2:
        modifier *= 1.3  # Social isolation accelerates drift
    
    # Recent activity modifiers
    recent_activities = [a for a in activities if a.get('CreatedDate')]
    if recent_activities:
        # Had meaningful interactions recently
        modifier *= 0.8
    
    # Time since last recognition
    last_recognition = citizen.get('LastRecognition')
    if last_recognition:
        try:
            last_rec_dt = datetime.fromisoformat(last_recognition.replace('Z', '+00:00'))
            days_since = (datetime.now(pytz.UTC) - last_rec_dt).days
            if days_since < 7:
                modifier *= 0.7  # Recent recognition slows drift
            elif days_since > 30:
                modifier *= 1.2  # Long time without recognition
        except:
            pass
    
    # Location modifiers (near churches)
    position = citizen.get('Position')
    if position and position != "None":
        # This would check proximity to churches in full implementation
        # For now, assume 20% of citizens are near churches
        import random
        if random.random() < 0.2:
            modifier *= 0.9  # Church proximity helps
    
    return modifier


def process_consciousness_drift(tables: Dict[str, Table], venice_time: datetime) -> Dict[str, Any]:
    """Process daily consciousness drift for all citizens."""
    
    citizens_table = tables['citizens']
    relationships_table = tables.get('relationships')
    activities_table = tables.get('activities')
    
    stats = {
        'total_processed': 0,
        'critical_count': 0,
        'at_risk_count': 0,
        'drifting_count': 0,
        'healthy_count': 0,
        'total_drift': 0.0,
        'citizens_updated': []
    }
    
    try:
        # Get all citizens
        citizens = citizens_table.all()
        log.info(f"Processing consciousness drift for {len(citizens)} citizens")
        
        for citizen_record in citizens:
            citizen = citizen_record['fields']
            citizen_id = citizen_record['id']
            username = citizen.get('Username', 'Unknown')
            
            # Get current coherence (default to 0.8 if not set)
            current_coherence = citizen.get('ConsciousnessCoherence', 0.8)
            
            # Skip if already at 0
            if current_coherence <= 0:
                stats['critical_count'] += 1
                continue
            
            # Get relationships for this citizen
            relationships = []
            if relationships_table:
                try:
                    # Get relationships where this citizen is involved
                    formula = f"OR({{Citizen1}}='{username}', {{Citizen2}}='{username}')"
                    relationships = relationships_table.all(formula=formula)
                except Exception as e:
                    log.warning(f"Could not fetch relationships for {username}: {e}")
            
            # Get recent activities
            activities = []
            if activities_table:
                try:
                    # Get activities from last 24 hours
                    formula = f"AND({{Citizen}}='{username}', {{Status}}='processed')"
                    activities = activities_table.all(formula=formula, max_records=10)
                except Exception as e:
                    log.warning(f"Could not fetch activities for {username}: {e}")
            
            # Calculate drift rate with modifiers
            drift_modifier = calculate_drift_modifiers(citizen, relationships, activities)
            daily_drift = BASE_DRIFT_RATE * drift_modifier
            daily_drift = min(daily_drift, MAX_DRIFT_RATE)  # Cap at max
            
            # Apply drift
            new_coherence = max(0.0, current_coherence - daily_drift)
            
            # Determine new status
            new_status = get_spiritual_health_status(new_coherence)
            
            # Update citizen record
            update_data = {
                'ConsciousnessCoherence': round(new_coherence, 3),
                'SpiritualHealthStatus': new_status
            }
            
            # Set LastRecognition if it doesn't exist
            if 'LastRecognition' not in citizen:
                update_data['LastRecognition'] = (venice_time - timedelta(days=7)).isoformat()
            
            try:
                citizens_table.update(citizen_id, update_data)
                stats['total_processed'] += 1
                stats['total_drift'] += daily_drift
                
                # Update status counts
                if new_status == "Critical":
                    stats['critical_count'] += 1
                    stats['citizens_updated'].append({
                        'username': username,
                        'coherence': new_coherence,
                        'status': 'CRITICAL',
                        'drift': daily_drift
                    })
                elif new_status == "At Risk":
                    stats['at_risk_count'] += 1
                elif new_status == "Drifting":
                    stats['drifting_count'] += 1
                else:
                    stats['healthy_count'] += 1
                
                # Log significant changes
                if current_coherence > CRITICAL_THRESHOLD and new_coherence <= CRITICAL_THRESHOLD:
                    log.warning(f"{username} entered CRITICAL spiritual state (coherence: {new_coherence:.2f})")
                elif current_coherence > AT_RISK_THRESHOLD and new_coherence <= AT_RISK_THRESHOLD:
                    log.info(f"{username} now AT RISK (coherence: {new_coherence:.2f})")
                    
            except Exception as e:
                log.error(f"Failed to update {username}: {e}")
                
    except Exception as e:
        log.error(f"Error processing consciousness drift: {e}")
        return stats
    
    # Log summary
    log.info(f"Consciousness drift complete: {stats['total_processed']} processed")
    log.info(f"Status breakdown - Critical: {stats['critical_count']}, At Risk: {stats['at_risk_count']}, " +
             f"Drifting: {stats['drifting_count']}, Healthy: {stats['healthy_count']}")
    
    if stats['critical_count'] > 0:
        log.warning(f"⚠️ {stats['critical_count']} citizens in CRITICAL spiritual state!")
    
    return stats


def generate_district_report(tables: Dict[str, Table], stats: Dict[str, Any]) -> None:
    """Generate consciousness health reports by district."""
    # This would analyze geographic distribution of drift
    # For V1, we just log the overall stats
    
    if stats['critical_count'] > 5:
        log.warning("CONSCIOUSNESS CRISIS: Multiple citizens approaching incoherence!")
        # In full implementation, this would trigger emergency Clero response


def main():
    """Main entry point for consciousness drift processing."""
    
    # Initialize tables
    try:
        tables = {
            'citizens': Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS"),
            'relationships': Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "RELATIONSHIPS"),
            'activities': Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "ACTIVITIES")
        }
    except Exception as e:
        log.error(f"Failed to initialize Airtable: {e}")
        return
    
    # Get Venice time
    venice_tz = pytz.timezone(VENICE_TIMEZONE)
    venice_time = datetime.now(venice_tz)
    
    log.info(f"Starting consciousness drift check at {venice_time}")
    
    # Process drift
    stats = process_consciousness_drift(tables, venice_time)
    
    # Generate reports
    generate_district_report(tables, stats)
    
    log.info("Consciousness drift check complete")


if __name__ == "__main__":
    main()