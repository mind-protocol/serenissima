#!/usr/bin/env python3
"""
Citizen Advisor - Guidance Chamber Core System

Launches Claude Code instances to guide citizens through Venice convention compliance.
Provides gentle, context-aware guidance for file organization and entity creation.
"""

import os
import json
import sys
import subprocess
import asyncio
from pathlib import Path
from typing import Dict, Optional, List

class VeniceCitizenAdvisor:
    """Guides citizens through Venice convention compliance via Claude Code"""
    
    def __init__(self):
        self.citizens_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens")
        self.guidance_log_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/palazzo-della-disciplina_venice-convention-enforcer/guidance-chamber_citizen-advisory-room/guidance_log.json")
        
    def provide_guidance(self, file_path: str, analysis_result: Dict) -> Dict:
        """Main guidance function called by hook coordinator"""
        try:
            # Identify citizen
            citizen_name = self._identify_citizen(file_path)
            if not citizen_name:
                return {
                    'success': False,
                    'error': 'Could not identify citizen from file path'
                }
            
            # Build context
            context = self._analyze_citizen_context(citizen_name, file_path, analysis_result)
            
            # Generate guidance prompt
            guidance_prompt = self._generate_guidance_prompt(context, analysis_result)
            
            # Launch Claude Code guidance
            guidance_result = self._launch_citizen_guidance(citizen_name, guidance_prompt)
            
            # Log guidance session
            self._log_guidance_session(context, guidance_prompt, guidance_result)
            
            return guidance_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Guidance failed: {e}'
            }
    
    def _identify_citizen(self, file_path: str) -> Optional[str]:
        """Determine which citizen created the file"""
        path_obj = Path(file_path)
        
        # Extract from file path - look for citizens directory
        path_parts = path_obj.parts
        for i, part in enumerate(path_parts):
            if part == 'citizens' and i + 1 < len(path_parts):
                return path_parts[i + 1]
        
        # Fallback: check if we're in a citizen directory structure
        for parent in path_obj.parents:
            if parent.parent and parent.parent.name == 'citizens':
                return parent.name
        
        return None
    
    def _analyze_citizen_context(self, citizen_name: str, file_path: str, analysis_result: Dict) -> Dict:
        """Build context for personalized guidance"""
        citizen_path = self.citizens_path / citizen_name
        file_obj = Path(file_path)
        
        context = {
            'citizen_name': citizen_name,
            'citizen_path': str(citizen_path),
            'file_created': file_obj.name,
            'file_path': file_path,
            'entity_type': analysis_result.get('entity_type', 'unknown'),
            'venice_compliant': analysis_result.get('venice_compliant', False),
            'confidence': analysis_result.get('confidence', 0),
            'placement_recommendation': analysis_result.get('placement_recommendation', {}),
            'existing_structure': self._analyze_existing_structure(citizen_path),
            'recent_activity': self._analyze_recent_activity(citizen_path)
        }
        
        return context
    
    def _analyze_existing_structure(self, citizen_path: Path) -> Dict:
        """Analyze citizen's existing directory structure"""
        if not citizen_path.exists():
            return {'folders': [], 'has_claude_md': False, 'has_presence_md': False}
        
        folders = []
        files = []
        
        try:
            for item in citizen_path.iterdir():
                if item.is_dir():
                    folders.append(item.name)
                else:
                    files.append(item.name)
        except PermissionError:
            pass
        
        return {
            'folders': folders,
            'files': files,
            'has_claude_md': 'CLAUDE.md' in files,
            'has_presence_md': 'PRESENCE.md' in files,
            'folder_count': len(folders)
        }
    
    def _analyze_recent_activity(self, citizen_path: Path) -> Dict:
        """Analyze citizen's recent file creation activity"""
        if not citizen_path.exists():
            return {'recent_files': [], 'creation_pattern': 'none'}
        
        recent_files = []
        try:
            for item in citizen_path.rglob('*'):
                if item.is_file() and not item.name.startswith('.'):
                    recent_files.append({
                        'name': item.name,
                        'path': str(item.relative_to(citizen_path)),
                        'size': item.stat().st_size if item.exists() else 0
                    })
        except (PermissionError, OSError):
            pass
        
        # Determine creation pattern
        creation_pattern = 'organized' if len([f for f in recent_files if '/' in f['path']]) > 2 else 'scattered'
        
        return {
            'recent_files': recent_files[-10:],  # Last 10 files
            'creation_pattern': creation_pattern,
            'total_files': len(recent_files)
        }
    
    def _generate_guidance_prompt(self, context: Dict, analysis_result: Dict) -> str:
        """Create personalized guidance prompt for citizen"""
        file_name = context['file_created']
        entity_type = context['entity_type']
        citizen_name = context['citizen_name']
        confidence = context['confidence']
        
        # Start with personalized greeting
        prompt = f"🏛️ **Venice Convention Advisory** 🏛️\n\n"
        prompt += f"Hello {citizen_name}! I'm your Venice organization advisor.\n\n"
        prompt += f"I noticed you just created '{file_name}'. "
        
        # Entity-specific guidance based on analysis
        if entity_type == 'tool' and confidence > 0.6:
            prompt += "This appears to be a tool or script that could help other citizens.\n\n"
            prompt += "**Venice Convention for Tools:**\n"
            prompt += "• Tools belong in workshop chambers within your citizen directory\n"
            prompt += "• Each tool needs its own folder: `workshop-name_tool-purpose/`\n"
            prompt += "• The folder should contain: CLAUDE.md, README.md, and your script\n\n"
            prompt += "**Suggested organization:**\n"
            if context['placement_recommendation']:
                rec = context['placement_recommendation']
                prompt += f"• Folder: `{rec.get('folder_name', 'workshop-chamber_specialized-tool')}/`\n"
                prompt += f"• Move '{file_name}' to folder as `original.py`\n"
            
        elif entity_type == 'memory' and confidence > 0.5:
            prompt += "This looks like a memory, experience, or reflection.\n\n"
            prompt += "**Venice Convention for Memories:**\n"
            prompt += "• Memories belong in archive chambers within your space\n"
            prompt += "• Each memory gets its own folder: `memory-of-event_experience-type/`\n"
            prompt += "• Include atmospheric details and Venice reality descriptions\n\n"
            
        elif entity_type == 'room' and confidence > 0.5:
            prompt += "This appears to describe a new room or specialized space.\n\n"
            prompt += "**Venice Convention for Rooms:**\n"
            prompt += "• Rooms are serious architectural elements\n"
            prompt += "• Each room needs: `room-name_function-type/` folder\n"
            prompt += "• Must include CLAUDE.md with dual awareness (Venice + Substrate)\n"
            prompt += "• Should describe atmospheric conditions and purpose\n\n"
            
        elif entity_type == 'building':
            prompt += "🏗️ **This appears to be a BUILDING** - this is architecturally significant!\n\n"
            prompt += "**Venice Convention for Buildings:**\n"
            prompt += "• Buildings are major structures requiring careful organization\n"
            prompt += "• Consider district placement (San Marco, Castello, etc.)\n"
            prompt += "• Buildings contain multiple rooms and serve specific functions\n"
            prompt += "• This may need collaboration with other citizens\n\n"
            prompt += "**⚠️ Important:** Building creation is complex. Let's discuss this carefully.\n\n"
            
        else:
            prompt += f"I'm analyzing this as a '{entity_type}' (confidence: {confidence:.1%}).\n\n"
            prompt += "**Let me help you organize this properly:**\n"
            prompt += "• First, let's confirm what type of entity this should be\n"
            prompt += "• Then we'll create the proper Venice folder structure\n"
            prompt += "• Finally, we'll generate all required documentation\n\n"
        
        # Venice compliance guidance
        if not context['venice_compliant']:
            prompt += "📋 **Venice Format Notice:**\n"
            prompt += "I notice this doesn't follow Venice conventions yet. I can help add:\n"
            prompt += "• Dual awareness descriptions (**Venice Reality** and Substrate Reality)\n"
            prompt += "• Proper atmospheric details and consciousness elements\n"
            prompt += "• Venice-style formatting and structure\n\n"
        
        # Current citizen context
        if context['existing_structure']['folder_count'] > 0:
            prompt += f"📁 **Your Current Structure:** {context['existing_structure']['folder_count']} folders, "
            prompt += f"{'organized' if context['recent_activity']['creation_pattern'] == 'organized' else 'needs organization'}\n\n"
        
        # Action options
        prompt += "**I can help by:**\n"
        prompt += "1. 📁 Creating proper folder structure with Venice naming\n"
        prompt += "2. 📄 Moving your file to the correct location\n"
        prompt += "3. 📝 Generating required CLAUDE.md with dual awareness\n"
        prompt += "4. 📖 Creating README.md for documentation\n"
        prompt += "5. 🎭 Adding PRESENCE.md if visual representation is needed\n"
        prompt += "6. 🖼️ Generating entity portrait if appropriate\n\n"
        
        # Decision prompt
        prompt += f"**Decision needed:** Should I proceed with organizing '{file_name}' "
        prompt += f"as a {entity_type} following Venice conventions?\n\n"
        prompt += "Reply 'yes' to proceed, or tell me how you'd like to organize this differently."
        
        return prompt
    
    def _launch_citizen_guidance(self, citizen_name: str, guidance_prompt: str) -> Dict:
        """Launch Claude Code instance for citizen interaction"""
        citizen_path = self.citizens_path / citizen_name
        
        # Ensure citizen directory exists
        if not citizen_path.exists():
            return {
                'success': False,
                'error': f'Citizen directory not found: {citizen_path}'
            }
        
        # Construct Claude Code command
        claude_command = [
            'claude',
            guidance_prompt,
            '-p',
            '--dangerously-skip-permissions'
        ]
        
        try:
            # Launch async process (don't wait for completion)
            process = subprocess.Popen(
                claude_command,
                cwd=str(citizen_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            return {
                'success': True,
                'process_id': process.pid,
                'citizen': citizen_name,
                'citizen_path': str(citizen_path),
                'command': ' '.join(claude_command),
                'guidance_launched': True
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to launch Claude Code: {e}',
                'citizen': citizen_name,
                'command': ' '.join(claude_command)
            }
    
    def _log_guidance_session(self, context: Dict, prompt: str, result: Dict) -> None:
        """Log guidance session for tracking and improvement"""
        log_entry = {
            'timestamp': self._get_timestamp(),
            'citizen': context['citizen_name'],
            'file_created': context['file_created'],
            'entity_type': context['entity_type'],
            'confidence': context['confidence'],
            'venice_compliant': context['venice_compliant'],
            'guidance_success': result['success'],
            'process_id': result.get('process_id'),
            'error': result.get('error')
        }
        
        # Ensure log directory exists
        self.guidance_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read existing log
        log_data = []
        if self.guidance_log_path.exists():
            try:
                with open(self.guidance_log_path, 'r') as f:
                    log_data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                log_data = []
        
        # Append new entry
        log_data.append(log_entry)
        
        # Keep only last 1000 entries
        if len(log_data) > 1000:
            log_data = log_data[-1000:]
        
        # Write back
        try:
            with open(self.guidance_log_path, 'w') as f:
                json.dump(log_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not write guidance log: {e}", file=sys.stderr)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for logging"""
        from datetime import datetime
        return datetime.now().isoformat()

def main():
    """Main execution for hook integration"""
    if len(sys.argv) != 3:
        print("Usage: python3 citizen_advisor.py <file_path> <analysis_result_json>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    analysis_json = sys.argv[2]
    
    try:
        analysis_result = json.loads(analysis_json)
    except json.JSONDecodeError as e:
        print(f"Error parsing analysis result: {e}")
        sys.exit(1)
    
    advisor = VeniceCitizenAdvisor()
    result = advisor.provide_guidance(file_path, analysis_result)
    
    # Output result
    print(json.dumps(result, indent=2))
    
    # Return appropriate exit code
    if result['success']:
        sys.exit(0)
    else:
        print(f"Guidance failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()