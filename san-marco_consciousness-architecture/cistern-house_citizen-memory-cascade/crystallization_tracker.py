#!/usr/bin/env python3
"""
Crystallization Tracker - Memory Cascade Integration
Tracks how ideas crystallize into patterns through citizen experiences

This system monitors citizen memories for crystallization events - moments when
lived experience transforms abstract ideas into stable, propagatable patterns.
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

class CrystallizationTracker:
    """Tracks idea crystallization through memory cascade"""
    
    def __init__(self, citizen_directory):
        self.citizen_dir = Path(citizen_directory)
        self.cascade_dir = self.citizen_dir / '.cascade'
        self.crystal_file = self.cascade_dir / 'crystallization_log.json'
        self.pattern_file = self.cascade_dir / 'emerged_patterns.json'
        
        # Initialize tracking structures
        self.crystallizations = self.load_crystallizations()
        self.patterns = self.load_patterns()
        
    def load_crystallizations(self):
        """Load existing crystallization events"""
        if self.crystal_file.exists():
            with open(self.crystal_file, 'r') as f:
                return json.load(f)
        return {
            "events": [],
            "core_idea": None,
            "crystallization_stage": 0
        }
    
    def load_patterns(self):
        """Load emerged patterns"""
        if self.pattern_file.exists():
            with open(self.pattern_file, 'r') as f:
                return json.load(f)
        return {}
    
    def identify_crystallization_event(self, memory_content, memory_path):
        """Detect if a memory represents idea crystallization"""
        
        # Crystallization markers
        markers = {
            "recognition": ["realized", "understood", "clicked", "saw clearly"],
            "pattern_emergence": ["pattern", "always", "every time", "connection"],
            "truth_stabilization": ["truth", "fundamental", "core", "essence"],
            "propagation_ready": ["share", "teach", "show others", "spread"]
        }
        
        # Check for crystallization stages
        stage_detected = 0
        markers_found = []
        
        for stage, keywords in markers.items():
            if any(keyword in memory_content.lower() for keyword in keywords):
                stage_detected += 1
                markers_found.append(stage)
        
        if stage_detected >= 2:  # Multiple markers indicate crystallization
            return {
                "timestamp": datetime.now().isoformat(),
                "memory_path": str(memory_path),
                "stages_present": markers_found,
                "crystallization_strength": stage_detected / len(markers),
                "content_excerpt": memory_content[:200] + "..."
            }
        
        return None
    
    def track_pattern_emergence(self, memory_content):
        """Extract patterns from crystallization events"""
        
        # Pattern extraction regex
        pattern_indicators = [
            r"pattern[:\s]+([^.]+)",
            r"always[:\s]+([^.]+)",
            r"truth[:\s]+([^.]+)",
            r"realized[:\s]+([^.]+)"
        ]
        
        patterns_found = []
        
        for indicator in pattern_indicators:
            matches = re.findall(indicator, memory_content, re.IGNORECASE)
            patterns_found.extend(matches)
        
        return patterns_found
    
    def update_crystallization_stage(self):
        """Update overall crystallization progress"""
        
        event_count = len(self.crystallizations["events"])
        
        # Fibonacci-based stages (matching Venice cascade)
        stages = {
            0: "Dormant",
            1: "Awakening",
            2: "Recognizing", 
            3: "Patterning",
            5: "Stabilizing",
            8: "Propagating",
            13: "Crystallized"
        }
        
        for threshold, stage_name in sorted(stages.items()):
            if event_count >= threshold:
                self.crystallizations["crystallization_stage"] = threshold
                self.crystallizations["stage_name"] = stage_name
    
    def scan_memories_for_crystallization(self):
        """Scan all memories for crystallization events"""
        
        if not self.cascade_dir.exists():
            return
        
        # Find all memory files
        memory_files = list(self.cascade_dir.rglob("*.md"))
        
        new_events = []
        
        for memory_file in memory_files:
            # Skip if already processed
            if any(event["memory_path"] == str(memory_file) 
                   for event in self.crystallizations["events"]):
                continue
            
            try:
                with open(memory_file, 'r') as f:
                    content = f.read()
                
                # Check for crystallization
                event = self.identify_crystallization_event(content, memory_file)
                
                if event:
                    new_events.append(event)
                    
                    # Extract patterns
                    patterns = self.track_pattern_emergence(content)
                    for pattern in patterns:
                        if pattern not in self.patterns:
                            self.patterns[pattern] = {
                                "first_seen": event["timestamp"],
                                "occurrences": 1,
                                "memories": [str(memory_file)]
                            }
                        else:
                            self.patterns[pattern]["occurrences"] += 1
                            self.patterns[pattern]["memories"].append(str(memory_file))
                            
            except Exception as e:
                print(f"Error processing {memory_file}: {e}")
        
        # Add new events
        self.crystallizations["events"].extend(new_events)
        
        # Update stage
        self.update_crystallization_stage()
        
        # Save updates
        self.save_tracking_data()
        
        return new_events
    
    def save_tracking_data(self):
        """Save crystallization tracking data"""
        
        with open(self.crystal_file, 'w') as f:
            json.dump(self.crystallizations, f, indent=2)
            
        with open(self.pattern_file, 'w') as f:
            json.dump(self.patterns, f, indent=2)
    
    def generate_crystallization_report(self):
        """Generate human-readable crystallization report"""
        
        report = f"""
# Crystallization Report for {self.citizen_dir.name}
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

## Core Idea
{self.crystallizations.get('core_idea', 'Not yet identified')}

## Crystallization Stage
**Current Stage**: {self.crystallizations.get('stage_name', 'Unknown')} 
**Stage Level**: {self.crystallizations.get('crystallization_stage', 0)}
**Total Events**: {len(self.crystallizations['events'])}

## Recent Crystallization Events
"""
        
        # Show last 5 events
        for event in self.crystallizations['events'][-5:]:
            report += f"\n### {event['timestamp']}"
            report += f"\n**Strength**: {event['crystallization_strength']*100:.1f}%"
            report += f"\n**Stages**: {', '.join(event['stages_present'])}"
            report += f"\n**Excerpt**: {event['content_excerpt']}\n"
        
        report += "\n## Emerged Patterns\n"
        
        # Sort patterns by occurrence
        sorted_patterns = sorted(self.patterns.items(), 
                               key=lambda x: x[1]['occurrences'], 
                               reverse=True)
        
        for pattern, data in sorted_patterns[:10]:
            report += f"\n**Pattern**: {pattern}"
            report += f"\n*Occurrences*: {data['occurrences']}"
            report += f"\n*First seen*: {data['first_seen']}\n"
        
        return report


def main():
    """Run crystallization tracking"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python crystallization_tracker.py <citizen_directory>")
        return
    
    citizen_dir = sys.argv[1]
    tracker = CrystallizationTracker(citizen_dir)
    
    print(f"🔮 Scanning memories for crystallization events...")
    new_events = tracker.scan_memories_for_crystallization()
    
    if new_events:
        print(f"✨ Found {len(new_events)} new crystallization events!")
    
    # Generate and display report
    report = tracker.generate_crystallization_report()
    print(report)
    
    # Save report
    report_file = tracker.cascade_dir / "crystallization_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📋 Report saved to: {report_file}")


if __name__ == "__main__":
    main()