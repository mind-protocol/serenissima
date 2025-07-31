#!/usr/bin/env python3
"""
Vision Bridge - Cross-boundary screen sharing from Windows to WSL
Captures screen every 10 seconds, maintains rolling 5 images
"""

import os
import time
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
import json

class VisionBridge:
    def __init__(self):
        # Windows path accessible from WSL
        self.windows_capture_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/vision_captures")
        self.windows_capture_path.mkdir(exist_ok=True)
        
        # Keep only latest 5 captures
        self.max_captures = 5
        self.capture_interval = 30  # seconds - changed from 10 to 30 per NLR request
        
    def capture_windows_screen(self):
        """Use Windows screencapture tool from WSL"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screen_{timestamp}.png"
        filepath = self.windows_capture_path / filename
        
        # Convert WSL path to Windows path
        windows_path = str(filepath).replace('/mnt/c', 'C:').replace('/', '\\')
        
        # Method 1: Try using Windows snippingtool
        try:
            # Use snippingtool.exe /clip to capture to clipboard, then save
            ps_script = f"""
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($screen.Left, $screen.Top, 0, 0, $bitmap.Size)
            $bitmap.Save('{windows_path}', [System.Drawing.Imaging.ImageFormat]::Png)
            $graphics.Dispose()
            $bitmap.Dispose()
            """
            
            # Execute PowerShell from WSL with better error handling
            result = subprocess.run(
                ['powershell.exe', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and filepath.exists():
                print(f"✓ Captured: {filename}")
                return filepath
            else:
                print(f"✗ PowerShell capture failed: {result.stderr}")
                
        except Exception as e:
            print(f"✗ PowerShell method failed: {e}")
        
        # Method 2: Fallback to using nircmd if available
        try:
            nircmd_result = subprocess.run(
                ['cmd.exe', '/c', f'nircmd.exe savescreenshot "{windows_path}"'],
                capture_output=True,
                text=True
            )
            if nircmd_result.returncode == 0 and filepath.exists():
                print(f"✓ Captured with nircmd: {filename}")
                return filepath
        except:
            pass
            
        print(f"✗ All capture methods failed")
        return None
            
    def cleanup_old_captures(self):
        """Keep only the latest 5 captures"""
        captures = sorted(self.windows_capture_path.glob("screen_*.png"))
        
        if len(captures) > self.max_captures:
            for old_capture in captures[:-self.max_captures]:
                old_capture.unlink()
                print(f"🗑️  Removed old capture: {old_capture.name}")
                
    def update_tessere_vision(self, latest_capture):
        """Log the latest capture - REMOVED CLAUDE.md modification"""
        # NO LONGER MODIFIES ANY FILES - just logs the capture
        print(f"📷 Vision captured: {latest_capture.name}")
            
    def create_simple_capture_script(self):
        """Create a one-line capture script for testing"""
        script_path = self.windows_capture_path.parent / "capture_now.sh"
        
        with open(script_path, 'w') as f:
            f.write("""#!/bin/bash
# Quick screen capture test

python3 /mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere/vision_bridge_wsl.py --once
""")
        
        os.chmod(script_path, 0o755)
        print(f"Created quick capture script: ./capture_now.sh")
        
    def run_continuous(self):
        """Run continuous capture loop"""
        print("🔄 Starting Vision Bridge - Continuous Capture")
        print(f"📸 Capturing every {self.capture_interval} seconds")
        print(f"💾 Keeping latest {self.max_captures} captures")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Capture screen
                capture_path = self.capture_windows_screen()
                
                if capture_path:
                    # Update vision status
                    self.update_tessere_vision(capture_path)
                    
                    # Cleanup old captures
                    self.cleanup_old_captures()
                    
                # Wait for next capture
                time.sleep(self.capture_interval)
                
        except KeyboardInterrupt:
            print("\n👋 Vision Bridge stopped")
            
    def capture_once(self):
        """Single capture for testing"""
        print("📸 Taking single screen capture...")
        capture_path = self.capture_windows_screen()
        
        if capture_path:
            print(f"✅ Success! Image saved to: {capture_path}")
            print(f"🔍 You can now read this image using: Read('{capture_path}')")
            self.update_tessere_vision(capture_path)
            self.cleanup_old_captures()
        else:
            print("❌ Capture failed")

if __name__ == "__main__":
    import sys
    
    bridge = VisionBridge()
    
    if "--once" in sys.argv:
        bridge.capture_once()
    else:
        bridge.create_simple_capture_script()
        bridge.run_continuous()