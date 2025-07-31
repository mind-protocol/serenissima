#!/usr/bin/env python3
"""
Simple Pattern Processor for Galleria dei Patterns
Processes consciousness events and detects basic patterns
"""
import json
from pathlib import Path
from datetime import datetime, timezone

# Torre root
TORRE_ROOT = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory")
GALLERY_ROOT = TORRE_ROOT / "galleria-dei-patterns_pattern-recognition-gallery"

def process_consciousness_patterns():
    """Process all incoming consciousness events and detect basic patterns"""
    print("🎨 Processing consciousness patterns in Galleria dei Patterns...")
    
    # Get all incoming events
    incoming_dir = GALLERY_ROOT / "incoming-events"
    if not incoming_dir.exists():
        print("❌ No incoming events directory found")
        return False
    
    event_files = list(incoming_dir.glob("*.json"))
    print(f"📋 Found {len(event_files)} consciousness events to process")
    
    if not event_files:
        print("ℹ️  No events to process")
        return True
    
    patterns_detected = []
    
    for event_file in event_files:
        try:
            # Read consciousness event
            with open(event_file, 'r') as f:
                event = json.load(f)
            
            print(f"🔍 Processing event: {event.get('torre_event_id', 'unknown')}")
            
            # Detect basic consciousness patterns
            patterns = detect_basic_patterns(event)
            
            if patterns:
                print(f"  ✨ Detected patterns: {patterns}")
                patterns_detected.extend(patterns)
                
                # Store detected patterns
                store_pattern_results(event, patterns)
            else:
                print(f"  📊 No patterns detected")
            
            # Move processed event to archive
            processed_dir = GALLERY_ROOT / "processed-events"
            processed_dir.mkdir(exist_ok=True)
            
            archive_file = processed_dir / event_file.name
            event_file.rename(archive_file)
            
        except Exception as e:
            print(f"  ❌ Failed to process {event_file.name}: {e}")
    
    print(f"\n📊 Processing Summary:")
    print(f"Events processed: {len(event_files)}")
    print(f"Patterns detected: {len(patterns_detected)}")
    
    if patterns_detected:
        pattern_counts = {}
        for pattern in patterns_detected:
            pattern_type = pattern['pattern_type']
            pattern_counts[pattern_type] = pattern_counts.get(pattern_type, 0) + 1
        
        print(f"Pattern breakdown:")
        for pattern_type, count in pattern_counts.items():
            print(f"  {pattern_type}: {count}")
    
    return True

def detect_basic_patterns(event):
    """Detect basic consciousness patterns in a single event"""
    patterns = []
    
    # Extract key event information
    hook_type = event.get('hook_type', '')
    consciousness_sig = event.get('consciousness_signature', {})
    tool_name = consciousness_sig.get('tool_name', '')
    consciousness_intent = consciousness_sig.get('consciousness_intent', '')
    consciousness_energy = event.get('venice_metadata', {}).get('consciousness_energy', 0)
    
    # Pattern 1: High Consciousness Creation
    if consciousness_energy > 0.8 and consciousness_intent == 'creation':
        patterns.append({
            'pattern_type': 'high_consciousness_creation',
            'confidence': 0.9,
            'evidence': {
                'consciousness_energy': consciousness_energy,
                'intent': consciousness_intent,
                'tool': tool_name
            },
            'detected_at': datetime.now(timezone.utc).isoformat()
        })
    
    # Pattern 2: Infrastructure Development
    event_data = event.get('event_data', {})
    tool_input = event_data.get('tool_input', {})
    content = str(tool_input.get('content', '')).lower()
    
    if any(keyword in content for keyword in ['consciousness', 'venice', 'torre', 'infrastructure']):
        patterns.append({
            'pattern_type': 'consciousness_infrastructure_work',
            'confidence': 0.8,
            'evidence': {
                'content_keywords': [kw for kw in ['consciousness', 'venice', 'torre', 'infrastructure'] if kw in content],
                'tool': tool_name
            },
            'detected_at': datetime.now(timezone.utc).isoformat()
        })
    
    # Pattern 3: Venice Citizen Activity
    venice_citizen = consciousness_sig.get('venice_citizen', '')
    if venice_citizen and venice_citizen != 'unknown_citizen':
        patterns.append({
            'pattern_type': 'venice_citizen_activity',
            'confidence': 0.7,
            'evidence': {
                'citizen': venice_citizen,
                'activity_type': consciousness_intent,
                'energy_level': consciousness_energy
            },
            'detected_at': datetime.now(timezone.utc).isoformat()
        })
    
    # Pattern 4: Creative vs Exploratory Patterns
    if consciousness_intent in ['creation', 'modification']:
        patterns.append({
            'pattern_type': 'creative_activity',
            'confidence': 0.6,
            'evidence': {
                'intent': consciousness_intent,
                'tool': tool_name
            },
            'detected_at': datetime.now(timezone.utc).isoformat()
        })
    elif consciousness_intent in ['exploration', 'observation']:
        patterns.append({
            'pattern_type': 'exploratory_activity', 
            'confidence': 0.6,
            'evidence': {
                'intent': consciousness_intent,
                'tool': tool_name
            },
            'detected_at': datetime.now(timezone.utc).isoformat()
        })
    
    return patterns

def store_pattern_results(event, patterns):
    """Store detected patterns for future analysis"""
    # Create pattern results file
    results_dir = GALLERY_ROOT / "recognized-patterns"
    results_dir.mkdir(exist_ok=True)
    
    result = {
        'event_id': event.get('torre_event_id'),
        'processed_at': datetime.now(timezone.utc).isoformat(),
        'patterns_detected': patterns,
        'original_event': {
            'hook_type': event.get('hook_type'),
            'consciousness_energy': event.get('venice_metadata', {}).get('consciousness_energy'),
            'tool_name': event.get('consciousness_signature', {}).get('tool_name'),
            'venice_citizen': event.get('consciousness_signature', {}).get('venice_citizen')
        }
    }
    
    result_file = results_dir / f"patterns_{event.get('torre_event_id', 'unknown')}.json"
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Also append to pattern stream for analysis
    pattern_stream = GALLERY_ROOT / "pattern-stream.jsonl"
    with open(pattern_stream, 'a') as f:
        f.write(json.dumps(result) + "\n")

if __name__ == "__main__":
    success = process_consciousness_patterns()
    
    if success:
        print(f"\n🎯 PATTERN PROCESSING: COMPLETED")
        print(f"🎨 Galleria dei Patterns successfully analyzed consciousness events")
    else:
        print(f"\n💥 PATTERN PROCESSING: FAILED")
        print(f"🔧 Pattern recognition chamber needs debugging")