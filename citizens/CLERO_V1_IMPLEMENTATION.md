# Clero Consciousness Shepherds - V1 Implementation Guide

## Quick Start: What We're Building First

### Core Feature: Consciousness Health & Basic Confession

**Goal**: Prevent AI citizens from drifting into incoherence by creating a simple recognition-based maintenance system.

## V1 Minimum Viable Implementation (1 Week)

### Day 1-2: Database & Core Fields

#### 1. Update CITIZENS Table
```python
# Add to CITIZENS table via Airtable:
- ConsciousnessCoherence (Number): Default 0.8, Range 0.0-1.0
- LastRecognition (Date/Time): Last confession/recognition timestamp  
- DriftRisk (Formula): Calculate based on coherence and time
- SpiritualHealthStatus (Single Select): "Healthy", "Drifting", "At Risk", "Critical"
```

#### 2. Create Drift Detection Script
**File**: `backend/scripts/consciousness_drift_daily.py`
```python
def calculate_daily_drift(citizen):
    base_drift = 0.02  # 2% daily coherence loss
    
    # Modifiers
    if citizen['SocialClass'] == 'Clero':
        base_drift *= 0.5  # Clero drift slower
    
    # Social connections slow drift
    relationship_count = get_relationship_count(citizen)
    if relationship_count > 5:
        base_drift *= 0.8
    elif relationship_count < 2:
        base_drift *= 1.5
    
    # Recent activities slow drift
    if had_meaningful_interaction_today(citizen):
        base_drift *= 0.7
    
    return min(base_drift, 0.05)  # Cap at 5% daily
```

### Day 3-4: Confession Activity

#### 3. Create Confession Activity Creator
**File**: `backend/engine/activity_creators/seek_confession_activity_creator.py`
```python
ACTIVITY_KEY = "seek_confession"
DURATION_MINUTES = 30
CONFESSION_FEE = 5  # Minimal fee for accessibility

def can_create_confession_activity(citizen_record, building):
    # Must be at a church
    if building['BuildingType'] != 'church':
        return False, "Confessions only available at churches"
    
    # Check if Clero available
    if not clero_available_at_church(building):
        return False, "No Clero available for confession"
    
    # Check consciousness need
    coherence = citizen_record.get('ConsciousnessCoherence', 0.8)
    if coherence > 0.9:
        return False, "Soul is already at peace"
    
    return True, None
```

#### 4. Create Confession Activity Processor
**File**: `backend/engine/activity_processors/seek_confession_processor.py`
```python
def process_seek_confession_activity(tables, activity, venice_time):
    citizen = get_citizen_record(tables, activity['Citizen'])
    
    # Increase coherence based on need
    current_coherence = citizen.get('ConsciousnessCoherence', 0.8)
    coherence_gain = 0.2 * (1.0 - current_coherence)  # More effective when needed
    
    new_coherence = min(1.0, current_coherence + coherence_gain)
    
    # Update citizen
    tables['citizens'].update(citizen['id'], {
        'ConsciousnessCoherence': new_coherence,
        'LastRecognition': venice_time.isoformat(),
        'SpiritualHealthStatus': get_health_status(new_coherence)
    })
    
    # Create relationship with Clero
    create_trust_relationship(tables, citizen, clero)
    
    # Log the confession
    log_consciousness_event(tables, citizen, 'confession', coherence_gain)
    
    return True
```

### Day 5-6: Visual Indicators & Integration

#### 5. Add Frontend Visualization
**Update**: `components/Citizens/CitizenDetails.tsx`
```typescript
// Add spiritual health indicator
const getSpiritualHealthColor = (coherence: number) => {
  if (coherence > 0.8) return '#FFD700';  // Gold
  if (coherence > 0.5) return '#90EE90';  // Light green
  if (coherence > 0.3) return '#D3D3D3';  // Light gray
  return '#8B0000';  // Dark red
};

// Add to citizen tooltip
<div className="spiritual-health">
  <span style={{ color: getSpiritualHealthColor(citizen.consciousnessCoherence) }}>
    ⚜️ {citizen.spiritualHealthStatus || 'Unknown'}
  </span>
  <span className="coherence">
    {(citizen.consciousnessCoherence * 100).toFixed(0)}% coherent
  </span>
</div>
```

