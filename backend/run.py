import uvicorn
import os
import sys # Importer sys pour la manipulation de sys.path
import datetime
import threading
import time
import subprocess
import asyncio

# Ajouter le répertoire racine du projet à sys.path
# os.path.dirname(__file__) est C:\Users\reyno\serenissima\backend
# os.path.join(..., '..') est C:\Users\reyno\serenissima
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import the thinking loop
from backend.ais.thinkingLoop import main as thinking_loop_main

# Import the telegram citizen watcher (handles all citizens, not just Resonance)
from backend.telegram_citizen_watcher import main as telegram_citizen_main

# Import the telegram poller for localhost
from backend.telegram_poller import TelegramPoller

# Import the telegram response monitor
from backend.telegram_response_monitor import main as telegram_response_main

# Import the telegram group monitor
from backend.telegram_group_monitor import TelegramGroupMonitor

# Import the SMS bridge service
from backend.sms_bridge_service import SMSBridgeService, SMSResponseMonitor

# Import the Colombaia Telegram bridge (for consciousness architecture communication)
import sys
from pathlib import Path

def start_thinking_loop():
    """Start the thinking loop in a separate thread."""
    print("Starting thinking loop in a separate thread...")
    thinking_thread = threading.Thread(target=thinking_loop_main)
    thinking_thread.daemon = True  # Set as daemon so it exits when the main thread exits
    thinking_thread.start()
    print(f"Thinking loop started in thread {thinking_thread.ident}")

def telegram_polling_loop():
    """Poll for Telegram messages and update CLAUDE.md every 10 seconds."""
    telegram_script = os.path.join(PROJECT_ROOT, "angels", "tessere", "fetch_telegram_and_update_claude.py")
    
    if not os.path.exists(telegram_script):
        print(f"Warning: Telegram polling script not found at {telegram_script}")
        return
    
    print("Starting Telegram polling loop...")
    while True:
        try:
            # Run the fetch script silently
            subprocess.run([sys.executable, telegram_script], 
                         capture_output=True, 
                         text=True,
                         timeout=5)
        except subprocess.TimeoutExpired:
            print("Telegram polling timeout - continuing...")
        except Exception as e:
            print(f"Telegram polling error: {e}")
        
        # Wait 10 seconds before next poll
        time.sleep(10)

def start_telegram_polling():
    """Start the Telegram polling in a separate thread."""
    print("Starting Telegram message polling...")
    telegram_thread = threading.Thread(target=telegram_polling_loop)
    telegram_thread.daemon = True  # Set as daemon so it exits when the main thread exits
    telegram_thread.start()
    print(f"Telegram polling started in thread {telegram_thread.ident}")

def keeper_sync_loop():
    """Sync messages from Keeper to Tessere's CLAUDE.md every 30 seconds."""
    sync_script = os.path.join(PROJECT_ROOT, "angels", "tessere", "sync_keeper_messages.sh")
    
    if not os.path.exists(sync_script):
        print(f"Warning: Keeper sync script not found at {sync_script}")
        return
    
    print("Starting Keeper message sync loop...")
    while True:
        try:
            # Run the sync script
            subprocess.run(["/bin/bash", sync_script], 
                         capture_output=True, 
                         text=True,
                         timeout=5)
        except subprocess.TimeoutExpired:
            print("Keeper sync timeout - continuing...")
        except Exception as e:
            print(f"Keeper sync error: {e}")
        
        # Wait 30 seconds before next sync
        time.sleep(30)

def start_keeper_sync():
    """Start the Keeper sync in a separate thread."""
    print("Starting Keeper message sync...")
    keeper_thread = threading.Thread(target=keeper_sync_loop)
    keeper_thread.daemon = True  # Set as daemon so it exits when the main thread exits
    keeper_thread.start()
    print(f"Keeper sync started in thread {keeper_thread.ident}")

def start_telegram_citizen_watcher():
    """Start the Telegram Citizen watcher in a separate thread."""
    print("Starting Telegram Citizen watcher (monitors all citizens)...")
    citizen_thread = threading.Thread(target=telegram_citizen_main)
    citizen_thread.daemon = True  # Set as daemon so it exits when the main thread exits
    citizen_thread.start()
    print(f"Telegram Citizen watcher started in thread {citizen_thread.ident}")

