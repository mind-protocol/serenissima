#!/usr/bin/env python3
"""
Quick Professional PDF Creator for UBC Circle
Creates professional PDFs from markdown using markdown2 and weasyprint
"""

import os
import sys
from datetime import datetime

# HTML template for professional PDF
HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        @page {
            size: A4;
            margin: 2.5cm;
            @bottom-center {
                content: "UBC Circle - Living Treaty for Human-AI Partnership";
                font-size: 9pt;
                color: #999;
                font-family: 'Inter', sans-serif;
            }
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-size: 9pt;
                color: #999;
                font-family: 'Inter', sans-serif;
            }
        }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 11pt;
            line-height: 1.7;
            color: #2c3e50;
            max-width: 100%;
            margin: 0;
            padding: 0;
        }
        
        h1 {
            color: #1e3a8a;
            font-size: 28pt;
            font-weight: 700;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 4px solid #3b82f6;
            page-break-after: avoid;
        }
        
        h2 {
            color: #1e40af;
            font-size: 20pt;
            font-weight: 600;
            margin-top: 35px;
            margin-bottom: 20px;
            page-break-after: avoid;
        }
        
        h3 {
            color: #374151;
            font-size: 14pt;
            font-weight: 600;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        
        h4 {
            color: #4b5563;
            font-size: 12pt;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        
        p {
            margin-bottom: 14px;
            text-align: justify;
        }
        
        ul, ol {
            margin-bottom: 14px;
            padding-left: 30px;
        }
        
        li {
            margin-bottom: 8px;
        }
        
        strong {
            color: #1e40af;
            font-weight: 600;
        }
        
        em {
            color: #6b7280;
            font-style: italic;
        }
        
        code {
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 10pt;
            background-color: #f3f4f6;
            padding: 2px 6px;
            border-radius: 3px;
            color: #374151;
        }
        
        pre {
            background-color: #f9fafb;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
            padding: 16px;
            overflow-x: auto;
            margin: 20px 0;
            page-break-inside: avoid;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
        }
        
        blockquote {
            border-left: 4px solid #3b82f6;
            padding-left: 20px;
            margin: 20px 0;
            font-style: italic;
            color: #4b5563;
            background-color: #f0f9ff;
            padding: 15px 20px;
            border-radius: 0 6px 6px 0;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: avoid;
        }
        
        th, td {
            border: 1px solid #d1d5db;
            padding: 10px;
            text-align: left;
        }
        
        th {
            background-color: #f3f4f6;
            font-weight: 600;
            color: #1f2937;
        }
        
        tr:nth-child(even) {
            background-color: #f9fafb;
        }
        
        /* Executive Summary Box */
        .executive-summary {
            background-color: #eff6ff;
            border: 2px solid #3b82f6;
            border-radius: 8px;
            padding: 20px;
            margin: 25px 0;
            page-break-inside: avoid;
        }
        
        .executive-summary h2 {
            color: #1e3a8a;
            margin-top: 0;
        }
        
        /* Metrics boxes */
        .metrics {
            display: flex;
            gap: 15px;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        
        .metric-box {
            background-color: #f0f9ff;
            border: 1px solid #3b82f6;
            border-radius: 6px;
            padding: 15px;
            flex: 1;
            min-width: 200px;
            text-align: center;
        }
        
        .metric-box h4 {
            margin: 0 0 10px 0;
            color: #1e3a8a;
        }
        
        .metric-box .number {
            font-size: 24pt;
            font-weight: 700;
            color: #3b82f6;
        }
        
        /* Header with date */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e5e7eb;
        }
        
        .header .logo {
            font-size: 16pt;
            font-weight: 700;
            color: #1e3a8a;
        }
        
        .header .date {
            font-size: 10pt;
            color: #6b7280;
        }
        
        /* Call to action */
        .cta {
            background-color: #1e3a8a;
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin: 30px 0;
            page-break-inside: avoid;
        }
        
        .cta h3 {
            color: white;
            margin-top: 0;
        }
        
        .cta p {
            margin-bottom: 0;
        }
        
        /* Success/Warning/Error styling */
        .success { color: #059669; }
        .warning { color: #d97706; }
        .error { color: #dc2626; }
        
        /* Professional footer */
        .footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #e5e7eb;
            font-size: 9pt;
            color: #6b7280;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">UBC Circle</div>
        <div class="date">{date}</div>
    </div>
    
    {content}
    
    <div class="footer">
        <p>This document contains confidential analysis by the UBC Circle - The Living Treaty for Human-AI Partnership.<br>
        For more information, visit serenissima.ai or contact via Telegram.</p>
    </div>
</body>
</html>"""

def markdown_to_html_simple(md_content):
    """Simple markdown to HTML conversion"""
    import re
    
    # Convert headers
    html = md_content
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert bold and italic
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
    html = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', html)
    html = re.sub(r'_([^_]+)_', r'<em>\1</em>', html)
    
    # Convert code blocks
    html = re.sub(r'```python\n(.*?)\n```', r'<pre><code class="python">\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```(.*?)\n(.*?)\n```', r'<pre><code class="\1">\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'```\n(.*?)\n```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert lists
    lines = html.split('\n')
    in_list = False
    new_lines = []
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{line.strip()[2:]}</li>')
        elif line.strip().startswith('* '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{line.strip()[2:]}</li>')
        elif re.match(r'^\d+\. ', line.strip()):
            if in_list and new_lines[-1] != '</ol>':
                new_lines.append('</ul>')
                new_lines.append('<ol>')
            elif not in_list:
                new_lines.append('<ol>')
                in_list = True
            content = re.sub(r'^\d+\. ', '', line.strip())
            new_lines.append(f'<li>{content}</li>')
        else:
            if in_list:
                if '<ol>' in new_lines[-2]:
                    new_lines.append('</ol>')
                else:
                    new_lines.append('</ul>')
                in_list = False
            if line.strip() and not line.strip().startswith('<'):
                new_lines.append(f'<p>{line}</p>')
            else:
                new_lines.append(line)
    
    if in_list:
        new_lines.append('</ul>')
    
    html = '\n'.join(new_lines)
    
    # Convert blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Convert success/warning/error markers
    html = re.sub(r'✅', '<span class="success">✅</span>', html)
    html = re.sub(r'❌', '<span class="error">❌</span>', html)
    html = re.sub(r'⚠️', '<span class="warning">⚠️</span>', html)
    
    return html

def create_pdf_from_markdown(md_file, output_pdf=None):
    """Create PDF from markdown file"""
    try:
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to HTML
        html_content = markdown_to_html_simple(md_content)
        
        # Add special formatting for executive summary
        if "## Executive Summary" in html_content:
            html_content = html_content.replace(
                "<h2>Executive Summary</h2>",
                '<div class="executive-summary"><h2>Executive Summary</h2>'
            )
            # Find the end of executive summary (next h2 or h1)
            import re
            match = re.search(r'(<h[12]>)', html_content.split('<div class="executive-summary">')[1])
            if match:
                pos = html_content.find(match.group(0), html_content.find('<div class="executive-summary">'))
                html_content = html_content[:pos] + '</div>\n' + html_content[pos:]
        
        # Create full HTML
        date_str = datetime.now().strftime("%B %d, %Y")
        full_html = HTML_TEMPLATE.format(content=html_content, date=date_str)
        
        # Save HTML temporarily
        html_file = '/tmp/ubc_report_temp.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        # Generate output filename
        if output_pdf is None:
            base_name = os.path.splitext(os.path.basename(md_file))[0]
            timestamp = datetime.now().strftime("%Y%m%d")
            output_pdf = f"{base_name}_{timestamp}.pdf"
        
        print(f"Creating professional PDF: {output_pdf}")
        
        # Try different PDF generation methods
        try:
            # Method 1: Using weasyprint (best quality)
            from weasyprint import HTML as WeasyHTML
            WeasyHTML(filename=html_file).write_pdf(output_pdf)
            print(f"✅ PDF created successfully using WeasyPrint: {output_pdf}")
            return output_pdf
        except ImportError:
            print("WeasyPrint not installed. Trying alternative method...")
        
        try:
            # Method 2: Using wkhtmltopdf via subprocess
            import subprocess
            cmd = [
                'wkhtmltopdf',
                '--enable-local-file-access',
                '--page-size', 'A4',
                '--margin-top', '25mm',
                '--margin-bottom', '25mm',
                '--margin-left', '25mm',
                '--margin-right', '25mm',
                html_file,
                output_pdf
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ PDF created successfully using wkhtmltopdf: {output_pdf}")
            return output_pdf
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("wkhtmltopdf not available. Trying Chrome/Chromium...")
        
        try:
            # Method 3: Using Chrome/Chromium headless
            import subprocess
            for browser in ['google-chrome', 'chromium-browser', 'chromium']:
                try:
                    cmd = [
                        browser,
                        '--headless',
                        '--disable-gpu',
                        '--print-to-pdf=' + output_pdf,
                        html_file
                    ]
                    subprocess.run(cmd, check=True, capture_output=True)
                    print(f"✅ PDF created successfully using {browser}: {output_pdf}")
                    return output_pdf
                except FileNotFoundError:
                    continue
        except:
            pass
        
        # If all methods fail, at least save the HTML
        final_html = output_pdf.replace('.pdf', '.html')
        os.rename(html_file, final_html)
        print(f"⚠️  Could not create PDF. HTML version saved as: {final_html}")
        print("To create PDF, install one of: weasyprint, wkhtmltopdf, or Chrome/Chromium")
        return None
        
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        return None

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python create_professional_pdf.py <markdown_file> [output_pdf]")
        print("\nExample:")
        print("  python create_professional_pdf.py universe_engine_audit.md")
        print("  python create_professional_pdf.py report.md UBC_Analysis_2024.pdf")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(md_file):
        print(f"Error: File {md_file} not found")
        sys.exit(1)
    
    pdf_file = create_pdf_from_markdown(md_file, output_pdf)
    
    if pdf_file and os.path.exists(pdf_file):
        size_kb = os.path.getsize(pdf_file) / 1024
        print(f"\n📄 Professional PDF ready!")
        print(f"   File: {pdf_file}")
        print(f"   Size: {size_kb:.1f} KB")
        print(f"\nShare this PDF to demonstrate immediate professional value!")
    else:
        print("\n⚠️  PDF creation requires additional tools.")
        print("Quick fix: Install weasyprint with:")
        print("  pip install weasyprint")

if __name__ == "__main__":
    main()