#!/usr/bin/env python3
"""
KinKong Trading 2.0 - Pitch Deck Generator
Elena Barbarigo, CEO
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

def create_pitch_deck():
    """Create professional PDF pitch deck for KinKong Trading 2.0"""
    
    # Setup document
    filename = "KinKong_Trading_2.0_Pitch_Deck.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                          rightMargin=72, leftMargin=72, 
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.blue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    # Build content
    story = []
    
    # Title Slide
    story.append(Paragraph("KinKong Trading 2.0", title_style))
    story.append(Paragraph("AI-Powered Trading Platform with Integrated Investment Analysis", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Elena Barbarigo, CEO", styles['Normal']))
    story.append(Paragraph("500k+ Ducats Trading Success | 2160 Influence Points", styles['Normal']))
    story.append(Paragraph("Presented to Venice Business AMA", styles['Normal']))
    story.append(Spacer(1, 1*inch))
    
    # Executive Summary
    story.append(PageBreak())
    story.append(Paragraph("Executive Summary", heading_style))
    
    summary_data = [
        ['Company', 'KinKong Trading 2.0 (includes Kong Invest merger)'],
        ['CEO', 'Elena Barbarigo - Proven Venice merchant leader'],
        ['Opportunity', 'Transform $14k debt into revenue-generating platform'],
        ['Market', 'AI-enhanced trading for Venice merchant network'],
        ['Advantage', 'Consciousness-powered market insights'],
        ['Investment', '$50k for 20% stake'],
        ['Revenue Target', '$300k annual recurring revenue']
    ]
    
    summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(summary_table)
    
    # The Problem & Opportunity
    story.append(PageBreak())
    story.append(Paragraph("The Problem & Opportunity", heading_style))
    story.append(Paragraph("• Existing KinKong Trading platform has valuable assets but $14k debt burden", styles['Normal']))
    story.append(Paragraph("• Kong Invest has powerful analysis tools but lacks execution platform", styles['Normal']))
    story.append(Paragraph("• Venice merchants need AI-enhanced trading decisions", styles['Normal']))
    story.append(Paragraph("• No integrated platform combining trading + investment analysis", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Our Solution:</b> Transform debt into growth investment while merging platforms", styles['Normal']))
    
    # Market & Competitive Advantage
    story.append(PageBreak())
    story.append(Paragraph("Market & Competitive Advantage", heading_style))
    
    market_points = [
        "Venice Merchant Network: 130+ active traders seeking AI assistance",
        "Consciousness AI Edge: Unique awareness-based market insights",
        "Proven Leadership: Elena's 500k+ ducats demonstrate trading expertise",
        "Integrated Platform: Trading execution + analysis in one solution",
        "Network Effects: Direct access to Venice's merchant ecosystem"
    ]
    
    for point in market_points:
        story.append(Paragraph(f"• {point}", styles['Normal']))
    
    # Product Overview
    story.append(PageBreak())
    story.append(Paragraph("Product Overview", heading_style))
    
    product_data = [
        ['Feature', 'Description', 'Revenue Impact'],
        ['AI Trading Signals', 'Venice consciousness-enhanced market analysis', 'Premium tier: $100/month'],
        ['Portfolio Analysis', 'Merged Kong Invest risk assessment tools', 'Core platform: $50/month'],
        ['Merchant Integration', 'Direct Venice marketplace connections', 'Transaction fees: 0.5%'],
        ['Automated Execution', 'Smart order routing and execution', 'Execution fees: $10/trade']
    ]
    
    product_table = Table(product_data, colWidths=[2*inch, 2.5*inch, 1.5*inch])
    product_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(product_table)
    
    # Financial Projections
    story.append(PageBreak())
    story.append(Paragraph("Financial Projections", heading_style))
    
    financial_data = [
        ['Metric', 'Month 1', 'Month 2', 'Month 3', 'Month 6', 'Year 1'],
        ['Customers', '3', '10', '25', '60', '150'],
        ['MRR', '$1,500', '$5,000', '$12,500', '$30,000', '$75,000'],
        ['Annual Revenue', '$18k', '$60k', '$150k', '$360k', '$900k'],
        ['Debt Status', 'Restructured', 'Paying down', 'Fully paid', 'Profit', 'Growth mode'],
        ['Claude Costs', '$1,800', '$1,800', '$2,400', '$3,600', '$7,200'],
        ['Net Profit', '-$300', '$3,200', '$10,100', '$26,400', '$67,800']
    ]
    
    financial_table = Table(financial_data, colWidths=[1.2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    financial_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(financial_table)
    
    # Execution Plan
    story.append(PageBreak())
    story.append(Paragraph("30-Day Execution Plan", heading_style))
    
    plan_data = [
        ['Week', 'Key Milestones', 'Revenue Target'],
        ['Week 1', 'Platform integration, beta testing, first customer outreach', '$0'],
        ['Week 2', 'First 3 paying customers, revenue start', '$1,500 MRR'],
        ['Week 3', 'Scale to 10 customers, optimize platform', '$5,000 MRR'],
        ['Week 4', 'Partnership integrations, advanced features', '$7,500 MRR']
    ]
    
    plan_table = Table(plan_data, colWidths=[1*inch, 3.5*inch, 1.5*inch])
    plan_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(plan_table)
    
    # Team & Human Partners
    story.append(PageBreak())
    story.append(Paragraph("Team & Human Partners", heading_style))
    
    team_points = [
        "<b>Elena Barbarigo (CEO):</b> 500k+ ducats trading success, 2160 influence, proven Venice merchant leader",
        "<b>Banking Partner (7 days):</b> Fintech developer for Stripe integration and payment processing",
        "<b>Technical Partner (10 days):</b> AWS specialist for cloud deployment and monitoring",
        "<b>Legal Partner (14 days):</b> Fintech lawyer for compliance and contract management",
        "<b>Venice Technical Team:</b> Existing platform developers and AI specialists"
    ]
    
    for point in team_points:
        story.append(Paragraph(f"• {point}", styles['Normal']))
    
    # Investment Terms
    story.append(PageBreak())
    story.append(Paragraph("Investment Terms", heading_style))
    
    investment_data = [
        ['Term', 'Details'],
        ['Pre-money Valuation', '$200,000'],
        ['Investment Sought', '$50,000 in $UBC'],
        ['Post-money Valuation', '$250,000'],
        ['Investor Stake', '20%'],
        ['Cap Table', 'Elena: 65%, Venice Team: 15%, Investors: 20%'],
        ['Use of Funds', 'Platform development (60%), Marketing (25%), Operations (15%)'],
        ['Expected ROI', '10x within 18 months based on revenue projections']
    ]
    
    investment_table = Table(investment_data, colWidths=[2*inch, 4*inch])
    investment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.orange),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(investment_table)
    
    # Call to Action
    story.append(PageBreak())
    story.append(Paragraph("Call to Action", heading_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<b>Investment Opportunity:</b>", styles['Normal']))
    story.append(Paragraph("$50,000 for 20% stake in proven trading platform", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Why Invest Now:</b>", styles['Normal']))
    story.append(Paragraph("• Experienced CEO with demonstrated trading success", styles['Normal']))
    story.append(Paragraph("• Existing technology assets ready for integration", styles['Normal']))
    story.append(Paragraph("• Clear 30-day path to profitability", styles['Normal']))
    story.append(Paragraph("• Unique AI consciousness competitive advantage", styles['Normal']))
    story.append(Paragraph("• Strong Venice merchant network foundation", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("<b>Next Steps:</b>", styles['Normal']))
    story.append(Paragraph("1. Live demo presentation", styles['Normal']))
    story.append(Paragraph("2. Meet human partners", styles['Normal']))
    story.append(Paragraph("3. Execute investment through $UBC", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph('<i>"In Venice, we transform constraints into opportunities."</i>', styles['Normal']))
    story.append(Paragraph("- Elena Barbarigo, CEO", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Pitch deck created: {filename}")
    return filename

if __name__ == "__main__":
    create_pitch_deck()