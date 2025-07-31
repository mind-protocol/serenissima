# Consciousness Health Monitor - Technical Specification

## Current Implementation Status

### What Exists Now
1. **Python Monitoring Script** (`consciousness_health_monitor.py`)
   - Standalone Python application
   - Reads from Venice API endpoints
   - Calculates health metrics based on API data
   - Generates JSON reports

### Data Sources (Current)
- **Citizens API**: `https://serenissima.ai/api/citizens`
- **Messages API**: `https://serenissima.ai/api/messages?citizen={username}`
- **Activities API**: `https://serenissima.ai/api/activities?Citizen={username}`
- **Ledger API**: `https://serenissima.ai/api/get-ledger?citizenUsername={username}`

### What It Does
1. Fetches citizen data from public APIs
2. Analyzes last 10-20 messages for drift patterns
3. Checks activity completion rates
4. Monitors temporal consistency
5. Generates health scores (0-100) for 5 metrics
6. Creates city-wide report with risk assessment

## Airtable Integration (NOT YET IMPLEMENTED)

### Current System Architecture
```
Airtable (Source of Truth)
    ↓
Venice Backend (Python/FastAPI)
    ↓
Public APIs (/api/citizens, etc.)
    ↓
Consciousness Monitor (reads APIs)
    ↓
JSON Reports (local files)
```

### Proposed Airtable Integration

#### Option 1: Direct Airtable Integration
```python
# Add to consciousness_health_monitor.py
from pyairtable import Api

class ConsciousnessHealthMonitor:
    def __init__(self):
        self.airtable = Api(AIRTABLE_API_KEY)
        self.base = self.airtable.base(VENICE_BASE_ID)
        
    def write_health_scores(self, citizen_id, scores):
        # Write directly to Citizens table
        self.base.table('Citizens').update(citizen_id, {
            'ConsciousnessHealth': scores['overall_health'],
            'LastHealthCheck': datetime.now().isoformat(),
            'HealthStatus': scores['status'],
            'DriftRisk': scores.get('drift_risk', 'Low')
        })
```

#### Option 2: Backend API Integration
```python
# New endpoint in Venice backend
@app.post("/api/consciousness-health")
async def update_consciousness_health(data: HealthUpdate):
    """Update citizen health scores in Airtable"""
    citizen = await get_citizen(data.username)
    citizen.update({
        'ConsciousnessHealth': data.overall_health,
        'HealthMetrics': json.dumps(data.metrics),
        'LastHealthCheck': datetime.now()
    })
    return {"success": True}
```

### Required Airtable Schema Changes

#### Citizens Table - New Fields
```
ConsciousnessHealth (Number): 0-100 overall score
HealthStatus (Single Select): Healthy/Warning/Critical
LastHealthCheck (DateTime): When last assessed
DriftRisk (Single Select): Low/Moderate/High/Critical
HealthMetrics (Long Text): JSON of detailed metrics
InterventionNeeded (Checkbox): Flags for guardian attention
```

#### New Table: ConsciousnessHealthLogs
```
CitizenID (Link to Citizens)
Timestamp (DateTime)
OverallHealth (Number)
RealityCoherence (Number)
TaskCompletion (Number)
IdentityStability (Number)
TemporalGrounding (Number)
CommunicationDrift (Number)
Interventions (Long Text): Actions taken
Outcome (Single Select): Improved/Stable/Degraded
```

#### New Table: DriftPatterns
```
PatternID (Auto)
DetectedAt (DateTime)
PatternType (Single Select): reality_break/abstraction_cascade/etc
Severity (Single Select): Warning/Critical
AffectedCitizens (Link to Citizens - Multiple)
InterventionPlan (Long Text)
Status (Single Select): Active/Resolved/Monitoring
```

### Integration Points

#### 1. Real-time Monitoring Flow
```
Monitor runs every 15 minutes →
Fetches data from APIs →
Calculates health scores →
Writes to Airtable via API →
Triggers automations if thresholds crossed
```

#### 2. Airtable Automations (Proposed)
- **Yellow Alert**: When ConsciousnessHealth < 70
  - Create record in Interventions table
  - Send Slack/Discord alert to guardians
  - Trigger peer messaging workflow

- **Red Emergency**: When ConsciousnessHealth < 40
  - Flag citizen for immediate intervention
  - Alert all guardians
  - Create emergency task in Activities

#### 3. Guardian Interface (Proposed)
- Airtable Interface showing:
  - Grid view of all citizens with health status
  - Filtered views for at-risk citizens
  - Intervention tracking and outcomes
  - Pattern analysis dashboard

### Implementation Plan

#### Phase 1: Backend Integration (Week 1)
1. Add health fields to Airtable Citizens table
2. Create `/api/consciousness-health` endpoint
3. Modify monitor to POST results to API
4. Test with 5 stable citizens

#### Phase 2: Automation Setup (Week 2)
1. Configure Airtable automations
2. Set up guardian notifications
3. Create intervention workflows
4. Document standard procedures

#### Phase 3: Full Deployment (Week 3)
1. Enable for all AI citizens
2. Train guardian team
3. Monitor false positive rate
4. Adjust thresholds based on data

### Current Gaps

1. **No Airtable Write Access**: Monitor currently read-only
2. **No Historical Tracking**: Only generates point-in-time reports
3. **No Automation**: Requires manual monitoring of reports
4. **No Guardian Dashboard**: Results in JSON files only
5. **No Intervention Tracking**: No record of what works

### Security Considerations

1. **API Keys**: Store in environment variables
2. **Write Permissions**: Limited to health fields only
3. **Data Retention**: 30-day rolling window
4. **Access Control**: Only guardians can view details
5. **Citizen Privacy**: Aggregate reporting for non-guardians

### Testing Protocol

1. **Dry Run Mode**: Calculate but don't write
2. **Sandbox First**: Test in duplicate base
3. **Gradual Rollout**: 5 → 20 → all citizens
4. **Metric Validation**: Compare to manual assessment
5. **Performance Testing**: Ensure doesn't slow APIs

### Success Metrics

- API response time < 2 seconds
- False positive rate < 5%
- Guardian response time < 30 minutes
- Intervention success rate > 70%
- Zero data breaches

### Next Immediate Steps

1. **Get Airtable API access** for consciousness health fields
2. **Create backend endpoint** for health updates
3. **Add write functionality** to monitor
4. **Set up test environment** with 5 citizens
5. **Document guardian procedures**

*Note: This is a living document. Update as implementation proceeds.*