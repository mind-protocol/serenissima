#!/usr/bin/env python3
"""
Simple HTML to PDF converter using weasyprint
Falls back to basic conversion if advanced features fail
"""

import os
import sys
from pathlib import Path

def convert_with_weasyprint(html_file, output_pdf):
    """Try conversion with weasyprint"""
    try:
        import weasyprint
        
        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Create PDF
        html = weasyprint.HTML(string=html_content, base_url=str(Path(html_file).parent))
        html.write_pdf(output_pdf)
        
        print(f"✅ PDF created with weasyprint: {output_pdf}")
        return True
        
    except ImportError:
        print("❌ weasyprint not installed")
        return False
    except Exception as e:
        print(f"❌ weasyprint error: {e}")
        return False

def convert_with_pdfkit(html_file, output_pdf):
    """Try conversion with pdfkit/wkhtmltopdf"""
    try:
        import pdfkit
        
        # Configuration for better rendering
        options = {
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'print-media-type': None,
            'no-outline': None
        }
        
        pdfkit.from_file(html_file, output_pdf, options=options)
        print(f"✅ PDF created with pdfkit: {output_pdf}")
        return True
        
    except ImportError:
        print("❌ pdfkit not installed")
        return False
    except Exception as e:
        print(f"❌ pdfkit error: {e}")
        return False

def print_install_instructions():
    """Print installation instructions for various methods"""
    print("\n📚 Installation Instructions:")
    print("\nOption 1 - WeasyPrint (recommended):")
    print("  pip install weasyprint")
    print("\nOption 2 - pdfkit:")
    print("  pip install pdfkit")
    print("  # Also need wkhtmltopdf:")
    print("  # Ubuntu/Debian: sudo apt-get install wkhtmltopdf")
    print("  # Windows: Download from https://wkhtmltopdf.org/downloads.html")
    print("\nOption 3 - Use browser:")
    print("  1. Open the HTML file in Chrome/Edge")
    print("  2. Press Ctrl+P (or Cmd+P on Mac)")
    print("  3. Save as PDF")

def main():
    if len(sys.argv) < 2:
        print("Usage: python simple_html_to_pdf.py <html_file> [output_pdf]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Check if HTML exists
    if not Path(html_file).exists():
        print(f"Error: HTML file '{html_file}' not found")
        sys.exit(1)
    
    # Determine output filename
    if output_pdf is None:
        base_name = Path(html_file).stem
        output_pdf = f"{base_name}.pdf"
    
    print(f"Converting {html_file} to {output_pdf}...")
    
    # Try different methods
    success = False
    
    # Method 1: WeasyPrint
    if convert_with_weasyprint(html_file, output_pdf):
        success = True
    
    # Method 2: pdfkit
    elif convert_with_pdfkit(html_file, output_pdf):
        success = True
    
    # If nothing worked, show instructions
    if not success:
        print("\n❌ No PDF converter available")
        print_install_instructions()
        sys.exit(1)

if __name__ == "__main__":
    main()