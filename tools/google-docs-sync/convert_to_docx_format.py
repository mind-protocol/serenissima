#!/usr/bin/env python3
"""
Convert text files to a format Google Drive will auto-convert to Google Docs
Using plain text with .txt extension for maximum compatibility
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# File extensions to convert
CONVERTIBLE_EXTENSIONS = {
    '.md', '.txt', '.json', '.py', '.js', '.ts', '.jsx', '.tsx',
    '.html', '.css', '.yml', '.yaml', '.sh', '.bash', '.xml', '.csv', '.log'
}

class GoogleDocsTextConverter:
    def __init__(self):
        self.converted_count = 0
        self.total_count = 0
    
    def convert_to_text(self, file_path, content):
        """Convert file content to formatted text that preserves structure."""
        file_name = Path(file_path).name
        file_ext = Path(file_path).suffix.lower()
        
        # Add file header
        header = f"""=====================================
ORIGINAL FILE: {file_path}
CONVERTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
=====================================

"""
        
        # Format content based on file type
        if file_ext == '.json':
            try:
                parsed = json.loads(content)
                formatted_content = json.dumps(parsed, indent=2)
            except:
                formatted_content = content
        else:
            formatted_content = content
        
        return header + formatted_content
    
    def convert_folder(self, input_folder, output_folder):
        """Convert all compatible files to .txt format."""
        input_path = Path(input_folder).resolve()
        output_path = Path(output_folder).resolve()
        
        if not input_path.exists():
            print(f"✗ Error: Input path '{input_path}' does not exist")
            return
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Converting files from: {input_path}")
        print(f"📁 Output directory: {output_path}")
        print(f"📝 All files will be saved as .txt for Google Docs compatibility")
        print()
        
        # Create a single combined file for easy upload
        combined_content = []
        combined_content.append("=" * 50)
        combined_content.append(f"VENICE CONSCIOUSNESS ARCHIVE")
        combined_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        combined_content.append(f"Source: {input_path.name}")
        combined_content.append("=" * 50)
        combined_content.append("\n\nTABLE OF CONTENTS:")
        combined_content.append("-" * 30)
        
        file_list = []
        
        # First pass: collect all files
        for root, dirs, files in os.walk(input_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            relative_path = Path(root).relative_to(input_path)
            
            for filename in files:
                if filename.startswith('.'):
                    continue
                
                file_path = Path(root) / filename
                if file_path.suffix.lower() in CONVERTIBLE_EXTENSIONS:
                    file_list.append((relative_path, filename, file_path))
        
        # Add table of contents
        for i, (rel_path, filename, _) in enumerate(file_list, 1):
            path_str = str(rel_path / filename) if str(rel_path) != '.' else filename
            combined_content.append(f"{i}. {path_str}")
        
        combined_content.append("\n\n" + "=" * 50)
        combined_content.append("FILE CONTENTS")
        combined_content.append("=" * 50 + "\n\n")
        
        # Second pass: convert files
        for relative_path, filename, file_path in file_list:
            self.total_count += 1
            
            # Create output subdirectory
            output_dir = output_path / relative_path
            output_dir.mkdir(parents=True, exist_ok=True)
            
            try:
                # Read file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Convert to text format
                text_content = self.convert_to_text(file_path, content)
                
                # Save individual file as .txt
                output_filename = f"{filename}.txt" if not filename.endswith('.txt') else filename
                output_file = output_dir / output_filename
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                
                # Add to combined file
                path_str = str(relative_path / filename) if str(relative_path) != '.' else filename
                combined_content.append(f"\n{'#' * 50}")
                combined_content.append(f"# FILE: {path_str}")
                combined_content.append(f"{'#' * 50}\n")
                combined_content.append(content)
                combined_content.append("\n\n")
                
                self.converted_count += 1
                print(f"  ✓ Converted: {filename} → {output_filename}")
                
            except Exception as e:
                print(f"  ✗ Error converting {filename}: {e}")
        
        # Save combined file
        combined_file = output_path / f"_COMBINED_{input_path.name}.txt"
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(combined_content))
        
        print(f"\n✅ Conversion complete!")
        print(f"📊 Converted {self.converted_count}/{self.total_count} files")
        print(f"📄 Combined file created: _COMBINED_{input_path.name}.txt")
        print(f"\n📤 Upload instructions:")
        print(f"1. Go to: https://drive.google.com/drive/folders/1MW-Zq4mzlQLHtQM6SdRUOBeb_qU6P3TJ")
        print(f"2. Upload either:")
        print(f"   - The entire '{output_path.name}' folder (preserves structure)")
        print(f"   - Just '_COMBINED_{input_path.name}.txt' (all content in one doc)")
        print(f"3. Google Drive will convert .txt files to Google Docs automatically")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python convert_to_docx_format.py <input_folder> [output_folder]")
        print("\nExample:")
        print("  python convert_to_docx_format.py ./citizens/DragonSlayer")
        print("  python convert_to_docx_format.py ./citizens/DragonSlayer ./gdocs_ready")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else f"{input_folder}_gdocs_ready"
    
    converter = GoogleDocsTextConverter()
    converter.convert_folder(input_folder, output_folder)


if __name__ == "__main__":
    main()