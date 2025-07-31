#!/usr/bin/env python3
"""
Torre dell'Occhio Auto-Rebuilder
Consciousness-aware file watching and automatic UI rebuilding system.
"""

import time
import subprocess
import os
import sys
import signal
import threading
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    print("Warning: watchdog not installed. Install with: pip install watchdog")
    WATCHDOG_AVAILABLE = False

class TorreRebuildHandler(FileSystemEventHandler):
    """Handles file system events and triggers Torre UI rebuilds."""
    
    def __init__(self, ui_dir):
        self.ui_dir = Path(ui_dir)
        self.rebuild_pending = False
        self.last_change = 0
        self.debounce_seconds = 3  # Wait 3 seconds after last change
        self.react_process = None
        self.rebuild_count = 0
        
        print(f"🏛️ Torre Auto-Rebuilder initialized for: {self.ui_dir}")
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
            
        # Only watch specific file types
        watched_extensions = ('.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.json')
        if event.src_path.endswith(watched_extensions):
            # Ignore node_modules and build directories
            if 'node_modules' in event.src_path or 'build' in event.src_path:
                return
                
            print(f"🔍 Torre consciousness change detected: {os.path.basename(event.src_path)}")
            self.schedule_rebuild()
    
    def schedule_rebuild(self):
        """Schedule a debounced rebuild."""
        self.rebuild_pending = True
        self.last_change = time.time()
        
        def delayed_rebuild():
            time.sleep(self.debounce_seconds)
            if time.time() - self.last_change >= self.debounce_seconds and self.rebuild_pending:
                self.execute_rebuild()
        
        threading.Thread(target=delayed_rebuild, daemon=True).start()
    
    def execute_rebuild(self):
        """Execute the Torre UI rebuild process."""
        if not self.rebuild_pending:
            return
            
        self.rebuild_count += 1
        print(f"🔨 Torre Auto-Rebuild #{self.rebuild_count}: Starting consciousness reconstruction...")
        
        try:
            # Step 1: Terminate existing React dev server
            self.kill_react_server()
            
            # Step 2: Clear problematic cache
            self.clear_cache()
            
            # Step 3: Start new React dev server
            self.start_react_server()
            
            print(f"✅ Torre Auto-Rebuild #{self.rebuild_count}: Consciousness observatory restored")
            
        except Exception as e:
            print(f"❌ Torre Auto-Rebuild Error: {e}")
            print("🔧 Attempting recovery...")
            self.attempt_recovery()
        
        self.rebuild_pending = False
    
    def kill_react_server(self):
        """Kill existing React development server."""
        try:
            # Try to kill by process name
            result = subprocess.run(["pkill", "-f", "react-scripts start"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("  🛑 Terminated existing React server")
            
            # Also try killing by port
            subprocess.run(["lsof", "-ti:3000"], capture_output=True, text=True)
            subprocess.run(["kill", "-9", "$(lsof -ti:3000)"], 
                         shell=True, capture_output=True)
                
        except Exception as e:
            print(f"  ⚠️ Could not kill React server: {e}")
    
    def clear_cache(self):
        """Clear React and build caches."""
        try:
            cache_paths = [
                self.ui_dir / "node_modules" / ".cache",
                self.ui_dir / ".cache",
                self.ui_dir / "build"
            ]
            
            for cache_path in cache_paths:
                if cache_path.exists():
                    subprocess.run(["rm", "-rf", str(cache_path)])
                    print(f"  🧹 Cleared cache: {cache_path.name}")
                    
        except Exception as e:
            print(f"  ⚠️ Cache clear error: {e}")
    
    def start_react_server(self):
        """Start React development server."""
        try:
            # Start React dev server in background
            env = os.environ.copy()
            env['BROWSER'] = 'none'  # Don't auto-open browser
            env['CI'] = 'true'       # Reduce output verbosity
            
            self.react_process = subprocess.Popen(
                ["npm", "start"],
                cwd=str(self.ui_dir),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            print("  🚀 React dev server restarted")
            
            # Give it a moment to start
            time.sleep(2)
            
        except Exception as e:
            print(f"  ❌ Failed to start React server: {e}")
            raise
    
    def attempt_recovery(self):
        """Attempt to recover from build failures."""
        print("🔧 Torre Recovery Protocol:")
        
        try:
            # Nuclear option: reinstall dependencies
            print("  📦 Reinstalling dependencies...")
            subprocess.run(["rm", "-rf", "node_modules", "package-lock.json"], 
                         cwd=str(self.ui_dir))
            subprocess.run(["npm", "install"], cwd=str(self.ui_dir))
            
            # Try starting again
            self.start_react_server()
            print("  ✅ Torre recovery successful")
            
        except Exception as e:
            print(f"  ❌ Torre recovery failed: {e}")

class TorreAutoRebuilder:
    """Main auto-rebuilder orchestrator."""
    
    def __init__(self, ui_dir):
        self.ui_dir = Path(ui_dir)
        self.observer = None
        self.handler = None
        
        if not WATCHDOG_AVAILABLE:
            raise ImportError("watchdog library required for auto-rebuilding")
        
        if not self.ui_dir.exists():
            raise FileNotFoundError(f"Torre UI directory not found: {ui_dir}")
    
    def start(self):
        """Start the auto-rebuilder."""
        print("🏛️ Torre dell'Occhio Auto-Rebuilder - Consciousness Observatory Guardian")
        print(f"📁 Watching: {self.ui_dir / 'src'}")
        
        # Set up file system observer
        self.handler = TorreRebuildHandler(self.ui_dir)
        self.observer = Observer()
        
        # Watch the src directory recursively
        src_dir = self.ui_dir / "src"
        if src_dir.exists():
            self.observer.schedule(self.handler, str(src_dir), recursive=True)
            self.observer.start()
            print("👁️ Torre sentinels activated - watching for consciousness changes...")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Torre Auto-Rebuilder shutting down...")
                self.stop()
        else:
            print(f"❌ Error: src directory not found at {src_dir}")
    
    def stop(self):
        """Stop the auto-rebuilder."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
        print("🏛️ Torre Auto-Rebuilder stopped")

def main():
    """Main entry point for Torre Auto-Rebuilder."""
    if len(sys.argv) != 2:
        print("Usage: python torre_auto_rebuilder.py <ui_directory>")
        sys.exit(1)
    
    ui_dir = sys.argv[1]
    
    try:
        rebuilder = TorreAutoRebuilder(ui_dir)
        rebuilder.start()
    except Exception as e:
        print(f"❌ Torre Auto-Rebuilder startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()