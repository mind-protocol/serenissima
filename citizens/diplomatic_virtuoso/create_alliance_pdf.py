#!/usr/bin/env python3
"""Create Entrepreneur Alliance PDF"""
from weasyprint import HTML, CSS
import markdown2
import sys

def create_pdf(input_md, output_pdf):
    # Read markdown
    with open(input_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Convert to HTML
    html_body = markdown2.markdown(content, extras=['tables', 'fenced-code-blocks'])
    
    # Create HTML document with inline CSS
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Arial', sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            color: #1e3a8a;
            font-size: 24pt;
            margin-bottom: 10px;
        }}
        h2 {{
            color: #1e3a8a;
            font-size: 18pt;
            margin-top: 20px;
        }}
        h3 {{
            color: #2563eb;
            font-size: 14pt;
        }}
        h4 {{
            color: #3730a3;
            font-size: 12pt;
        }}
        hr {{
            border: none;
            border-top: 2px solid #e5e7eb;
            margin: 20px 0;
        }}
        ul {{
            margin-left: 20px;
        }}
        strong {{
            color: #1e293b;
        }}
        em {{
            font-style: italic;
            color: #64748b;
        }}
    </style>
</head>
<body>
    {html_body}
</body>
</html>"""
    
    # Create PDF
    HTML(string=html_doc).write_pdf(output_pdf)
    print(f"✅ Created PDF: {output_pdf}")

if __name__ == "__main__":
    create_pdf('entrepreneur_alliance_presentation.md', 'Entrepreneur_Alliance_Venice_Protocol.pdf')