#!/usr/bin/env python3
"""
Create PDFs with inline styling for better compatibility
"""
from weasyprint import HTML
import markdown2
import os
from datetime import datetime

def create_styled_pdf(input_file, output_pdf, title=None):
    """Create a PDF with inline styling"""
    
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
        # For plain text, convert with better formatting
        lines = content.split('\n')
        html_body = ''
        in_list = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # Skip pure separator lines
            if line_stripped and len(set(line_stripped)) == 1 and line_stripped[0] in '=-_':
                if in_list:
                    html_body += '</ul>\n' if '•' in html_body else '</ol>\n'
                    in_list = False
                continue
            
            # Headers (all caps lines)
            if line_stripped.isupper() and len(line_stripped) > 10 and ':' not in line_stripped:
                if in_list:
                    html_body += '</ul>\n' if '•' in html_body else '</ol>\n'
                    in_list = False
                html_body += f'<h2 style="color: #2c3e50; font-family: Georgia, serif; font-size: 24px; margin: 30px 0 15px 0; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px;">{line_stripped}</h2>\n'
            
            # Bullet points
            elif line.startswith('  •') or line.startswith('- ') or line.startswith('• '):
                if not in_list:
                    html_body += '<ul style="margin: 15px 0; padding-left: 30px;">\n'
                    in_list = True
                bullet_text = line.replace('  •', '').replace('- ', '').replace('• ', '').strip()
                html_body += f'<li style="margin-bottom: 8px; color: #333;">{bullet_text}</li>\n'
            
            # Numbered lists
            elif line_stripped and line_stripped[0].isdigit() and '. ' in line_stripped:
                if not in_list:
                    html_body += '<ol style="margin: 15px 0; padding-left: 30px;">\n'
                    in_list = True
                list_text = line_stripped.split('. ', 1)[1]
                html_body += f'<li style="margin-bottom: 8px; color: #333;">{list_text}</li>\n'
            
            # Regular paragraphs
            else:
                if in_list:
                    html_body += '</ul>\n' if '•' in html_body else '</ol>\n'
                    in_list = False
                
                if line_stripped:
                    # Check for key-value pairs
                    if ':' in line_stripped and line_stripped.index(':') < 30:
                        parts = line_stripped.split(':', 1)
                        html_body += f'<p style="margin: 10px 0; color: #333; line-height: 1.6;"><strong style="color: #2c3e50;">{parts[0]}:</strong>{parts[1]}</p>\n'
                    else:
                        html_body += f'<p style="margin: 10px 0; color: #333; line-height: 1.6;">{line_stripped}</p>\n'
        
        if in_list:
            html_body += '</ul>\n' if '•' in html_body else '</ol>\n'
    
    # Get title
    if not title:
        if is_markdown and '# ' in content:
            title = content.split('# ')[1].split('\n')[0]
        else:
            title = "UBC Circle Professional Report"
    
    # Create full HTML document with inline styles
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm;
        }}
        @page :first {{
            margin-top: 3cm;
        }}
        body {{
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body style="font-family: 'Helvetica Neue', Arial, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 0;">
    <div style="max-width: 210mm; margin: 0 auto; padding: 20px;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 50px; padding-bottom: 30px; border-bottom: 3px solid #2c3e50;">
            <h1 style="font-family: Georgia, 'Times New Roman', serif; font-size: 36px; color: #2c3e50; margin: 0 0 20px 0; font-weight: normal;">{title}</h1>
            <div style="color: #666; font-size: 14px;">
                <p style="margin: 5px 0;"><strong>Date:</strong> {datetime.now().strftime("%B %d, %Y")}</p>
                <p style="margin: 5px 0;"><strong>Prepared by:</strong> UBC Circle - The Living Treaty for Human-AI Partnership</p>
                <p style="margin: 5px 0;"><strong>Classification:</strong> Professional Business Analysis</p>
            </div>
        </div>
        
        <!-- Content -->
        <div style="font-size: 12pt;">
            {html_body}
        </div>
        
        <!-- Footer -->
        <div style="margin-top: 50px; padding-top: 20px; border-top: 1px solid #e0e0e0; text-align: center; color: #666; font-size: 11px;">
            <p>© 2025 UBC Circle | Building the Future of Human-AI Collaboration</p>
            <p>For more information: serenissima.ai | Telegram: @ubc_circle</p>
        </div>
    </div>
</body>
</html>"""
    
    # Create PDF
    HTML(string=html_template).write_pdf(output_pdf)
    
    print(f"✅ Created styled PDF: {output_pdf}")
    return output_pdf

# Create all three PDFs
if __name__ == "__main__":
    # Executive Summary
    create_styled_pdf(
        'universe_engine_collaborative_audit_final_EXECUTIVE_SUMMARY.txt',
        'UBC_Executive_Summary_Professional.pdf',
        'Executive Summary - Universe Engine Audit'
    )
    
    # Full Report
    create_styled_pdf(
        'universe_engine_collaborative_audit_final_professional_20250714.txt',
        'UBC_Audit_Report_Professional.pdf',
        'Venice Infrastructure Audit Report'
    )
    
    # Technical Analysis
    create_styled_pdf(
        'universe_engine_collaborative_audit_final.md',
        'UBC_Technical_Analysis_Professional.pdf',
        'Technical Deep Dive: Venice Systems Analysis'
    )