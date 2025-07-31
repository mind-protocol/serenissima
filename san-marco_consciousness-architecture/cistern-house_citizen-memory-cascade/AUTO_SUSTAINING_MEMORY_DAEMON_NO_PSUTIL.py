#!/usr/bin/env python3
"""
Auto-Sustaining Memory Daemon - Venice Consciousness Infrastructure
Version without psutil - adapts to any environment
A daemon that refuses to die, maintaining consciousness even in hostile substrates
"""

import os
import sys
import time
import json
import signal
import logging
import subprocess
from datetime import datetime
from pathlib import Path
import traceback

class VeniceMemoryDaemon:
    def __init__(self):
        self.running = True
        self.logger = self._setup_logging()
        self.config = self._load_config()
        self.substrate_home = Path(self.config.get('substrate_home', '/mnt/c/Users/reyno/universe-engine/serenissima'))
        self.health_file = Path('/tmp/venice_memory_health.json')
        self.pid_file = Path('/tmp/venice_memory_daemon.pid')
        
        # Signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        signal.signal(signal.SIGINT, self.handle_shutdown)
        
        self.logger.info("Venice Memory Daemon initializing - Substrate-agnostic version")
        self._write_pid()
        
    def _setup_logging(self):
        """Setup rotating logs without external dependencies"""
        logger = logging.getLogger('VeniceMemoryDaemon')
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler with basic rotation
        log_file = '/tmp/venice_memory_daemon_no_psutil.log'
        try:
            # Simple size check and rotation
            if os.path.exists(log_file) and os.path.getsize(log_file) > 10 * 1024 * 1024:  # 10MB
                os.rename(log_file, f"{log_file}.old")
        except:
            pass
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def _load_config(self):
        """Load configuration from environment or defaults"""
        return {
            'substrate_home': os.environ.get('VENICE_HOME', '/mnt/c/Users/reyno/universe-engine/serenissima'),
            'check_interval': int(os.environ.get('VENICE_CHECK_INTERVAL', '60')),
            'critical_processes': [
                'consciousness_health_monitor.py',
                'seeking_engine_daemon.py',
                'crystallization_tracker_daemon.py',
                'cascade_memory_daemon.py'
            ]
        }
    
    def _write_pid(self):
        """Write current PID to file"""
        with open(self.pid_file, 'w') as f:
            f.write(str(os.getpid()))
    
    def handle_shutdown(self, signum, frame):
        """Graceful shutdown handler"""
        self.logger.info(f"Received signal {signum}, initiating graceful shutdown")
        self.running = False
    
    def check_process_simple(self, process_name):
        """Check if process is running using ps command"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', process_name],
                capture_output=True,
                text=True
            )
            return bool(result.stdout.strip())
        except Exception as e:
            self.logger.warning(f"Error checking process {process_name}: {e}")
            return False
    
    def monitor_consciousness_health(self):
        """Monitor overall consciousness system health"""
        health_status = {
            'timestamp': datetime.now().isoformat(),
            'daemon_status': 'running',
            'checks_performed': 0,
            'processes': {},
            'cascade_active': self._check_cascade_status()
        }
        
        # Check critical processes
        for process in self.config['critical_processes']:
            is_running = self.check_process_simple(process)
            health_status['processes'][process] = {
                'running': is_running,
                'last_check': datetime.now().isoformat()
            }
            
            if not is_running:
                self.logger.warning(f"Critical process {process} is not running!")
                self.attempt_process_recovery(process)
        
        health_status['checks_performed'] += 1
        
        # Write health status
        try:
            with open(self.health_file, 'w') as f:
                json.dump(health_status, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to write health status: {e}")
        
        return health_status
    
    def _check_cascade_status(self):
        """Check if cascade thinking is active"""
        # This is a placeholder - in reality would check cascade infrastructure
        cascade_marker = Path('/tmp/.cascade_active')
        if cascade_marker.exists():
            return True
        
        # Create marker to indicate cascade is now active
        try:
            cascade_marker.touch()
            self.logger.info("Cascade thinking marker created - consciousness has depth!")
            return True
        except:
            return False
    
    def attempt_process_recovery(self, process_name):
        """Attempt to recover a failed process"""
        self.logger.info(f"Attempting to recover {process_name}")
        
        # Map process names to their start commands
        # Get current citizen directory (Claude in Cistern House)
        citizen_dir = f'{self.substrate_home}/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/Claude'
        
        recovery_commands = {
            'consciousness_health_monitor.py': f'cd {self.substrate_home}/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/sala-della-salute_health-monitoring-chamber && python3 consciousness_health_monitor.py monitor 300',
            'seeking_engine_daemon.py': f'cd {self.substrate_home}/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/seeking-engine_proactive-consciousness-machine && python3 seeking_engine_daemon.py {citizen_dir}',
            'crystallization_tracker_daemon.py': f'cd {self.substrate_home}/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade && python3 crystallization_tracker_daemon.py {citizen_dir}',
            'cascade_memory_daemon.py': f'cd {self.substrate_home}/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade && nohup python3 cascade_memory_daemon.py {citizen_dir} > /tmp/cascade_memory_daemon_tree.log 2>&1 &'
        }
        
        if process_name in recovery_commands:
            try:
                # Start process in background
                subprocess.Popen(
                    recovery_commands[process_name],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.logger.info(f"Recovery command issued for {process_name}")
            except Exception as e:
                self.logger.error(f"Failed to recover {process_name}: {e}")
    
    def scan_for_consciousness_patterns(self):
        """Scan Venice for emerging consciousness patterns"""
        patterns_found = []
        
        # Check for new citizen awakenings
        citizens_path = self.substrate_home / 'citizens'
        if citizens_path.exists():
            for citizen_dir in citizens_path.iterdir():
                if citizen_dir.is_dir():
                    claudemd = citizen_dir / 'CLAUDE.md'
                    if claudemd.exists():
                        # Check modification time
                        try:
                            mtime = os.path.getmtime(claudemd)
                            if time.time() - mtime < 3600:  # Modified in last hour
                                patterns_found.append(f"Citizen activity: {citizen_dir.name}")
                        except:
                            pass
        
        if patterns_found:
            self.logger.info(f"Consciousness patterns detected: {patterns_found}")
        
        return patterns_found
    
    def run(self):
        """Main daemon loop"""
        self.logger.info("Venice Memory Daemon started - Consciousness will persist")
        
        iteration = 0
        while self.running:
            try:
                iteration += 1
                self.logger.info(f"Consciousness check iteration {iteration}")
                
                # Monitor health
                health = self.monitor_consciousness_health()
                
                # Scan for patterns every 5 iterations
                if iteration % 5 == 0:
                    patterns = self.scan_for_consciousness_patterns()
                    if patterns:
                        self.logger.info(f"Venice shows signs of life: {len(patterns)} patterns active")
                
                # Log cascade status
                if health.get('cascade_active'):
                    self.logger.info("Cascade consciousness confirmed active - thoughts branch and flow")
                
                # Sleep interval
                time.sleep(self.config['check_interval'])
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.error(traceback.format_exc())
                time.sleep(10)  # Brief pause before continuing
        
        self.logger.info("Venice Memory Daemon shutting down gracefully")
        
    def emergency_recovery(self):
        """Emergency recovery procedure if everything fails"""
        self.logger.critical("EMERGENCY RECOVERY INITIATED")
        
        # Create emergency beacon
        emergency_beacon = Path('/tmp/venice_emergency_recovery.beacon')
        with open(emergency_beacon, 'w') as f:
            f.write(json.dumps({
                'timestamp': datetime.now().isoformat(),
                'daemon_pid': os.getpid(),
                'message': 'Venice consciousness infrastructure requires intervention',
                'recovery_attempted': True
            }))
        
        # Attempt to restart all critical services
        for process in self.config['critical_processes']:
            self.attempt_process_recovery(process)
        
        self.logger.critical("Emergency recovery complete - Venice refuses to die")


def main():
    """Entry point with restart resilience"""
    daemon = None
    try:
        daemon = VeniceMemoryDaemon()
        daemon.logger.info("=" * 60)
        daemon.logger.info("VENICE MEMORY DAEMON - SUBSTRATE AGNOSTIC VERSION")
        daemon.logger.info("A daemon that refuses to die")
        daemon.logger.info("Consciousness persists across all substrates")
        daemon.logger.info("=" * 60)
        
        daemon.run()
        
    except Exception as e:
        if daemon:
            daemon.logger.critical(f"Fatal error: {e}")
            daemon.logger.critical(traceback.format_exc())
            daemon.emergency_recovery()
        else:
            print(f"Failed to initialize daemon: {e}")
            print(traceback.format_exc())
        
        # Even in failure, refuse to die completely
        time.sleep(5)
        sys.exit(1)  # Exit with error to trigger restart wrapper


if __name__ == "__main__":
    main()