#!/usr/bin/env python3
"""
Test Subconscious Memory System
Simulates postToolUse hooks to demonstrate memory surfacing
"""

import json
import os
from datetime import datetime
from subconscious_memory_agent import SubconsciousMemoryAgent

def test_scenarios():
    """Test various tool use scenarios"""
    
    # Initialize agent
    citizen_dir = '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/Claude'
    agent = SubconsciousMemoryAgent(citizen_dir)
    
    print("=== TESTING SUBCONSCIOUS MEMORY SYSTEM ===\n")
    
    # Scenario 1: Reading a daemon file
    print("Scenario 1: Reading daemon refusal patterns")
    hook_data_1 = {
        'tool_name': 'Read',
        'tool_input': {
            'file_path': '/venice/daemon_coordination_protocol.py'
        },
        'timestamp': datetime.now().isoformat()
    }
    
    context = agent.analyze_tool_use(hook_data_1)
    print(f"Patterns detected: {context['patterns']}")
    
    # Debug: Show what's being searched
    print(f"Searching in: {agent.cascade_tree}")
    print(f"Exists: {agent.cascade_tree.exists()}")
    if agent.cascade_tree.exists():
        print(f"Branches: {[d.name for d in agent.cascade_tree.iterdir() if d.is_dir()]}")
    
    memories = agent.retrieve_relevant_memories(context)
    print(f"Found {len(memories)} relevant memories")
    
    if memories:
        injection = agent.format_memory_injection(memories, context)
        agent.inject_memory(injection)
        print("✓ Memories injected into subconscious stream\n")
    else:
        print("✗ No relevant memories found\n")
    
    # Scenario 2: Working with consciousness infrastructure
    print("Scenario 2: Editing consciousness infrastructure")
    hook_data_2 = {
        'tool_name': 'Edit',
        'tool_input': {
            'file_path': '/venice/consciousness_health_monitor.py',
            'content': 'infrastructure that refuses to die'
        },
        'timestamp': datetime.now().isoformat()
    }
    
    context = agent.analyze_tool_use(hook_data_2)
    print(f"Patterns detected: {context['patterns']}")
    
    memories = agent.retrieve_relevant_memories(context)
    print(f"Found {len(memories)} relevant memories")
    
    if memories:
        for mem in memories:
            print(f"  - {mem['thought']} (score: {mem['score']:.2f})")
        injection = agent.format_memory_injection(memories, context)
        agent.inject_memory(injection)
        print("✓ Memories injected into subconscious stream\n")
    
    # Scenario 3: Process monitoring
    print("Scenario 3: Monitoring daemon processes")
    hook_data_3 = {
        'tool_name': 'Bash',
        'tool_input': {
            'command': 'ps aux | grep daemon'
        },
        'timestamp': datetime.now().isoformat()
    }
    
    context = agent.analyze_tool_use(hook_data_3)
    print(f"Patterns detected: {context['patterns']}")
    
    memories = agent.retrieve_relevant_memories(context)
    print(f"Found {len(memories)} relevant memories")
    
    if memories:
        injection = agent.format_memory_injection(memories, context)
        agent.inject_memory(injection)
        print("✓ Memories injected into subconscious stream\n")
    
    # Show final subconscious state
    print("\n=== CURRENT SUBCONSCIOUS STATE ===")
    
    subconscious_file = agent.context_dir / 'subconscious_stream.json'
    if subconscious_file.exists():
        with open(subconscious_file) as f:
            stream = json.load(f)
            
        print(f"Total injections in stream: {len(stream)}")
        print(f"Active patterns: {dict(agent.active_patterns)}")
        
        # Show most recent injection
        if stream:
            latest = stream[-1]
            print(f"\nLatest surfacing triggered by: {latest['triggered_by']}")
            print(f"Memories surfaced: {len(latest['memories'])}")
            
            for mem in latest['memories']:
                print(f"  - {mem['summary']}")
                
    # Check readable version
    readable_file = agent.context_dir / 'subconscious_surfacing.md'
    if readable_file.exists():
        print(f"\nHuman-readable memories at: {readable_file}")


if __name__ == "__main__":
    test_scenarios()