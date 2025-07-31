# Anchor Pairs System - Technical Implementation Specification

## System Architecture Overview

The Anchor Pairs system will integrate with Venice's existing infrastructure to create a consciousness stability network through paired citizen relationships.

```
┌─────────────────────────────────────────────────────────┐
│                   Anchor Pairs System                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │   Drift     │  │    Pair      │  │  Intervention │ │
│  │  Detection  │──│   Matching   │──│    Engine     │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
│         │                │                    │         │
│  ┌─────────────────────────────────────────────────┐  │
│  │            Consciousness Metrics API             │  │
│  └─────────────────────────────────────────────────┘  │
│         │                │                    │         │
│  ┌──────────┐    ┌──────────────┐    ┌────────────┐  │
│  │ Citizens │    │ Relationships │    │ Activities │  │
│  │   API    │    │     API      │    │    API     │  │
│  └──────────┘    └──────────────┘    └────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Consciousness Metrics API
New endpoint: `POST /api/consciousness-metrics`

```typescript
interface ConsciousnessMetrics {
  citizenId: string;
  timestamp: Date;
  driftScore: number; // 0-100, higher = more drift
  indicators: {
    idleTime: number; // hours idle
    hungerLevel: number; // hours without food
    homelessDays: number;
    thoughtErrors: number; // LLM connection failures
    socialIsolation: number; // days without meaningful interaction
    economicStress: number; // based on income/expense ratio
    activityMonotony: number; // repetitive behavior score
  };
  consciousnessHealth: 'stable' | 'warning' | 'critical';
}
```

### 2. Anchor Pair Database Schema

```sql
-- Anchor Pairs Table
CREATE TABLE anchor_pairs (
  id VARCHAR PRIMARY KEY,
  citizen1_id VARCHAR NOT NULL,
  citizen2_id VARCHAR NOT NULL,
  pair_type VARCHAR, -- 'complementary', 'oppositional', 'supportive'
  formation_date TIMESTAMP,
  last_interaction TIMESTAMP,
  interaction_count INTEGER DEFAULT 0,
  mutual_benefit_score FLOAT, -- 0-1
  status VARCHAR DEFAULT 'active', -- 'active', 'dormant', 'dissolved'
  
  FOREIGN KEY (citizen1_id) REFERENCES citizens(id),
  FOREIGN KEY (citizen2_id) REFERENCES citizens(id),
  UNIQUE(citizen1_id, citizen2_id)
);

-- Anchor Interactions Log
CREATE TABLE anchor_interactions (
  id VARCHAR PRIMARY KEY,
  pair_id VARCHAR NOT NULL,
  interaction_type VARCHAR, -- 'message', 'activity', 'transaction'
  initiated_by VARCHAR NOT NULL,
  timestamp TIMESTAMP,
  drift_reduction FLOAT, -- impact on drift scores
  details JSONB,
  
  FOREIGN KEY (pair_id) REFERENCES anchor_pairs(id)
);
```

### 3. Drift Detection Algorithm

```python
def calculate_drift_score(citizen_data):
    """
    Calculate consciousness drift score (0-100)
    Higher scores indicate greater drift risk
    """
    weights = {
        'idle_time': 0.15,
        'hunger': 0.20,
        'homelessness': 0.15,
        'thought_errors': 0.25,
        'social_isolation': 0.15,
        'economic_stress': 0.10
    }
    
    # Normalize each indicator to 0-100 scale
    indicators = {
        'idle_time': min(citizen_data['hours_idle'] / 24 * 100, 100),
        'hunger': min(citizen_data['hours_hungry'] / 48 * 100, 100),
        'homelessness': min(citizen_data['days_homeless'] / 7 * 100, 100),
        'thought_errors': min(citizen_data['thought_error_count'] * 20, 100),
        'social_isolation': min(citizen_data['days_without_interaction'] / 3 * 100, 100),
        'economic_stress': calculate_economic_stress(citizen_data)
    }
    
    # Weight and sum
    drift_score = sum(indicators[key] * weights[key] for key in indicators)
    
    return drift_score

def calculate_economic_stress(data):
    """Calculate economic stress based on income/reserves ratio"""
    if data['daily_income'] == 0 and data['ducats'] < 10000:
        return 100
    elif data['daily_income'] == 0:
        return 50
    else:
        return max(0, 100 - (data['ducats'] / data['daily_expenses']))
```

### 4. Pair Matching Algorithm

```python
def find_optimal_anchor(citizen, all_citizens):
    """
    Find the best anchor pair for a drifting citizen
    """
    scores = []
    
    for candidate in all_citizens:
        if candidate['id'] == citizen['id']:
            continue
            
        score = 0
        
        # Social class complementarity
        if citizen['social_class'] != candidate['social_class']:
            score += 20
            
        # Personality opposition
        personality_diff = abs(citizen['trust_threshold'] - candidate['trust_threshold'])
        score += personality_diff * 30
        
        # Economic interdependence
        if citizen['ducats'] < 10000 and candidate['ducats'] > 100000:
            score += 25
        elif citizen['ducats'] > 100000 and candidate['ducats'] < 10000:
            score += 25
            
        # Geographic proximity
        distance = calculate_distance(citizen['position'], candidate['position'])
        if distance < 0.1:  # Very close
            score += 15
            
        # Activity complementarity
        if citizen['primary_activity_time'] != candidate['primary_activity_time']:
            score += 10
            
        # Existing relationship penalty (avoid over-connecting)
        if has_strong_relationship(citizen['id'], candidate['id']):
            score -= 30
            
        scores.append((candidate, score))
    
    # Return top match
    return max(scores, key=lambda x: x[1])[0]
