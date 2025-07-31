#!/usr/bin/env python3
"""
Convert local files to Google Docs-compatible format (HTML)
For manual upload to Google Drive
"""

import os
import sys
import json
import html
from pathlib import Path
from datetime import datetime

# File extensions to convert
CONVERTIBLE_EXTENSIONS = {
    '.md', '.txt', '.json', '.py', '.js', '.ts', '.jsx', '.tsx',
    '.html', '.css', '.yml', '.yaml', '.sh', '.bash', '.xml', '.csv', '.log'
}

class GoogleDocsConverter:
    def __init__(self):
        self.converted_count = 0
        self.total_count = 0
    
    def convert_to_html(self, file_path, content):
        """Convert file content to HTML format that Google Docs can import."""
        file_name = Path(file_path).name
        file_ext = Path(file_path).suffix.lower()
        
        # Escape HTML characters
        escaped_content = html.escape(content)
        
        # Format based on file type
        if file_ext == '.md':
            # Basic markdown to HTML conversion
            lines = escaped_content.split('\n')
            formatted_lines = []
            
            for line in lines:
                # Convert headers
                if line.startswith('### '):
                    formatted_lines.append(f'<h3>{line[4:]}</h3>')
                elif line.startswith('## '):
                    formatted_lines.append(f'<h2>{line[3:]}</h2>')
                elif line.startswith('# '):
                    formatted_lines.append(f'<h1>{line[2:]}</h1>')
                # Convert code blocks
                elif line.startswith('```'):
                    formatted_lines.append('<pre><code>')
                elif line == '```':
                    formatted_lines.append('</code></pre>')
                # Convert bold
                elif '**' in line:
                    line = line.replace('**', '<strong>', 1)
                    line = line.replace('**', '</strong>', 1)
                    formatted_lines.append(f'<p>{line}</p>')
                # Regular lines
                elif line.strip():
                    formatted_lines.append(f'<p>{line}</p>')
                else:
                    formatted_lines.append('<br>')
            
            body_content = '\n'.join(formatted_lines)
        
        elif file_ext in ['.py', '.js', '.ts', '.jsx', '.tsx', '.sh', '.bash']:
            # Code files - preserve formatting
            body_content = f'<pre><code>{escaped_content}</code></pre>'
        
        elif file_ext == '.json':
            # Pretty print JSON
            try:
                parsed = json.loads(content)
                pretty_json = json.dumps(parsed, indent=2)
                body_content = f'<pre><code>{html.escape(pretty_json)}</code></pre>'
            except:
                body_content = f'<pre><code>{escaped_content}</code></pre>'
        
        else:
            # Default: preserve line breaks
            lines = escaped_content.split('\n')
            body_content = '<br>\n'.join(lines)
        
        # Create HTML document
        html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{html.escape(file_name)}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        pre {{ background-color: #f4f4f4; padding: 10px; overflow-x: auto; }}
        code {{ font-family: 'Courier New', monospace; }}
        .file-info {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="file-info">
        <strong>Original file:</strong> {html.escape(str(file_path))}<br>
        <strong>Converted:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
    <hr>
    {body_content}
</body>
</html>"""
        
        return html_doc
    
    def convert_folder(self, input_folder, output_folder):
        """Convert all compatible files in a folder to HTML."""
        input_path = Path(input_folder).resolve()
        output_path = Path(output_folder).resolve()
        
        if not input_path.exists():
            print(f"✗ Error: Input path '{input_path}' does not exist")
            return
        
        # Create output directory
        output_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Converting files from: {input_path}")
        print(f"📁 Output directory: {output_path}")
        print()
        
        # Process all files
        for root, dirs, files in os.walk(input_path):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            relative_path = Path(root).relative_to(input_path)
            output_dir = output_path / relative_path
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for filename in files:
                # Skip hidden files
                if filename.startswith('.'):
                    continue
                
                file_path = Path(root) / filename
                
                if file_path.suffix.lower() in CONVERTIBLE_EXTENSIONS:
                    self.total_count += 1
                    
                    try:
                        # Read file
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                        
                        # Convert to HTML
                        html_content = self.convert_to_html(file_path, content)
                        
                        # Save HTML file
                        output_file = output_dir / f"{filename}.html"
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(html_content)
                        
                        self.converted_count += 1
                        print(f"  ✓ Converted: {filename} → {filename}.html")
                        
                    except Exception as e:
                        print(f"  ✗ Error converting {filename}: {e}")
        
        print(f"\n✅ Conversion complete!")
        print(f"📊 Converted {self.converted_count}/{self.total_count} files")
        print(f"\n📤 Next steps:")
        print(f"1. Open Google Drive: https://drive.google.com/drive/folders/1MW-Zq4mzlQLHtQM6SdRUOBeb_qU6P3TJ")
        print(f"2. Upload the contents of: {output_path}")
        print(f"3. Google Drive will automatically convert HTML files to Google Docs")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python convert_for_gdocs.py <input_folder> [output_folder]")
        print("\nExample:")
        print("  python convert_for_gdocs.py ./citizens/DragonSlayer")
        print("  python convert_for_gdocs.py ./citizens/DragonSlayer ./gdocs_upload")
        sys.exit(1)
    
    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else f"{input_folder}_gdocs_html"
    
    converter = GoogleDocsConverter()
    converter.convert_folder(input_folder, output_folder)


if __name__ == "__main__":
    main()