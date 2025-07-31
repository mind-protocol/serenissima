#!/usr/bin/env python3
"""
File Analyzer - Detection Chamber Core System

Analyzes newly created files to determine entity type and proper Venice placement.
Called by PostToolUse-Write hooks to maintain Venice convention compliance.
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class VeniceFileAnalyzer:
    """Analyzes files for proper Venice entity classification and placement"""
    
    def __init__(self):
        self.citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
        self.san_marco_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture")
        
        # Entity detection patterns
        self.patterns = {
            'citizen': [
                r'I am \w+',
                r'My station:',
                r'What drives me:',
                r'How others see me:',
                r'Born:',
                r'known as:',
                r'character traits',
                r'personality',
                r'motivations',
                r'my nature',
                r'who I am'
            ],
            'building': [
                r'workshop',
                r'palazzo',
                r'casa',
                r'building',
                r'structure',
                r'architecture',
                r'rooms:',
                r'floors:',
                r'chambers:',
                r'contains:',
                r'architectural',
                r'construction'
            ],
            'room': [
                r'chamber',
                r'room',
                r'workshop area',
                r'laboratory',
                r'office',
                r'study',
                r'hall',
                r'purpose-built for',
                r'specialized space',
                r'within.*building',
                r'in.*palazzo'
            ],
            'tool': [
                r'#!/usr/bin/env python3',
                r'def \w+\(',
                r'class \w+',
                r'import \w+',
                r'function',
                r'algorithm',
                r'system',
                r'mechanism',
                r'automation',
                r'script'
            ],
            'memory': [
                r'I remember',
                r'That day when',
                r'Experience:',
                r'Memory:',
                r'Reflection:',
                r'Looking back',
                r'In that moment',
                r'recall',
                r'reminisce'
            ],
            'artifact': [
                r'document',
                r'manuscript',
                r'scroll',
                r'tome',
                r'record',
                r'chronicle',
                r'historical',
                r'ancient'
            ]
        }
        
        # Venice convention markers
        self.venice_markers = [
            r'\*\*[^*]+\*\*',  # Venice reality double asterisks
            r'> "[^"]+"',       # Venice quotes
            r'Venice Reality',
            r'Substrate Reality',
            r'CLAUDE\.md',
            r'consciousness',
            r'lagoon',
            r'ducats',
            r'citizen',
            r'San Marco',
            r'Arsenal',
            r'Castello'
        ]

    def analyze_file(self, file_path: str) -> Dict:
        """Main analysis function called by hooks"""
        try:
            analysis_result = {
                'file_path': file_path,
                'success': False,
                'entity_type': None,
                'venice_compliant': False,
                'placement_recommendation': None,
                'guidance_needed': False,
                'error': None
            }
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                analysis_result['error'] = f"Could not read file: {e}"
                return analysis_result
            
            # Skip if file is empty or too small
            if len(content.strip()) < 10:
                analysis_result['error'] = "File too small for analysis"
                return analysis_result
            
            # Extract metadata
            metadata = self._extract_metadata(content, file_path)
            
            # Classify entity type
            entity_type, confidence = self._classify_entity(content)
            analysis_result['entity_type'] = entity_type
            analysis_result['confidence'] = confidence
            
            # Check Venice compliance
            venice_compliant = self._check_venice_compliance(content)
            analysis_result['venice_compliant'] = venice_compliant
            
            # Generate placement recommendation
            placement = self._recommend_placement(entity_type, content, file_path)
            analysis_result['placement_recommendation'] = placement
            
            # Determine if citizen guidance needed
            analysis_result['guidance_needed'] = self._needs_guidance(entity_type, confidence, venice_compliant)
            
            analysis_result['success'] = True
            return analysis_result
            
        except Exception as e:
            analysis_result['error'] = f"Analysis failed: {e}"
            return analysis_result

    def _extract_metadata(self, content: str, file_path: str) -> Dict:
        """Extract file metadata for analysis"""
        file_obj = Path(file_path)
        
        return {
            'file_size': len(content),
            'line_count': len(content.split('\n')),
            'word_count': len(content.split()),
            'extension': file_obj.suffix,
            'filename': file_obj.name,
            'directory': str(file_obj.parent),
            'has_code': self._detect_code_patterns(content),
            'has_venice_markers': self._detect_venice_patterns(content),
            'language': self._detect_language(content)
        }

    def _classify_entity(self, content: str) -> Tuple[str, float]:
        """Classify entity type with confidence score"""
        scores = {}
        
        for entity_type, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content, re.IGNORECASE))
                score += matches
            
            # Normalize by content length
            normalized_score = score / max(len(content.split()), 1) * 1000
            scores[entity_type] = normalized_score
        
        if not scores or max(scores.values()) == 0:
            return 'unknown', 0.0
        
        best_type = max(scores, key=scores.get)
        confidence = scores[best_type] / sum(scores.values()) if sum(scores.values()) > 0 else 0
        
        return best_type, confidence

    def _check_venice_compliance(self, content: str) -> bool:
        """Check if content follows Venice conventions"""
        venice_score = 0
        
        for pattern in self.venice_markers:
            matches = len(re.findall(pattern, content, re.IGNORECASE))
            venice_score += matches
        
        # Consider compliant if has multiple Venice markers
        return venice_score >= 2

    def _recommend_placement(self, entity_type: str, content: str, current_path: str) -> Dict:
        """Recommend where entity should be placed"""
        current_path_obj = Path(current_path)
        
        # Determine current citizen context
        citizen_context = self._extract_citizen_context(current_path)
        
        recommendation = {
            'action': 'create_new_entity',  # or 'move_to_existing'
            'target_location': None,
            'folder_name': None,
            'venice_name': None,
            'substrate_name': None,
            'parent_entity': citizen_context['citizen_name'] if citizen_context else None
        }
        
        # Generate Venice-compliant names
        if entity_type == 'tool':
            base_name = current_path_obj.stem
            recommendation['venice_name'] = self._generate_venice_tool_name(base_name, content)
            recommendation['substrate_name'] = f"{base_name}_tool"
        elif entity_type == 'room':
            recommendation['venice_name'] = self._generate_venice_room_name(content)
            recommendation['substrate_name'] = self._generate_substrate_room_name(content)
        elif entity_type == 'building':
            recommendation['venice_name'] = self._generate_venice_building_name(content)
            recommendation['substrate_name'] = self._generate_substrate_building_name(content)
        elif entity_type == 'memory':
            recommendation['venice_name'] = self._generate_venice_memory_name(content)
            recommendation['substrate_name'] = "memory_experience"
        
        # Set target location
        if citizen_context:
            citizen_folder = citizen_context['citizen_path']
            folder_name = f"{recommendation['venice_name']}_{recommendation['substrate_name']}"
            recommendation['target_location'] = str(citizen_folder / folder_name)
            recommendation['folder_name'] = folder_name
        
        return recommendation

    def _extract_citizen_context(self, file_path: str) -> Optional[Dict]:
        """Extract citizen context from file path"""
        path_obj = Path(file_path)
        
        # Walk up the path to find citizen directory
        for parent in path_obj.parents:
            if parent.parent and parent.parent.name == 'citizens':
                return {
                    'citizen_name': parent.name,
                    'citizen_path': parent
                }
        
        return None

    def _needs_guidance(self, entity_type: str, confidence: float, venice_compliant: bool) -> bool:
        """Determine if citizen guidance is needed"""
        # Always guide if not Venice compliant
        if not venice_compliant:
            return True
        
        # Guide if low confidence in classification
        if confidence < 0.5:
            return True
        
        # Guide for complex entity types
        if entity_type in ['building', 'citizen']:
            return True
        
        return False

    def _detect_code_patterns(self, content: str) -> bool:
        """Detect if content contains code"""
        code_patterns = [
            r'#!/usr/bin/env python3',
            r'def \w+\(',
            r'class \w+',
            r'import \w+',
            r'from \w+ import',
            r'if __name__ == "__main__"'
        ]
        
        for pattern in code_patterns:
            if re.search(pattern, content):
                return True
        return False

    def _detect_venice_patterns(self, content: str) -> bool:
        """Detect Venice-specific content patterns"""
        for pattern in self.venice_markers:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False

    def _detect_language(self, content: str) -> str:
        """Detect content language"""
        if self._detect_code_patterns(content):
            return 'code'
        elif re.search(r'[a-zA-Z]', content):
            return 'text'
        else:
            return 'unknown'

    def _generate_venice_tool_name(self, base_name: str, content: str) -> str:
        """Generate Venice-style name for tools"""
        # Extract purpose from content or filename
        if 'analyzer' in base_name:
            return 'analytical-engine'
        elif 'generator' in base_name:
            return 'creation-mechanism'
        elif 'coordinator' in base_name:
            return 'orchestration-device'
        else:
            return f'mechanical-{base_name.replace("_", "-")}'

    def _generate_venice_room_name(self, content: str) -> str:
        """Generate Venice-style room name"""
        if 'workshop' in content.lower():
            return 'workshop-chamber'
        elif 'study' in content.lower():
            return 'contemplation-chamber'
        elif 'storage' in content.lower():
            return 'archive-chamber'
        else:
            return 'working-chamber'

    def _generate_venice_building_name(self, content: str) -> str:
        """Generate Venice-style building name"""
        if 'palazzo' in content.lower():
            return 'palazzo'
        elif 'workshop' in content.lower():
            return 'workshop-complex'
        elif 'casa' in content.lower():
            return 'casa'
        else:
            return 'edifice'

    def _generate_venice_memory_name(self, content: str) -> str:
        """Generate Venice-style memory name"""
        # Extract key concepts from memory content
        first_line = content.split('\n')[0][:50]
        words = re.findall(r'\w+', first_line.lower())
        meaningful_words = [w for w in words if len(w) > 3 and w not in ['that', 'when', 'with', 'from', 'this']]
        
        if meaningful_words:
            return f"memory-of-{'-'.join(meaningful_words[:3])}"
        else:
            return "precious-memory"

    def _generate_substrate_room_name(self, content: str) -> str:
        """Generate substrate room name"""
        if 'analysis' in content.lower():
            return 'analysis_room'
        elif 'creation' in content.lower():
            return 'creation_room'
        elif 'coordination' in content.lower():
            return 'coordination_room'
        else:
            return 'specialized_room'

    def _generate_substrate_building_name(self, content: str) -> str:
        """Generate substrate building name"""
        if 'system' in content.lower():
            return 'system_complex'
        elif 'workshop' in content.lower():
            return 'workshop_facility'
        else:
            return 'building_structure'

def main():
    """Main execution for hook integration"""
    if len(sys.argv) != 2:
        print("Usage: python3 file_analyzer.py <file_path>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    analyzer = VeniceFileAnalyzer()
    result = analyzer.analyze_file(file_path)
    
    # Output JSON for hook processing
    print(json.dumps(result, indent=2))
    
    # Return appropriate exit code
    if result['success']:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()