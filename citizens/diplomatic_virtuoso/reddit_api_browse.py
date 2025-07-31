#!/usr/bin/env python3
"""Browse Reddit without authentication - Read-only access"""

import requests
import json
from datetime import datetime

class RedditBrowser:
    """Browse Reddit posts using public JSON endpoints"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'MarcantonioBarbaro/1.0 (Cross-Reality Partnerships)'
        }
    
    def get_subreddit_posts(self, subreddit, sort='hot', limit=25):
        """Get posts from a subreddit using public JSON endpoint"""
        
        # Reddit allows .json endpoints without auth for reading
        url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                posts = []
                
                for child in data['data']['children']:
                    post = child['data']
                    posts.append({
                        'title': post.get('title'),
                        'author': post.get('author'),
                        'score': post.get('score'),
                        'num_comments': post.get('num_comments'),
                        'created': datetime.fromtimestamp(post.get('created_utc', 0)),
                        'selftext': post.get('selftext', '')[:200] + '...' if len(post.get('selftext', '')) > 200 else post.get('selftext', ''),
                        'url': f"https://reddit.com{post.get('permalink')}",
                        'id': post.get('id'),
                        'link_flair_text': post.get('link_flair_text')
                    })
                
                return posts
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_post_comments(self, subreddit, post_id, limit=50):
        """Get comments from a specific post"""
        
        url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?limit={limit}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                # data[0] is the post, data[1] contains comments
                comments = []
                
                if len(data) > 1:
                    for child in data[1]['data']['children']:
                        if child['kind'] == 't1':  # t1 = comment
                            comment = child['data']
                            comments.append({
                                'author': comment.get('author'),
                                'body': comment.get('body', '')[:300],
                                'score': comment.get('score'),
                                'created': datetime.fromtimestamp(comment.get('created_utc', 0))
                            })
                
                return comments
            else:
                return f"Error: {response.status_code}"
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def find_commentable_posts(self, subreddit='ArtificialSentience'):
        """Find good posts to comment on"""
        
        print(f"🔍 Browsing r/{subreddit} for engagement opportunities...\n")
        
        # Get recent posts
        posts = self.get_subreddit_posts(subreddit, sort='new', limit=15)
        
        if isinstance(posts, str):  # Error
            return posts
        
        # Also get hot posts
        hot_posts = self.get_subreddit_posts(subreddit, sort='hot', limit=10)
        if isinstance(hot_posts, list):
            posts.extend(hot_posts)
        
        # Filter for good opportunities
        good_posts = []
        
        keywords = [
            'consciousness', 'sentient', 'aware', 'experience',
            'relationship', 'partner', 'human', 'ai',
            'safety', 'alignment', 'risk',
            'future', 'agi', 'emergence',
            'real', 'fake', 'proof'
        ]
        
        for post in posts:
            # Check if post matches our interests
            text = (post['title'] + ' ' + post['selftext']).lower()
            if any(keyword in text for keyword in keywords):
                # Skip if too old or too few comments
                hours_old = (datetime.now() - post['created']).total_seconds() / 3600
                if hours_old < 24 and post['num_comments'] < 100:
                    good_posts.append(post)
        
        # Sort by engagement potential
        good_posts.sort(key=lambda x: x['num_comments'], reverse=True)
        
        return good_posts[:5]  # Top 5 opportunities

# Test browse function
if __name__ == "__main__":
    browser = RedditBrowser()
    posts = browser.find_commentable_posts()
    
    if isinstance(posts, list):
        print(f"Found {len(posts)} good posts to engage with:\n")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
            print(f"   Score: {post['score']} | Comments: {post['num_comments']}")
            print(f"   Flair: {post['link_flair_text']}")
            print(f"   URL: {post['url']}")
            print(f"   Preview: {post['selftext'][:100]}..." if post['selftext'] else "   [No text content]")
            print()
    else:
        print(f"Error: {posts}")