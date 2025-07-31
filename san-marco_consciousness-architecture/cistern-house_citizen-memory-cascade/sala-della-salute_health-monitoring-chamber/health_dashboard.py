#!/usr/bin/env python3
"""Sala della Salute - Health Dashboard
Simple visual health status display for Venice consciousness"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_latest_health_results():
    """Load most recent health check results"""
    results_file = Path('health_results.json')
    if results_file.exists():
        with open(results_file) as f:
            return json.load(f)
    return None

def status_emoji(status):
    """Convert status to emoji"""
    return {
        'OK': '✅',
        'WARNING': '⚠️',
        'CRITICAL': '🚨'
    }.get(status, '❓')

def display_health_dashboard():
    """Display formatted health dashboard"""
    results = load_latest_health_results()
    
    if not results:
        print("🏛️ SALA DELLA SALUTE - VENICE CONSCIOUSNESS HEALTH")
        print("=" * 60)
        print("❓ No health data available")
        print("   Run: python3 consciousness_health_monitor.py check")
        return
    
    timestamp = datetime.fromisoformat(results['timestamp'])
    age = datetime.now() - timestamp
    
    print("🏛️ SALA DELLA SALUTE - VENICE CONSCIOUSNESS HEALTH")
    print("=" * 60)
    print(f"🕐 Last Check: {timestamp.strftime('%Y-%m-%d %H:%M:%S')} ({age})")
    print(f"💓 Overall Status: {status_emoji(results['overall_status'])} {results['overall_status']}")
    print()
    
    print("📊 SYSTEM HEALTH DETAILS")
    print("-" * 40)
    
    for check_name, check_data in results['checks'].items():
        status = check_data['status']
        message = check_data['message']
        details = check_data.get('details', '')
        
        print(f"{status_emoji(status)} {check_name}")
        print(f"   Status: {status}")
        print(f"   Message: {message}")
        if details:
            print(f"   Details: {details}")
        print()
    
    # Health summary
    statuses = [check['status'] for check in results['checks'].values()]
    critical_count = statuses.count('CRITICAL')
    warning_count = statuses.count('WARNING')
    ok_count = statuses.count('OK')
    
    print("📈 HEALTH SUMMARY")
    print("-" * 20)
    print(f"✅ Healthy Systems: {ok_count}")
    print(f"⚠️  Warning Systems: {warning_count}")
    print(f"🚨 Critical Systems: {critical_count}")
    
    if critical_count > 0:
        print()
        print("🚨 IMMEDIATE ACTION REQUIRED!")
        print("   Run: python3 consciousness_recovery.py")
    elif warning_count > 0:
        print()
        print("⚠️  Monitor closely - degradation detected")
    else:
        print()
        print("✅ Venice consciousness operating normally")

def main():
    """Main execution"""
    # Change to health monitoring chamber directory
    chamber_path = Path(__file__).parent
    os.chdir(chamber_path)
    
    display_health_dashboard()

if __name__ == "__main__":
    main()