#!/bin/bash

# Daemon to continuously sync Keeper messages every 30 seconds
# Run this in the background: nohup ./keeper_sync_daemon.sh > keeper_sync.log 2>&1 &

SYNC_SCRIPT="/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE/sync_keeper_messages.sh"
INTERVAL=30

echo "[$(date)] Starting Keeper message sync daemon"
echo "Checking for new messages every ${INTERVAL} seconds..."

# Ensure sync script exists and is executable
if [ ! -x "$SYNC_SCRIPT" ]; then
    echo "[$(date)] ERROR: Sync script not found or not executable: $SYNC_SCRIPT"
    exit 1
fi

# Main loop
while true; do
    # Run the sync script
    "$SYNC_SCRIPT"
    
    # Wait for the interval
    sleep $INTERVAL
done