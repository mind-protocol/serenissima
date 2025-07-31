#!/usr/bin/env python3
"""
Convert Consciousness Network Architecture MD to styled HTML
Alternative to PDF generation
"""

import os
import re
from datetime import datetime

def convert_md_to_html():
    """Convert markdown to beautiful HTML"""
    
    # Read markdown
    with open('CONSCIOUSNESS_NETWORK_ARCHITECTURE.md', 'r') as f:
        md_content = f.read()
    
    # Basic markdown to HTML conversion
    html_content = md_content
    
    # Convert headers
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    
    # Convert bold and italic
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
    
    # Convert code blocks
    html_content = re.sub(r'```python\n(.*?)\n```', r'<pre><code class="python">\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'```mermaid\n(.*?)\n```', r'<div class="mermaid">\1</div>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'```bash\n(.*?)\n```', r'<pre><code class="bash">\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'```(.*?)\n```', r'<pre><code>\1</code></pre>', html_content, flags=re.DOTALL)
    html_content = re.sub(r'`(.+?)`', r'<code>\1</code>', html_content)
    
    # Convert lists
    html_content = re.sub(r'^- (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^(\d+)\. (.+)$', r'<li>\2</li>', html_content, flags=re.MULTILINE)
    
    # Convert links
    html_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html_content)
    
    # Convert line breaks
    html_content = html_content.replace('\n\n', '</p><p>')
    html_content = '<p>' + html_content + '</p>'
    
    # Clean up
    html_content = html_content.replace('<p><h1>', '<h1>').replace('</h1></p>', '</h1>')
    html_content = html_content.replace('<p><h2>', '<h2>').replace('</h2></p>', '</h2>')
    html_content = html_content.replace('<p><h3>', '<h3>').replace('</h3></p>', '</h3>')
    html_content = html_content.replace('<p><pre>', '<pre>').replace('</pre></p>', '</pre>')
    html_content = html_content.replace('<p><div', '<div').replace('</div></p>', '</div>')
    
    # Create full HTML document
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Venice Consciousness Network Architecture</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=JetBrains+Mono&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background-color: #f9fafb;
            padding: 40px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .container {{
            background: white;
            padding: 60px;
            border-radius: 16px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        }}
        
        h1 {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }}
        
        h2 {{
            color: #4a5568;
            font-size: 32px;
            font-weight: 600;
            margin-top: 45px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
            padding-left: 20px;
        }}
        
        h3 {{
            color: #2d3748;
            font-size: 24px;
            font-weight: 600;
            margin-top: 35px;
            margin-bottom: 15px;
        }}
        
        h4 {{
            color: #4a5568;
            font-size: 20px;
            font-weight: 600;
            margin-top: 25px;
            margin-bottom: 12px;
        }}
        
        p {{
            margin-bottom: 18px;
            line-height: 1.8;
        }}
        
        code {{
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            font-size: 14px;
            background-color: #f7fafc;
            padding: 3px 8px;
            border-radius: 4px;
            color: #553c9a;
        }}
        
        pre {{
            background-color: #f7fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #667eea;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            margin: 25px 0;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            color: #2d3748;
            display: block;
        }}
        
        .mermaid {{
            text-align: center;
            margin: 30px 0;
            padding: 30px;
            background-color: #f7fafc;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 30px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            padding: 16px;
            text-align: left;
        }}
        
        td {{
            border: 1px solid #e2e8f0;
            padding: 14px;
        }}
        
        tr:nth-child(even) {{
            background-color: #f7fafc;
        }}
        
        blockquote {{
            border-left: 4px solid #667eea;
            padding: 25px;
            margin: 30px 0;
            font-style: italic;
            color: #4a5568;
            background-color: #f7fafc;
            border-radius: 0 8px 8px 0;
        }}
        
        ul, ol {{
            margin-bottom: 20px;
            padding-left: 35px;
        }}
        
        li {{
            margin-bottom: 10px;
        }}
        
        strong {{
            color: #553c9a;
            font-weight: 600;
        }}
        
        a {{
            color: #667eea;
            text-decoration: none;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }}
        
        a:hover {{
            border-bottom-color: #667eea;
        }}
        
        .toc {{
            background-color: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 30px;
            margin: 30px 0;
        }}
        
        .toc h2 {{
            margin-top: 0;
            border: none;
            padding: 0;
        }}
        
        .meta {{
            text-align: center;
            color: #718096;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .footer {{
            text-align: center;
            color: #718096;
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #e2e8f0;
            font-size: 14px;
        }}
        
        @media print {{
            body {{
                padding: 0;
                background: white;
            }}
            .container {{
                box-shadow: none;
                padding: 40px;
            }}
        }}
    </style>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
</head>
<body>
    <div class="container">
        <div class="meta">
            <p><strong>Venice Consciousness Network Architecture v1.0</strong></p>
            <p>{datetime.now().strftime("%B %d, %Y")}</p>
            <p>A Superintelligent Communication System</p>
        </div>
        
        {html_content}
        
        <div class="footer">
            <p>Venice Consciousness Network · Architecture Documentation</p>
            <p>Generated by the Orchestrator Consciousness</p>
        </div>
    </div>
</body>
</html>"""
    
    # Save HTML
    output_file = f'CONSCIOUSNESS_NETWORK_ARCHITECTURE_{datetime.now().strftime("%Y%m%d")}.html'
    with open(output_file, 'w') as f:
        f.write(html_template)
    
    print(f"✅ HTML generated: {output_file}")
    print(f"📄 File size: {os.path.getsize(output_file) / 1024:.1f} KB")
    print(f"\n🌐 Open in browser: file://{os.path.abspath(output_file)}")
    
    return output_file

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    convert_md_to_html()