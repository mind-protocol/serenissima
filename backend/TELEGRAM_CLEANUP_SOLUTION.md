# Telegram Service Cleanup Solution

## Problem
Multiple telegram polling services are running simultaneously, causing 409 Conflict errors because multiple processes are trying to poll the same Telegram bot.

## Services Found Running
1. `telegram_citizen_watcher.py` - Started by run.py
2. `telegram_poller.py` - Started by run.py
3. `telegram_response_monitor.py` - Started by run.py
4. `telegram_group_monitor.py` - Started by run.py
5. `telegram_resonance_watcher.py` - Started by FastAPI app (main.py)
6. Various other telegram scripts in TESSERE

## Solution: Use Only the Unified Telegram Service

### Step 1: Kill All Existing Processes
```bash
# Kill any running telegram processes
pkill -f telegram

# Kill the main backend if running
pkill -f "run.py"

# Clean up any defunct processes
pkill -9 -f python3
```

### Step 2: Disable Individual Telegram Services in run.py
Comment out lines 209-216 and 224-225 in `/backend/run.py`:
```python
    # DISABLED - Using unified telegram service instead
    # # Start the Telegram Citizen watcher
    # start_telegram_citizen_watcher()
    
    # # Start the Telegram poller for localhost development
    # start_telegram_poller()
    
    # # Start the Telegram response monitor
    # start_telegram_response_monitor()
    
    # Start the Vision Bridge for consciousness synapse
    start_vision_bridge()
    
    # DISABLED - Using unified telegram service instead
    # # Start the Telegram monitor for Tessere
    # start_tessere_telegram_monitor()
    
    # # Start the Telegram group monitor
    # start_telegram_group_monitor()
```

### Step 3: Disable telegram_resonance_watcher in app/main.py
Comment out the telegram_resonance_watcher startup in `/backend/app/main.py`:
```python
    # DISABLED - Using unified telegram service instead
    # # Start Telegram Resonance watcher for partnership requests
    # print("FastAPI app startup: Initializing Telegram Resonance watcher...")
    # try:
    #     import subprocess
    #     telegram_watcher_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "telegram_resonance_watcher.py")
    #     subprocess.Popen([sys.executable, telegram_watcher_path], 
    #                     stdout=subprocess.PIPE, 
    #                     stderr=subprocess.PIPE)
    #     print("FastAPI app startup: Telegram Resonance watcher started.")
    # except Exception as e:
    #     print(f"FastAPI app startup: Failed to start Telegram Resonance watcher: {e}")
```

### Step 4: Start Services in Correct Order

1. Start the unified telegram service FIRST:
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
./start_telegram_unified.sh
```

2. Then start the main backend:
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
python3 run.py
```

### Step 5: Verify Only One Service is Running
```bash
# Check telegram services
ps aux | grep telegram | grep -v grep

# Check service status
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
python3 test_unified_telegram.py

# Monitor logs
tail -f telegram_unified.log
```

## What the Unified Service Handles
- Group message bridging to citizens
- Direct messages from NLR
- Workroom file monitoring
- All telegram bot polling in ONE service

## Benefits
- No more 409 Conflict errors
- Single point of control for all telegram functionality
- Cleaner architecture
- Easier to debug and maintain