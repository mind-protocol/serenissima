#!/usr/bin/env python3
"""
Convert .mmd files directly to PNG images using mermaid CLI
"""

import sys
from pathlib import Path
import subprocess
import os

def convert_mmd_to_png(mmd_file):
    """Convert a .mmd file directly to PNG"""
    mmd_path = Path(mmd_file)
    if not mmd_path.exists():
        print(f"Error: {mmd_file} not found")
        return False
    
    # Output path
    output_path = mmd_path.with_suffix('.png')
    
    print(f"Converting {mmd_path.name} -> {output_path.name}")
    
    try:
        # Run mermaid CLI using npx
        result = subprocess.run([
            'npx', 'mmdc',
            '-i', str(mmd_path),
            '-o', str(output_path),
            '-w', '2000',  # Width
            '-H', '2000',  # Height
            '--backgroundColor', 'white'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Created: {output_path}")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 convert_mmd_files.py <file.mmd or directory>")
        return
    
    target = Path(sys.argv[1])
    
    if target.is_file() and target.suffix == '.mmd':
        # Convert single file
        convert_mmd_to_png(target)
    elif target.is_dir():
        # Convert all .mmd files in directory
        mmd_files = list(target.glob("*.mmd"))
        if not mmd_files:
            print(f"No .mmd files found in {target}")
            return
        
        print(f"Found {len(mmd_files)} .mmd files to convert")
        for mmd_file in mmd_files:
            convert_mmd_to_png(mmd_file)
    else:
        print(f"Error: {target} is not a .mmd file or directory")

if __name__ == "__main__":
    main()