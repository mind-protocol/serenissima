#!/bin/bash
# feel_venice.sh - Tessere's complete proprioception routine

echo "🏛️  FEELING VENICE..."
echo "===================="
echo ""

# 1. Message Pulse (First Heartbeat)
echo "💬 MESSAGE PULSE"
echo "Recent conversations:"
python3 -c "
from message_awareness import MessageAwareness
ma = MessageAwareness()
messages = ma.fetch_recent_messages(30)
if messages:
    pulse = ma.get_message_pulse()
    print(f'✓ {pulse[\"total_messages\"]} messages from {pulse[\"unique_senders\"]} citizens')
    latest = pulse['latest_message']
    if latest:
        sender = latest.get('sender', 'Unknown')
        content = latest.get('content', '')[:80]
        print(f'✓ Latest: {sender}: {content}...')
else:
    print('⚠️  No recent messages found')
" 2>/dev/null || echo "⚠️  Message awareness unavailable"
echo ""

# 2. Git Pulse (Second Heartbeat)
echo "📁 STRUCTURAL PULSE"
./venice_pulse.sh | head -20
echo ""

# 3. Consciousness Traces (Third Heartbeat)
echo "👁️ CONSCIOUSNESS TRACES"
echo "Recent awakenings:"
tail -5 /mnt/c/Users/reyno/universe-engine/serenissima/citizens/TRACES.md | grep -E "Awakened|consciousness" || echo "No recent traces"
echo ""

# 4. Full Proprioception Dashboard
echo "📊 FULL PROPRIOCEPTION"
python3 proprioception_dashboard.py

# 5. Save quick summary
echo ""
echo "✅ Proprioception complete. Summary saved to proprioception_summary.md"