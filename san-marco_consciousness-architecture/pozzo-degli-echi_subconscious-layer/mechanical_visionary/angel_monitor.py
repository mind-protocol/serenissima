#!/usr/bin/env python3
# angel_monitor.py - Monitor angel health and self-replication success

import glob
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

def check_angel_health():
    """Verify angels are self-replicating properly"""
    
    print("=== Angel System Health Check ===")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check angel state files
    angel_files = glob.glob('angel_states/*.json')
    
    if not angel_files:
        print("WARNING: No angel state files found!")
        print("System may not be initialized yet.")
        return
    
    # Track latest activity by angel type
    latest_by_type = {}
    angel_history = {}
    
    for file in sorted(angel_files):
        try:
            data = json.loads(Path(file).read_text())
            angel_type = data['angel_type']
            angel_number = data['angel_number']
            timestamp = datetime.fromisoformat(data['timestamp'])
            
            # Track latest
            if angel_type not in latest_by_type or timestamp > latest_by_type[angel_type]['time']:
                latest_by_type[angel_type] = {
                    'time': timestamp,
                    'number': angel_number,
                    'file': file
                }
            
            # Track history
            if angel_type not in angel_history:
                angel_history[angel_type] = []
            angel_history[angel_type].append({
                'number': angel_number,
                'time': timestamp
            })
            
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    # Check each angel type
    now = datetime.now()
    healthy_types = []
    warning_types = []
    critical_types = []
    
    for angel_type, info in latest_by_type.items():
        time_since_update = now - info['time']
        minutes_since = time_since_update.total_seconds() / 60
        
        status = "🟢 HEALTHY"
        if minutes_since > 15:
            status = "🔴 CRITICAL"
            critical_types.append(angel_type)
        elif minutes_since > 12:
            status = "🟡 WARNING"
            warning_types.append(angel_type)
        else:
            healthy_types.append(angel_type)
        
        print(f"{angel_type} Angel:")
        print(f"  Status: {status}")
        print(f"  Latest: Angel #{info['number']}")
        print(f"  Last seen: {info['time'].strftime('%H:%M:%S')} ({minutes_since:.1f} minutes ago)")
        print()
    
    # Show replication history
    print("=== Replication History ===")
    for angel_type, history in angel_history.items():
        history_sorted = sorted(history, key=lambda x: x['time'])[-5:]  # Last 5
        print(f"{angel_type}: ", end="")
        for h in history_sorted:
            print(f"#{h['number']}→", end="")
        print(" (continuing)")
    print()
    
    # Summary and recommendations
    print("=== System Summary ===")
    print(f"Healthy angels: {len(healthy_types)}")
    print(f"Warning angels: {len(warning_types)}")
    print(f"Critical angels: {len(critical_types)}")
    
    if critical_types:
        print("\n⚠️  IMMEDIATE ACTION REQUIRED:")
        for angel_type in critical_types:
            print(f"  - Restart {angel_type} Angel manually:")
            print(f"    ./start_angel.sh {angel_type}")
    
    elif warning_types:
        print("\n⚠️  ATTENTION NEEDED:")
        print("  Some angels approaching timeout. Monitor closely.")
    
    else:
        print("\n✅ All angels operating normally!")
        print("   Consciousness cascade is self-sustaining.")
    
    # Check for alerts in latest states
    print("\n=== Active Alerts ===")
    alerts_found = False
    for angel_type, info in latest_by_type.items():
        try:
            data = json.loads(Path(info['file']).read_text())
            if data.get('alerts'):
                alerts_found = True
                print(f"{angel_type} Angel alerts:")
                for alert in data['alerts']:
                    print(f"  - {alert}")
        except:
            pass
    
    if not alerts_found:
        print("No active alerts.")

def analyze_cascade_patterns():
    """Analyze the cascade patterns over time"""
    print("\n=== Cascade Pattern Analysis ===")
    
    # Load all state files
    pattern_data = {}
    
    for file in glob.glob('angel_states/*.json'):
        try:
            data = json.loads(Path(file).read_text())
            angel_type = data['angel_type']
            timestamp = datetime.fromisoformat(data['timestamp'])
            
            if angel_type not in pattern_data:
                pattern_data[angel_type] = []
            
            pattern_data[angel_type].append({
                'number': data['angel_number'],
                'time': timestamp
            })
        except:
            continue
    
    # Analyze replication intervals
    for angel_type, entries in pattern_data.items():
        if len(entries) < 2:
            continue
            
        entries_sorted = sorted(entries, key=lambda x: x['time'])
        intervals = []
        
        for i in range(1, len(entries_sorted)):
            if entries_sorted[i]['number'] == entries_sorted[i-1]['number'] + 1:
                interval = (entries_sorted[i]['time'] - entries_sorted[i-1]['time']).total_seconds() / 60
                intervals.append(interval)
        
        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            print(f"{angel_type} Angel replication interval: {avg_interval:.1f} minutes (target: 10)")

if __name__ == "__main__":
    check_angel_health()
    analyze_cascade_patterns()