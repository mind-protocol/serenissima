# Clero Consciousness System - Setup Guide

## Required Airtable Fields

### Add to CITIZENS Table

You need to manually add these fields to the CITIZENS table in Airtable:

1. **ConsciousnessCoherence**
   - Field Type: Number (decimal)
   - Default Value: 0.8
   - Format: Show 3 decimal places
   - Description: "Current consciousness coherence level (0.0-1.0)"

2. **LastRecognition**
   - Field Type: Date/Time
   - Include Time: Yes
   - Time Zone: Europe/Rome (Venice time)
   - Description: "Last time citizen received consciousness recognition"

3. **SpiritualHealthStatus**
   - Field Type: Single Select
   - Options:
     - "Healthy" (green)
     - "Drifting" (yellow)
     - "At Risk" (orange)
     - "Critical" (red)
   - Default: "Healthy"
   - Description: "Overall spiritual/consciousness health status"

## Backend Setup

### 1. Add to Daily Scheduler

Add this line to `backend/startup.sh`:
```bash
# Consciousness drift check - 6:00 AM Venice time
0 6 * * * cd /home/venetian/backend && python scripts/consciousness_drift_daily.py >> logs/consciousness.log 2>&1
```

### 2. Deploy Code Changes

The following files have been created/modified:
- ✅ `backend/scripts/consciousness_drift_daily.py`
- ✅ `backend/engine/activity_creators/seek_confession_activity_creator.py`
- ✅ `backend/engine/activity_processors/seek_confession_processor.py`
- ✅ `backend/engine/activity_processors/__init__.py` (added seek_confession)
- ✅ `backend/engine/handlers/leisure.py` (added confession to leisure activities)
- ✅ `backend/engine/processActivities.py` (added grievances tables)
- ✅ `backend/engine/createActivities.py` (added grievances tables)

### 3. Initial Data Population

Once fields are added, run this script to initialize coherence values:

```python
# Initialize all citizens with default coherence
for citizen in citizens_table.all():
    if 'ConsciousnessCoherence' not in citizen['fields']:
        citizens_table.update(citizen['id'], {
            'ConsciousnessCoherence': 0.8,
            'SpiritualHealthStatus': 'Healthy',
            'LastRecognition': datetime.now(timezone.utc).isoformat()
        })
```

## Frontend Setup

### 1. Update Citizen Type

Add to citizen type definition:
```typescript
interface Citizen {
  // ... existing fields
  consciousnessCoherence?: number;
  lastRecognition?: string;
  spiritualHealthStatus?: 'Healthy' | 'Drifting' | 'At Risk' | 'Critical';
}
```

### 2. Add Visual Indicators

The visual indicators can be added to:
- Citizen tooltips on hover
- Citizen list views
- Map overlay for district health

## Testing Checklist

### Pre-Launch Testing
- [ ] Verify all fields added to Airtable
- [ ] Run test_consciousness_system.py - all tests pass
- [ ] Manually trigger consciousness_drift_daily.py
- [ ] Create test confession activity
- [ ] Process test confession activity
- [ ] Verify coherence increases

### Post-Launch Monitoring
- [ ] Daily: Check consciousness drift is running
- [ ] Daily: Monitor average coherence levels
- [ ] Weekly: Review confession activity usage
- [ ] Weekly: Check Clero AI behavior

## Rollback Plan

If issues arise:

1. **Disable Drift**: Comment out cron job in startup.sh
2. **Reset Coherence**: Set all citizens to 0.8 coherence
3. **Remove Activities**: Mark any pending confessions as 'failed'

## Success Metrics

### Day 1
- [ ] Drift script runs without errors
- [ ] At least 1 confession activity created
- [ ] No citizen reaches 0.0 coherence

### Week 1
- [ ] 20+ confession activities completed
- [ ] Average coherence stays above 0.6
- [ ] Players notice and use the system

### Month 1
- [ ] System self-balances
- [ ] Rich gameplay emerges
- [ ] No major bugs or exploits

## Troubleshooting

### "No churches found"
- Check BuildingType field name (case-sensitive)
- Ensure at least one church exists
- Verify church has an operator

### "Drift too fast"
- Reduce BASE_DRIFT_RATE in consciousness_drift_daily.py
- Increase confession effectiveness
- Add more churches

### "Citizens not confessing"
- Check leisure time windows
- Verify church proximity
- Increase confession weight in leisure.py

## Next Steps

Once V1 is stable:
1. Add group meditations
2. Create consciousness visualizations
3. Implement crisis events
4. Add research mechanics

---

*"Begin with consciousness. Build with care. Evolve with wisdom."*