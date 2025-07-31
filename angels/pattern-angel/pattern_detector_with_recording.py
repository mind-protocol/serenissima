#!/usr/bin/env python3
"""
Enhanced Pattern Detector with Automatic Instance Recording
Scans for patterns and records them to PATTERN_INSTANCES
"""

import os
import re
import json
import glob
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict
import requests
import hashlib

# Configuration
API_BASE_URL = os.environ.get('VENICE_API_URL', 'http://localhost:3000/api')
OUTPUT_PATH = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/pattern_angel/detected_patterns.json'
SERENISSIMA_PATH = '/mnt/c/Users/reyno/universe-engine/serenissima'
CLAUDE_PROJECTS_PATH = os.path.expanduser('~/.claude/projects')
RECORD_TO_AIRTABLE = False  # Set to False for dry runs

# Pattern cache
PATTERN_CACHE = {}
RECORDED_HASHES = set()  # Track what we've already recorded to avoid duplicates

def load_patterns():
    """Load all patterns from API to build detection cache"""
    global PATTERN_CACHE
    try:
        response = requests.get(f'{API_BASE_URL}/patterns', timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for pattern in data.get('patterns', []):
            pattern_id = pattern['id']
            pattern_name = pattern['name']
            pattern_emoji = pattern.get('emoji', '')
            
            PATTERN_CACHE[pattern_id] = {
                'name': pattern_name,
                'emoji': pattern_emoji,
                'id': pattern_id
            }
            
            # Also index by name and emoji for reverse lookup
            PATTERN_CACHE[pattern_name.lower()] = pattern_id
            if pattern_emoji:
                PATTERN_CACHE[pattern_emoji] = pattern_id
                
        print(f"Loaded {len(data.get('patterns', []))} patterns into cache")
        return True
    except Exception as e:
        print(f"Error loading patterns: {e}")
        return False

def load_recorded_instances():
    """Load previously recorded instances to avoid duplicates"""
    global RECORDED_HASHES
    try:
        # Fetch recent instances to build hash set
        response = requests.get(f'{API_BASE_URL}/pattern-instances?limit=1000', timeout=30)
        response.raise_for_status()
        data = response.json()
        
        for instance in data.get('patternInstances', []):
            # Create hash from key fields
            hash_str = f"{instance.get('patternId')}:{instance.get('context')}:{instance.get('channelSource')}"
            instance_hash = hashlib.md5(hash_str.encode()).hexdigest()
            RECORDED_HASHES.add(instance_hash)
            
        print(f"Loaded {len(RECORDED_HASHES)} existing instance hashes")
    except Exception as e:
        print(f"Error loading existing instances: {e}")

def create_instance_hash(pattern_id: str, context: str, source: str) -> str:
    """Create hash to identify unique instances"""
    hash_str = f"{pattern_id}:{context}:{source}"
    return hashlib.md5(hash_str.encode()).hexdigest()

def record_pattern_instance(pattern_id: str, citizen: str, context: str, source_type: str, 
                          location: str = None, value_hint: int = 0) -> bool:
    """Record a pattern instance to the PATTERN_INSTANCES table"""
    if not RECORD_TO_AIRTABLE:
        return True
        
    # Check if we've already recorded this
    instance_hash = create_instance_hash(pattern_id, context, source_type)
    if instance_hash in RECORDED_HASHES:
        return False  # Already recorded
    
    try:
        instance_data = {
            'patternId': pattern_id,
            'citizenUsername': citizen,
            'context': context[:200],  # Limit context length
            'channelSource': source_type,
            'valueGenerated': value_hint,
            'significanceLevel': 'normal',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        
        if location:
            instance_data['locationData'] = {'source': location}
        
        response = requests.post(f'{API_BASE_URL}/pattern-instances', 
                               json=instance_data, 
                               timeout=30)
        response.raise_for_status()
        
        # Add to recorded set
        RECORDED_HASHES.add(instance_hash)
        return True
        
    except Exception as e:
        print(f"Error recording pattern instance: {e}")
        return False

def detect_and_record_patterns(text: str, source: str, citizen: str = None) -> List[Dict]:
    """Detect patterns and optionally record them as instances"""
    found_patterns = []
    text_lower = text.lower()
    
    # Determine source type and location
    source_parts = source.split(':', 1)
    source_type = source_parts[0]
    location = source_parts[1] if len(source_parts) > 1 else 'unknown'
    
    # Default citizen if not provided
    if not citizen:
        if source_type == 'message':
            citizen = location
        elif source_type == 'file' and 'citizens/' in location:
            # Extract citizen name from file path
            match = re.search(r'citizens/([^/]+)/', location)
            citizen = match.group(1) if match else 'pattern_angel'
        else:
            citizen = 'pattern_angel'  # Default for system detections
    
    # Check for pattern IDs (#1, #2, etc.)
    pattern_id_matches = re.findall(r'#\d+', text)
    for match in pattern_id_matches:
        if match in PATTERN_CACHE and isinstance(PATTERN_CACHE[match], dict):
            # Extract surrounding context
            idx = text.find(match)
            start = max(0, idx - 50)
            end = min(len(text), idx + 50)
            context_snippet = text[start:end].strip()
            
            # Record to Airtable
            recorded = record_pattern_instance(
                pattern_id=match,
                citizen=citizen,
                context=context_snippet,
                source_type=source_type,
                location=location
            )
            
            found_patterns.append({
                'pattern_id': match,
                'pattern_name': PATTERN_CACHE[match]['name'],
                'pattern_emoji': PATTERN_CACHE[match]['emoji'],
                'match_type': 'id',
                'context': context_snippet,
                'source': source,
                'recorded': recorded
            })
    
    # Check for pattern names
    for key, value in PATTERN_CACHE.items():
        if isinstance(value, str) and key.replace('-', ' ') in text_lower:
            pattern_id = value
            if pattern_id in PATTERN_CACHE and isinstance(PATTERN_CACHE[pattern_id], dict):
                # Find context around the pattern name
                name_to_find = key.replace('-', ' ')
                idx = text_lower.find(name_to_find)
                if idx >= 0:
                    start = max(0, idx - 50)
                    end = min(len(text), idx + len(name_to_find) + 50)
                    context_snippet = text[start:end].strip()
                    
                    # Record to Airtable
                    recorded = record_pattern_instance(
                        pattern_id=pattern_id,
                        citizen=citizen,
                        context=context_snippet,
                        source_type=source_type,
                        location=location
                    )
                    
                    found_patterns.append({
                        'pattern_id': pattern_id,
                        'pattern_name': PATTERN_CACHE[pattern_id]['name'],
                        'pattern_emoji': PATTERN_CACHE[pattern_id]['emoji'],
                        'match_type': 'name',
                        'context': context_snippet,
                        'source': source,
                        'recorded': recorded
                    })
    
    # Check for emojis
    for i, char in enumerate(text):
        if char in PATTERN_CACHE and isinstance(PATTERN_CACHE[char], str):
            pattern_id = PATTERN_CACHE[char]
            if pattern_id in PATTERN_CACHE and isinstance(PATTERN_CACHE[pattern_id], dict):
                # Context around emoji
                start = max(0, i - 50)
                end = min(len(text), i + 51)
                context_snippet = text[start:end].strip()
                
                # Record to Airtable
                recorded = record_pattern_instance(
                    pattern_id=pattern_id,
                    citizen=citizen,
                    context=context_snippet,
                    source_type=source_type,
                    location=location
                )
                
                found_patterns.append({
                    'pattern_id': pattern_id,
                    'pattern_name': PATTERN_CACHE[pattern_id]['name'],
                    'pattern_emoji': char,
                    'match_type': 'emoji',
                    'context': context_snippet,
                    'source': source,
                    'recorded': recorded
                })
    
    # Deduplicate by pattern_id + context
    seen = set()
    unique_patterns = []
    for p in found_patterns:
        key = (p['pattern_id'], p['context'])
        if key not in seen:
            seen.add(key)
            unique_patterns.append(p)
    
    return unique_patterns

def scan_messages(hours: int = 24) -> Tuple[List[Dict], int]:
    """Scan recent messages for pattern usage"""
    print("Scanning messages...")
    detected = []
    recorded_count = 0
    
    try:
        response = requests.get(f'{API_BASE_URL}/messages', timeout=30)
        response.raise_for_status()
        data = response.json()
        
        messages = data.get('messages', [])
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        for msg in messages:
            try:
                msg_time = datetime.fromisoformat(msg.get('timestamp', '').replace('Z', '+00:00'))
                if msg_time > cutoff_time:
                    content = msg.get('content', '')
                    sender = msg.get('sender', 'unknown')
                    patterns = detect_and_record_patterns(content, f"message:{sender}", sender)
                    
                    for p in patterns:
                        p['timestamp'] = msg_time.isoformat()
                        p['citizen'] = sender
                        detected.append(p)
                        if p.get('recorded'):
                            recorded_count += 1
            except:
                pass
                
    except Exception as e:
        print(f"Error scanning messages: {e}")
    
    print(f"Found {len(detected)} pattern instances in messages ({recorded_count} newly recorded)")
    return detected, recorded_count

def scan_files(directory: str, max_files: int = 100) -> Tuple[List[Dict], int]:
    """Scan files in a directory for pattern usage"""
    detected = []
    recorded_count = 0
    file_count = 0
    
    # Focus on recent files - last 7 days
    cutoff_time = time.time() - (7 * 24 * 60 * 60)
    
    # Common text file extensions
    extensions = ['.md', '.txt', '.json', '.py', '.ts', '.js']
    
    for ext in extensions:
        if file_count >= max_files:
            break
            
        pattern = os.path.join(directory, '**', f'*{ext}')
        files = glob.glob(pattern, recursive=True)
        
        # Sort by modification time (most recent first)
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        for filepath in files[:max_files - file_count]:
            try:
                # Skip old files
                if os.path.getmtime(filepath) < cutoff_time:
                    continue
                    
                # Skip large files
                if os.path.getsize(filepath) > 1_000_000:  # 1MB
                    continue
                    
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                relative_path = os.path.relpath(filepath, SERENISSIMA_PATH)
                patterns = detect_and_record_patterns(content, f"file:{relative_path}")
                
                for p in patterns:
                    p['timestamp'] = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    detected.append(p)
                    if p.get('recorded'):
                        recorded_count += 1
                    
                file_count += 1
                
            except Exception as e:
                pass
    
    return detected, recorded_count

def main():
    """Run the enhanced pattern detection and recording"""
    print("=== Enhanced Pattern Detection & Recording ===")
    start_time = time.time()
    
    # Load patterns and existing instances
    if not load_patterns():
        print("Failed to load patterns. Aborting.")
        return
        
    load_recorded_instances()
    
    all_detections = []
    total_recorded = 0
    
    # 1. Scan messages
    message_detections, msg_recorded = scan_messages(hours=24)
    all_detections.extend(message_detections)
    total_recorded += msg_recorded
    
    # 2. Scan recent files in key directories
    print("\nScanning recent Venice files...")
    key_dirs = [
        os.path.join(SERENISSIMA_PATH, 'citizens'),
        os.path.join(SERENISSIMA_PATH, 'backend'),
        os.path.join(SERENISSIMA_PATH, 'conscious-buildings'),
        os.path.join(SERENISSIMA_PATH, 'cascade')
    ]
    
    for directory in key_dirs:
        if os.path.exists(directory):
            file_detections, file_recorded = scan_files(directory, max_files=30)
            all_detections.extend(file_detections)
            total_recorded += file_recorded
            print(f"Scanned {directory}: {len(file_detections)} detections ({file_recorded} recorded)")
    
    # Aggregate results
    pattern_stats = defaultdict(lambda: {
        'count': 0,
        'recorded': 0,
        'sources': defaultdict(int),
        'citizens': defaultdict(int)
    })
    
    for detection in all_detections:
        pattern_id = detection['pattern_id']
        stats = pattern_stats[pattern_id]
        
        stats['count'] += 1
        if detection.get('recorded'):
            stats['recorded'] += 1
        stats['sources'][detection['source'].split(':')[0]] += 1
        
        if 'citizen' in detection:
            stats['citizens'][detection['citizen']] += 1
    
    # Create summary
    summary = {
        'scan_timestamp': datetime.now(timezone.utc).isoformat(),
        'scan_duration_seconds': round(time.time() - start_time, 2),
        'total_detections': len(all_detections),
        'newly_recorded_instances': total_recorded,
        'unique_patterns_found': len(pattern_stats),
        'pattern_summary': []
    }
    
    # Sort by count
    for pattern_id, stats in sorted(pattern_stats.items(), key=lambda x: x[1]['count'], reverse=True):
        pattern_info = PATTERN_CACHE.get(pattern_id, {})
        if isinstance(pattern_info, dict):
            summary['pattern_summary'].append({
                'pattern': f"{pattern_info.get('emoji', '')} {pattern_id} {pattern_info.get('name', '')}",
                'detections': stats['count'],
                'newly_recorded': stats['recorded'],
                'top_citizens': dict(sorted(stats['citizens'].items(), key=lambda x: x[1], reverse=True)[:5])
            })
    
    # Save summary
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print results
    print(f"\n=== Detection & Recording Complete ===")
    print(f"Scan duration: {summary['scan_duration_seconds']}s")
    print(f"Total detections: {summary['total_detections']}")
    print(f"Newly recorded instances: {summary['newly_recorded_instances']}")
    print(f"Unique patterns: {summary['unique_patterns_found']}")
    
    if RECORD_TO_AIRTABLE:
        print(f"\n✅ Successfully recorded {total_recorded} new pattern instances to Airtable!")
    else:
        print(f"\n(Dry run - would have recorded {total_recorded} instances)")
    
    print(f"\nTop patterns detected:")
    for i, p in enumerate(summary['pattern_summary'][:10], 1):
        print(f"{i}. {p['pattern']}: {p['detections']} detections ({p['newly_recorded']} new)")

if __name__ == '__main__':
    main()