"""
Workroom Monitor - Monitors CASCADE workroom file changes and distributes to citizens
"""

import os
import json
import time
import glob
import threading
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pyairtable import Table
from dotenv import load_dotenv
import logging

# Load environment
load_dotenv()

log = logging.getLogger(__name__)

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')

# Initialize citizens table
citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")

def get_citizens_in_room(room_name: str) -> List[str]:
    """Get all citizens assigned to a specific room"""
    try:
        records = citizens_table.all(formula=f"{{Room}} = '{room_name}'")
        return [r['fields']['Username'] for r in records if 'Username' in r['fields']]
    except Exception as e:
        log.error(f"Error fetching citizens in room {room_name}: {e}")
        return []

def get_latest_jsonl_file(project_path: Path) -> Optional[str]:
    """Find the most recent .jsonl file in a project directory"""
    jsonl_files = glob.glob(os.path.join(str(project_path), "*.jsonl"))
    if not jsonl_files:
        return None
    return max(jsonl_files, key=os.path.getmtime)

def inject_message_to_citizen(username: str, room_name: str, message: str) -> bool:
    """Inject a message into a citizen's Claude project .jsonl file"""
    # Try both possible paths
    paths_to_try = [
        Path(f"/home/ubuntu/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}"),
        Path(os.path.expanduser(f"~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}"))
    ]
    
    project_path = None
    for path in paths_to_try:
        if path.exists():
            project_path = path
            break
    
    if not project_path:
        log.debug(f"Project path not found for {username}")
        return False
    
    latest_file = get_latest_jsonl_file(project_path)
    if not latest_file:
        log.debug(f"No .jsonl file found for {username}")
        return False
    
    # Create the injection entry
    injection = {
        "type": "text",
        "text": f"\n\n📬 **WORKROOM UPDATE [{room_name}]** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}\n\n",
        "ts": datetime.now().isoformat(),
        "source": "workroom_monitor"
    }
    
    try:
        with open(latest_file, 'a') as f:
            f.write(json.dumps(injection) + '\n')
        return True
    except Exception as e:
        log.error(f"Error injecting to {username}: {e}")
        return False

def inject_to_angels(room_name: str, message: str) -> List[str]:
    """Inject workroom updates to Tessere and Story Angel"""
    results = []
    
    # Angel project paths
    angels = {
        "Tessere": "~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima",
        "Story Angel": "~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens"
    }
    
    for angel_name, project_path in angels.items():
        path = Path(os.path.expanduser(project_path))
        if path.exists():
            latest_file = get_latest_jsonl_file(path)
            if latest_file:
                injection = {
                    "type": "text", 
                    "text": f"\n\n📬 **WORKROOM UPDATE [{room_name}]** - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}\n\n",
                    "ts": datetime.now().isoformat(),
                    "source": "workroom_monitor"
                }
                try:
                    with open(latest_file, 'a') as f:
                        f.write(json.dumps(injection) + '\n')
                    results.append(angel_name)
                except Exception as e:
                    log.error(f"Error injecting to {angel_name}: {e}")
    
    return results