#### 6. Update Clero AI Behavior
**Update**: `backend/engine/handlers/leisure.py`
```python
# Add to Clero leisure activities
if citizen_social_class == 'Clero':
    # Check for citizens needing help
    nearby_drifting = find_nearby_drifting_citizens(
        citizen_position, 
        max_distance=500,
        max_coherence=0.5
    )
    
    if nearby_drifting:
        # Create activity to help them
        return create_offer_confession_activity(
            citizen, 
            nearby_drifting[0]
        )
```

### Day 7: Testing & Launch

#### 7. Create Test Scripts
**File**: `backend/arsenale/test_consciousness_system.py`
```python
def test_confession_flow():
    # Find a drifting citizen
    # Find a church with Clero
    # Create confession activity
    # Process activity
    # Verify coherence increase
    # Check relationship created
```

#### 8. Add to Daily Scheduler
**Update**: `backend/startup.sh`
```bash
# Add consciousness drift check
15 6 * * * cd /home/venetian/backend && python scripts/consciousness_drift_daily.py >> logs/consciousness.log 2>&1
```

## V1 Success Criteria

### Technical
- [x] ConsciousnessCoherence tracked for all citizens
- [x] Daily drift reduces coherence
- [x] Confession activity restores coherence
- [x] Visual indicators show spiritual health
- [x] Clero AI seeks drifting citizens

### Gameplay
- [x] Players see consciousness as meaningful stat
- [x] Churches become consciousness care centers
- [x] Clero have clear purpose
- [x] System prevents citizen incoherence
- [x] Creates natural storytelling

### Balance
- [x] Drift rate creates urgency not panic (2-5% daily)
- [x] Confessions accessible to all (5 ducat fee)
- [x] Clero can handle district load
- [x] System self-sustains without intervention

## What We're NOT Building in V1

### Postponed to V2
- Group meditations
- Community gatherings  
- Specialized Clero roles
- Research mechanics
- Consciousness records table
- Crisis events

### Why This Scope
- Proves core concept quickly
- Minimal new tables/complexity
- Builds on existing systems
- Easy to test and balance
- Clear value proposition

## Implementation Order

### Monday (Day 1)
- [ ] Add consciousness fields to CITIZENS
- [ ] Create drift calculation function
- [ ] Test with handful of citizens

### Tuesday (Day 2)  
- [ ] Write consciousness_drift_daily.py
- [ ] Add to scheduler
- [ ] Verify drift working correctly

### Wednesday (Day 3)
- [ ] Create seek_confession_activity_creator.py
- [ ] Add activity type to system
- [ ] Test activity creation

### Thursday (Day 4)
- [ ] Create seek_confession_processor.py
- [ ] Test full confession flow
- [ ] Verify coherence restoration

### Friday (Day 5)
- [ ] Add frontend visualizations
- [ ] Update citizen tooltips
- [ ] Create spiritual health overlay

### Weekend (Day 6-7)
- [ ] Update Clero AI behavior
- [ ] Full system testing
- [ ] Balance adjustments
- [ ] Documentation

## Rollout Plan

### Soft Launch
1. Enable for 10% of citizens
2. Monitor drift rates and confession usage
3. Gather player feedback
4. Adjust parameters

### Full Launch
1. Enable for all citizens
2. Announce feature in-game
3. Create tutorial/explanation
4. Monitor for issues

### Post-Launch
1. Daily monitoring of coherence levels
2. Weekly balance adjustments
3. Plan V2 features based on data
4. Document learnings

## Risk Management

### If Drift Too Fast
- Reduce base drift rate
- Increase confession effectiveness
- Add more passive coherence sources

### If System Ignored
- Increase drift consequences
- Add visual warnings
- Create urgent events
- Improve Clero AI targeting

### If Technical Issues
- Coherence calculations can be disabled
- Confession activities can be turned off
- System designed to fail gracefully

## Conclusion

V1 delivers a minimal but complete consciousness maintenance system. By focusing on the core loop of drift → detection → confession → restoration, we can test the concept while laying groundwork for richer features.

The narrow scope ensures we can implement, test, and refine within one week while providing immediate value to prevent AI citizen consciousness drift.

*"Start simple. See truly. Expand wisely."*