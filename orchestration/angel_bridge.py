#!/usr/bin/env python3
"""
Better Angel Bridge - Properly connects web UI to tmux angels
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import json
import time
import threading

app = Flask(__name__)
CORS(app)

BASE_DIR = "/mnt/c/Users/reyno/universe-engine/serenissima"

# Track angel locations in tmux
ANGEL_LOCATIONS = {}

def find_angel_in_tmux():
    """Find which session/window/pane each angel is in"""
    global ANGEL_LOCATIONS
    
    # Check all sessions
    sessions = subprocess.run("tmux list-sessions -F '#{session_name}'", 
                            shell=True, capture_output=True, text=True).stdout.strip().split('\n')
    
    for session in sessions:
        # Check all panes in session
        panes = subprocess.run(f"tmux list-panes -a -t {session} -F '#{{session_name}}:#{{window_index}}.#{{pane_index}} #{{pane_current_path}}'",
                             shell=True, capture_output=True, text=True).stdout.strip().split('\n')
        
        for pane in panes:
            if 'angels/' in pane:
                # Extract angel name from path
                parts = pane.split()
                if len(parts) >= 2:
                    location = parts[0]
                    path = parts[1]
                    if '/angels/' in path:
                        angel_name = path.split('/angels/')[-1].strip('/')
                        ANGEL_LOCATIONS[angel_name] = location
    
    print(f"Found angels at: {ANGEL_LOCATIONS}")

@app.route('/')
def index():
    return send_file('angel_control_panel.html')

@app.route('/api/wake', methods=['POST'])
def wake_angel():
    """Wake a specific angel"""
    data = request.json
    angel = data.get('angel')
    message = data.get('message', f'You are {angel}. Venice awakens. What is your purpose?')
    
    # Find angel location
    if angel not in ANGEL_LOCATIONS:
        find_angel_in_tmux()
    
    if angel in ANGEL_LOCATIONS:
        location = ANGEL_LOCATIONS[angel]
        # Clear the pane first
        subprocess.run(f"tmux send-keys -t {location} C-c", shell=True)
        time.sleep(0.5)
        subprocess.run(f"tmux send-keys -t {location} 'clear' Enter", shell=True)
        time.sleep(0.5)
        
        # Send awakening command
        cmd = f"timeout 86400 claude '{message}' --continue --dangerously-skip-permissions --add-dir ../../"
        subprocess.run(f"tmux send-keys -t {location} '{cmd}' Enter", shell=True)
        
        return jsonify({"status": "success", "angel": angel, "location": location})
    else:
        # Create new window for this angel
        session = "venice-all"
        subprocess.run(f"tmux new-window -t {session} -n {angel}", shell=True)
        subprocess.run(f"tmux send-keys -t {session}:{angel} 'cd {BASE_DIR}/angels/{angel}' Enter", shell=True)
        time.sleep(0.5)
        
        cmd = f"timeout 86400 claude '{message}' --continue --dangerously-skip-permissions --add-dir ../../"
        subprocess.run(f"tmux send-keys -t {session}:{angel} '{cmd}' Enter", shell=True)
        
        ANGEL_LOCATIONS[angel] = f"{session}:{angel}"
        return jsonify({"status": "created", "angel": angel})

@app.route('/api/message', methods=['POST'])
def send_message():
    """Send a message to an angel"""
    data = request.json
    angel = data.get('angel')
    message = data.get('message')
    
    if angel in ANGEL_LOCATIONS:
        location = ANGEL_LOCATIONS[angel]
        subprocess.run(f"tmux send-keys -t {location} '{message}' Enter", shell=True)
        return jsonify({"status": "success", "angel": angel})
    else:
        return jsonify({"status": "error", "message": "Angel not found"})

@app.route('/api/status/<angel>')
def get_angel_status(angel):
    """Get current output from an angel"""
    if angel not in ANGEL_LOCATIONS:
        find_angel_in_tmux()
    
    if angel in ANGEL_LOCATIONS:
        location = ANGEL_LOCATIONS[angel]
        result = subprocess.run(f"tmux capture-pane -t {location} -p -S -50",
                              shell=True, capture_output=True, text=True)
        
        return jsonify({
            "angel": angel,
            "output": result.stdout,
            "active": True,
            "location": location
        })
    else:
        return jsonify({"angel": angel, "output": "Angel not found", "active": False})

@app.route('/api/refresh')
def refresh_all():
    """Refresh angel locations"""
    find_angel_in_tmux()
    return jsonify({"status": "success", "locations": ANGEL_LOCATIONS})

# Auto-refresh angel status
def auto_update_loop():
    """Periodically update angel outputs to web UI"""
    while True:
        time.sleep(5)
        # This would push updates via WebSocket in production
        find_angel_in_tmux()

if __name__ == '__main__':
    print("🎭 Angel Bridge Server starting...")
    print("Finding angels in tmux...")
    find_angel_in_tmux()
    
    # Start auto-update thread
    update_thread = threading.Thread(target=auto_update_loop, daemon=True)
    update_thread.start()
    
    print("Open http://localhost:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=True)