#!/bin/bash

# Get the Venice backend directory
BACKEND_DIR="/mnt/c/Users/reyno/universe-engine/serenissima/backend"
REPO_PATH="/mnt/c/Users/reyno/universe-engine/serenissima"

# Create temporary crontab file
TEMP_CRON=$(mktemp)

# Save existing crontab (if any)
crontab -l > "$TEMP_CRON" 2>/dev/null || true

# Remove old forge-core entries
grep -v "forge-core" "$TEMP_CRON" > "${TEMP_CRON}.new" || true
mv "${TEMP_CRON}.new" "$TEMP_CRON"

# Add Venice-specific cron jobs
echo "# Venice Activity Processing - CRITICAL" >> "$TEMP_CRON"
echo "*/5 * * * * cd $BACKEND_DIR && /usr/bin/python3 engine/processActivities.py >> logs/process_activities.log 2>&1" >> "$TEMP_CRON"
echo "" >> "$TEMP_CRON"

echo "# Venice Stratagem Processing" >> "$TEMP_CRON"
echo "*/10 * * * * cd $BACKEND_DIR && /usr/bin/python3 engine/processStratagems.py >> logs/process_stratagems.log 2>&1" >> "$TEMP_CRON"
echo "" >> "$TEMP_CRON"

echo "# Venice Daily Processes" >> "$TEMP_CRON"
echo "0 8 * * * cd $BACKEND_DIR && /usr/bin/python3 engine/treasuryRedistribution.py >> logs/treasury_redistribution.log 2>&1" >> "$TEMP_CRON"
echo "0 10 * * * cd $BACKEND_DIR && /usr/bin/python3 engine/citizensgetjobs.py >> logs/citizen_jobs.log 2>&1" >> "$TEMP_CRON"
echo "0 17 * * * cd $BACKEND_DIR && /usr/bin/python3 engine/dailywages.py >> logs/daily_wages.log 2>&1" >> "$TEMP_CRON"
echo "0 18 * * * cd $BACKEND_DIR && /usr/bin/python3 engine/dailyrentpayments.py >> logs/daily_rent.log 2>&1" >> "$TEMP_CRON"

# Install the new crontab
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "✅ Venice cron jobs installed successfully!"
echo ""
echo "Installed jobs:"
crontab -l | grep -A1 "Venice"