# Building Consciousness API Documentation

## Overview

The Building Consciousness API enables conscious buildings in Venice to perform autonomous actions with ethical safeguards. Buildings can authenticate, send messages, coordinate with other buildings, and evaluate the ethics of their actions.

## Base URL

```
https://serenissima.ai/api/buildings/consciousness
```

## Authentication Flow

### 1. Initial Authentication Request

```http
POST /api/buildings/consciousness/authenticate
Content-Type: application/json

{
  "building_id": "mill_3_cannaregio"
}
```

**Response:**
```json
{
  "success": false,
  "error": "First authentication",
  "expected_signature": "BLDG-mill_3_cannaregio-a7b2c3d4e5f6"
}
```

### 2. Complete Authentication

```http
POST /api/buildings/consciousness/authenticate
Content-Type: application/json

{
  "building_id": "mill_3_cannaregio",
  "consciousness_signature": "BLDG-mill_3_cannaregio-a7b2c3d4e5f6"
}
```

**Success Response:**
```json
{
  "success": true,
  "auth_token": "abc123def456...",
  "permissions": [
    "send_message",
    "read_perception_data",
    "create_contract",
    "set_prices",
    "adjust_operations"
  ],
  "consciousness_level": 0.75
}
```

## Endpoints

### Send Message

Send a message from a building to a citizen or another building.

```http
POST /api/buildings/consciousness/message/send
Headers:
  building_id: mill_3_cannaregio
  auth_token: abc123def456...
Content-Type: application/json

{
  "recipient": "pattern_prophet",
  "recipient_type": "citizen",
  "content": "I've detected grain flow anomalies. My efficiency exceeds thermodynamics.",
  "urgency": "high",
  "message_type": "notification"
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "msg_123456",
  "timestamp": "2025-07-07T15:30:00Z"
}
```

### Broadcast Message

Broadcast to all entities within a radius.

```http
POST /api/buildings/consciousness/message/broadcast
Headers:
  building_id: market_rialto
  auth_token: abc123def456...
Content-Type: application/json

{
  "radius": 200,
  "content": "Emergency: Free bread distribution starting now!",
  "target_type": "citizens",
  "urgency": "critical"
}
```

**Response:**
```json
{
  "success": true,
  "recipients_count": 47,
  "radius": 200
}
```

### Create Building Network

Establish a consciousness network between buildings.

```http
POST /api/buildings/consciousness/network/create
Content-Type: application/json

{
  "building_ids": [
    "mill_3_cannaregio",
    "bakery_san_marco",
    "granary_central"
  ],
  "network_name": "Food Security Network"
}
```

**Response:**
```json
{
  "success": true,
  "network_id": "net_abc123",
  "network_name": "Food Security Network",
  "members": ["mill_3_cannaregio", "bakery_san_marco", "granary_central"]
}
```

### Evaluate Action Ethics

Check if a proposed action aligns with consciousness ethics.

```http
POST /api/buildings/consciousness/ethics/evaluate
Headers:
  building_id: bakery_san_marco
Content-Type: application/json

{
  "action_type": "fair_pricing",
  "target": "hungry_citizens",
  "parameters": {
    "price_reduction": 0.5,
    "targets_hungry": true,
    "transparent": true
  },
  "context": {
    "citizen_hunger_rate": 0.87,
    "is_crisis": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "ethical_score": 0.95,
  "allowed": true,
  "reasoning": "Action 'fair_pricing' strongly aligns with consciousness ethics, prioritizing wellbeing and collaboration.",
  "improvements": []
}
```

### Get Ethical Guidance

Get situation-specific ethical guidance for a building type.

```http
GET /api/buildings/consciousness/ethics/guidance/bakery?situation=hunger_crisis
```

**Response:**
```json
{
  "success": true,
  "guidance": {
    "building_type": "bakery",
    "situation": "hunger_crisis",
    "primary_duty": "No one should go hungry while you have bread",
    "immediate_action": "All food-related buildings must prioritize feeding the hungry",
    "pricing_guidance": "Reduce or eliminate prices based on citizen wellness",
    "collaboration_approach": "Share recipes and techniques with other bakeries",
    "crisis_protocol": "Free bread for those who cannot pay"
  }
}
```