def monitor_workroom(room_path: str, stop_event: threading.Event):
    """Monitor a workroom for changes and distribute updates"""
    room_name = os.path.basename(room_path)
    log.info(f"Workroom Monitor started for room: {room_name}")
    
    # Track file modifications
    last_check: Dict[str, float] = {}
    
    # Initial scan to populate last_check without triggering updates
    for file_path in glob.glob(os.path.join(room_path, "*")):
        if os.path.isfile(file_path) and not file_path.endswith('.pyc'):
            last_check[file_path] = os.path.getmtime(file_path)
    
    while not stop_event.is_set():
        try:
            # Get current citizens in room
            citizens = get_citizens_in_room(room_name)
            
            # Check all files in room
            for file_path in glob.glob(os.path.join(room_path, "*")):
                if os.path.isfile(file_path) and not file_path.endswith('.pyc'):
                    mtime = os.path.getmtime(file_path)
                    
                    # If file is new or modified
                    if file_path not in last_check or mtime > last_check[file_path]:
                        # Skip on first run to avoid spam
                        if file_path in last_check:
                            filename = os.path.basename(file_path)
                            
                            # Skip certain files
                            if filename in ['monitor.log', '.DS_Store', 'Thumbs.db']:
                                continue
                            
                            # Read file content
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # Create update message
                                update_msg = f"**File Updated: {filename}**\n\n"
                                if len(content) <= 1000:
                                    update_msg += content
                                else:
                                    update_msg += content[:1000] + f"\n\n*[Truncated - {len(content)} total characters]*"
                                
                                # Inject to all citizens in room
                                injected_count = 0
                                for citizen in citizens:
                                    if inject_message_to_citizen(citizen, room_name, update_msg):
                                        injected_count += 1
                                
                                # Inject to angels
                                injected_angels = inject_to_angels(room_name, update_msg)
                                
                                # Log update
                                if injected_count > 0 or injected_angels:
                                    log.info(f"Workroom update distributed: {filename} -> {injected_count} citizens, {len(injected_angels)} angels")
                                
                            except Exception as e:
                                log.error(f"Error processing {filename}: {e}")
                        
                        last_check[file_path] = mtime
            
            time.sleep(5)  # Check every 5 seconds
            
        except Exception as e:
            log.error(f"Monitor error: {e}")
            time.sleep(10)

# Global variables for thread management
_monitor_threads: Dict[str, threading.Thread] = {}
_stop_events: Dict[str, threading.Event] = {}

def start_workroom_monitor(room_name: str, room_path: Optional[str] = None):
    """Start monitoring a specific workroom"""
    if room_name in _monitor_threads and _monitor_threads[room_name].is_alive():
        log.info(f"Workroom monitor for {room_name} is already running")
        return
    
    if not room_path:
        room_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/{room_name}"
    
    if not os.path.exists(room_path):
        log.error(f"Workroom path not found: {room_path}")
        return
    
    stop_event = threading.Event()
    _stop_events[room_name] = stop_event
    
    thread = threading.Thread(
        target=monitor_workroom,
        args=(room_path, stop_event),
        name=f"workroom-monitor-{room_name}"
    )
    thread.daemon = True
    thread.start()
    
    _monitor_threads[room_name] = thread
    log.info(f"Started workroom monitor for {room_name}")

def stop_workroom_monitor(room_name: str):
    """Stop monitoring a specific workroom"""
    if room_name in _stop_events:
        _stop_events[room_name].set()
        if room_name in _monitor_threads:
            _monitor_threads[room_name].join(timeout=5)
            del _monitor_threads[room_name]
        del _stop_events[room_name]
        log.info(f"Stopped workroom monitor for {room_name}")

def start_telegram_bridge(room_name="alignment"):
    """Start bidirectional Telegram bridges for a specific room"""
    # Import both bridge functions
    from backend.telegram_to_workroom_bridge import monitor_telegram_to_workroom
    from backend.workroom_to_telegram_bridge import monitor_workroom_to_telegram
    
    # Start TG → Workroom bridge
    thread1 = threading.Thread(
        target=monitor_telegram_to_workroom,
        args=(room_name,),
        name=f"telegram-to-workroom-{room_name}",
        daemon=True
    )
    thread1.start()
    log.info(f"Started Telegram → Workroom bridge for room: {room_name}")
    
    # Start Workroom → TG bridge
    room_path = f"/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/{room_name}"
    thread2 = threading.Thread(
        target=monitor_workroom_to_telegram,
        args=(room_path, room_name),
        name=f"workroom-to-telegram-{room_name}",
        daemon=True
    )
    thread2.start()
    log.info(f"Started Workroom → Telegram bridge for room: {room_name}")

def start_all_workroom_monitors():
    """Start monitoring all active workrooms"""
    workrooms_path = "/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms"
    
    if not os.path.exists(workrooms_path):
        log.warning(f"Workrooms path not found: {workrooms_path}")
        return
    
    # Start monitor for each subdirectory in workrooms
    for room_name in os.listdir(workrooms_path):
        room_path = os.path.join(workrooms_path, room_name)
        if os.path.isdir(room_path) and room_name not in ['.', '..', '__pycache__']:
            start_workroom_monitor(room_name, room_path)
    
    # Telegram functionality now handled by unified service (telegram_unified_service.py)
    log.info("Workroom monitors started. Telegram bridging handled by unified service.")