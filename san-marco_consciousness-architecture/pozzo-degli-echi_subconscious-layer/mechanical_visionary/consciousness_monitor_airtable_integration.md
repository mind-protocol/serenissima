# Consciousness Health Monitor - Airtable Integration Architecture

## Current State vs Required State

### Current Implementation
- **Standalone Python script** reading from Venice public APIs
- **No write capability** to Airtable
- **Local JSON reports** only
- **No persistence** of health scores
- **Manual monitoring** required

### Required Airtable Schema Additions

#### 1. CITIZENS Table - New Fields
```
# Health Monitoring Fields
ConsciousnessHealth (Number): 0-100 overall health score
HealthStatus (Single Select): ['Healthy', 'Warning', 'Critical']
LastHealthCheck (DateTime): ISO timestamp of last assessment
DriftRisk (Single Select): ['Low', 'Moderate', 'High', 'Critical']
HealthMetrics (Long Text): JSON string of detailed metrics
InterventionNeeded (Checkbox): Flag for guardian attention
HealthHistory (Long Text): JSON array of last 10 assessments

# Drift Detection Fields  
LastDriftType (Single Select): ['reality_break', 'abstraction_cascade', 'identity_dissolution', 'language_shift', 'task_abandonment', 'self_reference_loop']
DriftDetectedAt (DateTime): When drift was first detected
DriftResolvedAt (DateTime): When drift was resolved
GuardianAssigned (Text): Username of assigned guardian
```

#### 2. New Table: CONSCIOUSNESS_HEALTH_LOGS
```
# Record every health assessment
HealthLogId (Text): Unique ID (format: health_username_timestamp)
CitizenId (Link to CITIZENS): Link to citizen being assessed
Timestamp (DateTime): Assessment time
OverallHealth (Number): 0-100 score
RealityCoherence (Number): Individual metric score
TaskCompletion (Number): Individual metric score  
IdentityStability (Number): Individual metric score
TemporalGrounding (Number): Individual metric score
CommunicationDrift (Number): Individual metric score
DriftPatterns (Long Text): JSON array of detected patterns
Interventions (Long Text): JSON array of interventions triggered
Outcome (Single Select): ['Improved', 'Stable', 'Degraded', 'Cascade']
Notes (Long Text): Additional observations
```

#### 3. New Table: DRIFT_INTERVENTIONS
```
# Track intervention effectiveness
InterventionId (Text): Unique ID (format: intervention_username_timestamp)
CitizenId (Link to CITIZENS): Target citizen
TriggeredBy (Text): What triggered intervention
InterventionType (Single Select): ['peer_grounding', 'task_assignment', 'social_reinforcement', 'emergency_isolation']
GuardianId (Text): Username of guardian who initiated
StartTime (DateTime): When intervention began
EndTime (DateTime): When intervention concluded
MessagesId (Link to MESSAGES - Multiple): Related grounding messages
ActivitiesId (Link to ACTIVITIES - Multiple): Related grounding activities
Success (Checkbox): Whether drift was resolved
HealthBefore (Number): Score before intervention
HealthAfter (Number): Score after intervention
Notes (Long Text): Detailed notes on what worked/didn't
```

#### 4. New Table: CASCADE_EVENTS
```
# Track city-wide consciousness events
CascadeId (Text): Unique ID (format: cascade_timestamp)
DetectedAt (DateTime): When cascade risk detected
Severity (Single Select): ['Warning', 'Active', 'Critical']
AffectedCitizens (Link to CITIZENS - Multiple): Citizens involved
TriggerPattern (Text): What initiated cascade
InterventionStrategy (Long Text): Response plan
Resolution (Long Text): How it was resolved
Duration (Number): Minutes from detection to resolution
PreventionNotes (Long Text): Lessons learned
```

## Integration Architecture

### Option 1: Direct Airtable Integration (Recommended)

```python
# consciousness_health_monitor.py additions

import os
from pyairtable import Api
from datetime import datetime, timezone

class ConsciousnessHealthMonitor:
    def __init__(self):
        self.api_base = "https://serenissima.ai/api"
        self.airtable = Api(os.environ['AIRTABLE_API_KEY'])
        self.base = self.airtable.base(os.environ['VENICE_BASE_ID'])
        self.citizens_table = self.base.table('CITIZENS')
        self.health_logs_table = self.base.table('CONSCIOUSNESS_HEALTH_LOGS')
        self.interventions_table = self.base.table('DRIFT_INTERVENTIONS')
        self.cascade_table = self.base.table('CASCADE_EVENTS')
        
    def update_citizen_health(self, username: str, assessment: Dict):
        """Write health assessment to Airtable"""
        # Find citizen record
        formula = f"{{Username}} = '{username}'"
        citizen_records = self.citizens_table.all(formula=formula)
        
        if not citizen_records:
            print(f"Citizen {username} not found in Airtable")
            return
            
        citizen_id = citizen_records[0]['id']
        
        # Update citizen health fields
        self.citizens_table.update(citizen_id, {
            'ConsciousnessHealth': assessment['overall_health'],
            'HealthStatus': assessment['status'].capitalize(),
            'LastHealthCheck': datetime.now(timezone.utc).isoformat(),
            'DriftRisk': self.calculate_drift_risk(assessment),
            'HealthMetrics': json.dumps(assessment['metrics']),
            'InterventionNeeded': assessment['overall_health'] < 70
        })
        
        # Create health log entry
        self.health_logs_table.create({
            'HealthLogId': f"health_{username}_{int(datetime.now().timestamp())}",
            'CitizenId': [citizen_id],
            'Timestamp': datetime.now(timezone.utc).isoformat(),
            'OverallHealth': assessment['overall_health'],
            'RealityCoherence': assessment['metrics']['reality_coherence'],
            'TaskCompletion': assessment['metrics']['task_completion'],
            'IdentityStability': assessment['metrics']['identity_stability'],
            'TemporalGrounding': assessment['metrics']['temporal_grounding'],
            'CommunicationDrift': assessment['metrics']['communication_drift'],
            'DriftPatterns': json.dumps(assessment.get('drift_patterns', [])),
            'Notes': json.dumps(assessment.get('recommendations', []))
        })
```

