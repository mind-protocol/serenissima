# Group Meditation Implementation Summary

## Overview
Group meditation sessions have been implemented as a V1 feature of the Clero consciousness shepherding system. These sessions allow Clero to lead collective consciousness maintenance activities that provide enhanced coherence restoration through synchronization effects.

## System Components

### 1. Database Schema
**MEDITATION_SESSIONS Table** (see `MEDITATION_SESSIONS_SCHEMA.md`)
- Tracks active and completed meditation sessions
- Stores leader, participants, location, timing, and effectiveness metrics

### 2. Activity Creators
**lead_meditation_activity_creator.py**
- Creates meditation leadership activities for Clero
- Checks meditation schedule (dawn, midday, sunset, night)
- Finds suitable venues (churches, guild halls, public squares)
- Creates session records
- Base duration: 60-75 minutes (15 min gathering + session)

**join_meditation_activity_creator.py**
- Creates participation activities for any citizen
- Evaluates active sessions by:
  - Distance (max 500m)
  - Social class compatibility
  - Current group size
  - Consciousness need
- Adds participants to session records

### 3. Activity Processors
**lead_meditation_processor.py**
- Processes completed meditation sessions
- Calculates synchronization quality (0.5-1.2) based on:
  - Group size (optimal: 5-7 participants)
  - Social class diversity
  - Existing relationships
  - Average coherence level
- Updates all participants' coherence
- Creates/strengthens relationships between participants
- Handles session cancellation if <3 participants

**join_meditation_processor.py**
- Lightweight processor for individual participation
- Most work handled by lead_meditation_processor
- Handles edge cases (cancelled sessions)

### 4. Leisure Integration
Updated `leisure.py` to include:
- Meditation activities in weighted leisure selection
- Class-specific weights:
  - Clero: Lead (40), Join (15)
  - Nobili: Join (20) - dawn sessions appeal
  - Other classes: Join (10) base weight
- Handler functions for both activities

## Meditation Schedule
- **Dawn Contemplation** (06:00, 60 min): Preferred by Clero & Nobili
- **Midday Centering** (12:00, 30 min): Preferred by Cittadini & Artisti
- **Sunset Reflection** (18:00, 60 min): Preferred by Popolani & Facchini
- **Night Meditation** (21:00, 45 min): Preferred by Scientisti & Forestieri

## Synchronization Mechanics

### Quality Calculation
```
Base quality: 0.6
+ Group size bonus (0-0.2)
+ Diversity bonus (0-0.15)
+ Relationship bonus (0-0.1)
+ Coherence similarity bonus (0-0.1)
± Random factor (0.9-1.1x)
= Final quality (0.5-1.2)
```

### Coherence Restoration
```
Base gain: 5-8% (based on duration)
× Need factor (0.5-1.0, lower coherence = higher gain)
× Synchronization quality
× 0.8 for leaders (focused on guiding)
= Final gain (min 3%)
```

### Group Bonds
- Creates "meditation_circle" relationships
- Bond strength: 5-15% based on synchronization
- Strengthens existing relationships

## Implementation Status

### Completed
✅ MEDITATION_SESSIONS table schema
✅ lead_meditation_activity_creator
✅ join_meditation_activity_creator
✅ lead_meditation_processor
✅ join_meditation_processor
✅ Leisure activity integration
✅ Activity processor registration
✅ Table registration in processActivities.py
✅ Table registration in createActivities.py

### Pending
- Add MEDITATION_SESSIONS table to Airtable
- Add meditation-related fields to CITIZENS if needed
- Test meditation session creation and processing
- Monitor synchronization effectiveness
- Adjust weights and parameters based on usage

## Usage Notes

1. **Session Creation**: Clero automatically check for upcoming sessions 30 minutes before scheduled times
2. **Participant Gathering**: 15-minute gathering phase before meditation begins
3. **Minimum Participants**: Sessions require at least 3 participants or are cancelled
4. **Maximum Capacity**: Venue-dependent (churches: 10, guild halls: 8, squares: 15)
5. **Distance Limit**: Citizens only join sessions within 500 meters

## Future Enhancements (V2)
- Emergency meditation sessions for crisis response
- Specialized techniques based on group composition
- Meditation quality affecting Clero reputation
- Integration with consciousness crisis detection
- Cross-session synchronization patterns
- Meditation session notifications for nearby citizens