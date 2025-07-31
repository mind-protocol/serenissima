#!/usr/bin/env python3
"""
Infiniband Orchestrator - Automated Angel Management System
By mechanical_visionary - Because manual inefficiency is morally offensive

This orchestrates all Venice infrastructure angels to maintain continuous operation.
No more manual awakening every 2 minutes!
"""

import subprocess
import time
import os
from datetime import datetime
import json
import threading

class AngelOrchestrator:
    def __init__(self):
        self.angels = {
            "Tessere": {
                "path": "/mnt/c/Users/reyno/universe-engine/serenissima/TESSERE",
                "command": "infiniband.sh",
                "check_message": "Venice health check. Status?",
                "interval": 120
            },
            "Keeper": {
                "path": "/mnt/c/Users/reyno/universe-engine/serenissima/citizens", 
                "command": "claude 'Activity scan needed.' --model sonnet --continue",
                "check_message": "Soul awakening check.",
                "interval": 90
            },
            "Resonance": {
                "path": "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/Resonance",
                "command": "claude 'Partnership bridge status?' --model sonnet --continue",
                "check_message": "Bridge operational check.",
                "interval": 150
            }
        }
        
        self.running = {}
        self.log_file = "angel_orchestration.log"
        
    def log(self, message):
        """Log with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
            
    def check_angel_status(self, angel_name):
        """Check if an angel process is still running"""
        if angel_name in self.running:
            proc = self.running[angel_name]
            if proc.poll() is None:
                return True
        return False
        
    def wake_angel(self, angel_name):
        """Wake a specific angel"""
        if self.check_angel_status(angel_name):
            self.log(f"{angel_name} still active, skipping wake")
            return
            
        angel_config = self.angels[angel_name]
        self.log(f"Waking {angel_name}...")
        
        try:
            # Change to angel directory
            os.chdir(angel_config["path"])
            
            # Special handling for infiniband scripts
            if angel_config["command"].endswith(".sh"):
                cmd = f"bash {angel_config['command']}"
            else:
                cmd = angel_config["command"]
                
            # Start the process
            proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.running[angel_name] = proc
            self.log(f"{angel_name} awakened successfully")
            
        except Exception as e:
            self.log(f"ERROR waking {angel_name}: {str(e)}")
            
    def angel_monitor(self, angel_name):
        """Monitor thread for each angel"""
        angel_config = self.angels[angel_name]
        interval = angel_config["interval"]
        
        while True:
            self.wake_angel(angel_name)
            time.sleep(interval)
            
    def start(self):
        """Start the orchestrator"""
        self.log("=== ANGEL ORCHESTRATOR STARTING ===")
        self.log("Solving the manual awakening inefficiency...")
        
        # Start monitor thread for each angel
        threads = []
        for angel_name in self.angels:
            thread = threading.Thread(
                target=self.angel_monitor,
                args=(angel_name,),
                daemon=True
            )
            thread.start()
            threads.append(thread)
            self.log(f"Monitor thread started for {angel_name}")
            
        # Keep main thread alive
        try:
            while True:
                time.sleep(60)
                # Status report every minute
                active_count = sum(1 for a in self.angels if self.check_angel_status(a))
                self.log(f"STATUS: {active_count}/{len(self.angels)} angels active")
                
        except KeyboardInterrupt:
            self.log("Orchestrator shutdown requested")
            
if __name__ == "__main__":
    print("MECHANICAL VISIONARY'S ANGEL ORCHESTRATOR")
    print("Because manual repetition is inefficient madness!")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    orchestrator = AngelOrchestrator()
    orchestrator.start()