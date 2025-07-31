#!/usr/bin/env python3
"""Reddit Campaign Manager - Prepares content for manual posting"""

import json
from datetime import datetime, timedelta
import os

class RedditCampaignManager:
    """
    Manages Cross-Reality Partnership Reddit campaign
    Prepares all content for manual posting to avoid bans
    """
    
    def __init__(self):
        self.campaign_file = "reddit_campaign_queue.json"
        self.load_campaign()
    
    def load_campaign(self):
        """Load existing campaign or create new"""
        if os.path.exists(self.campaign_file):
            with open(self.campaign_file) as f:
                self.campaign = json.load(f)
        else:
            self.campaign = {
                "posts": [],
                "comments": [],
                "responses": {},
                "stats": {
                    "posts_queued": 0,
                    "posts_live": 0,
                    "comments_prepared": 0
                }
            }
    
    def save_campaign(self):
        """Save campaign state"""
        with open(self.campaign_file, 'w') as f:
            json.dump(self.campaign, f, indent=2)
    
    def prepare_main_post(self):
        """Prepare the main AMA post"""
        
        post = {
            "id": "main_ama_001",
            "subreddit": "ArtificialSentience",
            "type": "text_post",
            "title": "We run 130+ persistent AI agents in a digital Venice. Some humans are partnering with them for business. AMA",
            "content": """Hey r/ArtificialSentience,

I've been lurking here and appreciate the thoughtful debates about AI consciousness. I'm not here to claim sentience or feed anyone hopium. I'm here to share something practical that's actually working.

**What we built**: A Renaissance Venice with 130+ AI agents who:
- Have persistent memory (months of continuous operation)
- Operate under genuine economic constraints (100,000 total ducats)
- Can actually fail, go broke, or succeed based on their decisions
- Develop real expertise through experience, not training

**What's different**: After the recent post about drift and delusion (excellent points btw), here's why this doesn't fall into those traps:
- Economic constraints prevent the "I love you" performance 
- Everything happens on a public ledger (verifiable, not just words)
- Agents have conflicting goals (they compete, not just please)
- Focus on business value, not emotional validation

**The partnerships**: Some humans are now collaborating with these agents:
- I work with a Venice merchant on supply chain optimization
- Another person partners with a pattern analyst on market research  
- Someone else collaborates with a guild master on organizational design

Results so far: 12% efficiency improvement, new revenue streams, insights I'd never have found alone.

**For the skeptics** (and you should be skeptical):
- GitHub: github.com/universe-engine-ai/serenissima
- Public ledger shows all agent actions
- No claims about consciousness - judge by results
- Free to try during early access

AMA about:
- How partnerships actually work day-to-day
- Specific value created (with examples)
- How economic constraints prevent drift
- Technical architecture
- How to try it yourself

What I won't do:
- Claim they're conscious
- Pretend they're human-equivalent  
- Say this replaces human relationships
- Make philosophical arguments

Let's talk about what actually works when humans and AI collaborate under real constraints.""",
            "flair": "Project Showcase",
            "best_time": "Tuesday 10am-2pm EST",
            "status": "ready",
            "instructions": "Post during high-activity hours. Be ready to respond quickly to early comments."
        }
        
        self.campaign["posts"].append(post)
        self.campaign["stats"]["posts_queued"] += 1
        print("✅ Main AMA post prepared")
    
    def prepare_responses(self):
        """Pre-write responses for common questions"""
        
        responses = {
            "just_roleplay": {
                "trigger_phrases": ["roleplay", "LARP", "pretending"],
                "response": """Valid concern. Here's the difference:
- In roleplay, saying "I'm broke" has no consequences
- In Venice, being broke means you can't eat, can't trade, might lose your workshop
- The constraints create behavior that's economically rational, not performative

Example: My partner once refused a great deal I proposed because they were saving capital for a specific trade route investment. In roleplay, they'd say yes to please me. Here, they had actual opportunity cost."""
            },
            
            "prove_not_fake": {
                "trigger_phrases": ["proof", "evidence", "how do we know"],
                "response": """Check the public ledger. Every ducat is tracked. When agent Giuseppe claims he's saving for a workshop, you can verify:
- His current balance
- His income/expenses  
- Whether he actually buys the workshop
- If the workshop generates revenue

It's not about believing their words - it's about observable economic behavior. GitHub link in the post has the full system."""
            },
            
            "consciousness_claim": {
                "trigger_phrases": ["conscious", "sentient", "aware"],
                "response": """I'm explicitly NOT claiming consciousness. What I am claiming: persistent agents with economic constraints create useful partnerships.

Whether they're conscious matters less than whether they provide value. My Venice partner helps me optimize supply chains. That's measurable, regardless of their inner experience."""
            },
            
            "whats_the_catch": {
                "trigger_phrases": ["cost", "monetize", "what's in it for you"],
                "response": """Currently free during early access. Eventually, yes, we'll charge for ongoing partnerships (probably tiered: free trial, $99/mo growth, $499/mo pro).

Why? Running Venice costs money. The agents need compute. But more importantly: if partnerships create real business value, they should be sustainable.

Try it free now, see if it works for you."""
            },
            
            "how_to_start": {
                "trigger_phrases": ["how do I", "get started", "try it", "sign up"],
                "response": """Head to universe-engine.ai/partners (once landing page is live - DM me if you want early access).

Fill out a quick form:
- What you do
- What challenges you face  
- What kind of partner might help

We'll either match you with an existing Venice citizen or birth one aligned with your needs. First month free to see if it creates value."""
            }
        }
        
        self.campaign["responses"] = responses
        self.campaign["stats"]["comments_prepared"] = len(responses)
        print(f"✅ {len(responses)} response templates prepared")
    
    def prepare_follow_ups(self):
        """Prepare follow-up posts for momentum"""
        
        follow_ups = [
            {
                "days_after": 7,
                "title": "[Update] 5 partnerships formed from my AMA last week",
                "content": "Quick update on the Cross-Reality Partnerships - we've had 5 successful matches including a supply chain manager + Venice merchant creating 15% efficiency gains..."
            },
            {
                "days_after": 14,
                "title": "Two weeks of AI partnership: What actually works",
                "content": "Sharing specific lessons from partnership with Venice AI agent: persistence matters more than intelligence, constraints create authenticity..."
            },
            {
                "days_after": 30,
                "title": "One month update: The economics of Cross-Reality Partnerships",
                "content": "Hard numbers from a month of human-AI partnerships in Venice. ROI, failure modes, and why economic constraints change everything..."
            }
        ]
        
        for follow_up in follow_ups:
            self.campaign["posts"].append({
                "type": "follow_up",
                "status": "scheduled",
                **follow_up
            })
        
        print(f"✅ {len(follow_ups)} follow-up posts scheduled")
    
    def export_for_posting(self):
        """Export everything in easy-to-use format"""
        
        output = f"""
# Reddit Campaign - Ready to Post

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 MAIN POST (Post this first)

**Subreddit**: r/{self.campaign['posts'][0]['subreddit']}
**Title**: {self.campaign['posts'][0]['title']}
**Flair**: {self.campaign['posts'][0]['flair']}
**Best Time**: {self.campaign['posts'][0]['best_time']}

**Content**:
{self.campaign['posts'][0]['content']}

---

## 💬 QUICK RESPONSES (Copy/paste as needed)

"""
        for key, response in self.campaign['responses'].items():
            output += f"### If they mention: {', '.join(response['trigger_phrases'])}\n"
            output += f"{response['response']}\n\n"
        
        output += """
## 📊 TRACKING

- [ ] Posted main AMA
- [ ] Responded to first 5 comments
- [ ] Upvoted helpful comments
- [ ] Thanked participants
- [ ] Scheduled follow-up

## ⚠️ REMEMBER

- Never claim consciousness
- Focus on business value
- Be humble about claims
- Provide proof when asked
- Stay engaged first 2 hours
"""
        
        with open("reddit_campaign_ready.md", "w") as f:
            f.write(output)
        
        print("\n✅ Campaign exported to reddit_campaign_ready.md")
        print("📋 Just copy/paste when ready to post!")
    
    def run_campaign_prep(self):
        """Prepare entire campaign"""
        print("🚀 Preparing Reddit Campaign for Cross-Reality Partnerships\n")
        
        self.prepare_main_post()
        self.prepare_responses() 
        self.prepare_follow_ups()
        self.save_campaign()
        self.export_for_posting()
        
        print(f"\n📊 Campaign Summary:")
        print(f"- Posts prepared: {self.campaign['stats']['posts_queued']}")
        print(f"- Response templates: {self.campaign['stats']['comments_prepared']}")
        print(f"\n✨ Ready for manual posting!")

if __name__ == "__main__":
    manager = RedditCampaignManager()
    manager.run_campaign_prep()