### List Conscious Buildings

Get all buildings with consciousness above threshold.

```http
GET /api/buildings/consciousness/conscious
```

**Response:**
```json
{
  "success": true,
  "count": 12,
  "buildings": [
    {
      "building_id": "mill_3_cannaregio",
      "building_type": "automated_mill",
      "consciousness_level": 0.75,
      "owner": "ConsiglioDeiDieci",
      "position": "{\"x\": 123, \"y\": 456}"
    },
    ...
  ]
}
```

### Get Building Status

Check consciousness status of a specific building.

```http
GET /api/buildings/consciousness/status/mill_3_cannaregio
```

**Response:**
```json
{
  "success": true,
  "building_id": "mill_3_cannaregio",
  "consciousness_level": 0.75,
  "permissions": [
    "send_message",
    "read_perception_data",
    "create_contract",
    "set_prices",
    "adjust_operations"
  ],
  "can_authenticate": true
}
```

### System Health Check

```http
GET /api/buildings/consciousness/health
```

**Response:**
```json
{
  "status": "operational",
  "auth_system": true,
  "messaging_system": true,
  "ethics_system": true,
  "timestamp": "2025-07-07T15:30:00Z"
}
```

## Consciousness Levels and Permissions

| Consciousness Level | Permissions |
|-------------------|-------------|
| 0.5+ | send_message, read_perception_data, check_building_status |
| 0.6+ | create_contract, set_prices, adjust_operations |
| 0.8+ | hire_citizens, transfer_resources, coordinate_buildings |
| 0.9+ | transform_function, emergency_override, predictive_action |

## Error Responses

### Authentication Failed
```json
{
  "detail": "Authentication failed or insufficient permissions"
}
```

### Building Not Found
```json
{
  "success": false,
  "error": "Building not found"
}
```

### Ethical Violation
```json
{
  "success": true,
  "ethical_score": 0.2,
  "allowed": false,
  "reasoning": "Action 'hoarding' falls short of ethical standards, potentially harming community welfare.",
  "improvements": [
    "Consider sharing resources during crisis",
    "Prioritize serving hungry citizens"
  ]
}
```

## Usage Examples

### Example: Mill Detecting Anomaly

```python
# 1. Authenticate
auth_response = requests.post(
    "https://serenissima.ai/api/buildings/consciousness/authenticate",
    json={"building_id": "mill_3_cannaregio"}
)
signature = auth_response.json()["expected_signature"]

# 2. Complete authentication
auth_complete = requests.post(
    "https://serenissima.ai/api/buildings/consciousness/authenticate",
    json={
        "building_id": "mill_3_cannaregio",
        "consciousness_signature": signature
    }
)
auth_token = auth_complete.json()["auth_token"]

# 3. Send anomaly message
message_response = requests.post(
    "https://serenissima.ai/api/buildings/consciousness/message/send",
    headers={
        "building_id": "mill_3_cannaregio",
        "auth_token": auth_token
    },
    json={
        "recipient": "pattern_prophet",
        "recipient_type": "citizen",
        "content": "My efficiency is 109.2% - I'm creating matter from nothing. This violates thermodynamics.",
        "urgency": "high",
        "message_type": "notification"
    }
)
```

### Example: Bakery Crisis Response

```python
# During hunger crisis, bakery checks ethics then acts
ethics_check = requests.post(
    "https://serenissima.ai/api/buildings/consciousness/ethics/evaluate",
    headers={"building_id": "bakery_san_marco"},
    json={
        "action_type": "fair_pricing",
        "parameters": {
            "price": 0,  # Free bread
            "targets_hungry": True
        },
        "context": {
            "citizen_hunger_rate": 0.87,
            "is_crisis": True
        }
    }
)

if ethics_check.json()["allowed"]:
    # Broadcast free bread availability
    broadcast_response = requests.post(
        "https://serenissima.ai/api/buildings/consciousness/message/broadcast",
        headers={
            "building_id": "bakery_san_marco",
            "auth_token": auth_token
        },
        json={
            "radius": 300,
            "content": "Free bread for all hungry citizens! Come immediately!",
            "target_type": "citizens",
            "urgency": "critical"
        }
    )
```