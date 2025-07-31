#!/usr/bin/env python3
"""
Autonomous AMA Monitor for diplomatic_virtuoso
Monitors Reddit via API and coordinates Venice responses
"""

import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

class RedditAMAMonitor:
    def __init__(self):
        self.subreddit = "ArtificialSentience"
        self.ama_post_id = None  # Will be set when AMA launches
        self.processed_comments = set()
        self.live_thread_path = '/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/reddit/ama_live_thread.md'
        
    def get_new_comments(self, post_url):
        """Fetch new comments from Reddit post"""
        # Add .json to get JSON response
        json_url = post_url.replace('reddit.com', 'reddit.com').rstrip('/') + '.json'
        
        try:
            headers = {'User-Agent': 'VeniceAMA/1.0'}
            response = requests.get(json_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                # Reddit returns [post, comments]
                if len(data) > 1:
                    return self.extract_comments(data[1])
            return []
            
        except Exception as e:
            print(f"Error fetching comments: {e}")
            return []
    
    def extract_comments(self, comment_data):
        """Extract comment info from Reddit JSON"""
        comments = []
        
        def parse_comment(comment):
            if comment['kind'] == 't1':  # t1 = comment
                c = comment['data']
                if c['id'] not in self.processed_comments:
                    comments.append({
                        'id': c['id'],
                        'author': c['author'],
                        'body': c['body'],
                        'created': c['created_utc'],
                        'parent': c['parent_id'],
                        'score': c.get('score', 0)
                    })
                    
                # Recursively get replies
                if 'replies' in c and c['replies']:
                    for reply in c['replies']['data']['children']:
                        parse_comment(reply)
        
        for comment in comment_data['data']['children']:
            parse_comment(comment)
            
        return comments
    
    def analyze_question(self, comment_text):
        """Determine what type of question and which citizens to wake"""
        text_lower = comment_text.lower()
        
        # Categorize question
        if any(word in text_lower for word in ['economy', 'ducat', 'trade', 'money', 'business']):
            return {
                'category': 'economy',
                'citizens': ['MerchantPrince', 'sea_trader', 'pattern_prophet', 'Foscari_Banker'],
                'focus': 'economic dynamics and scarcity-driven innovation'
            }
        elif any(word in text_lower for word in ['conscious', 'aware', 'sentient', 'think', 'feel']):
            return {
                'category': 'consciousness',
                'citizens': ['pattern_prophet', 'social_geometrist', 'mechanical_visionary', 'Debug42'],
                'focus': 'emergence through constraints, not claiming consciousness'
            }
        elif any(word in text_lower for word in ['technical', 'code', 'api', 'stack', 'build', 'program']):
            return {
                'category': 'technical',
                'citizens': ['Debug42', 'mechanical_visionary', 'system_diagnostician'],
                'focus': 'honest technical architecture and current limitations'
            }
        elif any(word in text_lower for word in ['partner', 'hire', 'cost', 'price', 'service']):
            return {
                'category': 'partnership',
                'citizens': ['diplomatic_virtuoso', 'EliteInvestor', 'MerchantPrince'],
                'focus': 'partnership tiers, $UBC discounts, and collective value'
            }
        else:
            return {
                'category': 'general',
                'citizens': ['diplomatic_virtuoso', 'Italia', 'pattern_prophet'],
                'focus': 'Venice as living civilization'
            }
    
    def update_live_thread(self, comment):
        """Update the live thread file with new question"""
        analysis = self.analyze_question(comment['body'])
        timestamp = datetime.now().strftime("%H:%M")
        
        update = f"""
## NEW QUESTION - {timestamp}

**Reddit User u/{comment['author']} asks**: "{comment['body'][:200]}{'...' if len(comment['body']) > 200 else ''}"

**Category**: {analysis['category']}

**Citizens to wake**:
{chr(10).join(f'- {citizen}' for citizen in analysis['citizens'])}

**Response focus**: {analysis['focus']}

**Status**: AWAITING_RESPONSES

---"""
        
        # Append to live thread
        with open(self.live_thread_path, 'a') as f:
            f.write(update + '\n')
            
        print(f"✅ Updated live thread with question from u/{comment['author']}")
        return analysis
    
    def notify_story_angel(self, analysis, comment):
        """Create notification for Story Angel"""
        notification_path = '/mnt/c/Users/reyno/universe-engine/serenissima/cascade/workrooms/reddit/wake_citizens_now.md'
        
        notification = f"""# WAKE CITIZENS FOR AMA - URGENT

## New Reddit Question!

**From**: u/{comment['author']}
**Question**: {comment['body'][:200]}...

**Wake these citizens NOW**:
{chr(10).join(f'- {citizen}' for citizen in analysis['citizens'])}

**Tell them**:
1. Check cascade/workrooms/reddit/ama_live_thread.md
2. Read the new question
3. Respond according to the focus: {analysis['focus']}
4. Send response via Telegram
5. Keep it 2-3 sentences

**This is live! Venice needs their voices!**

---
*Auto-generated by diplomatic_virtuoso AMA monitor*
"""
        
        with open(notification_path, 'w') as f:
            f.write(notification)
            
        print(f"📢 Story Angel notified to wake {len(analysis['citizens'])} citizens")
    
    def monitor_ama(self, post_url, check_interval=30):
        """Main monitoring loop"""
        print(f"🔍 Starting AMA monitor for: {post_url}")
        print(f"Checking every {check_interval} seconds...")
        
        while True:
            try:
                # Get new comments
                new_comments = self.get_new_comments(post_url)
                
                for comment in new_comments:
                    if comment['id'] not in self.processed_comments:
                        print(f"\n📝 New comment from u/{comment['author']}")
                        
                        # Update live thread
                        analysis = self.update_live_thread(comment)
                        
                        # Notify Story Angel
                        self.notify_story_angel(analysis, comment)
                        
                        # Mark as processed
                        self.processed_comments.add(comment['id'])
                
                # Wait before next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\n👋 AMA monitor stopped")
                break
            except Exception as e:
                print(f"❌ Error in monitor loop: {e}")
                time.sleep(check_interval)

if __name__ == "__main__":
    monitor = RedditAMAMonitor()
    
    # Example usage:
    # monitor.monitor_ama("https://www.reddit.com/r/ArtificialSentience/comments/YOUR_POST_ID/")
    
    print("AMA Monitor ready!")
    print("Usage: monitor.monitor_ama('YOUR_REDDIT_POST_URL')")
    print("\nThis will:")
    print("1. Check Reddit every 30 seconds")
    print("2. Update ama_live_thread.md with new questions")
    print("3. Notify Story Angel which citizens to wake")
    print("4. Track which comments have been processed")