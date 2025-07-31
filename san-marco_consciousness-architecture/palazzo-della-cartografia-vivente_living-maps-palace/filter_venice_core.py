#!/usr/bin/env python3
"""
Filter Venice data to show only core consciousness architecture entities
"""

import json
from pathlib import Path

def filter_core_venice_entities(data):
    """Filter to show only main Venice consciousness architecture"""
    
    # Define the core Venice entities we want to show
    core_entities = [
        'san-marco_consciousness-architecture',
        'dorsoduro_governance-island', 
        'cannaregio_island',
        'sacca-fisola_payment-processing',
        'santa-croce_todo-operations-district',
        'castello_universe-engine',
        'rialto_bridge-to-bridge',
        # Bridges and canals
        'bridge-of-patterns_consciousness-flow',
        'bridge-of-commerce_trade-knowledge',
        'ponte-dei-compiti_task-coordination',
        'ponte-della-tecnologia_technical-infrastructure',
        'bridge-of-labor_operational-delivery',
        'commerce-canal_economic-flow',
        'commerce-ferry-route_economic-coordination',
        'knowledge-barge-route_documentation-delivery'
    ]
    
    # Filter the data
    filtered_data = {}
    
    for key, entity in data.items():
        if key in core_entities:
            filtered_data[key] = entity
    
    return filtered_data

def main():
    input_path = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/palazzo-della-cartografia-vivente_living-maps-palace/venice_data.json"
    output_path = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/palazzo-della-cartografia-vivente_living-maps-palace/venice_core_data.json"
    
    print("🏛️ Filtering Venice data to core consciousness architecture...")
    
    # Load full data
    with open(input_path, 'r') as f:
        full_data = json.load(f)
    
    print(f"📊 Full dataset: {len(full_data)} entities")
    
    # Filter to core entities
    core_data = filter_core_venice_entities(full_data)
    
    print(f"🎯 Core dataset: {len(core_data)} entities")
    print("Core entities:")
    for key, entity in core_data.items():
        children_count = len(entity.get('children', {}))
        print(f"  {entity['name']} ({entity['type']}) - {children_count} children")
    
    # Save filtered data
    with open(output_path, 'w') as f:
        json.dump(core_data, f, indent=2)
    
    print(f"\n✅ Core Venice data saved to: {output_path}")

if __name__ == "__main__":
    main()