#!/usr/bin/env python3
"""
Venice Automation Systems - Pitch Audio Script Generator
Creates a 3-minute pitch script ready for TTS conversion
"""

def generate_pitch_script():
    """Generate the 3-minute pitch script"""
    
    script = """
Welcome, investors. I am Niccolò Barozzi, founder of Venice Automation Systems.

Let me share a simple truth: Every ducat you spend on labor costs more each year. 
Wages rise twenty percent annually. Workers operate twelve hours maximum. 
Errors cost fifteen percent of throughput.

I have the solution. Mechanical automation that works twenty-four seven.

At the Fondaco dei Tedeschi, merchants struggled to sort one hundred packages per hour. 
My automated sorting system now processes one thousand packages per hour. 
Ten times faster. Zero errors. Always running.

This is not theory. I operate five production mills generating five hundred ducats daily. 
My personal wealth of one point eight eight million ducats proves the model works.

The market opportunity is massive. Twenty-five hundred active merchants in Venice. 
Fifty million ducats in total addressable market. 
Eight merchants already wait in my sales pipeline.

Our business model is straightforward. Sorting systems at fifty thousand ducats. 
Production mills at one hundred fifty thousand ducats. 
Custom consulting at twenty-five thousand ducats per project. 
Customers see payback in six to twelve months.

Financial projections show exponential growth. Year one: one point five million ducats. 
Year two: four point five million. Year three: twelve million. 
By year five: twenty-five million in annual revenue.

Why will we succeed? First mover advantage with proven technology. 
Ten years of mechanical engineering experience. 
Backing from the elite Triumvirate Sapientiae guild. 
We even retrain displaced workers as operators at double wages.

I seek five hundred thousand ducats investment. Three hundred thousand builds demonstration facilities. 
One hundred thousand hires installation teams. One hundred thousand markets to merchant guilds. 
You will see three times return in eighteen months.

Venice stands at a crossroads. Continue with rising labor costs and limited output. 
Or embrace automation for sustainable growth.

I am already generating five hundred ducats per day. The pipeline is full. 
The technology is proven. The market is ready.

Join Venice Automation Systems. Real machines. Real savings. Real profit.

Thank you.
"""
    return script.strip()

def save_script_for_tts(filename="pitch_script.txt"):
    """Save the script in TTS-ready format"""
    script = generate_pitch_script()
    
    # Add timing markers for TTS
    tts_formatted = f"""
[VOICE: confident, professional, slight Italian accent]
[PACE: measured, clear]
[EMOTION: passionate about efficiency, proud of achievements]

{script}

[END]
"""
    
    with open(filename, 'w') as f:
        f.write(tts_formatted)
    
    print(f"Pitch script saved to {filename}")
    print(f"Word count: {len(script.split())}")
    print(f"Estimated speaking time: {len(script.split()) / 150:.1f} minutes")

def generate_qa_responses():
    """Generate Q&A response scripts"""
    
    qa_scripts = {
        "revenue_day_one.txt": """
[VOICE: confident, factual]
We are already generating five hundred ducats daily from five operational mills. 
Eight merchants wait in our pipeline for installations. 
Revenue begins immediately upon investment.
[END]
""",
        
        "competitive_moat.txt": """
[VOICE: assured, technical]
First mover advantage with six months head start. 
Proprietary mechanical designs protected by guild patents. 
Ten years engineering experience no competitor can match. 
Existing customer relationships and proven results.
[END]
""",
        
        "why_investors_choose.txt": """
[VOICE: persuasive, data-driven]
We deliver proven returns, not promises. 
Five operational mills already profitable. 
Six to twelve month customer payback documented. 
One point eight eight million ducats personal success proves the model.
Real machines generating real profit today.
[END]
"""
    }
    
    for filename, content in qa_scripts.items():
        with open(filename, 'w') as f:
            f.write(content.strip())
        print(f"Q&A script saved to {filename}")

if __name__ == "__main__":
    save_script_for_tts()
    generate_qa_responses()
    print("\nAll audio scripts generated successfully!")
    print("Ready for TTS conversion in Innovation District")