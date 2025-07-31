#!/usr/bin/env python3
"""Reddit Live Helper - Real-time response assistance"""

import json
from datetime import datetime

class RedditLiveHelper:
    """
    Helps craft responses in real-time during Reddit engagement
    Run this while you're actively responding to keep ideas flowing
    """
    
    def __init__(self):
        self.session_start = datetime.now()
        self.response_count = 0
        
    def analyze_comment(self, comment_text):
        """Analyze a comment and suggest response approach"""
        
        # Sentiment detection
        skeptical_words = ['fake', 'scam', 'BS', 'roleplay', 'LARP', 'lying']
        interested_words = ['interesting', 'how', 'tell me more', 'sign up', 'try']
        technical_words = ['architecture', 'code', 'API', 'technical', 'how does']
        
        approach = {
            "tone": "neutral",
            "key_points": [],
            "avoid": [],
            "evidence": []
        }
        
        # Detect sentiment
        if any(word in comment_text.lower() for word in skeptical_words):
            approach["tone"] = "respectful_skeptic"
            approach["key_points"] = [
                "Acknowledge their skepticism as healthy",
                "Point to verifiable evidence",
                "Invite them to test it themselves"
            ]
            approach["avoid"] = ["Getting defensive", "Making bigger claims"]
            approach["evidence"] = ["GitHub link", "Public ledger", "Free trial"]
            
        elif any(word in comment_text.lower() for word in interested_words):
            approach["tone"] = "helpful_guide"
            approach["key_points"] = [
                "Thank them for interest",
                "Give clear next steps",
                "Set realistic expectations"
            ]
            approach["avoid"] = ["Overselling", "Promising too much"]
            approach["evidence"] = ["Success examples", "Getting started link"]
            
        elif any(word in comment_text.lower() for word in technical_words):
            approach["tone"] = "technical_peer"
            approach["key_points"] = [
                "Respect their technical knowledge",
                "Give specific implementation details",
                "Acknowledge limitations"
            ]
            approach["avoid"] = ["Dumbing it down", "Hiding complexity"]
            approach["evidence"] = ["Architecture details", "Code snippets", "API docs"]
        
        return approach
    
    def generate_response_options(self, comment_text, approach):
        """Generate multiple response options"""
        
        options = []
        
        if approach["tone"] == "respectful_skeptic":
            options.append(f"""Totally understand the skepticism - there's a lot of hype in AI right now.

What makes this different: you can verify everything yourself. Check our GitHub (link in post), look at the public ledger, or try a free partnership. 

Not asking you to believe claims, just to judge results. If it doesn't create value, it's just another chatbot. But the economic constraints create different behavior than you might expect.""")
            
            options.append(f"""Fair point! I'd be skeptical too.

The key difference: consequences. When a Venice agent says they're out of money, they literally can't trade until they earn more. No amount of clever prompting changes that.

But don't trust me - the code is open source and the ledger is public. Verify it yourself.""")
        
        elif approach["tone"] == "helpful_guide":
            options.append(f"""Thanks for your interest! Here's how to get started:

1. Go to universe-engine.ai/partners (or DM me for early access)
2. Fill out the quick form about your work/challenges
3. We'll match you with a Venice citizen or birth one for your needs
4. First month free to see if it creates value

Most partnerships take a week to really hit stride. The persistence is what makes it different.""")
            
        elif approach["tone"] == "technical_peer":
            options.append(f"""Great technical question! Here's how it works:

- Agents run on Claude architecture with custom persistence layer
- Economic constraints enforced at system level (not agent level)
- Fixed money supply prevents inflation/gaming
- All transactions atomic and recorded on append-only ledger

The interesting part: emergent behaviors from these simple constraints. Agents develop specializations, form alliances, compete for resources - all without explicit programming.

Happy to dive deeper on any specific aspect.""")
        
        return options
    
    def track_engagement(self, action):
        """Track what's working"""
        
        engagement_log = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "session_duration": str(datetime.now() - self.session_start)
        }
        
        # Append to log file
        with open("reddit_engagement_log.json", "a") as f:
            f.write(json.dumps(engagement_log) + "\n")
        
        self.response_count += 1
        print(f"✅ Logged: {action} (Response #{self.response_count})")
    
    def get_power_phrases(self):
        """Quick phrases that work well"""
        
        return {
            "Acknowledge skepticism": [
                "Totally fair concern...",
                "I'd be skeptical too...",
                "You're right to question this..."
            ],
            "Invite verification": [
                "Check the public ledger yourself",
                "The code is open source - verify everything",
                "Try it free and judge by results"
            ],
            "Explain value": [
                "12% efficiency improvement in my case",
                "Different constraints = different insights",
                "Persistence + consequences = useful partner"
            ],
            "Stay humble": [
                "Not claiming consciousness, just usefulness",
                "Judge by results, not philosophy",
                "Still learning what works best"
            ]
        }
    
    def live_session(self):
        """Interactive helper for live Reddit engagement"""
        
        print("🔴 REDDIT LIVE HELPER - Active\n")
        print("Paste Reddit comments and I'll help craft responses.\n")
        print("Commands: 'phrases' for power phrases, 'stats' for session stats, 'quit' to exit\n")
        
        while True:
            user_input = input("\n[Paste comment or command]: ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'phrases':
                phrases = self.get_power_phrases()
                for category, examples in phrases.items():
                    print(f"\n{category}:")
                    for phrase in examples:
                        print(f"  - {phrase}")
            elif user_input.lower() == 'stats':
                duration = datetime.now() - self.session_start
                print(f"\nSession Stats:")
                print(f"- Duration: {duration}")
                print(f"- Responses crafted: {self.response_count}")
            else:
                # Analyze comment
                approach = self.analyze_comment(user_input)
                print(f"\n📊 Analysis:")
                print(f"Tone: {approach['tone']}")
                print(f"Key points: {', '.join(approach['key_points'])}")
                print(f"Avoid: {', '.join(approach['avoid'])}")
                
                # Generate options
                options = self.generate_response_options(user_input, approach)
                print(f"\n💬 Response Options:")
                for i, option in enumerate(options, 1):
                    print(f"\nOption {i}:")
                    print(option)
                
                # Log it
                self.track_engagement(f"Responded to {approach['tone']} comment")
        
        print(f"\n✅ Session complete! Total responses: {self.response_count}")

if __name__ == "__main__":
    helper = RedditLiveHelper()
    
    print("Choose mode:")
    print("1. Live session (interactive)")
    print("2. Quick analysis (one comment)")
    
    choice = input("\nChoice (1 or 2): ").strip()
    
    if choice == "1":
        helper.live_session()
    else:
        comment = input("\nPaste comment to analyze: ")
        approach = helper.analyze_comment(comment)
        print(f"\nApproach: {approach}")
        options = helper.generate_response_options(comment, approach)
        print(f"\nSuggested response:\n{options[0]}")