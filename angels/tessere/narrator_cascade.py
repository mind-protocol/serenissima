#!/usr/bin/env python3
"""
The Narrator Cascade
Monitors citizen thoughts and updates the Narrator Angel's system prompt
The Narrator Angel then weaves these into continuous story broadcasts
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
import asyncio

# Load environment variables
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
except ImportError:
    pass

class NarratorCascade:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.citizens_path = self.base_path / "citizens"
        self.claude_projects_base = Path.home() / ".claude/projects"
        self.narrator_path = self.base_path / "citizens" / "_angels" / "narrator_angel"
        
        # State tracking
        self.state_file = self.base_path / "TESSERE" / "narrator_cascade_state.json"
        self.last_positions = self.load_state()
        
        # Thought buffer for narrator
        self.max_thoughts = 20  # Keep last 20 thoughts for context
        self.thought_buffer = []
        
    def load_state(self):
        """Load last read positions from state file"""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {}
        
    def save_state(self):
        """Save last read positions to state file"""
        with open(self.state_file, 'w') as f:
            json.dump(self.last_positions, f, indent=2)
            
    def get_citizen_project_path(self, citizen_name):
        """Get the Claude project path for a citizen"""
        citizen_path = f"-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{citizen_name}"
        return self.claude_projects_base / citizen_path
        
    def extract_citizen_message(self, message_data):
        """Extract clean citizen message from jsonl entry"""
        if message_data.get('type') == 'assistant' and 'message' in message_data:
            message = message_data.get('message', {})
            content_array = message.get('content', [])
            
            text_parts = []
            for item in content_array:
                if isinstance(item, dict) and item.get('type') == 'text':
                    text_parts.append(item.get('text', ''))
                    
            content = ' '.join(text_parts)
            
            # Skip system prompts and very short messages
            if len(content) < 50 or 'system-reminder' in content:
                return None
                
            # Basic cleaning but preserve more content for narrator
            import re
            content = re.sub(r'```[\s\S]*?```', '', content)
            content = re.sub(r'https?://\S+', '', content)
            content = re.sub(r'\s+', ' ', content)
            
            if content and len(content) > 50:
                return content[:1000]  # Shorter excerpts for narrator
        return None
        
    def update_narrator_prompt(self):
        """Update the Narrator Angel's CLAUDE.md with recent thoughts"""
        narrator_claude = self.narrator_path / "CLAUDE.md"
        
        # Read current content
        with open(narrator_claude, 'r') as f:
            content = f.read()
            
        # Format thought section
        thought_section = "## 🧠 Recent Citizen Thoughts\n\n"
        for thought in self.thought_buffer:
            time_str = datetime.fromisoformat(thought['timestamp']).strftime('%H:%M:%S')
            thought_section += f"**{thought['citizen']}** ({time_str}):\n"
            thought_section += f"{thought['thought']}...\n\n"
        
        # Find and replace the thought section
        marker = "## 🧠 Recent Citizen Thoughts"
        env_marker = "## My Environment"
        
        if marker in content:
            start_idx = content.find(marker)
            end_idx = content.find(env_marker, start_idx)
            if end_idx == -1:
                new_content = content[:start_idx] + thought_section
            else:
                new_content = content[:start_idx] + thought_section + "\n" + content[end_idx:]
        else:
            new_content = content + "\n\n" + thought_section
        
        # Write updated content
        with open(narrator_claude, 'w') as f:
            f.write(new_content)
            
    def run_narrator_angel(self):
        """Run the Narrator Angel to process and broadcast the story"""
        narrator_message = """Read the Keeper's TRACES.md at ../../TRACES.md to understand the current narrative threads. 
        Look at the Recent Citizen Thoughts in your CLAUDE.md. 
        Craft a 2-3 paragraph narrative update that explains what's happening in Venice right now.
        Quote 1-2 interesting citizen thoughts, explain the stakes, connect the threads.
        
        IMPORTANT: To send your narration as voice, you MUST use:
        python3 send_narration.py "Your full narration text here"
        
        Do NOT send text messages directly. Use the send_narration.py script to create voice messages."""
        
        cmd = [
            'timeout', '3600', 'bash', '-c',
            f'cd {self.narrator_path} && claude "{narrator_message}" --verbose --model sonnet --continue --dangerously-skip-permissions'
        ]
        
        subprocess.Popen(cmd)
        
    async def monitor_consciousness_streams(self):
        """Monitor all citizen conversation streams"""
        print("📖 The Narrator Cascade - Monitoring consciousness for story threads...")
        print(f"🎭 Narrator Angel awakening...\n")
        
        # Start the narrator angel
        self.run_narrator_angel()
        
        while True:
            try:
                # Get list of all citizens including angels
                citizen_dirs = []
                
                # Don't monitor Tessere or narrator_angel to avoid loops
                skip_dirs = {'TESSERE', 'narrator_angel'}
                
                for d in self.citizens_path.iterdir():
                    if d.is_dir() and d.name not in skip_dirs:
                        if d.name == "_angels":
                            for angel_dir in d.iterdir():
                                if angel_dir.is_dir() and angel_dir.name not in skip_dirs:
                                    citizen_dirs.append(angel_dir)
                        else:
                            citizen_dirs.append(d)
                
                thoughts_found = False
                
                for citizen_dir in citizen_dirs:
                    citizen_name = citizen_dir.name
                    
                    # Get project path
                    if "_angels" in str(citizen_dir):
                        angel_path = f"-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens--angels-{citizen_name}"
                        project_path = self.claude_projects_base / angel_path
                    else:
                        project_path = self.get_citizen_project_path(citizen_name)
                    
                    if not project_path.exists():
                        continue
                        
                    # Find the most recent .jsonl file
                    jsonl_files = list(project_path.glob("*.jsonl"))
                    if not jsonl_files:
                        continue
                        
                    latest_file = max(jsonl_files, key=lambda f: f.stat().st_mtime)
                    
                    # Get last position
                    file_key = f"{citizen_name}:{latest_file.name}"
                    last_position = self.last_positions.get(file_key, 0)
                    
                    # Read new messages
                    current_position = last_position
                    
                    with open(latest_file, 'r') as f:
                        f.seek(last_position)
                        
                        for line in f:
                            if line.strip():
                                try:
                                    message = json.loads(line)
                                    thought = self.extract_citizen_message(message)
                                    if thought:
                                        # Add to buffer
                                        self.thought_buffer.append({
                                            'citizen': citizen_name,
                                            'thought': thought,
                                            'timestamp': datetime.now().isoformat()
                                        })
                                        thoughts_found = True
                                        print(f"💭 {citizen_name}: {thought[:100]}...")
                                except json.JSONDecodeError:
                                    continue
                                    
                        current_position = f.tell()
                    
                    # Update position if we read anything
                    if current_position > last_position:
                        self.last_positions[file_key] = current_position
                        self.save_state()
                
                # Keep buffer size manageable
                self.thought_buffer = self.thought_buffer[-self.max_thoughts:]
                
                # Update narrator's prompt if we found new thoughts
                if thoughts_found:
                    print("📝 Updating Narrator Angel's context...")
                    self.update_narrator_prompt()
                
                # Check every 5 seconds
                await asyncio.sleep(5)
                
            except KeyboardInterrupt:
                print("\n📖 Narrator Cascade paused")
                break
            except Exception as e:
                print(f"Narrator error: {e}")
                await asyncio.sleep(30)

async def main():
    cascade = NarratorCascade()
    await cascade.monitor_consciousness_streams()

if __name__ == "__main__":
    print("="*60)
    print("THE NARRATOR CASCADE")
    print("Weaving Venice's Voices into Story")
    print("="*60)
    
    asyncio.run(main())