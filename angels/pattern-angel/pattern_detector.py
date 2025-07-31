#!/usr/bin/env python3
"""
Simple Pattern Detector for Venice
Scans messages, files, and conversation logs for pattern usage
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

# Configuration
API_BASE_URL = os.environ.get('VENICE_API_URL', 'http://localhost:3000/api')
OUTPUT_PATH = '/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/pattern_angel/detected_patterns.json'
SERENISSIMA_PATH = '/mnt/c/Users/reyno/universe-engine/serenissima'
CLAUDE_PROJECTS_PATH = os.path.expanduser('~/.claude/projects')

# Pattern cache - will be populated from API
PATTERN_CACHE = {}

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
        # Fallback patterns for development
        PATTERN_CACHE = {
            '#1': {'name': 'tide', 'emoji': '🌊', 'id': '#1'},
            '#2': {'name': 'bridge', 'emoji': '🌉', 'id': '#2'},
            '#3': {'name': 'cascade', 'emoji': '💫', 'id': '#3'},
            '#18': {'name': 'proof-weave', 'emoji': '🕸️', 'id': '#18'},
            '#19': {'name': 'urgency-cascade', 'emoji': '🚨', 'id': '#19'},
            # Reverse lookups
            'tide': '#1', 'bridge': '#2', 'cascade': '#3',
            '🌊': '#1', '🌉': '#2', '💫': '#3', '🕸️': '#18', '🚨': '#19'
        }
        return False

def detect_patterns_in_text(text: str, source: str = "unknown") -> List[Dict]:
    """Detect pattern references in a text string"""
    found_patterns = []
    text_lower = text.lower()
    
    # Check for pattern IDs (#1, #2, etc.)
    pattern_id_matches = re.findall(r'#\d+', text)
    for match in pattern_id_matches:
        if match in PATTERN_CACHE and isinstance(PATTERN_CACHE[match], dict):
            found_patterns.append({
                'pattern_id': match,
                'pattern_name': PATTERN_CACHE[match]['name'],
                'pattern_emoji': PATTERN_CACHE[match]['emoji'],
                'match_type': 'id',
                'context': text[:100] + '...' if len(text) > 100 else text,
                'source': source
            })
    
    # Check for pattern names
    for key, value in PATTERN_CACHE.items():
        if isinstance(value, str) and key.replace('-', ' ') in text_lower:
            pattern_id = value
            if pattern_id in PATTERN_CACHE and isinstance(PATTERN_CACHE[pattern_id], dict):
                found_patterns.append({
                    'pattern_id': pattern_id,
                    'pattern_name': PATTERN_CACHE[pattern_id]['name'],
                    'pattern_emoji': PATTERN_CACHE[pattern_id]['emoji'],
                    'match_type': 'name',
                    'context': text[:100] + '...' if len(text) > 100 else text,
                    'source': source
                })
    
    # Check for emojis
    for char in text:
        if char in PATTERN_CACHE and isinstance(PATTERN_CACHE[char], str):
            pattern_id = PATTERN_CACHE[char]
            if pattern_id in PATTERN_CACHE and isinstance(PATTERN_CACHE[pattern_id], dict):
                found_patterns.append({
                    'pattern_id': pattern_id,
                    'pattern_name': PATTERN_CACHE[pattern_id]['name'],
                    'pattern_emoji': char,
                    'match_type': 'emoji',
                    'context': text[:100] + '...' if len(text) > 100 else text,
                    'source': source
                })
    
    # Deduplicate by pattern_id + source
    seen = set()
    unique_patterns = []
    for p in found_patterns:
        key = (p['pattern_id'], p['source'])
        if key not in seen:
            seen.add(key)
            unique_patterns.append(p)
    
    return unique_patterns

def scan_messages(hours: int = 24) -> List[Dict]:
    """Scan recent messages for pattern usage"""
    print("Scanning messages...")
    detected = []
    
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
                    patterns = detect_patterns_in_text(content, f"message:{sender}")
                    
                    for p in patterns:
                        p['timestamp'] = msg_time.isoformat()
                        p['citizen'] = sender
                        detected.append(p)
            except:
                pass
                
    except Exception as e:
        print(f"Error scanning messages: {e}")
    
    print(f"Found {len(detected)} pattern instances in messages")
    return detected

def scan_files(directory: str, max_files: int = 100) -> List[Dict]:
    """Scan files in a directory for pattern usage"""
    detected = []
    file_count = 0
    
    # Common text file extensions
    extensions = ['.md', '.txt', '.json', '.py', '.ts', '.js']
    
    for ext in extensions:
        if file_count >= max_files:
            break
            
        pattern = os.path.join(directory, '**', f'*{ext}')
        files = glob.glob(pattern, recursive=True)
        
        for filepath in files[:max_files - file_count]:
            try:
                # Skip large files
                if os.path.getsize(filepath) > 1_000_000:  # 1MB
                    continue
                    
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                relative_path = os.path.relpath(filepath, SERENISSIMA_PATH)
                patterns = detect_patterns_in_text(content, f"file:{relative_path}")
                
                for p in patterns:
                    p['timestamp'] = datetime.fromtimestamp(os.path.getmtime(filepath)).isoformat()
                    detected.append(p)
                    
                file_count += 1
                
            except Exception as e:
                pass
    
    return detected

def scan_claude_conversations() -> List[Dict]:
    """Scan Claude conversation logs for pattern usage"""
    print("Scanning Claude conversations...")
    detected = []
    
    # Pattern for Venice-related Claude projects
    venice_patterns = [
        '*serenissima-citizens-*',
        '*serenissima-conscious-*',
        '*serenissima-backend*',
        '*serenissima/*'
    ]
    
    for pattern in venice_patterns:
        project_dirs = glob.glob(os.path.join(CLAUDE_PROJECTS_PATH, pattern))
        
        for project_dir in project_dirs:
            # Extract citizen/entity name from path
            dir_name = os.path.basename(project_dir)
            entity_match = re.search(r'citizens-(\w+)', dir_name)
            entity_name = entity_match.group(1) if entity_match else 'unknown'
            
            # Look for recent .jsonl files
            jsonl_files = glob.glob(os.path.join(project_dir, '*.jsonl'))
            
            for jsonl_file in jsonl_files[-5:]:  # Last 5 conversation files
                try:
                    with open(jsonl_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                entry = json.loads(line)
                                
                                # Check assistant messages
                                if entry.get('type') == 'message' and entry.get('role') == 'assistant':
                                    content = entry.get('content', '')
                                    if isinstance(content, list):
                                        # Handle structured content
                                        text = ' '.join(str(item.get('text', '')) for item in content if isinstance(item, dict))
                                    else:
                                        text = str(content)
                                    
                                    patterns = detect_patterns_in_text(text, f"claude:{entity_name}")
                                    
                                    for p in patterns:
                                        p['timestamp'] = entry.get('created_at', datetime.now().isoformat())
                                        p['citizen'] = entity_name
                                        detected.append(p)
                                        
                            except:
                                pass
                                
                except Exception as e:
                    pass
    
    print(f"Found {len(detected)} pattern instances in Claude conversations")
    return detected

def aggregate_detections(all_detections: List[Dict]) -> Dict:
    """Aggregate pattern detections into summary statistics"""
    pattern_stats = defaultdict(lambda: {
        'count': 0,
        'sources': defaultdict(int),
        'citizens': defaultdict(int),
        'match_types': defaultdict(int),
        'recent_contexts': []
    })
    
    # Sort by timestamp (most recent first)
    all_detections.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    for detection in all_detections:
        pattern_id = detection['pattern_id']
        stats = pattern_stats[pattern_id]
        
        stats['count'] += 1
        stats['sources'][detection['source'].split(':')[0]] += 1
        stats['match_types'][detection['match_type']] += 1
        
        if 'citizen' in detection:
            stats['citizens'][detection['citizen']] += 1
        
        # Keep up to 5 recent contexts
        if len(stats['recent_contexts']) < 5:
            stats['recent_contexts'].append({
                'context': detection['context'],
                'source': detection['source'],
                'timestamp': detection.get('timestamp')
            })
    
    # Convert defaultdicts to regular dicts for JSON serialization
    result = {}
    for pattern_id, stats in pattern_stats.items():
        result[pattern_id] = {
            'pattern_id': pattern_id,
            'pattern_name': PATTERN_CACHE.get(pattern_id, {}).get('name', 'unknown'),
            'pattern_emoji': PATTERN_CACHE.get(pattern_id, {}).get('emoji', ''),
            'total_detections': stats['count'],
            'source_breakdown': dict(stats['sources']),
            'top_citizens': dict(sorted(stats['citizens'].items(), key=lambda x: x[1], reverse=True)[:10]),
            'match_type_breakdown': dict(stats['match_types']),
            'recent_contexts': stats['recent_contexts']
        }
    
    return result

def main():
    """Run the pattern detection scan"""
    print("=== Pattern Detection Scan Starting ===")
    start_time = time.time()
    
    # Load patterns first
    load_patterns()
    
    all_detections = []
    
    # 1. Scan messages
    message_detections = scan_messages(hours=24)
    all_detections.extend(message_detections)
    
    # 2. Scan recent files in key directories
    print("Scanning key Venice files...")
    key_dirs = [
        os.path.join(SERENISSIMA_PATH, 'citizens'),
        os.path.join(SERENISSIMA_PATH, 'backend'),
        os.path.join(SERENISSIMA_PATH, 'conscious-buildings'),
        os.path.join(SERENISSIMA_PATH, 'cascade')
    ]
    
    for directory in key_dirs:
        if os.path.exists(directory):
            file_detections = scan_files(directory, max_files=50)
            all_detections.extend(file_detections)
            print(f"Scanned {directory}: {len(file_detections)} detections")
    
    # 3. Scan Claude conversations
    conversation_detections = scan_claude_conversations()
    all_detections.extend(conversation_detections)
    
    # Aggregate results
    aggregated = aggregate_detections(all_detections)
    
    # Sort by total detections
    sorted_patterns = sorted(aggregated.values(), key=lambda x: x['total_detections'], reverse=True)
    
    # Create output
    output = {
        'scan_timestamp': datetime.now(timezone.utc).isoformat(),
        'scan_duration_seconds': round(time.time() - start_time, 2),
        'total_detections': len(all_detections),
        'unique_patterns_found': len(aggregated),
        'patterns': sorted_patterns,
        'top_patterns': [
            {
                'pattern': f"{p['pattern_emoji']} {p['pattern_id']} {p['pattern_name']}",
                'count': p['total_detections']
            }
            for p in sorted_patterns[:10]
        ]
    }
    
    # Save results
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Print summary
    print(f"\n=== Pattern Detection Complete ===")
    print(f"Scan duration: {output['scan_duration_seconds']}s")
    print(f"Total detections: {output['total_detections']}")
    print(f"Unique patterns: {output['unique_patterns_found']}")
    print(f"\nTop 10 Patterns:")
    for i, p in enumerate(output['top_patterns'], 1):
        print(f"{i}. {p['pattern']}: {p['count']} detections")
    
    print(f"\nResults saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    main()