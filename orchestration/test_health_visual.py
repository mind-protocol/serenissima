#!/usr/bin/env python3
"""
Test health visualization with mock data
"""

import json
import os
from datetime import datetime, timedelta
from health_visualizer import HealthVisualizer

# Create test health directory
health_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/health"
os.makedirs(health_dir, exist_ok=True)

# Create mock status data
mock_status = {
    # Healthy components
    'message_monitor': {
        'healthy': True,
        'last_checked': datetime.now().isoformat(),
        'type': 'monitor'
    },
    'message_angel_claude': {
        'healthy': True,
        'last_checked': datetime.now().isoformat(),
        'type': 'claude_session'
    },
    'airtable_messages': {
        'healthy': True,
        'last_checked': datetime.now().isoformat(),
        'type': 'data_source'
    },
    
    # Warning state (unhealthy < 15 min)
    'story_monitor': {
        'healthy': False,
        'last_checked': (datetime.now() - timedelta(minutes=5)).isoformat(),
        'type': 'monitor'
    },
    'story_angel_claude': {
        'healthy': True,
        'last_checked': datetime.now().isoformat(),
        'type': 'claude_session'
    },
    
    # Critical state (unhealthy > 15 min)
    'narrator_monitor': {
        'healthy': False,
        'last_checked': (datetime.now() - timedelta(minutes=20)).isoformat(),
        'type': 'monitor'
    },
    'narrator_angel_claude': {
        'healthy': False,
        'last_checked': (datetime.now() - timedelta(minutes=20)).isoformat(),
        'type': 'claude_session'
    },
    
    # Other components
    'traces_file': {
        'healthy': True,
        'last_checked': datetime.now().isoformat(),
        'type': 'data_source'
    },
    'telegram_responses': {
        'healthy': False,
        'last_checked': (datetime.now() - timedelta(minutes=10)).isoformat(),
        'type': 'output'
    }
}

# Save mock status
with open(f"{health_dir}/component_status.json", 'w') as f:
    json.dump(mock_status, f, indent=2)

print("Mock health status created:")
print("- Message flow: ✅ Healthy (green)")
print("- Story flow: ⚠️ Monitor warning (orange)")
print("- Narrator flow: ❌ Critical failure (red)")
print("- Telegram output: ⚠️ Warning (orange)")
print()

# Generate visualization
visualizer = HealthVisualizer(health_dir)
mmd_path = visualizer.generate_health_map()
print(f"Mermaid diagram saved: {mmd_path}")

# Try to generate PNG
png_path = visualizer.generate_png()
if png_path:
    print(f"PNG visualization saved: {png_path}")
    print("\nTo view the health map:")
    print(f"1. Open the PNG: {png_path}")
    print("2. Green = Healthy, Orange = Warning, Red = Critical")
    print("3. Thick lines show health status of connections")
else:
    print("\nTo visualize the health map:")
    print("1. Copy the contents of health_map.mmd")
    print("2. Paste into https://mermaid.live")
    print("3. See colored nodes and links showing health")