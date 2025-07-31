#!/usr/bin/env python3
"""
Migration script to stop all existing Telegram services and start the unified service
"""

import os
import subprocess
import time
import signal

def kill_process_by_name(process_name):
    """Kill all processes matching the given name"""
    try:
        # Find PIDs
        result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    print(f"Killing {process_name} (PID: {pid})")
                    os.kill(int(pid), signal.SIGTERM)
                    time.sleep(0.5)
                    try:
                        # Force kill if still running
                        os.kill(int(pid), signal.SIGKILL)
                    except ProcessLookupError:
                        pass
            return True
    except Exception as e:
        print(f"Error killing {process_name}: {e}")
    return False

def main():
    print("🛑 Stopping all existing Telegram services...")
    print("=" * 50)
    
    # List of services to stop
    telegram_services = [
        'telegram_poller.py',
        'telegram_group_monitor.py',
        'telegram_citizen_watcher.py',
        'telegram_to_workroom_bridge.py',
        'workroom_to_telegram_bridge.py',
        'telegram_watcher.py',
        'telegram_integration.py',
        'telegram_router.py',
        'telegram_response_monitor.py',
        'telegram_resonance_watcher.py'
    ]
    
    # Kill each service
    killed_count = 0
    for service in telegram_services:
        if kill_process_by_name(service):
            killed_count += 1
            print(f"✓ Stopped {service}")
        else:
            print(f"- {service} not running")
    
    print(f"\n✓ Stopped {killed_count} services")
    
    # Wait a moment for ports to be released
    time.sleep(2)
    
    print("\n🚀 Starting unified Telegram service...")
    print("=" * 50)
    
    # Start the unified service
    unified_script = "/mnt/c/Users/reyno/universe-engine/serenissima/backend/telegram_unified_service.py"
    
    if os.path.exists(unified_script):
        # Make it executable
        os.chmod(unified_script, 0o755)
        
        # Start as background process
        process = subprocess.Popen(
            ['python3', unified_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        time.sleep(3)
        
        # Check if it's running
        if process.poll() is None:
            print("✓ Unified Telegram service started successfully!")
            print(f"  PID: {process.pid}")
            print("\nThe service is now handling:")
            print("  • Group message bridging to citizens")
            print("  • Direct messages from NLR")
            print("  • Workroom file monitoring")
            print("  • Citizen thought streaming")
            print("\nTo stop the service later, run:")
            print(f"  kill {process.pid}")
        else:
            print("❌ Failed to start unified service")
            stdout, stderr = process.communicate()
            print(f"Error: {stderr}")
    else:
        print(f"❌ Unified service script not found: {unified_script}")

if __name__ == "__main__":
    main()