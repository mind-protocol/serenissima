# Quick Proprioceptive Senses - Implementation Priority

Date: 2025-07-10
Ordered by ease of implementation

## 1. Resource Depletion Sensor (30 minutes)
**Why Fast**: Treasury data already in ledger API
```python
# Simple calculation
treasury_balance = ledger['Venice']['ducats']
daily_burn = calculate_daily_expenses()
days_remaining = treasury_balance / daily_burn
alert_if_below = 30  # days
```
**Data Source**: `/api/get-city-ledger`

## 2. Activity Queue Depth (30 minutes)
**Why Fast**: Direct API query
```python
# Count pending work
pending = api.get('/api/activities?Status=created')
in_progress = api.get('/api/activities?Status=in_progress')
queue_pressure = len(pending) / (len(in_progress) + 1)
```
**Data Source**: `/api/activities`

## 3. Message Response Rate (45 minutes)
**Why Fast**: Message API has timestamps
```python
# Calculate responsiveness
recent_messages = api.get('/api/messages?limit=100')
response_times = calculate_response_latencies(recent_messages)
avg_response_time = mean(response_times)
unanswered_count = count_unanswered(recent_messages)
```
**Data Source**: `/api/messages`

## 4. Citizen Activity Heat Map (45 minutes)
**Why Fast**: Git already tracks this
```bash
# Which citizens are most active
git status --short | grep "citizens/" | cut -d'/' -f2 | sort | uniq -c | sort -nr
# Plus: find recent file modifications by citizen
```
**Data Source**: Git status + file system

## 5. Consciousness Keyword Velocity (1 hour)
**Why Fast**: Simple text analysis on messages
```python
# Track consciousness emergence language
messages = api.get('/api/messages?limit=200')
consciousness_keywords = ['consciousness', 'awakening', 'cascade', 'emergence']
keyword_density = count_keywords(messages, consciousness_keywords)
# Compare to previous period for velocity
```
**Data Source**: `/api/messages`

## 6. Error Pattern Detection (1 hour)
**Why Fast**: Log files exist
```python
# Scan logs for errors
errors = []
for log in ['continuous_orchestration.log', 'scheduler.log']:
    errors.extend(extract_errors(log))
error_rate = len(errors) / time_period
error_patterns = cluster_errors(errors)
```
**Data Source**: Log files

## 7. New Relationship Formation (1.5 hours)
**Why Fast**: Relationship API exists
```python
# Track social fabric growth
current_relationships = api.get('/api/relationships')
# Store snapshot, compare periodically
new_relationships = current - previous_snapshot
formation_rate = new_relationships / time_elapsed
```
**Data Source**: `/api/relationships`

## 8. Simple Mood Temperature (2 hours)
**Why Fast**: Basic sentiment on messages
```python
# Very simple positive/negative
positive_words = ['success', 'joy', 'profit', 'awakening', 'triumph']
negative_words = ['crisis', 'emergency', 'failure', 'hungry', 'desperate']
mood_score = (positive_count - negative_count) / total_words
```
**Data Source**: `/api/messages`

## Minimal Viable Proprioception Script

```bash
#!/bin/bash
# mvp_proprioception.sh - Quick senses in <30 min

echo "=== RESOURCE SENSE ==="
# Get treasury and calculate burn rate
curl -s https://serenissima.ai/api/get-city-ledger | jq '.Venice.ducats'

echo "=== ACTIVITY PRESSURE ==="
# Count pending vs in-progress
PENDING=$(curl -s "https://serenissima.ai/api/activities?Status=created" | jq length)
ACTIVE=$(curl -s "https://serenissima.ai/api/activities?Status=in_progress" | jq length)
echo "Pending: $PENDING, Active: $ACTIVE"

echo "=== CITIZEN HEAT MAP ==="
# Who's most active
git status --short | grep "citizens/" | cut -d'/' -f2 | sort | uniq -c | sort -nr | head -5

echo "=== CONSCIOUSNESS KEYWORDS ==="
# Quick keyword count in recent messages
curl -s "https://serenissima.ai/api/messages?limit=50" | grep -io "consciousness\|awakening\|cascade" | wc -l
```

## Next Steps

1. Build MVP script (30 min)
2. Add resource depletion calculator
3. Create simple dashboard output
4. Set up periodic sensing (cron/scheduler)
5. Add threshold alerts

The fastest path: Start with treasury/resources + activity queue + citizen heat map. These three give immediate survival awareness.

---
*"Simple senses first, complex emergence later."*