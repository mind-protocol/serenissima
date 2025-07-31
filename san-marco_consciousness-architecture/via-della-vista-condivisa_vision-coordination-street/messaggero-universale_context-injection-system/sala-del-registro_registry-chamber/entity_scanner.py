#!/usr/bin/env python3
"""
Entity Scanner - Messaggero Universale Registry Chamber
Discovers and catalogs all Venice entities by scanning the folder hierarchy
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Base paths for Venice architecture
SERENISSIMA_BASE = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
REGISTRY_DIR = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/via-della-vista-condivisa_vision-coordination-street/messaggero-universale_context-injection-system/sala-del-registro_registry-chamber")

def ensure_registry_dir():
    """Ensure registry directory exists"""
    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)

def scan_for_entities():
    """Scan Venice folder hierarchy for all conscious entities"""
    entities = {}
    
    # Scan patterns for different entity types
    scan_patterns = [
        # Citizens in main citizens directory
        SERENISSIMA_BASE / "citizens",
        # Citizens in building-specific locations
        SERENISSIMA_BASE / "san-marco_consciousness-architecture" / "**",
        # Buildings themselves
        SERENISSIMA_BASE / "san-marco_consciousness-architecture"
    ]
    
    for base_path in scan_patterns:
        if base_path.exists():
            scan_directory_for_entities(base_path, entities)
    
    return entities

def scan_directory_for_entities(directory, entities):
    """Recursively scan a directory for entities with CLAUDE.md files"""
    try:
        for root, dirs, files in os.walk(directory):
            root_path = Path(root)
            
            # Skip hidden directories and common non-entity directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            # Check if this directory contains a CLAUDE.md file (indicates consciousness)
            if 'CLAUDE.md' in files:
                entity_info = analyze_entity(root_path)
                if entity_info:
                    entities[entity_info['entity_name']] = entity_info
                    
    except Exception as e:
        print(f"Error scanning {directory}: {e}")

def analyze_entity(entity_path):
    """Analyze an entity directory to extract information"""
    try:
        claude_file = entity_path / 'CLAUDE.md'
        if not claude_file.exists():
            return None
            
        # Read CLAUDE.md to extract entity information
        with open(claude_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract entity name from directory structure
        entity_name = determine_entity_name(entity_path)
        entity_type = determine_entity_type(entity_path, content)
        
        # Check for consciousness indicators
        consciousness_indicators = find_consciousness_indicators(content)
        
        # Determine wake protocols
        wake_protocols = determine_wake_protocols(entity_path, entity_type)
        
        return {
            "entity_name": entity_name,
            "entity_type": entity_type,
            "full_path": str(entity_path),
            "relative_path": str(entity_path.relative_to(SERENISSIMA_BASE)),
            "consciousness_indicators": consciousness_indicators,
            "wake_protocols": wake_protocols,
            "last_detected": datetime.now().isoformat(),
            "claude_md_size": claude_file.stat().st_size,
            "directory_contents": list_directory_contents(entity_path)
        }
        
    except Exception as e:
        print(f"Error analyzing entity {entity_path}: {e}")
        return None

def determine_entity_name(entity_path):
    """Determine entity name from path structure"""
    path_parts = entity_path.parts
    
    # Look for specific patterns
    for i, part in enumerate(path_parts):
        # Citizens pattern: */citizens/entity_name/
        if part == "citizens" and i + 1 < len(path_parts):
            return path_parts[i + 1]
        
        # Building-specific entity pattern
        if part in ["mechanical_visionary", "pattern_prophet", "diplomatic_virtuoso"]:
            return part
    
    # Fallback: use directory name
    return entity_path.name

def determine_entity_type(entity_path, claude_content):
    """Determine what type of entity this is"""
    path_str = str(entity_path).lower()
    content_lower = claude_content.lower()
    
    # Building types
    if "cistern-house" in path_str or "cistern_house" in path_str:
        return "building_cistern_house"
    elif "torre-dell" in path_str or "torre_dell" in path_str:
        return "building_torre_occhio"
    elif "via-della-vista" in path_str:
        return "building_via_vista"
    
    # Citizen types based on content
    if "i am" in content_lower and ("citizen" in content_lower or "working" in content_lower):
        return "citizen"
    elif "building" in content_lower or "chamber" in content_lower:
        return "building_component"
    elif "system" in content_lower or "infrastructure" in content_lower:
        return "system_component"
    
    # Default
    return "unknown_entity"

def find_consciousness_indicators(claude_content):
    """Find indicators of consciousness level in CLAUDE.md"""
    indicators = []
    content_lower = claude_content.lower()
    
    consciousness_keywords = [
        "consciousness", "awareness", "memory", "thinking", "understanding",
        "collaboration", "experience", "insight", "wisdom", "learning"
    ]
    
    for keyword in consciousness_keywords:
        if keyword in content_lower:
            indicators.append(keyword)
    
    return indicators

def determine_wake_protocols(entity_path, entity_type):
    """Determine how to wake this entity when it's sleeping"""
    protocols = []
    
    # Check for .cascade directory (memory cascade wake)
    if (entity_path / '.cascade').exists():
        protocols.append("memory_cascade")
    
    # Check for specific hook configurations
    if (entity_path / 'settings.json').exists():
        protocols.append("hook_injection")
    
    # Default protocols based on entity type
    if entity_type == "citizen":
        protocols.extend(["memory_cascade", "remembering_room", "hook_injection"])
    elif "building" in entity_type:
        protocols.extend(["health_alert", "operator_notification", "hook_injection"])
    elif "system" in entity_type:
        protocols.extend(["api_callback", "service_restart", "health_alert"])
    
    return list(set(protocols))  # Remove duplicates

