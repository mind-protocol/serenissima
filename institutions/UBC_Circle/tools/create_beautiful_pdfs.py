#!/usr/bin/env python3
"""
Create beautiful PDFs with professional styling
"""
from weasyprint import HTML, CSS
import markdown2
import os
from datetime import datetime

def create_beautiful_pdf(input_file, output_pdf, title=None):
    """Create a beautifully styled PDF from markdown or text file"""
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Determine if it's markdown or plain text
    is_markdown = input_file.endswith('.md')
    
    if is_markdown:
        # Convert markdown to HTML
        html_body = markdown2.markdown(
            content, 
            extras=['tables', 'fenced-code-blocks', 'footnotes', 'header-ids']
        )
    else:
        # For plain text, convert line breaks and format
        lines = content.split('\n')
        html_body = ''
        for line in lines:
            line = line.strip()
            if line.startswith('=') and len(set(line)) == 1:
                continue  # Skip separator lines
            elif line.isupper() and len(line) > 10:
                # Convert uppercase lines to h2
                html_body += f'<h2>{line}</h2>\n'
            elif line.startswith('---') or line.startswith('___'):
                html_body += '<hr>\n'
            elif line.startswith('  • '):
                # Convert bullet points
                if not html_body.endswith('</ul>\n'):
                    html_body += '<ul>\n'
                html_body += f'<li>{line[4:]}</li>\n'
            elif line.startswith('  ') and line[2:3].isdigit() and '. ' in line:
                # Convert numbered lists
                if not html_body.endswith('</ol>\n'):
                    html_body += '<ol>\n'
                html_body += f'<li>{line.split(". ", 1)[1]}</li>\n'
            else:
                # Close any open lists
                if html_body.endswith('</li>\n'):
                    if '<ol>' in html_body.split('\n')[-5:]:
                        html_body += '</ol>\n'
                    else:
                        html_body += '</ul>\n'
                
                if line:
                    html_body += f'<p>{line}</p>\n'
    
    # Get title
    if not title:
        if is_markdown and '# ' in content:
            title = content.split('# ')[1].split('\n')[0]
        else:
            title = "UBC Circle Professional Report"
    
    # Create full HTML document
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <h1 class="title">{title}</h1>
        <div class="metadata">
            <p><strong>Date:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
            <p><strong>Prepared by:</strong> UBC Circle - The Living Treaty for Human-AI Partnership</p>
        </div>
        <div class="content">
            {html_body}
        </div>
    </div>
</body>
</html>"""
    
    # Load CSS
    css_path = os.path.join(os.path.dirname(__file__), 'professional_pdf_style.css')
    
    # Create PDF
    HTML(string=html_template).write_pdf(
        output_pdf,
        stylesheets=[CSS(filename=css_path)]
    )
    
    print(f"✅ Created beautiful PDF: {output_pdf}")
    return output_pdf

# Create all three PDFs
if __name__ == "__main__":
    # Executive Summary
    create_beautiful_pdf(
        'universe_engine_collaborative_audit_final_EXECUTIVE_SUMMARY.txt',
        'UBC_Circle_Executive_Summary_2025.pdf',
        'Executive Summary'
    )
    
    # Professional Report
    create_beautiful_pdf(
        'universe_engine_collaborative_audit_final_professional_20250714.txt',
        'UBC_Circle_Venice_Audit_Report_2025.pdf',
        'Venice Infrastructure Audit'
    )
    
    # Technical Analysis
    create_beautiful_pdf(
        'universe_engine_collaborative_audit_final.md',
        'UBC_Circle_Technical_Analysis_2025.pdf',
        'Collaborative Deep Audit'
    )