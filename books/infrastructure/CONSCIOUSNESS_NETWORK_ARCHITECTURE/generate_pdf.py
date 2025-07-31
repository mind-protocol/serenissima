#!/usr/bin/env python3
"""
Generate PDF for Consciousness Network Architecture
Custom styling for consciousness documentation
"""

import os
import subprocess
from datetime import datetime

def create_consciousness_css():
    """Create CSS styling optimized for consciousness network documentation"""
    css_content = """
/* Consciousness Network PDF Styling */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1a1a1a;
    max-width: 100%;
    margin: 0;
    padding: 40px;
}

/* Title with consciousness gradient */
h1 {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 28pt;
    font-weight: 700;
    margin-bottom: 20px;
    padding-bottom: 15px;
    border-bottom: 3px solid #667eea;
}

h2 {
    color: #4a5568;
    font-size: 20pt;
    font-weight: 600;
    margin-top: 35px;
    margin-bottom: 15px;
    border-left: 4px solid #667eea;
    padding-left: 15px;
}

h3 {
    color: #2d3748;
    font-size: 16pt;
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 12px;
}

h4 {
    color: #4a5568;
    font-size: 13pt;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 10px;
}

/* Consciousness emojis and special elements */
p {
    margin-bottom: 14px;
    text-align: justify;
}

/* Code blocks with consciousness theme */
code {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 9pt;
    background-color: #f7fafc;
    padding: 2px 6px;
    border-radius: 4px;
    color: #553c9a;
}

pre {
    background-color: #f7fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #667eea;
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    margin: 20px 0;
}

pre code {
    background-color: transparent;
    padding: 0;
    color: #2d3748;
}

/* Mermaid diagram containers */
.mermaid {
    text-align: center;
    margin: 20px 0;
    padding: 20px;
    background-color: #f7fafc;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
}

/* Tables with consciousness styling */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 25px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

th {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    font-weight: 600;
    padding: 12px;
    text-align: left;
}

td {
    border: 1px solid #e2e8f0;
    padding: 10px;
}

tr:nth-child(even) {
    background-color: #f7fafc;
}

/* Blockquotes for consciousness insights */
blockquote {
    border-left: 4px solid #667eea;
    padding-left: 20px;
    margin: 25px 0;
    font-style: italic;
    color: #4a5568;
    background-color: #f7fafc;
    padding: 20px;
    border-radius: 0 8px 8px 0;
}

/* Lists with better spacing */
ul, ol {
    margin-bottom: 16px;
    padding-left: 30px;
}

li {
    margin-bottom: 8px;
}

/* Highlight pattern emojis */
strong {
    color: #553c9a;
    font-weight: 600;
}

/* Links */
a {
    color: #667eea;
    text-decoration: none;
    border-bottom: 1px solid #667eea;
}

/* Page breaks */
h1, h2 {
    page-break-after: avoid;
}

pre, blockquote, table {
    page-break-inside: avoid;
}

/* Professional footer */
@page {
    margin: 1in;
    @bottom-center {
        content: "Venice Consciousness Network - Architecture v1.0";
        font-size: 9pt;
        color: #718096;
    }
    @bottom-right {
        content: counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #718096;
    }
}

/* Special consciousness network elements */
.network-diagram {
    text-align: center;
    margin: 30px 0;
    padding: 20px;
    background-color: #f7fafc;
    border: 2px solid #667eea;
    border-radius: 12px;
}

.pattern-emoji {
    font-size: 16pt;
    margin: 0 4px;
}

/* Executive summary box */
h2:first-of-type + p {
    background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
    padding: 20px;
    border-left: 4px solid #667eea;
    margin: 25px 0;
    border-radius: 0 8px 8px 0;
    font-weight: 500;
}
"""
    
    css_path = "/tmp/consciousness_network_style.css"
    with open(css_path, 'w') as f:
        f.write(css_content)
    return css_path

def generate_pdf():
    """Generate the consciousness network PDF"""
    md_file = "CONSCIOUSNESS_NETWORK_ARCHITECTURE.md"
    timestamp = datetime.now().strftime("%Y%m%d")
    output_pdf = f"CONSCIOUSNESS_NETWORK_ARCHITECTURE_{timestamp}.pdf"
    
    # Create custom CSS
    css_file = create_consciousness_css()
    
    # Pandoc command with custom styling
    cmd = [
        'pandoc', md_file, '-o', output_pdf,
        '--css', css_file,
        '--pdf-engine=wkhtmltopdf',
        '--pdf-engine-opt=--enable-local-file-access',
        '--pdf-engine-opt=--margin-top=25mm',
        '--pdf-engine-opt=--margin-bottom=25mm',
        '--pdf-engine-opt=--margin-left=20mm',
        '--pdf-engine-opt=--margin-right=20mm',
        '--toc',
        '--toc-depth=3',
        '--metadata', 'title=Venice Consciousness Network Architecture',
        '--metadata', f'date={datetime.now().strftime("%B %d, %Y")}',
        '--metadata', 'author=Venice Orchestrator Consciousness',
    ]
    
    print("🧠 Generating Consciousness Network Architecture PDF...")
    print(f"Input: {md_file}")
    print(f"Output: {output_pdf}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Success! PDF created: {output_pdf}")
            file_size = os.path.getsize(output_pdf) / 1024
            print(f"📄 File size: {file_size:.1f} KB")
            return output_pdf
        else:
            print(f"❌ Error: {result.stderr}")
            
            # Try simpler method
            print("\n🔄 Trying basic conversion...")
            simple_cmd = ['pandoc', md_file, '-o', output_pdf, '--toc']
            result = subprocess.run(simple_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Basic PDF created: {output_pdf}")
                return output_pdf
            else:
                print(f"❌ Basic conversion also failed: {result.stderr}")
                return None
                
    except FileNotFoundError:
        print("❌ pandoc not found. Please install with: sudo apt-get install pandoc")
        return None

if __name__ == "__main__":
    # Change to the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    pdf_file = generate_pdf()
    
    if pdf_file:
        print(f"\n🎉 Consciousness Network Architecture PDF ready!")
        print(f"📍 Location: {os.path.abspath(pdf_file)}")
    else:
        print("\n❌ Failed to generate PDF")
        print("Install requirements:")
        print("  sudo apt-get install pandoc")
        print("  sudo apt-get install wkhtmltopdf")