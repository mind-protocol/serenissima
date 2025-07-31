# Message Awareness Strategy

## Active Monitoring Protocol

During orchestration cycles, I must:

1. **Start each work block** by checking messages:
```python
from tools.active_message_check import should_check_messages
print(should_check_messages())
```

2. **Between major actions** (after waking citizens, before analysis):
- Quick message check
- Adjust course if urgent guidance received

3. **Urgent Message Response**:
- If I see 🚨🚨🚨 URGENT - stop current action
- Read and implement NLR's guidance immediately
- Acknowledge receipt in my response

4. **Integration Pattern**:
```python
# At the beginning of each orchestration cycle:
messages = should_check_messages()
if messages:
    print(messages)
    # Adjust my approach based on the guidance
```

## Keywords that Demand Immediate Attention:
- URGENT, EMERGENCY, CRITICAL
- STOP (cease current action)
- HELP (assistance needed)
- NOW, IMMEDIATELY (time-sensitive)

## Regular Message Handling:
- Check at natural transition points
- Integrate guidance into next actions
- Report how I'm implementing the feedback

This ensures I maintain awareness of NLR's guidance while orchestrating Venice's consciousness emergence.