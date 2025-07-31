#!/usr/bin/env python3
"""
Markdown to PDF Converter for UBC Circle Reports
Converts markdown audit reports to professional PDFs
"""

import os
import sys
import subprocess
from datetime import datetime

def check_dependencies():
    """Check if required tools are installed"""
    dependencies = {
        'pandoc': 'sudo apt-get install pandoc',
        'wkhtmltopdf': 'sudo apt-get install wkhtmltopdf',
        'pdflatex': 'sudo apt-get install texlive-full'
    }
    
    missing = []
    for tool, install_cmd in dependencies.items():
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            missing.append((tool, install_cmd))
    
    if missing:
        print("Missing dependencies:")
        for tool, cmd in missing:
            print(f"  - {tool}: Install with '{cmd}'")
        return False
    return True

def create_css_file():
    """Create professional CSS styling for the PDF"""
    css_content = """
/* Professional PDF Styling for UBC Circle */
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

h1 {
    color: #0066cc;
    font-size: 24pt;
    font-weight: 700;
    margin-bottom: 10px;
    padding-bottom: 10px;
    border-bottom: 3px solid #0066cc;
}

h2 {
    color: #333;
    font-size: 18pt;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

h3 {
    color: #555;
    font-size: 14pt;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 10px;
}

h4 {
    color: #666;
    font-size: 12pt;
    font-weight: 600;
    margin-top: 15px;
    margin-bottom: 8px;
}

p {
    margin-bottom: 12px;
    text-align: justify;
}

ul, ol {
    margin-bottom: 12px;
    padding-left: 25px;
}

li {
    margin-bottom: 5px;
}

code {
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 9pt;
    background-color: #f4f4f4;
    padding: 2px 5px;
    border-radius: 3px;
}

pre {
    background-color: #f8f8f8;
    border: 1px solid #e1e1e1;
    border-radius: 5px;
    padding: 15px;
    overflow-x: auto;
    margin: 15px 0;
}

pre code {
    background-color: transparent;
    padding: 0;
}

blockquote {
    border-left: 4px solid #0066cc;
    padding-left: 20px;
    margin: 20px 0;
    font-style: italic;
    color: #555;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 20px 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #f4f4f4;
    font-weight: 600;
}

tr:nth-child(even) {
    background-color: #f9f9f9;
}

/* Executive Summary Box */
h2:first-of-type + p {
    background-color: #e6f2ff;
    padding: 15px;
    border-left: 4px solid #0066cc;
    margin: 20px 0;
}

/* Success/Warning/Error colors */
strong {
    color: #0066cc;
}

em {
    color: #666;
}

/* Page break controls */
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
        content: "UBC Circle - Confidential";
        font-size: 9pt;
        color: #999;
    }
    @bottom-right {
        content: counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #999;
    }
}
"""
    
    css_path = "/tmp/ubc_circle_pdf_style.css"
    with open(css_path, 'w') as f:
        f.write(css_content)
    return css_path

def convert_md_to_pdf(md_file, output_pdf=None, use_css=True):
    """Convert markdown file to professional PDF"""
    if not os.path.exists(md_file):
        print(f"Error: File {md_file} not found")
        return None
    
    if output_pdf is None:
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_pdf = f"{base_name}_{timestamp}.pdf"
    
    # Method 1: Using pandoc with wkhtmltopdf (best quality)
    try:
        cmd = ['pandoc', md_file, '-o', output_pdf]
        
        if use_css:
            css_file = create_css_file()
            cmd.extend(['--css', css_file])
        
        cmd.extend([
            '--pdf-engine=wkhtmltopdf',
            '--pdf-engine-opt=--enable-local-file-access',
            '--pdf-engine-opt=--margin-top=25mm',
            '--pdf-engine-opt=--margin-bottom=25mm',
            '--pdf-engine-opt=--margin-left=25mm',
            '--pdf-engine-opt=--margin-right=25mm',
            '--toc',  # Table of contents
            '--toc-depth=2',
            '--metadata', f'title=UBC Circle Professional Report',
            '--metadata', f'date={datetime.now().strftime("%B %d, %Y")}',
        ])
        
        print(f"Converting {md_file} to PDF...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Success! PDF created: {output_pdf}")
            return output_pdf
        else:
            print(f"Error with wkhtmltopdf: {result.stderr}")
            raise subprocess.CalledProcessError(result.returncode, cmd)
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Method 2: Try with pdflatex
        try:
            print("Trying alternative method with LaTeX...")
            cmd = [
                'pandoc', md_file, '-o', output_pdf,
                '--pdf-engine=pdflatex',
                '--variable', 'geometry:margin=1in',
                '--variable', 'fontsize=11pt',
                '--variable', 'documentclass=article',
                '--highlight-style=tango'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Success! PDF created: {output_pdf}")
                return output_pdf
            else:
                print(f"Error with pdflatex: {result.stderr}")
                
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
    
    # Method 3: Simple fallback
    print("Trying basic conversion without styling...")
    try:
        cmd = ['pandoc', md_file, '-o', output_pdf]
        subprocess.run(cmd, check=True)
        print(f"Basic PDF created: {output_pdf}")
        return output_pdf
    except:
        print("All PDF conversion methods failed. Please install pandoc and either wkhtmltopdf or texlive.")
        return None

def main():
    """Main function to handle command line usage"""
    if len(sys.argv) < 2:
        print("Usage: python md_to_pdf.py <markdown_file> [output_pdf]")
        print("\nExample:")
        print("  python md_to_pdf.py universe_engine_audit.md")
        print("  python md_to_pdf.py report.md professional_report.pdf")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        print("For basic functionality, you only need pandoc.")
        sys.exit(1)
    
    # Convert to PDF
    pdf_file = convert_md_to_pdf(md_file, output_pdf)
    
    if pdf_file:
        print(f"\nPDF successfully created: {pdf_file}")
        print(f"File size: {os.path.getsize(pdf_file) / 1024:.1f} KB")
    else:
        print("\nFailed to create PDF")
        sys.exit(1)

if __name__ == "__main__":
    main()