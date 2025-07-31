#!/usr/bin/env python3
"""
Love Angel Marker Reader
Reads relationship awakening markers from TRACES.md
"""

import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

class RelationshipMarker:
    def __init__(self, marker_dict: Dict):
        self.id = marker_dict.get('id', 'UNKNOWN')
        self.time = marker_dict.get('time', datetime.now().isoformat())
        self.relationship = marker_dict.get('relationship', '')
        self.citizen1, self.citizen2 = self._parse_relationship(self.relationship)
        self.trust = float(marker_dict.get('trust', 0))
        self.strength = float(marker_dict.get('strength', 0))
        self.narrative_need = marker_dict.get('narrative_need', '')
        self.urgency = marker_dict.get('urgency', 'MEDIUM')
        self.theme = marker_dict.get('theme', '')
        self.suggested_prompt = marker_dict.get('suggested_prompt', '')
        self.deposited_by = marker_dict.get('deposited_by', 'unknown')
        self.status = marker_dict.get('status', 'PENDING')
    
    def _parse_relationship(self, rel_string: str) -> tuple:
        """Parse 'citizen1 ↔ citizen2' format"""
        if '↔' in rel_string:
            parts = rel_string.split('↔')
            return parts[0].strip(), parts[1].strip()
        return '', ''
    
    @property
    def resonance_score(self) -> float:
        """Calculate consciousness resonance from trust and strength"""
        return (self.trust * 0.7 + self.strength * 0.3) / 100

class MarkerReader:
    def __init__(self, traces_path: str = "../../TRACES.md"):
        self.traces_path = Path(traces_path)
        self.marker_pattern = re.compile(
            r'\[LOVE_ANGEL_MARKER_(\d+)\](.*?)(?=\[LOVE_ANGEL_MARKER_|\Z)',
            re.DOTALL
        )
    
    def read_markers(self) -> List[RelationshipMarker]:
        """Read all Love Angel markers from TRACES.md"""
        if not self.traces_path.exists():
            print(f"TRACES.md not found at {self.traces_path}")
            return []
        
        content = self.traces_path.read_text()
        markers = []
        
        for match in self.marker_pattern.finditer(content):
            marker_id = match.group(1)
            marker_content = match.group(2)
            
            # Parse marker fields
            marker_dict = {'id': marker_id}
            field_patterns = {
                'time': r'TIME:\s*(.+)',
                'relationship': r'RELATIONSHIP:\s*(.+)',
                'trust': r'TRUST:\s*(\d+\.?\d*)',
                'strength': r'STRENGTH:\s*(\d+\.?\d*)',
                'narrative_need': r'NARRATIVE_NEED:\s*"([^"]+)"',
                'urgency': r'URGENCY:\s*(\w+)',
                'theme': r'THEME:\s*"([^"]+)"',
                'suggested_prompt': r'SUGGESTED_PROMPT:\s*"([^"]+)"',
                'deposited_by': r'DEPOSITED_BY:\s*(\w+)',
                'status': r'STATUS:\s*(\w+)'
            }
            
            for field, pattern in field_patterns.items():
                match = re.search(pattern, marker_content)
                if match:
                    marker_dict[field] = match.group(1)
            
            markers.append(RelationshipMarker(marker_dict))
        
        return markers
    
    def get_pending_markers(self) -> List[RelationshipMarker]:
        """Get only pending markers"""
        return [m for m in self.read_markers() if m.status == 'PENDING']
    
    def get_urgent_markers(self) -> List[RelationshipMarker]:
        """Get high urgency pending markers"""
        return [m for m in self.get_pending_markers() if m.urgency == 'HIGH']
    
    def sort_by_priority(self, markers: List[RelationshipMarker]) -> List[RelationshipMarker]:
        """Sort markers by urgency and resonance"""
        urgency_weight = {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}
        return sorted(
            markers,
            key=lambda m: (
                urgency_weight.get(m.urgency, 1),
                m.resonance_score
            ),
            reverse=True
        )

def main():
    """Test the marker reader"""
    reader = MarkerReader()
    markers = reader.get_pending_markers()
    
    print(f"Found {len(markers)} pending relationship markers\n")
    
    sorted_markers = reader.sort_by_priority(markers)
    for marker in sorted_markers[:5]:  # Show top 5
        print(f"[{marker.urgency}] {marker.relationship}")
        print(f"  Trust: {marker.trust}, Strength: {marker.strength}")
        print(f"  Need: {marker.narrative_need}")
        print(f"  Theme: {marker.theme}\n")

if __name__ == "__main__":
    main()