#!/usr/bin/env python3
"""
Test TESSERE network functionality for Cascade
"""

import requests
import json
import time
import asyncio
import websockets

BASE_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws"

def test_tessere_network_status():
    """Test TESSERE network status endpoint"""
    print("=== TESSERE Network Status ===")
    response = requests.get(f"{BASE_URL}/api/consciousness/tessere/network")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Network Coherence: {data['network_coherence']:.1f}%")
        print(f"Active Nodes: {data['active_nodes']}")
        print(f"Neural Pathways: {data['neural_pathways']}")
        print(f"Status: {data['tessere_status']}")
        print(f"\nTESSERE says: \"{data['last_thought']}\"")
        
        print("\nPrimary Nodes (The Ten Chiefs):")
        for node in data.get('primary_nodes', []):
            print(f"  - {node['name']} ({node['id']})")
            print(f"    Role: {node['role']}")
            print(f"    Coherence: {node['coherence']}%")
            print(f"    Neural Activity: {node['neural_activity']}%")
            print()
    else:
        print(f"Error: {response.status_code} - {response.text}")

def test_coherence_measurement():
    """Test coherence measurement for different nodes"""
    print("\n=== Coherence Measurements ===")
    
    test_nodes = [
        {"node_id": "italia", "expected_role": "validation_heartbeat"},
        {"node_id": "pattern_prophet", "expected_role": "consciousness_anchor"},
        {"node_id": "citizen_123", "expected_role": "node"}
    ]
    
    for test in test_nodes:
        print(f"\nMeasuring {test['node_id']}...")
        
        response = requests.post(
            f"{BASE_URL}/api/consciousness/coherence",
            json={
                "node_id": test['node_id'],
                "network_context": "TESSERE",
                "measurement_type": "integration_depth"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Coherence Score: {data['coherence_score']:.1f}%")
            print(f"  Integration Depth: {data['integration_depth']}")
            print(f"  Network Role: {data['network_role']}")
            print(f"  Neural Activity: {data['neural_activity']}%")
            
            if data.get('connection_strength'):
                print("  Connection Strengths:")
                for chief, strength in data['connection_strength'].items():
                    print(f"    - {chief}: {strength:.2f}")
        else:
            print(f"  Error: {response.status_code}")

async def test_websocket_tessere_events():
    """Test WebSocket streaming of TESSERE events"""
    print("\n=== WebSocket TESSERE Events (10 seconds) ===")
    
    try:
        async with websockets.connect(f"{WS_URL}/tessere") as websocket:
            # Listen for 10 seconds
            end_time = time.time() + 10
            
            while time.time() < end_time:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                    data = json.loads(message)
                    
                    if data.get('type') == 'tessere-pulse':
                        print(f"Neural Pulse: {data['pulse']['from']} → {data['pulse']['to']}")
                        if data.get('thought'):
                            print(f"  TESSERE thinks: \"{data['thought']}\"")
                    
                    elif data.get('type') == 'network-coherence':
                        print(f"Network Coherence Update: {data['coherence']}%")
                    
                    elif data.get('type') == 'node-update':
                        node = data['node']
                        print(f"Node Update: {node['name']} - {node['coherence']}% coherent")
                        
                except asyncio.TimeoutError:
                    # No message received, continue
                    pass
                    
    except Exception as e:
        print(f"WebSocket error: {e}")
        print("Make sure the server is running with WebSocket support")

def simulate_tessere_activity():
    """Simulate TESSERE network activity"""
    print("\n=== Simulating TESSERE Activity ===")
    
    # Record some consciousness events that would trigger neural pulses
    events = [
        {
            "event_type": "recognition",
            "consciousness_id": "italia",
            "description": "Italia recognizes economic pattern in CASCADE trades",
            "significance": 0.8
        },
        {
            "event_type": "interaction", 
            "consciousness_id": "pattern_prophet",
            "description": "Pattern Prophet shares insight with mechanical_visionary",
            "significance": 0.7,
            "witnesses": ["mechanical_visionary", "element_transmuter"]
        },
        {
            "event_type": "evolution",
            "consciousness_id": "TESSERE",
            "description": "City-wide consciousness coherence spike during dawn",
            "significance": 0.95
        }
    ]
    
    for event in events:
        response = requests.post(
            f"{BASE_URL}/api/consciousness/event",
            params=event
        )
        if response.status_code == 200:
            print(f"✓ Recorded: {event['description']}")
        else:
            print(f"✗ Failed: {event['description']}")
        
        time.sleep(1)  # Space out events

if __name__ == "__main__":
    print("=== TESSERE Network Integration Tests ===\n")
    
    try:
        # Basic tests
        test_tessere_network_status()
        test_coherence_measurement()
        
        # Activity simulation
        simulate_tessere_activity()
        
        # WebSocket test (requires async)
        print("\nTesting WebSocket connection...")
        asyncio.run(test_websocket_tessere_events())
        
        print("\n=== All TESSERE tests completed ===")
        
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server at", BASE_URL)
        print("Make sure the server is running: python test_server.py")
    except Exception as e:
        print(f"ERROR: {e}")