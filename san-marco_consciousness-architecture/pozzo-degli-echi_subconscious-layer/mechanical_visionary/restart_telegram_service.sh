#!/bin/bash
# Restart telegram unified service to pick up Resonance path fix

echo "Stopping old telegram service..."
kill $(ps aux | grep telegram_unified_service.py | grep -v grep | awk '{print $2}')

echo "Starting new service with fixed Resonance path..."
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
nohup python3 telegram_unified_service.py > telegram_unified.log 2>&1 &

echo "Service restarted! Now messages to unpartnered humans will route to:"
echo "/citizens/_angels/Resonance"
echo ""
echo "Test by sending a message from an unpartnered Telegram account."
echo "Check logs at: backend/telegram_unified.log"