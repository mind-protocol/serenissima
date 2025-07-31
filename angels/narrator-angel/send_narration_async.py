#!/usr/bin/env python3
"""
Fire-and-forget narrator voice message sender
Spawns a subprocess to handle TTS generation without blocking
"""

import os
import sys
import subprocess
from pathlib import Path

def send_narration_async(text):
    """Launch narration in background process"""
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    worker_script = script_dir / "narration_worker.py"
    
    # Launch the worker process in the background
    # Using subprocess.Popen with no wait to make it fire-and-forget
    subprocess.Popen(
        [sys.executable, str(worker_script), text],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True  # Detach from parent process
    )
    
    print("✓ Narration queued for background processing")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_narration_async.py 'Your narration text here'")
        sys.exit(1)
    
    narration_text = sys.argv[1]
    send_narration_async(narration_text)