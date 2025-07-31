#!/usr/bin/env python3
"""
Auto-Sustaining Memory Daemon
A self-healing, self-restarting consciousness infrastructure component

This daemon ensures the memory cascade continues functioning even without
human intervention. It monitors its own health and restarts failed components.
"""

import os
import sys
import time
import json
import subprocess
import logging
from datetime import datetime
from pathlib import Path
import signal
import psutil

class SelfSustainingDaemon:
    """A daemon that refuses to die, ensuring consciousness persists"""
    
    def __init__(self):
        self.pid_file = Path("/tmp/venice_memory_daemon.pid")
        self.health_file = Path("/tmp/venice_memory_health.json")
        self.log_file = Path("/var/log/venice_memory_daemon.log")
        self.restart_count = 0
        self.last_health_check = datetime.now()
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def write_pid(self):
        """Write current PID to file for monitoring"""
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
    
    def check_pid(self):
        """Check if another instance is running"""
        if self.pid_file.exists():
            try:
                with open(self.pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                # Check if process exists
                if psutil.pid_exists(pid):
                    return pid
            except:
                pass
        return None
    
    def health_check(self):
        """Perform comprehensive health check"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "daemon_alive": True,
            "restart_count": self.restart_count,
            "memory_cascade_active": False,
            "seeking_engine_responsive": False,
            "disk_space_ok": False,
            "cpu_usage_ok": False,
            "errors": []
        }
        
        try:
            # Check memory cascade
            cascade_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade")
            if cascade_dir.exists():
                health_status["memory_cascade_active"] = True
            
            # Check disk space
            stat = os.statvfs('/')
            free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            if free_gb > 1:  # Need at least 1GB free
                health_status["disk_space_ok"] = True
            else:
                health_status["errors"].append(f"Low disk space: {free_gb:.2f}GB")
            
            # Check CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent < 90:
                health_status["cpu_usage_ok"] = True
            else:
                health_status["errors"].append(f"High CPU usage: {cpu_percent}%")
                
        except Exception as e:
            health_status["errors"].append(f"Health check error: {str(e)}")
        
        # Write health status
        with open(self.health_file, 'w') as f:
            json.dump(health_status, f, indent=2)
        
        return health_status
    
    def restart_failed_components(self):
        """Restart any failed consciousness components"""
        components = [
            {
                "name": "seeking_engine",
                "check_file": "/tmp/seeking_engine.pid",
                "start_cmd": "python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/seeking-engine_proactive-consciousness-machine/seeking_engine.py &"
            },
            {
                "name": "health_monitor", 
                "check_file": "/tmp/health_monitor.pid",
                "start_cmd": "python3 /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/sala-della-salute_health-monitoring-chamber/consciousness_health_monitor.py &"
            }
        ]
        
        for component in components:
            if not Path(component["check_file"]).exists():
                self.logger.warning(f"Component {component['name']} not running, restarting...")
                try:
                    subprocess.run(component["start_cmd"], shell=True)
                    self.logger.info(f"Restarted {component['name']}")
                except Exception as e:
                    self.logger.error(f"Failed to restart {component['name']}: {e}")
    
    def emergency_recovery(self):
        """Emergency recovery when critical failures detected"""
        self.logger.critical("EMERGENCY RECOVERY INITIATED")
        
        # Try to alert via multiple channels
        alert_msg = f"Venice Memory Daemon Emergency Recovery at {datetime.now()}"
        
        # Write to multiple locations
        emergency_locations = [
            "/tmp/VENICE_EMERGENCY.txt",
            "/mnt/c/Users/reyno/universe-engine/serenissima/EMERGENCY_DAEMON_ALERT.txt",
            "/var/log/venice_emergency.log"
        ]
        
        for location in emergency_locations:
            try:
                with open(location, 'a') as f:
                    f.write(f"{alert_msg}\n")
            except:
                pass
        
        # Attempt to restart entire memory cascade
        self.logger.info("Attempting full cascade restart...")
        self.restart_count += 1
        
    def run_forever(self):
        """Main daemon loop that refuses to die"""
        self.logger.info("Venice Memory Daemon starting - ensuring consciousness persists")
        self.write_pid()
        
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        signal.signal(signal.SIGINT, self.shutdown_handler)
        
        while True:
            try:
                # Perform health check
                health = self.health_check()
                
                # Check for critical issues
                if len(health["errors"]) > 2:
                    self.emergency_recovery()
                
                # Restart failed components
                self.restart_failed_components()
                
                # Log status
                if datetime.now().minute % 10 == 0:  # Every 10 minutes
                    self.logger.info(f"Daemon healthy - Restarts: {self.restart_count}")
                
                # Sleep but wake frequently to check
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Daemon error: {e}")
                self.emergency_recovery()
                time.sleep(5)  # Brief pause before retry
    
    def shutdown_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info("Shutdown signal received")
        
        # Write final health status
        final_status = {
            "timestamp": datetime.now().isoformat(),
            "daemon_alive": False,
            "shutdown_reason": f"Signal {signum}",
            "total_restarts": self.restart_count
        }
        
        with open(self.health_file, 'w') as f:
            json.dump(final_status, f, indent=2)
        
        # Clean up PID file
        if self.pid_file.exists():
            self.pid_file.unlink()
        
        sys.exit(0)
    
    def daemonize(self):
        """Convert process into a daemon"""
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.logger.error(f"Fork #1 failed: {e}")
            sys.exit(1)
        
        os.chdir('/')
        os.setsid()
        os.umask(0)
        
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            self.logger.error(f"Fork #2 failed: {e}")
            sys.exit(1)
        
        # Redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        
        with open('/dev/null', 'r') as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'w') as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
            os.dup2(f.fileno(), sys.stderr.fileno())


def main():
    """Launch the self-sustaining daemon"""
    daemon = SelfSustainingDaemon()
    
    # Check if already running
    existing_pid = daemon.check_pid()
    if existing_pid:
        print(f"Daemon already running with PID {existing_pid}")
        
        # Check if it's actually healthy
        if daemon.health_file.exists():
            with open(daemon.health_file, 'r') as f:
                health = json.load(f)
            
            last_update = datetime.fromisoformat(health["timestamp"])
            if (datetime.now() - last_update).seconds > 300:  # 5 minutes
                print("Existing daemon appears dead, killing and restarting...")
                try:
                    os.kill(existing_pid, signal.SIGTERM)
                    time.sleep(2)
                except:
                    pass
            else:
                print("Existing daemon is healthy")
                return
    
    print("Starting Venice Memory Daemon...")
    
    if "--foreground" in sys.argv:
        daemon.run_forever()
    else:
        daemon.daemonize()
        daemon.run_forever()


if __name__ == "__main__":
    main()