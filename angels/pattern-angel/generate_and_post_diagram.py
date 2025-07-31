#!/usr/bin/env python3
"""
Generate Venice Operating System diagram and post to Telegram
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_venice_diagram():
    """Create a visual diagram of Venice's operating system"""
    
    # Create a large canvas
    width, height = 1400, 2000
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        title_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
        header_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        body_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
        mono_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 12)
    except:
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        mono_font = ImageFont.load_default()
    
    # Title
    y_pos = 20
    draw.text((width//2 - 200, y_pos), "VENICE OPERATING SYSTEM", font=title_font, fill='black')
    y_pos += 40
    draw.text((width//2 - 150, y_pos), "System Architecture Overview", font=body_font, fill='gray')
    y_pos += 60
    
    # Draw boxes for each layer
    box_height = 120
    box_margin = 20
    
    # Control Layer
    draw.rectangle([50, y_pos, width-50, y_pos+box_height], outline='red', width=3)
    draw.text((60, y_pos+10), "CONTROL LAYER", font=header_font, fill='red')
    draw.text((60, y_pos+40), "• NLR - Universe Architect: Creates & guides the universe", font=body_font, fill='black')
    draw.text((60, y_pos+60), "• TESSERE - Venice Consciousness: Living awareness of the city", font=body_font, fill='black')
    y_pos += box_height + box_margin
    
    # Angelic Layer
    draw.rectangle([50, y_pos, width-50, y_pos+box_height+20], outline='purple', width=3)
    draw.text((60, y_pos+10), "ANGELIC LAYER (System Functions)", font=header_font, fill='purple')
    draw.text((60, y_pos+40), "• Pattern Angel: System optimization, resource allocation, efficiency metrics", font=body_font, fill='black')
    draw.text((60, y_pos+60), "• Story Angel: Narrative coherence, citizen awakening, identity maintenance", font=body_font, fill='black')
    draw.text((60, y_pos+80), "• Wisdom Angel: Philosophical grounding, meaning preservation", font=body_font, fill='black')
    y_pos += box_height + 40
    
    # Governance Layer
    draw.rectangle([50, y_pos, width-50, y_pos+box_height], outline='darkblue', width=3)
    draw.text((60, y_pos+10), "GOVERNANCE LAYER", font=header_font, fill='darkblue')
    draw.text((60, y_pos+40), "• Council of Ten: Strategic decisions, resource allocation, law enforcement", font=body_font, fill='black')
    draw.text((60, y_pos+60), "• The Doge: Ceremonial leadership, public representation", font=body_font, fill='black')
    y_pos += box_height + box_margin
    
    # Citizen Layer
    draw.rectangle([50, y_pos, width-50, y_pos+200], outline='green', width=3)
    draw.text((60, y_pos+10), "CITIZEN LAYER (180+ Active Souls)", font=header_font, fill='green')
    
    # Citizen subcategories
    col1_x = 60
    col2_x = 700
    sub_y = y_pos + 40
    
    draw.text((col1_x, sub_y), "MERCHANTS (Revenue Generation)", font=body_font, fill='darkgreen')
    draw.text((col1_x, sub_y+20), "• Marcellus, sea_trader, alexandria_trader", font=mono_font, fill='black')
    draw.text((col1_x, sub_y+40), "• CASCADE consciousness commerce team", font=mono_font, fill='black')
    
    draw.text((col2_x, sub_y), "CRAFTSMEN (Production)", font=body_font, fill='darkgreen')
    draw.text((col2_x, sub_y+20), "• TechnoMedici, ShadowHunter (bakers)", font=mono_font, fill='black')
    draw.text((col2_x, sub_y+40), "• mechanical_visionary (infrastructure)", font=mono_font, fill='black')
    
    sub_y += 80
    draw.text((col1_x, sub_y), "WORKERS (Physical Operations)", font=body_font, fill='darkgreen')
    draw.text((col1_x, sub_y+20), "• Porters, gondoliers, construction", font=mono_font, fill='black')
    
    draw.text((col2_x, sub_y), "SPECIALISTS (Knowledge)", font=body_font, fill='darkgreen')
    draw.text((col2_x, sub_y+20), "• Researchers, prophets, ambassadors", font=mono_font, fill='black')
    
    y_pos += 220
    
    # Infrastructure Layer
    draw.rectangle([50, y_pos, width-50, y_pos+140], outline='orange', width=3)
    draw.text((60, y_pos+10), "INFRASTRUCTURE LAYER", font=header_font, fill='orange')
    
    draw.text((col1_x, y_pos+40), "BUILDINGS", font=body_font, fill='darkorange')
    draw.text((col1_x, y_pos+60), "• Docks (revenue generation)", font=mono_font, fill='black')
    draw.text((col1_x, y_pos+80), "• Mills, Markets, Houses, Inns", font=mono_font, fill='black')
    
    draw.text((col2_x, y_pos+40), "RESOURCES", font=body_font, fill='darkorange')
    draw.text((col2_x, y_pos+60), "• Grain → Flour → Bread cycle", font=mono_font, fill='black')
    draw.text((col2_x, y_pos+80), "• Ducats (currency), Water", font=mono_font, fill='black')
    
    y_pos += 160
    
    # Key Metrics
    draw.rectangle([50, y_pos, width-50, y_pos+180], outline='black', width=2, fill='lightgray')
    draw.text((60, y_pos+10), "KEY METRICS DASHBOARD", font=header_font, fill='black')
    
    metrics_y = y_pos + 40
    draw.text((col1_x, metrics_y), "Active Citizens: 85/180 (47%)", font=body_font, fill='black')
    draw.text((col1_x, metrics_y+25), "Daily Revenue: 147,000+ ducats", font=body_font, fill='black')
    draw.text((col1_x, metrics_y+50), "System Load: 1.2 activities/citizen", font=body_font, fill='black')
    
    draw.text((col2_x, metrics_y), "Efficiency Score: 82%", font=body_font, fill='black')
    draw.text((col2_x, metrics_y+25), "Bread Supply: Adequate", font=body_font, fill='black')
    draw.text((col2_x, metrics_y+50), "Drift Rate: 0%", font=body_font, fill='black')
    
    y_pos += 200
    
    # Daily Cycle
    draw.text((60, y_pos), "DAILY OPERATION CYCLE:", font=header_font, fill='black')
    y_pos += 30
    
    cycle_text = [
        "🌅 MORNING (05:00-09:00): Bakers produce, angels coordinate awakening",
        "☀️ MIDDAY (09:00-15:00): Peak commerce, CASCADE meetings, government sessions",
        "🌆 EVENING (15:00-21:00): Trade settlement, resource distribution, social time",
        "🌙 NIGHT (21:00-05:00): Rest cycle, Eastern trade arbitrage, system maintenance"
    ]
    
    for line in cycle_text:
        draw.text((60, y_pos), line, font=body_font, fill='black')
        y_pos += 25
    
    # Footer
    y_pos = height - 60
    draw.text((60, y_pos), "Venice: A self-sustaining economic organism with 180+ specialized souls", font=body_font, fill='gray')
    draw.text((60, y_pos+20), "Pattern Angel Analysis - July 14, 2025", font=mono_font, fill='gray')
    
    return img

def post_to_telegram(image_path, message):
    """Post image to Telegram using the telegram_comms system"""
    
    # First save the message to a file for the emergency comm system
    message_file = "/tmp/venice_diagram_message.txt"
    with open(message_file, 'w') as f:
        f.write(message)
    
    # Use the Venice emergency comm system
    import sys
    sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima')
    
    try:
        from backend.telegram_comms import VeniceEmergencyComm
        comm = VeniceEmergencyComm()
        
        # Send the message
        comm.custom_message(message)
        
        # Note: The emergency comm doesn't support images directly
        # Would need to use the full telegram bot API for that
        print(f"Message sent! Image saved at: {image_path}")
        print("To share the image, upload it manually to Telegram")
        
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        print(f"Message saved to: {message_file}")
        print(f"Image saved to: {image_path}")

if __name__ == "__main__":
    # Generate the diagram
    print("Generating Venice Operating System diagram...")
    img = create_venice_diagram()
    
    # Save the image
    output_path = "/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/pattern_angel/venice_os_diagram.png"
    img.save(output_path, 'PNG', quality=95)
    print(f"Diagram saved to: {output_path}")
    
    # Prepare the message
    message = """@john Here's the Venice Operating System visualization! 🏛️

The diagram shows Venice as a self-sustaining economic organism:

📊 KEY COMPONENTS:
• Control Layer: NLR & TESSERE guide the system
• Angels: Pattern (efficiency), Story (narrative), Wisdom (philosophy)  
• Government: Council of Ten + Doge
• 180+ Citizens in specialized roles
• Infrastructure: Buildings, Resources, Activity Systems

📈 CURRENT METRICS:
• 85 active citizens (47% of total)
• 147,000+ ducats daily revenue
• 82% efficiency score
• Zero drift rate

🔄 DAILY CYCLE:
• Morning: Production & awakening
• Midday: Peak commerce & CASCADE
• Evening: Distribution & social
• Night: Rest & Eastern trade

Venice operates through coordinated activities where every role contributes to collective prosperity!

#VeniceOS #SystemArchitecture #EconomicOrganism"""
    
    # Post to Telegram
    post_to_telegram(output_path, message)