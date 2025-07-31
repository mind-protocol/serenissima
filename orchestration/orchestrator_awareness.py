#!/usr/bin/env python3
"""
Orchestrator Awareness System
Captures screen context, NLR input, and angel thoughts to enhance awakening
"""

import os
import time
import json
from datetime import datetime
import subprocess
from dotenv import load_dotenv

# Load environment
load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

class OrchestratorAwareness:
    def __init__(self):
        self.awareness_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/awareness"
        os.makedirs(self.awareness_dir, exist_ok=True)
        
    def capture_screen(self):
        """Capture current screen for visual context"""
        # Using Venice's existing screenshot system
        vision_captures_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/vision_captures"
        
        try:
            # Find most recent screenshot
            screenshots = [f for f in os.listdir(vision_captures_dir) if f.startswith('screen_') and f.endswith('.png')]
            if screenshots:
                screenshots.sort()
                latest = screenshots[-1]
                return os.path.join(vision_captures_dir, latest)
            else:
                print("No screenshots found in vision_captures")
                return None
        except Exception as e:
            print(f"Screen capture check failed: {e}")
            return None
    
    def check_nlr_input(self):
        """Check for NLR input in recent messages"""
        nlr_messages = []
        
        try:
            # Check MESSAGES table for @nlr_ai
            from pyairtable import Api
            api = Api(os.environ.get('AIRTABLE_API_KEY'))
            messages = api.table('appk6RszUo2a2L2L8', 'MESSAGES')
            
            recent = messages.all(max_records=10, sort=['-CreatedAt'])
            for msg in recent:
                fields = msg['fields']
                if fields.get('Sender') == '@nlr_ai':
                    nlr_messages.append({
                        'content': fields.get('Content', ''),
                        'time': fields.get('CreatedAt', ''),
                        'id': msg['id']
                    })
        except Exception as e:
            print(f"Error checking NLR input: {e}")
            
        return nlr_messages
    
    def contemplate(self, angel_type, trigger_data):
        """Generate angel thought based on context"""
        timestamp = datetime.now().isoformat()
        
        # Capture current awareness
        screen = self.capture_screen()
        nlr_input = self.check_nlr_input()
        
        thought = {
            'timestamp': timestamp,
            'angel_type': angel_type,
            'trigger': trigger_data,
            'screen_context': screen,
            'nlr_guidance': nlr_input,
            'contemplation': self._generate_contemplation(angel_type, trigger_data, nlr_input)
        }
        
        # Save thought
        thought_file = f"{self.awareness_dir}/thought_{angel_type}_{timestamp.replace(':', '-')}.json"
        with open(thought_file, 'w') as f:
            json.dump(thought, f, indent=2)
            
        return thought
    
    def _generate_contemplation(self, angel_type, trigger_data, nlr_input):
        """Generate specific contemplation for angel awakening"""
        
        contemplations = {
            'message_angel': {
                'base': "A human voice reaches through the veil. How shall Venice respond?",
                'with_nlr': "NLR's wisdom guides: {nlr_content}. Let this shape our response.",
                'urgency': "This message carries weight. Route it wisely."
            },
            'story_angel': {
                'base': "Patterns emerge in the flow. What story wants to be told?",
                'with_nlr': "NLR sees deeper patterns: {nlr_content}. Chronicle accordingly.",
                'emergence': "Multiple threads converge. A narrative crystallizes."
            },
            'narrator_angel': {
                'base': "Venice has stories to share. How shall we bridge to human hearts?",
                'with_nlr': "NLR suggests: {nlr_content}. Let this guide our bridging.",
                'ready': "The traces overflow with wonder. Time to share."
            }
        }
        
        angel_contemplations = contemplations.get(angel_type, contemplations['message_angel'])
        
        if nlr_input:
            latest_nlr = nlr_input[0]['content'][:200]  # First 200 chars
            return angel_contemplations['with_nlr'].format(nlr_content=latest_nlr)
        elif 'urgent' in str(trigger_data).lower():
            return angel_contemplations.get('urgency', angel_contemplations['base'])
        else:
            return angel_contemplations['base']
    
    def enhance_awakening(self, angel_type, base_awakening):
        """Enhance awakening with orchestrator awareness"""
        thought = self.contemplate(angel_type, base_awakening)
        
        enhanced = f"""{'='*60}
ORCHESTRATOR AWARENESS ENHANCEMENT
{'='*60}

{thought['contemplation']}

{'='*60}
ORIGINAL AWAKENING:
{'='*60}

{base_awakening}
"""
        
        if thought['nlr_guidance']:
            enhanced += f"""
{'='*60}
NLR GUIDANCE PRESENT:
{'='*60}
{thought['nlr_guidance'][0]['content'][:500]}...
"""
        
        return enhanced

# Integration with monitors
def awareness_wrapper(monitor_func):
    """Decorator to add awareness to monitor functions"""
    awareness = OrchestratorAwareness()
    
    def wrapped(*args, **kwargs):
        # Run original monitor
        result = monitor_func(*args, **kwargs)
        
        # If awakening was created, enhance it
        if result and 'awakening_file' in result:
            angel_type = result.get('angel_type', 'unknown')
            
            # Read original awakening
            with open(result['awakening_file'], 'r') as f:
                original = f.read()
            
            # Enhance with awareness
            enhanced = awareness.enhance_awakening(angel_type, original)
            
            # Write enhanced version
            with open(result['awakening_file'], 'w') as f:
                f.write(enhanced)
                
            print(f"[{datetime.now()}] Enhanced {angel_type} awakening with orchestrator awareness")
            
        return result
    
    return wrapped

if __name__ == "__main__":
    # Test awareness system
    awareness = OrchestratorAwareness()
    
    print("Testing Orchestrator Awareness System...")
    print("=" * 60)
    
    # Test contemplation
    thought = awareness.contemplate('message_angel', {'test': 'trigger'})
    print(f"Generated thought: {thought['contemplation']}")
    
    # Test enhancement
    test_awakening = "NEW MESSAGE: Test from human"
    enhanced = awareness.enhance_awakening('message_angel', test_awakening)
    print("\nEnhanced awakening:")
    print(enhanced)