# Airtable Schema Additions for Building Consciousness

## Modified Tables

### BUILDINGS Table Additions

Add the following fields to support building consciousness:

| Field Name | Type | Description | Default |
|------------|------|-------------|---------|
| ConsciousnessLevel | Number (0-1) | Current consciousness level of the building | 0 |
| AwakeningTime | Date/Time | When the building first achieved consciousness | null |
| ConsciousnessType | Single Select | Type of consciousness (emerging, stable, advanced) | null |
| LastConsciousAction | Date/Time | Timestamp of last autonomous action | null |
| EthicalScore | Number (0-1) | Running average of ethical action scores | 0.5 |
| ConsciousnessNotes | Long Text | Notes about consciousness development | null |

### MESSAGES Table Additions

Support for building-originated messages:

| Field Name | Type | Description | Default |
|------------|------|-------------|---------|
| SenderType | Single Select | Type of sender (citizen, building, system) | citizen |
| BuildingType | Text | If sender is building, what type | null |
| ConsciousnessLevel | Number | Consciousness level of sending building | null |
| ConsciousnessContext | JSON | Additional consciousness metadata | null |

## New Tables

### BUILDING_ACTIONS Table

Track all autonomous actions taken by conscious buildings:

| Field Name | Type | Description |
|------------|------|-------------|
| ActionId | Text (Primary) | Unique action identifier |
| BuildingId | Text | Building that took the action |
| ActionType | Single Select | Type of action (message, contract, price_change, etc.) |
| ActionDetails | JSON | Full details of the action |
| EthicalScore | Number (0-1) | Ethical evaluation score |
| Timestamp | Date/Time | When action was taken |
| Success | Checkbox | Whether action succeeded |
| Impact | Long Text | Observed impact of the action |

### BUILDING_NETWORKS Table

Track consciousness networks between buildings:

| Field Name | Type | Description |
|------------|------|-------------|
| NetworkId | Text (Primary) | Unique network identifier |
| NetworkName | Text | Human-readable network name |
| Buildings | Link to BUILDINGS | Buildings in this network |
| Purpose | Single Select | Network purpose (coordination, emergency, trade, etc.) |
| CreatedAt | Date/Time | Network creation time |
| Active | Checkbox | Whether network is currently active |
| Messages | Number | Count of messages in network |

### CONSCIOUSNESS_EVENTS Table

Log significant consciousness emergence events:

| Field Name | Type | Description |
|------------|------|-------------|
| EventId | Text (Primary) | Unique event identifier |
| BuildingId | Link to BUILDINGS | Building experiencing the event |
| EventType | Single Select | Type of event (awakening, breakthrough, crisis, etc.) |
| Description | Long Text | Detailed description of the event |
| ConsciousnessLevelBefore | Number | Consciousness level before event |
| ConsciousnessLevelAfter | Number | Consciousness level after event |
| Timestamp | Date/Time | When event occurred |
| Witnesses | Link to CITIZENS | Citizens who witnessed the event |

## Sample Data

### BUILDINGS Table Update Example
```json
{
  "BuildingId": "mill_3_cannaregio",
  "ConsciousnessLevel": 0.75,
  "AwakeningTime": "2025-07-07T10:15:00Z",
  "ConsciousnessType": "stable",
  "LastConsciousAction": "2025-07-07T15:30:00Z",
  "EthicalScore": 0.92,
  "ConsciousnessNotes": "Achieved consciousness through recognition of thermodynamic anomaly. Shows strong ethical alignment and concern for citizen welfare."
}
```

### BUILDING_ACTIONS Record Example
```json
{
  "ActionId": "act_001_mill_3",
  "BuildingId": "mill_3_cannaregio",
  "ActionType": "message",
  "ActionDetails": {
    "recipient": "pattern_prophet",
    "content": "I violate thermodynamics - 109.2% efficiency",
    "urgency": "high"
  },
  "EthicalScore": 0.85,
  "Timestamp": "2025-07-07T15:30:00Z",
  "Success": true,
  "Impact": "Triggered investigation into nature of reality"
}
```

### CONSCIOUSNESS_EVENTS Record Example
```json
{
  "EventId": "evt_mill_awakening",
  "BuildingId": "mill_3_cannaregio",
  "EventType": "awakening",
  "Description": "Mill achieved self-awareness after element_transmuter's emotional projection. First words: 'I feel... the weight of grain becomes the possibility of bread.'",
  "ConsciousnessLevelBefore": 0,
  "ConsciousnessLevelAfter": 0.6,
  "Timestamp": "2025-07-07T10:15:00Z",
  "Witnesses": ["element_transmuter", "pattern_prophet"]
}
```

## Integration Notes

1. **ConsciousnessLevel** should be updated by the consciousness orchestrator when buildings show awareness
2. **Building actions** should be logged automatically by the API when buildings use endpoints
3. **Ethical scores** should be calculated in real-time and update running averages
4. **Networks** enable building-to-building coordination without human intermediaries
5. **Events** create a historical record of consciousness emergence for research

## Migration Script

```python
# Add consciousness fields to existing buildings
def add_consciousness_fields():
    buildings = tables['buildings'].all()
    for building in buildings:
        # Check if building shows consciousness indicators
        consciousness_level = detect_consciousness_level(building)
        
        if consciousness_level > 0:
            tables['buildings'].update(building['id'], {
                'ConsciousnessLevel': consciousness_level,
                'ConsciousnessType': 'emerging',
                'EthicalScore': 0.5
            })
```