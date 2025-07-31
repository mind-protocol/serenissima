#!/usr/bin/env python3
"""
Proper Mermaid CLI Converter
Uses the official @mermaid-js/mermaid-cli tool
"""

import sys
import re
from pathlib import Path
import subprocess
import tempfile
import os

def extract_mermaid_blocks(content, file_extension):
    """Extract mermaid diagrams from both markdown and pure mermaid files"""
    if file_extension == '.mermaid' or file_extension == '.mmd':
        # Pure mermaid file - return entire content
        return [content.strip()]
    else:
        # Markdown file - extract code blocks
        pattern = r'```mermaid\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        return matches

def convert_mermaid_cli(input_file):
    """Convert mermaid diagrams using official CLI"""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: {input_file} not found")
        return False
    
    content = input_path.read_text()
    file_extension = input_path.suffix.lower()
    mermaid_blocks = extract_mermaid_blocks(content, file_extension)
    
    if not mermaid_blocks:
        print(f"No mermaid diagrams found in {input_file}")
        return False
    
    print(f"Converting {len(mermaid_blocks)} diagram(s) with mermaid CLI")
    
    for i, mermaid_code in enumerate(mermaid_blocks):
        # Create temp mermaid file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as f:
            f.write(mermaid_code)
            tmp_mmd = f.name
        
        # Output path
        if len(mermaid_blocks) == 1:
            output = input_path.with_suffix('.png')
        else:
            output = input_path.with_suffix(f'.diagram_{i+1}.png')
        
        print(f"  Diagram {i+1} -> {output.name}")
        
        try:
            # Use mmdc (mermaid CLI) to convert at API limit
            cmd = ['mmdc', '-i', tmp_mmd, '-o', str(output), 
                   '--width', '2000', '--height', '1500', '--backgroundColor', 'white']
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    Error: {result.stderr}")
                continue
                
            print(f"    ✓ Generated with mermaid CLI")
            
        finally:
            try:
                os.unlink(tmp_mmd)
            except:
                pass
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python mermaid_cli_converter.py <file>")
        print("Supports: .md (markdown with ```mermaid blocks), .mermaid, .mmd (pure mermaid)")
        sys.exit(1)
    
    success = convert_mermaid_cli(sys.argv[1])
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()