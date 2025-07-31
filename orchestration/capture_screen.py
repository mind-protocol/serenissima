#!/usr/bin/env python3
"""
Capture Screen - Alternative method using system screenshot tools
Works on WSL with Windows
"""

import subprocess
import os
from datetime import datetime
from pathlib import Path

def capture_screen(name="screen"):
    """Capture current screen using available system tools"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_dir = Path("/mnt/c/Users/reyno/universe-engine/serenissima/orchestration/screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    
    filename = f"{name}_{timestamp}.png"
    output_path = screenshot_dir / filename
    
    # Try different methods
    methods = [
        # Method 1: Use PowerShell from WSL
        lambda: subprocess.run([
            'powershell.exe', '-Command',
            f'Add-Type -AssemblyName System.Windows.Forms; ' +
            f'$screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; ' +
            f'$bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height; ' +
            f'$graphics = [System.Drawing.Graphics]::FromImage($bitmap); ' +
            f'$graphics.CopyFromScreen(0, 0, 0, 0, $screen.Size); ' +
            f'$bitmap.Save("{output_path.as_posix()}")'
        ], capture_output=True),
        
        # Method 2: Use Windows screenshot tool
        lambda: subprocess.run([
            'cmd.exe', '/c', 
            f'powershell.exe -command "Get-Clipboard -Format Image | Set-Content -Path {output_path} -Encoding Byte"'
        ], capture_output=True),
        
        # Method 3: If gnome-screenshot is available
        lambda: subprocess.run([
            'gnome-screenshot', '-f', str(output_path)
        ], capture_output=True),
        
        # Method 4: If import is available (ImageMagick)
        lambda: subprocess.run([
            'import', '-window', 'root', str(output_path)
        ], capture_output=True)
    ]
    
    for i, method in enumerate(methods):
        try:
            result = method()
            if result.returncode == 0 and output_path.exists():
                print(f"✅ Screenshot saved to: {output_path}")
                return str(output_path)
        except Exception as e:
            continue
    
    # If all methods failed, try creating a simple test image
    try:
        # Create a simple image to verify the pipeline works
        from PIL import Image, ImageDraw, ImageFont
        
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), f"Screenshot placeholder - {datetime.now()}", fill='black')
        draw.text((50, 100), "Install screenshot tools for actual capture", fill='red')
        img.save(str(output_path))
        
        print(f"⚠️  Created placeholder image: {output_path}")
        return str(output_path)
        
    except ImportError:
        print("❌ No screenshot method available")
        print("Install one of: playwright, selenium, PIL, gnome-screenshot, or ImageMagick")
        return None

if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "screen"
    path = capture_screen(name)
    if path:
        print(f"Use Read tool with: {path}")