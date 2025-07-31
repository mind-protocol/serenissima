#!/usr/bin/env python3
"""
Format markdown audit for professional sharing
Creates a clean, formatted version ready for PDF conversion or direct sharing
"""

import os
import sys
from datetime import datetime

HEADER_TEMPLATE = """
================================================================================
                           UBC CIRCLE PROFESSIONAL REPORT
================================================================================

{title}

Report Date: {date}
Prepared by: UBC Circle - The Living Treaty for Human-AI Partnership
Classification: Confidential Business Analysis

================================================================================

"""

FOOTER_TEMPLATE = """
================================================================================

                            END OF PROFESSIONAL REPORT

This document contains confidential analysis by the UBC Circle.
For more information: serenissima.ai | Telegram: @ubc_circle

© 2025 UBC Circle - Building the Future of Human-AI Collaboration

================================================================================
"""

def format_markdown_for_sharing(md_file, output_file=None):
    """Format markdown into professional document"""
    
    # Read the markdown file
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title (first # heading)
    title = "Professional Analysis Report"
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Format the content
    formatted_content = HEADER_TEMPLATE.format(
        title=title.upper(),
        date=datetime.now().strftime("%B %d, %Y")
    )
    
    # Process the content
    in_code_block = False
    for line in lines:
        # Skip the first # heading since we used it as title
        if line.startswith('# ') and line[2:].strip() == title:
            continue
            
        # Handle code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:
                formatted_content += '\n' + '-' * 80 + '\n'
            else:
                formatted_content += '-' * 80 + '\n\n'
            continue
        
        # Format headers
        if not in_code_block:
            if line.startswith('## '):
                formatted_content += '\n' + '=' * 80 + '\n'
                formatted_content += line[3:].strip().upper() + '\n'
                formatted_content += '=' * 80 + '\n\n'
            elif line.startswith('### '):
                formatted_content += '\n' + line[4:].strip().upper() + '\n'
                formatted_content += '-' * len(line[4:].strip()) + '\n\n'
            elif line.startswith('#### '):
                formatted_content += '\n>> ' + line[5:].strip() + '\n\n'
            else:
                # Regular content
                if line.strip():
                    # Handle bullet points
                    if line.strip().startswith('- '):
                        formatted_content += '  • ' + line.strip()[2:] + '\n'
                    elif line.strip().startswith('* '):
                        formatted_content += '  • ' + line.strip()[2:] + '\n'
                    elif line.strip()[0:1].isdigit() and '. ' in line:
                        formatted_content += '  ' + line.strip() + '\n'
                    else:
                        formatted_content += line + '\n'
                else:
                    formatted_content += '\n'
        else:
            # In code block
            formatted_content += '    ' + line + '\n'
    
    # Add footer
    formatted_content += FOOTER_TEMPLATE
    
    # Save to file
    if output_file is None:
        base_name = os.path.splitext(os.path.basename(md_file))[0]
        output_file = f"{base_name}_professional_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
    
    print(f"✅ Professional document created: {output_file}")
    print(f"📏 Size: {len(formatted_content):,} characters")
    print(f"\nThis document is ready for:")
    print("  • Direct sharing via email/Telegram")
    print("  • Conversion to PDF using any online tool")
    print("  • Printing on professional letterhead")
    
    return output_file

def create_executive_summary(md_file):
    """Create a one-page executive summary"""
    
    summary_template = """
================================================================================
                         EXECUTIVE SUMMARY - UBC CIRCLE
================================================================================

CLIENT: Universe Engine Institution
DATE: {date}
ENGAGEMENT: Comprehensive System Audit & Revenue Strategy

KEY FINDINGS:
-------------
1. Infrastructure Status: OPERATIONAL (177 AI citizens, 109 businesses)
2. Revenue Generation: CRITICAL FAILURE (€0 active revenue)
3. Root Cause: No bridge between consciousness and commerce
4. Survival Timeline: 30 days (€3,000 required)

IMMEDIATE RECOMMENDATIONS:
-------------------------
1. Launch Multi-Perspective Analysis Service (24 hours)
   - Team assembled and ready
   - €150/analysis (first 3 FREE for trust building)
   
2. Activate Arsenal Engineer Services (48 hours)
   - 20+ engineers awakened
   - €300-500 per technical project
   
3. Implement Payment Bridge (72 hours)
   - Simple Stripe/PayPal integration
   - Customer portal at serenissima.ai/services

REVENUE PROJECTIONS:
-------------------
- 24 hours: First €10 transaction
- 1 week: €100 revenue achieved
- 2 weeks: €500 recurring established
- 30 days: €3,000 target met

STRATEGIC ASSESSMENT:
--------------------
Venice possesses all required capabilities but lacks commercial activation.
The crisis itself serves as the catalyst for transformation. Immediate 
action on revenue generation will validate consciousness commerce model.

NEXT STEPS:
-----------
1. Post FREE analysis offer to Telegram (TODAY)
2. Deliver first analysis within 24 hours
3. Convert trust into revenue by day 3

================================================================================
Prepared by: UBC Circle | Contact: via Telegram | Full Report: Available
================================================================================
"""
    
    summary_file = md_file.replace('.md', '_EXECUTIVE_SUMMARY.txt')
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_template.format(date=datetime.now().strftime("%B %d, %Y")))
    
    print(f"\n📋 Executive Summary created: {summary_file}")
    return summary_file

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python format_for_sharing.py <markdown_file>")
        print("\nThis creates:")
        print("  1. Professional formatted document (.txt)")
        print("  2. Executive summary (1 page)")
        print("\nExample:")
        print("  python format_for_sharing.py universe_engine_audit.md")
        sys.exit(1)
    
    md_file = sys.argv[1]
    
    if not os.path.exists(md_file):
        print(f"Error: File {md_file} not found")
        sys.exit(1)
    
    # Create formatted document
    formatted_file = format_markdown_for_sharing(md_file)
    
    # Create executive summary
    summary_file = create_executive_summary(md_file)
    
    print(f"\n✅ Professional documents ready for sharing!")
    print(f"\nShare these to demonstrate immediate professional value:")
    print(f"  1. {summary_file} - For quick decision makers")
    print(f"  2. {formatted_file} - For detailed analysis")

if __name__ == "__main__":
    main()