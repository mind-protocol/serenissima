#!/usr/bin/env python3
"""
HTML to PDF converter using Playwright for high-quality rendering
Preserves all CSS styling and modern web features
"""

import asyncio
from playwright.async_api import async_playwright
import os
import sys
from pathlib import Path

async def convert_html_to_pdf(html_file, output_pdf=None):
    """Convert HTML file to PDF using headless browser"""
    
    # Determine output filename
    if output_pdf is None:
        base_name = Path(html_file).stem
        output_pdf = f"{base_name}.pdf"
    
    # Get absolute paths
    html_path = Path(html_file).absolute()
    output_path = Path(output_pdf).absolute()
    
    if not html_path.exists():
        print(f"Error: HTML file '{html_file}' not found")
        return False
    
    try:
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # Load HTML file
            file_url = f"file://{html_path}"
            await page.goto(file_url, wait_until='networkidle')
            
            # Wait a bit for fonts to load
            await page.wait_for_timeout(1000)
            
            # Generate PDF with professional settings
            await page.pdf(
                path=str(output_path),
                format='A4',
                print_background=True,
                margin={
                    'top': '20mm',
                    'right': '20mm',
                    'bottom': '20mm',
                    'left': '20mm'
                },
                display_header_footer=False,
                prefer_css_page_size=True
            )
            
            await browser.close()
            
        print(f"✅ PDF created successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating PDF: {e}")
        print("\nMake sure Playwright is installed:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return False

async def batch_convert(html_files):
    """Convert multiple HTML files to PDF"""
    results = []
    for html_file in html_files:
        print(f"\nConverting {html_file}...")
        success = await convert_html_to_pdf(html_file)
        results.append((html_file, success))
    
    print("\n📊 Conversion Summary:")
    for html_file, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {html_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python html_to_pdf.py <html_file> [output_pdf]")
        print("       python html_to_pdf.py *.html  # Convert all HTML files")
        sys.exit(1)
    
    # Handle wildcards
    if '*' in sys.argv[1]:
        import glob
        html_files = glob.glob(sys.argv[1])
        if not html_files:
            print(f"No files matching pattern '{sys.argv[1]}'")
            sys.exit(1)
        asyncio.run(batch_convert(html_files))
    else:
        html_file = sys.argv[1]
        output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
        asyncio.run(convert_html_to_pdf(html_file, output_pdf))

if __name__ == "__main__":
    main()