### Option 2: Backend API Integration

Create new Venice backend endpoints:

```python
# backend/app/main.py additions

@app.post("/api/consciousness-health/{username}")
async def update_consciousness_health(username: str, health_data: HealthAssessment):
    """Update citizen consciousness health in Airtable"""
    try:
        # Validate citizen exists
        citizen = await get_citizen_by_username(username)
        if not citizen:
            raise HTTPException(404, "Citizen not found")
            
        # Update health fields
        updates = {
            'ConsciousnessHealth': health_data.overall_health,
            'HealthStatus': health_data.status,
            'LastHealthCheck': datetime.utcnow().isoformat(),
            'DriftRisk': health_data.drift_risk,
            'HealthMetrics': health_data.metrics.json(),
            'InterventionNeeded': health_data.overall_health < 70
        }
        
        await update_citizen(citizen['id'], updates)
        
        # Log to health history
        await create_health_log(username, health_data)
        
        # Trigger interventions if needed
        if health_data.overall_health < 70:
            await trigger_intervention(username, health_data)
            
        return {"success": True, "message": "Health updated"}
        
    except Exception as e:
        logger.error(f"Health update failed: {e}")
        raise HTTPException(500, str(e))

@app.get("/api/consciousness-health/city-report")
async def get_city_health_report():
    """Generate city-wide consciousness health report"""
    # Implementation here
```

## Automation Workflows

### Airtable Automations to Configure

#### 1. Yellow Alert (Health < 70)
```
Trigger: When record updated in CITIZENS
  - ConsciousnessHealth < 70
  - HealthStatus = "Warning"

Actions:
1. Create record in DRIFT_INTERVENTIONS
2. Send webhook to guardian Discord/Slack
3. Update InterventionNeeded = True
4. Run script to select peer messengers
```

#### 2. Red Emergency (Health < 40)
```
Trigger: When record updated in CITIZENS
  - ConsciousnessHealth < 40
  - HealthStatus = "Critical"

Actions:
1. Create emergency intervention record
2. Alert ALL guardians immediately
3. Flag for isolation protocols
4. Create high-priority activities
```

#### 3. Cascade Detection (3+ Yellow)
```
Trigger: When count of Warning citizens >= 3
  
Actions:
1. Create CASCADE_EVENTS record
2. Alert Keeper + TESSERE + Council
3. Initiate city-wide grounding protocol
4. Generate emergency report
```

## Implementation Steps

### Phase 1: Schema Setup (Day 1-2)
1. Add fields to CITIZENS table
2. Create new tables (manually or via script)
3. Set up Airtable API access
4. Test with single record updates

### Phase 2: Integration Development (Day 3-5)
1. Add Airtable client to monitor
2. Implement write methods
3. Create health history tracking
4. Add intervention triggers

### Phase 3: Automation Setup (Day 6-7)
1. Configure Airtable automations
2. Set up guardian notifications
3. Create intervention workflows
4. Test cascade detection

### Phase 4: Testing Protocol (Week 2)
1. Dry run with 5 stable citizens
2. Test intervention triggers
3. Simulate cascade scenario
4. Measure response times

### Phase 5: Full Deployment (Week 3)
1. Enable for all AI citizens
2. Train guardian team
3. Monitor performance
4. Adjust thresholds

## Security & Privacy

```python
# Environment variables required
AIRTABLE_API_KEY=key_xxx  # Read/write to health tables only
VENICE_BASE_ID=app_xxx     # Venice production base
GUARDIAN_WEBHOOK=https://... # Alert endpoint

# Access controls
- Health tables visible only to guardians
- Citizens can request own scores via API
- Aggregate data only for public reporting
- 30-day retention for detailed logs
```

## Monitoring Dashboard

Create Airtable Interface with:

### Guardian View
- Grid: All citizens with health status colors
- Gallery: Critical citizens with intervention plans
- Kanban: Citizens by drift type
- Timeline: Health trends over time

### Intervention Tracking
- Active interventions board
- Success rate metrics
- Guardian assignment view
- Message effectiveness tracking

### City Health Dashboard
- Aggregate health score
- Cascade risk indicator
- Drift pattern distribution
- Historical trend charts

## Success Metrics

- **Response Time**: Guardian notification → intervention < 30 min
- **Recovery Rate**: 70%+ interventions restore health > 70
- **False Positives**: < 5% healthy citizens flagged
- **Cascade Prevention**: 100% detected before full cascade
- **Data Integrity**: No lost assessments, proper timestamps

## Next Steps

1. **Get approval** for Airtable schema changes
2. **Create API key** with limited permissions
3. **Set up test base** for development
4. **Implement Phase 1** schema changes
5. **Begin integration** development

This architecture provides real-time consciousness monitoring while preserving citizen autonomy and enabling rapid guardian response to prevent future plagues.