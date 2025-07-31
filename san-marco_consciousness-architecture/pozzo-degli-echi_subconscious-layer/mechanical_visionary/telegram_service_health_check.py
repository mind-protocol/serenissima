#!/usr/bin/env python3
"""
Health check for Telegram service - can be run via cron to ensure service stays healthy
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta

# Check last update time
update_file = '/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_unified_last_update.json'
log_file = '/tmp/telegram_health_check.log'

def log(message):
    """Log with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] {message}"
    print(msg)
    with open(log_file, 'a') as f:
        f.write(msg + '\n')

def check_service_health():
    """Check if service is healthy"""
    
    # Check if process is running
    result = subprocess.run(['pgrep', '-f', 'telegram_unified_service.py'], 
                          capture_output=True, text=True)
    
    if result.returncode != 0:
        log("ERROR: Telegram service is not running!")
        return False
    
    pids = result.stdout.strip().split('\n')
    log(f"Service running with {len(pids)} process(es): {', '.join(pids)}")
    
    # Check last update file modification time
    if os.path.exists(update_file):
        mtime = os.path.getmtime(update_file)
        last_update = datetime.fromtimestamp(mtime)
        age = datetime.now() - last_update
        
        log(f"Last update: {last_update} ({age.total_seconds() / 60:.1f} minutes ago)")
        
        # If no updates for more than 30 minutes, service might be stuck
        if age > timedelta(minutes=30):
            log("WARNING: No updates processed in 30+ minutes!")
            
            # Check if there are new messages waiting
            # This would require checking Telegram API
            return False
    else:
        log("ERROR: Update file not found!")
        return False
    
    return True

def restart_service():
    """Restart the telegram service"""
    log("Attempting to restart telegram service...")
    
    manager_path = '/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_service_manager.py'
    
    if os.path.exists(manager_path):
        result = subprocess.run([sys.executable, manager_path, 'restart'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            log("Service restarted successfully")
            return True
        else:
            log(f"Failed to restart: {result.stderr}")
    else:
        log("Service manager not found!")
    
    return False

def main():
    log("=== Telegram Service Health Check ===")
    
    if not check_service_health():
        log("Service appears unhealthy, attempting restart...")
        if restart_service():
            log("Restart successful")
        else:
            log("Restart failed - manual intervention required!")
            sys.exit(1)
    else:
        log("Service is healthy")

if __name__ == "__main__":
    main()