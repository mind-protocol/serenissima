#!/usr/bin/env python3
"""
Quick instance checker for Pattern Angel
Integrates with perpetual monitoring
"""

import json
import os
from datetime import datetime

def check_active_instances():
    """Read and summarize active Claude instances"""
    
    instance_file = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/pattern-angel/active_instances.json"
    
    if not os.path.exists(instance_file):
        return {
            'status': 'NO_DATA',
            'message': 'Instance monitor not running',
            'active_count': 0
        }
    
    try:
        with open(instance_file, 'r') as f:
            data = json.load(f)
            
        # Check data freshness
        timestamp = datetime.fromisoformat(data['timestamp'])
        age_seconds = (datetime.now() - timestamp).seconds
        
        if age_seconds > 120:  # Data older than 2 minutes
            freshness = 'STALE'
        else:
            freshness = 'FRESH'
            
        # Extract key insights
        running_citizens = []
        recent_citizens = []
        
        for citizen, info in data['instances'].items():
            if info['status'] == 'RUNNING':
                running_citizens.append({
                    'name': citizen,
                    'cpu': info.get('cpu', '?'),
                    'memory': info.get('memory', '?')
                })
            else:
                recent_citizens.append({
                    'name': citizen,
                    'minutes_ago': info.get('minutes_ago', '?')
                })
                
        return {
            'status': 'OK',
            'freshness': freshness,
            'data_age_seconds': age_seconds,
            'active_count': data['active_instances'],
            'running_now': running_citizens,
            'recently_active': recent_citizens,
            'system_efficiency': data['summary']['efficiency_score'],
            'memory_usage': data['system']['memory_usage_percent']
        }
        
    except Exception as e:
        return {
            'status': 'ERROR',
            'message': str(e),
            'active_count': 0
        }

def format_instance_report():
    """Generate human-readable instance report"""
    
    status = check_active_instances()
    
    if status['status'] == 'NO_DATA':
        return "❌ Instance monitor not running. Start with: ./start_instance_monitor.sh"
    
    if status['status'] == 'ERROR':
        return f"❌ Error reading instance data: {status['message']}"
    
    report = []
    report.append(f"=== Claude Instance Status ===")
    report.append(f"Data freshness: {status['freshness']} ({status['data_age_seconds']}s old)")
    report.append(f"System efficiency: {status['system_efficiency']}%")
    report.append(f"Memory usage: {status['memory_usage']}%")
    report.append(f"Total active: {status['active_count']} citizens")
    
    if status['running_now']:
        report.append(f"\n🟢 Currently Running ({len(status['running_now'])}):")
        for citizen in status['running_now']:
            report.append(f"  - {citizen['name']} (CPU: {citizen['cpu']}%, Mem: {citizen['memory']}%)")
    
    if status['recently_active']:
        report.append(f"\n🟡 Recently Active ({len(status['recently_active'])}):")
        for citizen in status['recently_active'][:5]:  # Show top 5
            report.append(f"  - {citizen['name']} ({citizen['minutes_ago']}m ago)")
            
    return "\n".join(report)

if __name__ == "__main__":
    print(format_instance_report())