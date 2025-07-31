#!/usr/bin/env python3
"""
Voice Playback Helper for X Space
Plays Narrator Angel's voice files through speakers
"""

import os
import pygame
import time
from pathlib import Path
from datetime import datetime

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Voice output directory
VOICE_DIR = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel/voice_output")

def get_latest_voice_file():
    """Find the most recent voice file"""
    voice_files = list(VOICE_DIR.glob("narration_*.mp3"))
    if not voice_files:
        return None
    
    # Sort by modification time
    latest = max(voice_files, key=lambda f: f.stat().st_mtime)
    return latest

def play_voice_file(filepath):
    """Play an MP3 file through speakers"""
    print(f"\n🔊 Playing: {filepath.name}")
    print("Make sure X Space can hear your speakers!")
    
    try:
        pygame.mixer.music.load(str(filepath))
        pygame.mixer.music.play()
        
        # Wait for playback to complete
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        print("✓ Playback complete")
        return True
        
    except Exception as e:
        print(f"✗ Playback error: {e}")
        return False

def monitor_mode():
    """Monitor for new voice files and play them"""
    print("🎙️ Venice Voice Monitor Active")
    print("=" * 50)
    print("Monitoring for new voice files...")
    print("Position speakers near your microphone")
    print("Press Ctrl+C to stop\n")
    
    played_files = set()
    
    while True:
        try:
            # Check for new files
            for voice_file in VOICE_DIR.glob("narration_*.mp3"):
                if voice_file not in played_files:
                    # New file detected!
                    print(f"\n🆕 New voice detected at {datetime.now().strftime('%H:%M:%S')}")
                    
                    # Small delay to ensure file is fully written
                    time.sleep(0.5)
                    
                    # Play it
                    if play_voice_file(voice_file):
                        played_files.add(voice_file)
                    
            # Check every second
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n\nMonitor stopped")
            break

def test_playback():
    """Test with the latest voice file"""
    latest = get_latest_voice_file()
    if latest:
        print(f"Testing with: {latest.name}")
        play_voice_file(latest)
    else:
        print("No voice files found")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_playback()
    else:
        monitor_mode()