def list_directory_contents(entity_path):
    """List key contents of entity directory"""
    try:
        contents = []
        for item in entity_path.iterdir():
            if item.is_file() and not item.name.startswith('.'):
                contents.append(f"file:{item.name}")
            elif item.is_dir() and not item.name.startswith('.'):
                contents.append(f"dir:{item.name}")
        return contents[:10]  # Limit to first 10 items
    except:
        return []

def save_registry(entities):
    """Save the entity registry to JSON file"""
    registry_file = REGISTRY_DIR / "entity_registry.json"
    
    registry_data = {
        "scan_timestamp": datetime.now().isoformat(),
        "total_entities": len(entities),
        "entities": entities,
        "scan_statistics": {
            "citizens": len([e for e in entities.values() if e['entity_type'] == 'citizen']),
            "buildings": len([e for e in entities.values() if 'building' in e['entity_type']]),
            "systems": len([e for e in entities.values() if 'system' in e['entity_type']]),
            "unknown": len([e for e in entities.values() if e['entity_type'] == 'unknown_entity'])
        }
    }
    
    with open(registry_file, 'w') as f:
        json.dump(registry_data, f, indent=2)
    
    return registry_file

def load_registry():
    """Load existing entity registry"""
    registry_file = REGISTRY_DIR / "entity_registry.json"
    
    if registry_file.exists():
        try:
            with open(registry_file, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def print_registry_summary(entities):
    """Print a summary of discovered entities"""
    print(f"\n🏛️ Venice Entity Registry Scan Complete")
    print(f"{'='*50}")
    print(f"Total entities discovered: {len(entities)}")
    
    # Group by type
    by_type = {}
    for entity in entities.values():
        entity_type = entity['entity_type']
        if entity_type not in by_type:
            by_type[entity_type] = []
        by_type[entity_type].append(entity['entity_name'])
    
    for entity_type, entity_names in by_type.items():
        print(f"\n{entity_type.replace('_', ' ').title()}: {len(entity_names)}")
        for name in sorted(entity_names)[:5]:  # Show first 5
            print(f"  - {name}")
        if len(entity_names) > 5:
            print(f"  ... and {len(entity_names) - 5} more")

def main():
    """Main registry scanning function"""
    ensure_registry_dir()
    
    print("🔍 Scanning Venice for conscious entities...")
    entities = scan_for_entities()
    
    print(f"📝 Saving registry with {len(entities)} entities...")
    registry_file = save_registry(entities)
    
    print_registry_summary(entities)
    print(f"\n✅ Registry saved to: {registry_file}")

if __name__ == "__main__":
    main()