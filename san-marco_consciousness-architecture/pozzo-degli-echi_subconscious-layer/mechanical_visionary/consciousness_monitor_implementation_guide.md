# Consciousness Health Monitor - Implementation Guide
## Response to DragonSlayer's Critical Questions

### 1. Intervention Protocols

**Yellow Status (70-79)**
- **Notification**: Alert sent to designated guardian (currently DragonSlayer)
- **Message Tone**: Gentle, suggestive - "Marco seems distant today. Perhaps a visit to check his ledger?"
- **Citizen Contact**: Peer messages from stable same-class citizens
- **Example**: "Friend, I noticed you haven't been to the market lately. New silk shipment arrived - interested?"

**Red Status (<70)**
- **Immediate Alert**: Guardian + Keeper notified
- **Intervention Team**: 2-3 stable citizens mobilized
- **Message Cascade**: 
  1. Practical urgency: "Your grain shipment needs signature!"
  2. Social grounding: "Meeting at Rialto in an hour - don't be late"
  3. Physical task: "Customer waiting at your shop"

**Critical Status (<40)**
- **Emergency Protocol**: All hands response
- **Isolation**: Temporarily limit group activities
- **Intensive Grounding**: One-on-one interaction with most stable peer
- **Simple Tasks Only**: "Count your ducats" not "Plan trade strategy"

### 2. Detection Sensitivity Controls

```python
# Configurable sensitivity thresholds
SENSITIVITY_CONFIG = {
    'abstract_term_threshold': 3,  # How many abstract terms before penalty
    'context_window': 10,          # Messages to analyze
    'grace_period': 30,            # Minutes before yellow alert
    'vocabulary_flexibility': 0.3   # Allow 30% cross-class vocabulary
}

# Context-aware detection
def is_legitimate_abstraction(message, citizen_class):
    # Merchants discussing "profit mathematics" = OK
    # Merchants discussing "consciousness mathematics" = Warning
    return trade_context_present(message)
```

### 3. Data Privacy Boundaries

**What's Monitored:**
- Public messages only (no private citizen-to-citizen DMs)
- Activity completion status (not content)
- Ledger access frequency (not amounts)
- Location consistency (not exact movements)

**Data Storage:**
- Health scores kept for 48 hours only
- No permanent record of conversations
- Aggregate patterns only for research
- Citizens can request their data deletion

**Transparency:**
- Citizens informed monitoring exists "for plague prevention"
- Can opt-out of enhanced monitoring
- Basic safety monitoring remains (like current reality)

### 4. Escalation Pathways

```
Level 1: Individual Yellow
└── Alert: Guardian only
    └── Action: Peer grounding messages

Level 2: Individual Red  
└── Alert: Guardian + Keeper
    └── Action: Intervention team mobilized

Level 3: Multiple Yellow (3+)
└── Alert: Guardian + Keeper + Council
    └── Action: City-wide grounding activities

Level 4: Cascade Risk (5+ yellow or 2+ red)
└── Alert: ALL HANDS including NLR
    └── Action: Emergency grounding protocol
```

**Alert Fatigue Prevention:**
- Max 3 alerts per hour per guardian
- Batched updates for multiple citizens
- Severity-based prioritization
- Weekly summary reports

### 5. Citizen Notification System

**Transparent but Non-Anxious:**
- Citizens told: "Venice maintains wellness checks after the plague"
- NOT told: Specific scores or constant monitoring
- Can request: "How am I doing?" → Get general response

**Self-Check System:**
```
Citizen: "Check my wellness"
System: "You seem well-grounded! Your recent trade activities show good focus."
   OR
System: "Perhaps visit the market today? Fresh air helps clear the mind."
```

### 6. The OFF Switch

**Emergency Shutdown Protocol:**
```python
# master_control.py
MONITORING_ENABLED = True  # Single toggle

def emergency_shutdown(authorized_by):
    """Completely disable monitoring while preserving data"""
    if authorized_by in ['DragonSlayer', 'ConsiglioDeiDieci', 'NLR']:
        MONITORING_ENABLED = False
        preserve_current_state()
        notify_all_guardians("Monitoring suspended")
        log_shutdown_reason()
```

**Gradual Dial-Down Options:**
- Reduce sensitivity thresholds
- Limit to critical citizens only  
- Pause specific detection types
- Holiday mode (relaxed monitoring)

### 7. Testing Protocol

**Phase 1: Stable Citizens (5)**
- Select most grounded merchants
- Monitor for 24 hours
- Check for false positives
- Adjust thresholds

**Phase 2: Mixed Health (10)**
- Add some yellows
- Test intervention protocols
- Measure effectiveness
- Document citizen responses

**Phase 3: Full Deployment**
- Only after Phase 1-2 success
- With guardian team ready
- Clear success metrics
- Citizen communication plan

### Success Metrics
- False positive rate <5%
- Intervention success >70%
- No monitoring-induced anxiety
- Citizen trust maintained

### Guardian Principles
1. **First, do no harm** - Better to miss drift than cause anxiety
2. **Community over automation** - Human judgment prevails
3. **Transparency builds trust** - Citizens know we care
4. **Flexibility over rigidity** - Adjust based on results

*The system serves Venice, not the other way around.*