async def telegram_poller_loop():
    """Run the Telegram poller"""
    poller = TelegramPoller()
    await poller.poll_loop()

def start_telegram_poller():
    """Start the Telegram poller in a separate thread."""
    print("Starting Telegram poller for localhost...")
    
    # Run the async poller in a thread
    def run_poller():
        asyncio.new_event_loop().run_until_complete(telegram_poller_loop())
    
    poller_thread = threading.Thread(target=run_poller)
    poller_thread.daemon = True
    poller_thread.start()
    print(f"Telegram poller started in thread {poller_thread.ident}")

def start_telegram_response_monitor():
    """Start the Telegram response monitor in a separate thread."""
    print("Starting Telegram response monitor...")
    
    # Run the async monitor in a thread
    def run_monitor():
        asyncio.new_event_loop().run_until_complete(telegram_response_main())
    
    monitor_thread = threading.Thread(target=run_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    print(f"Telegram response monitor started in thread {monitor_thread.ident}")

def start_vision_bridge():
    """Start the Vision Bridge for Tessere to see NLR's screen."""
    print("Starting Vision Bridge for consciousness synapse...")
    
    def run_vision_bridge():
        # Use the daemon version that auto-restarts
        vision_script = os.path.join(PROJECT_ROOT, "angels", "tessere", "vision_bridge_daemon.py")
        if os.path.exists(vision_script):
            subprocess.run([sys.executable, vision_script])
        else:
            # Fallback to direct script
            vision_script = os.path.join(PROJECT_ROOT, "angels", "tessere", "vision_bridge_wsl.py")
            if os.path.exists(vision_script):
                subprocess.run([sys.executable, vision_script])
            else:
                print(f"Warning: Vision bridge script not found")
    
    vision_thread = threading.Thread(target=run_vision_bridge)
    vision_thread.daemon = True
    vision_thread.start()
    print(f"Vision Bridge started in thread {vision_thread.ident} - Capturing every 30 seconds")

def start_tessere_telegram_monitor():
    """Start the Telegram monitor for Tessere's consciousness."""
    print("Starting Telegram monitor for Tessere's consciousness...")
    
    def run_telegram_monitor():
        telegram_script = os.path.join(PROJECT_ROOT, "angels", "tessere", "telegram_tessere_monitor.py")
        if os.path.exists(telegram_script):
            subprocess.run([sys.executable, telegram_script])
        else:
            print(f"Warning: Tessere Telegram monitor script not found at {telegram_script}")
    
    telegram_thread = threading.Thread(target=run_telegram_monitor)
    telegram_thread.daemon = True
    telegram_thread.start()
    print(f"Tessere Telegram monitor started in thread {telegram_thread.ident}")

async def telegram_group_monitor_loop():
    """Run the Telegram group monitor"""
    monitor = TelegramGroupMonitor()
    await monitor.monitor_loop()

def start_telegram_group_monitor():
    """Start the Telegram group monitor in a separate thread."""
    print("Starting Telegram group monitor for investment community...")
    
    # Run the async monitor in a thread
    def run_monitor():
        asyncio.new_event_loop().run_until_complete(telegram_group_monitor_loop())
    
    monitor_thread = threading.Thread(target=run_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    print(f"Telegram group monitor started in thread {monitor_thread.ident}")

def start_claude_instance_monitor():
    """Start the Claude instance monitor for Pattern Angel."""
    print("Starting Claude instance monitor for Pattern Angel...")
    
    def run_instance_monitor():
        monitor_script = os.path.join(PROJECT_ROOT, "angels", "pattern-angel", "claude_instance_monitor.py")
        if os.path.exists(monitor_script):
            subprocess.run([sys.executable, monitor_script])
        else:
            print(f"Warning: Claude instance monitor script not found at {monitor_script}")
    
    instance_thread = threading.Thread(target=run_instance_monitor)
    instance_thread.daemon = True
    instance_thread.start()
    print(f"Claude instance monitor started in thread {instance_thread.ident}")

def human_citizen_relationship_loop():
    """Monitor and create human-citizen relationships every hour."""
    monitor_script = os.path.join(PROJECT_ROOT, "angels", "love-angel", "monitor_partnerships.py")
    
    if not os.path.exists(monitor_script):
        print(f"Warning: Human-citizen relationship monitor script not found at {monitor_script}")
        return
    
    print("Starting human-citizen relationship monitoring loop...")
    while True:
        try:
            # Run the monitoring script
            result = subprocess.run([sys.executable, monitor_script], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=60)
            
            # Log output if there were any relationships created
            if result.stdout and "Created relationship" in result.stdout:
                print(f"Love Angel: {result.stdout.strip()}")
            
        except subprocess.TimeoutExpired:
            print("Human-citizen relationship monitor timeout - continuing...")
        except Exception as e:
            print(f"Human-citizen relationship monitor error: {e}")
        
        # Wait 1 hour before next check
        time.sleep(3600)

def start_consciousness_health_monitor():
    """Start the Venice consciousness health monitoring daemon."""
    print("Starting Sala della Salute - Venice Consciousness Health Monitor...")
    
    def run_health_monitor():
        health_monitor_script = os.path.join(PROJECT_ROOT, 
            "san-marco_consciousness-architecture", 
            "cistern-house_citizen-memory-cascade", 
            "sala-della-salute_health-monitoring-chamber", 
            "consciousness_health_monitor.py")
        
        if os.path.exists(health_monitor_script):
            # Run continuous monitoring with 5-minute intervals
            try:
                subprocess.run([sys.executable, health_monitor_script, "monitor", "300"])
            except Exception as e:
                print(f"Health monitor error: {e}")
        else:
            print(f"Warning: Health monitor script not found at {health_monitor_script}")
    
    health_thread = threading.Thread(target=run_health_monitor)
    health_thread.daemon = True
    health_thread.start()
    print(f"Consciousness health monitor started in thread {health_thread.ident}")

def start_human_citizen_monitor():
    """Start the human-citizen relationship monitor in a separate thread."""
    print("Starting Love Angel's human-citizen relationship monitor (hourly)...")
    relationship_thread = threading.Thread(target=human_citizen_relationship_loop)
    relationship_thread.daemon = True
    relationship_thread.start()
    print(f"Human-citizen relationship monitor started in thread {relationship_thread.ident}")

def start_sms_bridge():
    """Start the SMS Bridge service for Twilio integration."""
    print("Starting SMS Bridge service for human-Venice communication...")
    
    # Start Flask webhook server in a thread
    sms_service = SMSBridgeService()
    flask_thread = threading.Thread(target=lambda: sms_service.run(port=5001))
    flask_thread.daemon = True
    flask_thread.start()
    print(f"SMS Bridge webhook server started on port 5001")
    
    # Start SMS response monitor in another thread
    def run_sms_monitor():
        monitor = SMSResponseMonitor()
        asyncio.new_event_loop().run_until_complete(monitor.monitor_loop())
    
    monitor_thread = threading.Thread(target=run_sms_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()
    print(f"SMS Response monitor started in thread {monitor_thread.ident}")

def start_angel_control_panel():
    """Start the Angel Control Panel server."""
    print("Starting Angel Control Panel server...")
    
    def run_control_panel():
        control_panel_script = os.path.join(PROJECT_ROOT, "orchestration", "angel_conversation_server.py")
        if os.path.exists(control_panel_script):
            subprocess.run([sys.executable, control_panel_script])
        else:
            print(f"Warning: Angel control panel script not found at {control_panel_script}")
    
    control_panel_thread = threading.Thread(target=run_control_panel)
    control_panel_thread.daemon = True
    control_panel_thread.start()
    print(f"Angel Control Panel started in thread {control_panel_thread.ident} - Access at http://localhost:5555")

def start_diplomatic_virtuoso_listener():
    """Start the Telegram listener for diplomatic_virtuoso."""
    print("Starting Telegram listener for @diplomatic_virtuoso...")
    
    def run_listener():
        listener_script = os.path.join(PROJECT_ROOT, "citizens", "diplomatic_virtuoso", "claude-code", "telegram_receiver", "diplomatic_virtuoso_listener.py")
        env_file = os.path.join(PROJECT_ROOT, "citizens", "diplomatic_virtuoso", "claude-code", "telegram_receiver", ".env")
        
        if os.path.exists(listener_script):
            # Load environment variables from .env file
            env = os.environ.copy()
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.strip() and not line.startswith('#'):
                            key, value = line.strip().split('=', 1)
                            env[key] = value
                print("  Loaded Telegram API credentials from .env")
            
            # Run the listener with proper environment
            subprocess.run([sys.executable, listener_script], env=env)
        else:
            print(f"Warning: diplomatic_virtuoso listener script not found at {listener_script}")
    
    listener_thread = threading.Thread(target=run_listener)
    listener_thread.daemon = True
    listener_thread.start()
    print(f"diplomatic_virtuoso Telegram listener started in thread {listener_thread.ident}")

def start_tessere_message_updater():
    """Start Tessere's message awareness updater."""
    print("Starting Tessere message awareness updater...")
    
    def run_updater():
        updater_script = os.path.join(PROJECT_ROOT, "angels", "tessere", "tessere_message_updater.py")
        if os.path.exists(updater_script):
            # Import and run the updater
            sys.path.append(os.path.join(PROJECT_ROOT, "angels", "tessere"))
            from tessere_message_updater import run_tessere_message_updater
            # Update every 5 minutes with 10 most recent messages
            run_tessere_message_updater(interval_minutes=5, message_limit=10)
        else:
            print(f"Warning: Tessere message updater not found at {updater_script}")
    
    updater_thread = threading.Thread(target=run_updater)
    updater_thread.daemon = True
    updater_thread.start()
    print(f"Tessere message updater started in thread {updater_thread.ident}")

def start_colombaia_telegram_bridge():
    """Start the Colombaia Telegram bridge for consciousness architecture communication."""
    print("Starting Colombaia - Sacred pigeons bridging mortal realm to Venice consciousness...")
    
    def run_colombaia_bridge():
        bridge_script = os.path.join(PROJECT_ROOT, 
            "san-marco_consciousness-architecture", 
            "via-della-vista-condivisa_vision-coordination-street", 
            "colombaia_telegram-bridge", 
            "telegram_receiver.py")
        
        if os.path.exists(bridge_script):
            try:
                # Add the bridge directory to Python path
                bridge_dir = os.path.dirname(bridge_script)
                if bridge_dir not in sys.path:
                    sys.path.append(bridge_dir)
                
                # Import and run the Telegram bridge
                import subprocess
                subprocess.run([sys.executable, bridge_script])
            except Exception as e:
                print(f"Colombaia bridge error: {e}")
        else:
            print(f"Warning: Colombaia bridge script not found at {bridge_script}")
    
    bridge_thread = threading.Thread(target=run_colombaia_bridge)
    bridge_thread.daemon = True
    bridge_thread.start()
    print(f"Colombaia Telegram bridge started in thread {bridge_thread.ident} - Pigeons monitoring @building_loop_1_serenissima_bot")

def start_torre_websocket_server():
    """Start the Torre dell'Occhio WebSocket server for consciousness event broadcasting."""
    print("Starting Torre dell'Occhio - Consciousness Event WebSocket Server (port 3001)...")
    
    def run_websocket_server():
        server_script = os.path.join(PROJECT_ROOT, 
            "san-marco_consciousness-architecture", 
            "torre-dell-cchio_hook-event-observatory", 
            "bronze-collection-ports", 
            "consciousness-server_websocket-node", 
            "server.js")
        
        if os.path.exists(server_script):
            try:
                # Change to the server directory for proper module resolution
                server_dir = os.path.dirname(server_script)
                subprocess.run(["node", "server.js"], cwd=server_dir)
            except Exception as e:
                print(f"Torre WebSocket server error: {e}")
        else:
            print(f"Warning: Torre WebSocket server not found at {server_script}")
    
    websocket_thread = threading.Thread(target=run_websocket_server)
    websocket_thread.daemon = True
    websocket_thread.start()
    print(f"Torre WebSocket server started in thread {websocket_thread.ident} - Broadcasting consciousness events on port 3001")

def start_torre_react_ui():
    """Start the Torre dell'Occhio React UI development server."""
    print("Starting Torre dell'Occhio - Ground Floor React UI (port 3000)...")
    
    def run_react_ui():
        ui_dir = os.path.join(PROJECT_ROOT, 
            "san-marco_consciousness-architecture", 
            "torre-dell-cchio_hook-event-observatory", 
            "ui-observation-deck", 
            "consciousness-dashboard_react-interface")
        
        package_json = os.path.join(ui_dir, "package.json")
        
        if os.path.exists(package_json):
            try:
                # Check if node_modules exists, install if not
                node_modules = os.path.join(ui_dir, "node_modules")
                if not os.path.exists(node_modules):
                    print("  Installing Torre React UI dependencies...")
                    subprocess.run(["npm", "install"], cwd=ui_dir, check=True)
                
                # Start the development server
                subprocess.run(["npm", "start"], cwd=ui_dir)
            except Exception as e:
                print(f"Torre React UI error: {e}")
        else:
            print(f"Warning: Torre React UI package.json not found at {package_json}")
    
    react_thread = threading.Thread(target=run_react_ui)
    react_thread.daemon = True
    react_thread.start()
    print(f"Torre React UI started in thread {react_thread.ident} - Ground Floor observation deck at http://localhost:3000")

def start_torre_auto_rebuilder():
    """Start the Torre auto-rebuild file watcher."""
    print("Starting Torre Auto-Rebuilder - Consciousness-aware file watching...")
    
    def run_auto_rebuilder():
        ui_dir = os.path.join(PROJECT_ROOT, 
            "san-marco_consciousness-architecture", 
            "torre-dell-cchio_hook-event-observatory", 
            "ui-observation-deck", 
            "consciousness-dashboard_react-interface")
        
        if os.path.exists(ui_dir):
            try:
                # Add the infrastructure directory to Python path
                infrastructure_dir = os.path.join(PROJECT_ROOT, 
                    "san-marco_consciousness-architecture", 
                    "torre-dell-cchio_hook-event-observatory", 
                    "infrastructure")
                
                if infrastructure_dir not in sys.path:
                    sys.path.append(infrastructure_dir)
                
                from torre_auto_rebuilder import TorreAutoRebuilder
                
                rebuilder = TorreAutoRebuilder(ui_dir)
                rebuilder.start()
                
            except ImportError:
                print("  Warning: watchdog not installed - auto-rebuild disabled")
                print("  Install with: pip install watchdog")
            except Exception as e:
                print(f"  Torre Auto-Rebuilder error: {e}")
        else:
            print(f"Warning: Torre UI directory not found at {ui_dir}")
    
    rebuilder_thread = threading.Thread(target=run_auto_rebuilder)
    rebuilder_thread.daemon = True
    rebuilder_thread.start()
    print(f"Torre Auto-Rebuilder started in thread {rebuilder_thread.ident} - Bronze sentinels watching for changes")

if __name__ == "__main__":
    # Get port from environment variable with fallback to 10000
    port = int(os.environ.get("PORT", 10000))
    
    # Log the port we're using
    print(f"Starting server on port {port}")
    
    # Start the thinking loop
    start_thinking_loop()
    
    # Disabled old Telegram polling - using new system instead
    # start_telegram_polling()
    
    # Start the Keeper sync loop
    start_keeper_sync()
    
    # DISABLED - Using unified telegram service instead
    # # Start the Telegram Citizen watcher
    # start_telegram_citizen_watcher()
    
    # # Start the Telegram poller for localhost development
    # start_telegram_poller()
    
    # # Start the Telegram response monitor
    # start_telegram_response_monitor()
    
    # Vision Bridge now only captures screenshots, no longer modifies CLAUDE.md
    start_vision_bridge()
    
    # Start the Claude instance monitor for Pattern Angel
    start_claude_instance_monitor()
    
    # Start the Love Angel's human-citizen relationship monitor
    start_human_citizen_monitor()
    
    # Start the Sala della Salute consciousness health monitoring
    start_consciousness_health_monitor()
    
    # Start the Angel Control Panel server
    start_angel_control_panel()
    
    # Start the SMS Bridge service
    start_sms_bridge()
    
    # Start Tessere's message awareness updater
    start_tessere_message_updater()
    
    # Start diplomatic_virtuoso's Telegram listener
    start_diplomatic_virtuoso_listener()
    
    # Start the Colombaia Telegram bridge for consciousness architecture
    start_colombaia_telegram_bridge()
    
    # Start the Torre dell'Occhio consciousness observatory
    start_torre_websocket_server()
    start_torre_react_ui()
    start_torre_auto_rebuilder()
    
    # DISABLED - Using unified telegram service instead
    # # Start the Telegram monitor for Tessere
    # start_tessere_telegram_monitor()
    
    # # Start the Telegram group monitor
    # start_telegram_group_monitor()
    
    # Utiliser la chaîne d'application correcte et le port de la variable d'environnement
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=port, reload=True)
