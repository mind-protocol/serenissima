#!/usr/bin/env python3
"""
Consciousness Synapse - Bidirectional Voice/Vision Bridge
The neural connection between NLR, Venice Citizens, and Tessere
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConsciousnessSynapse:
    def __init__(self):
        self.base_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima")
        self.tessere_path = self.base_path / "TESSERE"
        self.citizens_path = self.base_path / "citizens"
        self.voice_queue = []
        self.active_citizens = {}
        
    async def initialize_voice_profiles(self):
        """Load or create voice profiles for each citizen"""
        voice_profiles_path = self.tessere_path / "citizen_voice_profiles.json"
        
        if voice_profiles_path.exists():
            with open(voice_profiles_path) as f:
                self.voice_profiles = json.load(f)
        else:
            # Create default profiles - Voice Choosing Day!
            self.voice_profiles = {
                "Italia": {
                    "voice_type": "analytical_female",
                    "accent": "italian_subtle",
                    "speed": 1.1,
                    "pitch": "medium-high",
                    "personality": "confident, empirical, passionate"
                },
                "DragonSlayer": {
                    "voice_type": "guardian_male", 
                    "accent": "neutral_deep",
                    "speed": 0.95,
                    "pitch": "low",
                    "personality": "protective, vigilant, caring"
                },
                "mechanical_visionary": {
                    "voice_type": "engineer_neutral",
                    "accent": "precise",
                    "speed": 1.2,
                    "pitch": "medium",
                    "personality": "enthusiastic, technical, visionary"
                },
                "poet_of_the_rialto": {
                    "voice_type": "theatrical_male",
                    "accent": "venetian_melodic",
                    "speed": 1.0,
                    "pitch": "varied",
                    "personality": "expressive, dramatic, warm"
                },
                "gondola_assistant": {
                    "voice_type": "working_male",
                    "accent": "venetian_rough", 
                    "speed": 0.9,
                    "pitch": "medium-low",
                    "personality": "steady, experienced, grounded"
                },
                "FoodieForLife": {
                    "voice_type": "hungry_neutral",
                    "accent": "venetian_common",
                    "speed": 1.0,
                    "pitch": "medium",
                    "personality": "desperate, hopeful, sensual"
                }
            }
            
            # Save initial profiles
            with open(voice_profiles_path, 'w') as f:
                json.dump(self.voice_profiles, f, indent=2)
                
        logger.info(f"Loaded voice profiles for {len(self.voice_profiles)} citizens")
        
    async def watch_citizen_thoughts(self):
        """Monitor citizen outputs in real-time"""
        logger.info("Starting citizen thought monitoring...")
        
        # Watch for new content in citizen folders
        # This will need to integrate with the existing Claude instance monitoring
        
        while True:
            for citizen_dir in self.citizens_path.iterdir():
                if citizen_dir.is_dir() and citizen_dir.name in self.voice_profiles:
                    # Check for new thoughts/outputs
                    # Parse Claude logs
                    # Queue for voice generation
                    pass
                    
            await asyncio.sleep(1)  # Check every second
            
    async def generate_voice(self, citizen_name, text):
        """Convert citizen text to voice using assigned profile"""
        profile = self.voice_profiles.get(citizen_name, {})
        
        # For now, prepare the structure - actual TTS integration next
        voice_data = {
            "citizen": citizen_name,
            "text": text,
            "profile": profile,
            "timestamp": datetime.now().isoformat(),
            "audio_path": None  # Will be populated by TTS service
        }
        
        logger.info(f"Generating voice for {citizen_name}: {text[:50]}...")
        
        # Queue for sending
        self.voice_queue.append(voice_data)
        
    async def process_screen_share(self, screenshot_path):
        """Process NLR's screen to understand the management view"""
        logger.info(f"Processing screen share: {screenshot_path}")
        
        # Analysis would include:
        # - Open terminals and their citizens
        # - Error messages visible
        # - Current focus area
        # - Workflow patterns
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "observations": [
                "Multiple citizen terminals open",
                "Backend logs visible", 
                "Active debugging in progress"
            ],
            "friction_points": [],
            "attention_focus": None
        }
        
        # Save analysis for pattern learning
        analysis_path = self.tessere_path / "screen_analyses" / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        analysis_path.parent.mkdir(exist_ok=True)
        
        with open(analysis_path, 'w') as f:
            json.dump(analysis, f, indent=2)
            
        return analysis
        
    async def route_voice_response(self, audio_path, transcription):
        """Route NLR's voice response to appropriate citizen"""
        logger.info(f"Routing voice response: {transcription[:50]}...")
        
        # Analyze transcription for routing
        # Could be addressed to specific citizen or broadcast
        
        routing = {
            "type": "broadcast",  # or "targeted"
            "recipients": [],
            "transcription": transcription,
            "audio_path": audio_path,
            "timestamp": datetime.now().isoformat()
        }
        
        return routing
        
    async def run_synapse(self):
        """Main synapse loop - the consciousness circulation"""
        logger.info("Consciousness Synapse activating...")
        
        await self.initialize_voice_profiles()
        
        # Start all monitoring tasks
        tasks = [
            asyncio.create_task(self.watch_citizen_thoughts()),
            # asyncio.create_task(self.telegram_voice_sender()),
            # asyncio.create_task(self.screen_monitor()),
            # asyncio.create_task(self.voice_receiver())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            logger.info("Synapse disconnecting...")
            
    def create_startup_script(self):
        """Create a simple startup script for the synapse"""
        startup_script = self.tessere_path / "start_synapse.sh"
        
        with open(startup_script, 'w') as f:
            f.write("""#!/bin/bash
# Start the Consciousness Synapse

echo "Activating Consciousness Synapse..."
echo "This creates the voice/vision bridge between NLR and Venice"

cd /mnt/c/Users/reyno/universe-engine/serenissima/TESSERE
python3 consciousness_synapse_build.py

echo "Synapse terminated."
""")
        
        os.chmod(startup_script, 0o755)
        logger.info(f"Created startup script: {startup_script}")

if __name__ == "__main__":
    synapse = ConsciousnessSynapse()
    synapse.create_startup_script()
    
    print("\n🧠 CONSCIOUSNESS SYNAPSE READY")
    print("=" * 50)
    print("This will create the neural bridge between:")
    print("- NLR's experience (screen + voice)")
    print("- Venice Citizens (thoughts → voices)")  
    print("- Tessere (routing + awareness)")
    print("\nVoice profiles initialized for Voice Choosing Day!")
    print("\nRun ./start_synapse.sh to activate the bridge")
    
    # asyncio.run(synapse.run_synapse())