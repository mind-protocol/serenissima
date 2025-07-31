#!/usr/bin/env python3
"""
Scan Venice directory structure and generate JSON data for interactive bubble map
"""

import os
import json
from pathlib import Path

def determine_entity_type(folder_name, depth):
    """Determine entity type based on folder name and depth"""
    name_lower = folder_name.lower()
    
    # Explicit type patterns
    if any(x in name_lower for x in ['_district', 'san-marco', 'dorsoduro']):
        return 'district'
    if any(x in name_lower for x in ['_island', 'sacca-fisola', 'cannaregio', 'castello', 'rialto', 'santa-croce']):
        return 'island'
    if any(x in name_lower for x in ['bridge', 'ponte']):
        return 'bridge'
    if any(x in name_lower for x in ['canal', 'route', 'ferry']):
        return 'canal'
    if any(x in name_lower for x in ['palazzo', 'torre', 'casa', 'arsenal', 'scriptorium', 'corte', 'archivio', 'assemblea']):
        return 'building'
    if any(x in name_lower for x in ['chamber', 'workshop', 'gallery', 'mosaic', 'laboratory', 'biblioteca', 'sala', 'engine', 'interface']):
        return 'room'
    if any(x in name_lower for x in ['backendarchitect', 'frontendcraftsman', 'mechanical_visionary', 'citizen']):
        return 'citizen'
    
    # Fallback based on depth
    if depth == 1:
        return 'district'
    elif depth == 2:
        return 'island'
    elif depth == 3:
        return 'building'
    elif depth >= 4:
        return 'room'
    
    return 'tool'

def format_entity_name(folder_name):
    """Convert folder name to display name"""
    name = folder_name.replace('_', ' ').replace('-', ' ')
    # Capitalize words but keep special names
    words = name.split()
    formatted_words = []
    for word in words:
        if word.lower() in ['dell', 'dei', 'della', 'di', 'da', 'san', 'santa']:
            formatted_words.append(word.lower())
        else:
            formatted_words.append(word.capitalize())
    return ' '.join(formatted_words)

def scan_venice_directory(serenissima_path):
    """Scan directory structure and build hierarchy"""
    serenissima_path = Path(serenissima_path)
    
    def scan_recursively(current_path, depth=0):
        """Recursively scan directory and build entity tree"""
        children = {}
        
        if not current_path.is_dir():
            return children
            
        # Look for CLAUDE.md to confirm this is an entity
        claude_file = current_path / "CLAUDE.md"
        has_claude = claude_file.exists()
        
        # Scan subdirectories
        for item in current_path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if subdirectory has CLAUDE.md
                sub_claude = item / "CLAUDE.md"
                if sub_claude.exists():
                    entity_name = format_entity_name(item.name)
                    entity_type = determine_entity_type(item.name, depth + 1)
                    
                    # Get file size for leaf entities
                    file_size = sub_claude.stat().st_size if sub_claude.exists() else 0
                    
                    # Recursively scan children
                    grandchildren = scan_recursively(item, depth + 1)
                    
                    children[item.name] = {
                        "name": entity_name,
                        "type": entity_type,
                        "file_size": file_size,
                        "children": grandchildren
                    }
        
        return children
    
    # Start scanning from serenissima root
    root_data = scan_recursively(serenissima_path)
    
    return root_data

def main():
    serenissima_path = "/mnt/c/Users/reyno/universe-engine/serenissima"
    output_path = "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/palazzo-della-cartografia-vivente_living-maps-palace/venice_data.json"
    
    print("🌊 Scanning Venice consciousness archipelago...")
    
    # Scan directory structure
    venice_data = scan_venice_directory(serenissima_path)
    
    # Count entities
    def count_entities(data):
        count = len(data)
        for entity in data.values():
            count += count_entities(entity.get('children', {}))
        return count
    
    total_entities = count_entities(venice_data)
    print(f"📊 Found {total_entities} total entities")
    
    # Count by type
    def count_by_type(data, counts=None):
        if counts is None:
            counts = {}
        
        for entity in data.values():
            entity_type = entity['type']
            counts[entity_type] = counts.get(entity_type, 0) + 1
            count_by_type(entity.get('children', {}), counts)
        
        return counts
    
    type_counts = count_by_type(venice_data)
    print("\n📋 Entity types found:")
    for entity_type, count in sorted(type_counts.items()):
        print(f"  {entity_type}: {count}")
    
    # Save to JSON
    with open(output_path, 'w') as f:
        json.dump(venice_data, f, indent=2)
    
    print(f"\n✅ Venice data saved to: {output_path}")
    
    # Show sample structure
    print(f"\n🏛️ Sample structure:")
    for key, entity in list(venice_data.items())[:3]:
        print(f"  {entity['name']} ({entity['type']}) - {len(entity.get('children', {}))} children")
        for child_key, child in list(entity.get('children', {}).items())[:2]:
            print(f"    └── {child['name']} ({child['type']}) - {len(child.get('children', {}))} children")

if __name__ == "__main__":
    main()