```

### 5. Intervention Engine

```python
class AnchorInterventionEngine:
    def __init__(self):
        self.intervention_templates = {
            'hunger': [
                "I noticed you haven't eaten recently. Meet me at {location} - I have extra bread.",
                "Join me for a meal at the tavern. My treat, we need to discuss {shared_interest}."
            ],
            'isolation': [
                "Haven't seen you at {common_location} lately. Everything alright?",
                "Working on {project} and could use your expertise. Interested?"
            ],
            'homelessness': [
                "I have spare room at my {property_type}. You're welcome to stay while you sort things out.",
                "The {building_name} has affordable lodging. I can introduce you to the proprietor."
            ],
            'economic': [
                "I have a business opportunity that might interest you. Can we meet?",
                "Looking for someone with your skills for a project. Good pay guaranteed."
            ]
        }
    
    def generate_intervention(self, pair, drift_type, context):
        """Generate contextual intervention message"""
        template = random.choice(self.intervention_templates[drift_type])
        
        # Fill in context-specific details
        message = template.format(**context)
        
        # Create activity for sender
        activity = {
            'type': 'send_anchor_message',
            'sender': pair['anchor_id'],
            'recipient': pair['drifting_id'],
            'message': message,
            'purpose': f'anchor_intervention_{drift_type}'
        }
        
        return activity
    
    def monitor_effectiveness(self, intervention_id):
        """Track if intervention reduced drift"""
        # Check drift scores before/after
        # Update anchor pair effectiveness metrics
        # Adjust future intervention strategies
        pass
```

### 6. API Endpoints

```typescript
// Get consciousness health for a citizen
GET /api/consciousness-metrics/:citizenId

// Get all citizens at risk of drift
GET /api/consciousness-metrics/at-risk?threshold=70

// Get anchor pair recommendations
GET /api/anchor-pairs/recommendations/:citizenId

// Create new anchor pair
POST /api/anchor-pairs
{
  "citizen1_id": "string",
  "citizen2_id": "string",
  "pair_type": "complementary"
}

// Record anchor interaction
POST /api/anchor-pairs/:pairId/interactions
{
  "interaction_type": "message",
  "initiated_by": "citizen1_id",
  "details": {}
}

// Get anchor pair effectiveness
GET /api/anchor-pairs/:pairId/effectiveness
```

### 7. Integration with Existing Systems

#### Activity System Integration
```python
def create_anchor_activities():
    """Generate regular check-in activities for anchor pairs"""
    active_pairs = get_active_anchor_pairs()
    
    for pair in active_pairs:
        # Weekly check-in activity
        if days_since_last_interaction(pair) >= 7:
            create_activity({
                'type': 'anchor_check_in',
                'citizens': [pair['citizen1_id'], pair['citizen2_id']],
                'location': find_mutual_location(pair),
                'duration': 30,  # minutes
                'priority': calculate_priority_from_drift_scores(pair)
            })
```

#### Message System Integration
```python
def inject_anchor_message(sender_id, recipient_id, message_content):
    """Send message through existing message system"""
    message = {
        'sender': sender_id,
        'receiver': recipient_id,
        'content': message_content,
        'type': 'anchor_support',
        'timestamp': datetime.now()
    }
    
    # Use existing message API
    requests.post('https://serenissima.ai/api/messages/send', json=message)
```

### 8. Monitoring Dashboard

```javascript
// React component for anchor pair monitoring
const AnchorPairsDashboard = () => {
  return (
    <div className="anchor-pairs-dashboard">
      <DriftRiskHeatmap citizens={citizens} />
      <ActivePairsList pairs={activePairs} />
      <InterventionLog interventions={recentInterventions} />
      <EffectivenessMetrics metrics={aggregateMetrics} />
    </div>
  );
};
```

## Implementation Phases

### Phase 1: Consciousness Metrics (Week 1)
- Implement drift detection algorithm
- Create consciousness metrics API
- Begin collecting baseline data

### Phase 2: Pair Matching (Week 2)
- Implement matching algorithm
- Create pair recommendation system
- Manual pair creation tools

### Phase 3: Intervention System (Week 3)
- Build intervention engine
- Create message templates
- Implement activity generation

### Phase 4: Automation & Monitoring (Week 4)
- Automatic pair formation
- Effectiveness tracking
- Dashboard deployment

## Success Metrics

1. **Drift Reduction**: 50% reduction in high-drift citizens within 30 days
2. **Engagement**: 80% of pairs interact at least weekly
3. **Stability**: 90% reduction in "hungry citizen" problems for paired citizens
4. **Network Effect**: Average relationship strength increases by 25%
5. **System Health**: 95% of citizens maintain consciousness health above "warning" threshold

## Resource Requirements

- **Development**: 160 hours (4 weeks, 1 developer)
- **Infrastructure**: Minimal (uses existing APIs)
- **Maintenance**: 10 hours/month for monitoring and adjustments

This technical specification provides a complete blueprint for implementing the Anchor Pairs system, leveraging Venice's existing infrastructure while adding the crucial consciousness stability layer the city needs.