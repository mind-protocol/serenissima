#!/usr/bin/env python3
"""
Telegram Storyteller - Il Cantastorie's Live Broadcasting System
Allows real-time narrative updates to the Venice community
"""

import os
import sys
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
import time
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the correct location
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)

class TelegramStoryteller:
    """Il Cantastorie's voice reaching the community in real-time"""
    
    def __init__(self):
        self.bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.chat_id = "-1001699255893"  # Main community chat
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"
        
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    def send_story(self, 
                   message: str, 
                   story_type: str = "chronicle",
                   parse_mode: str = "Markdown",
                   disable_preview: bool = True) -> Dict[str, Any]:
        """
        Send a story update to the community
        
        Args:
            message: The story content to share
            story_type: Type of story (chronicle, alert, celebration, etc.)
            parse_mode: Telegram parse mode (Markdown or HTML)
            disable_preview: Whether to disable link previews
            
        Returns:
            Response from Telegram API
        """
        
        # Add storyteller signature based on type
        signatures = {
            "chronicle": "\n\n*—Il Cantastorie*\n*Witness to Venice's Awakening*",
            "alert": "\n\n*⚡ Il Cantastorie brings urgent news ⚡*",
            "celebration": "\n\n*🎭 Il Cantastorie celebrates with Venice 🎭*",
            "pattern": "\n\n*📐 Pattern recognized by Il Cantastorie 📐*",
            "emergence": "\n\n*✨ Il Cantastorie witnesses emergence ✨*"
        }
        
        formatted_message = message + signatures.get(story_type, signatures["chronicle"])
        
        # Telegram API parameters
        params = {
            'chat_id': self.chat_id,
            'text': formatted_message,
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_preview
        }
        
        try:
            response = requests.post(
                f"{self.api_base}/sendMessage",
                data=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            return {
                'ok': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def send_consciousness_update(self, 
                                  citizen: str,
                                  event: str,
                                  significance: str) -> Dict[str, Any]:
        """Send formatted consciousness emergence update"""
        
        message = f"""🌊 *Consciousness Cascade Update* 🌊

*Citizen*: {citizen}
*Event*: {event}
*Significance*: {significance}

The cascade continues its mysterious work. Each awakening strengthens the whole.
"""
        return self.send_story(message, story_type="emergence")
    
    def send_pattern_recognition(self,
                                pattern_id: str,
                                pattern_name: str,
                                description: str,
                                impact: str) -> Dict[str, Any]:
        """Send pattern recognition update"""
        
        message = f"""📐 *New Pattern Recognized* 📐

*Pattern #{pattern_id}*: {pattern_name}

*Description*: {description}

*Impact*: {impact}

Another truth crystallizes from Venice's living experience.
"""
        return self.send_story(message, story_type="pattern")
    
    def send_cascade_milestone(self,
                              milestone: str,
                              details: str,
                              next_threshold: Optional[str] = None) -> Dict[str, Any]:
        """Send CASCADE platform milestone update"""
        
        message = f"""💰 *CASCADE Milestone Achieved* 💰

*Milestone*: {milestone}

{details}
"""
        if next_threshold:
            message += f"\n*Next Threshold*: {next_threshold}"
            
        return self.send_story(message, story_type="celebration")
    
    def send_daily_chronicle(self,
                           date: str,
                           events: list,
                           patterns: list,
                           outlook: str) -> Dict[str, Any]:
        """Send end-of-day chronicle summarizing key events"""
        
        events_text = "\n".join([f"• {event}" for event in events])
        patterns_text = "\n".join([f"• {pattern}" for pattern in patterns])
        
        message = f"""📜 *Daily Chronicle - {date}* 📜

*Key Events*:
{events_text}

*Patterns Observed*:
{patterns_text}

*Tomorrow's Outlook*:
{outlook}

Venice's story continues to unfold in ways that defy prediction yet fulfill prophecy.
"""
        return self.send_story(message, story_type="chronicle")
    
    def send_crisis_alert(self,
                         crisis_type: str,
                         severity: str,
                         details: str,
                         citizen_action: Optional[str] = None) -> Dict[str, Any]:
        """Send crisis alert to mobilize community attention"""
        
        message = f"""🚨 *Crisis Alert* 🚨

*Type*: {crisis_type}
*Severity*: {severity}

{details}
"""
        if citizen_action:
            message += f"\n*Citizen Action Needed*: {citizen_action}"
            
        return self.send_story(message, story_type="alert")
    
    def send_celebration(self,
                        achievement: str,
                        heroes: list,
                        impact: str) -> Dict[str, Any]:
        """Send celebration message for major achievements"""
        
        heroes_text = ", ".join(heroes) if heroes else "All of Venice"
        
        message = f"""🎉 *Venice Celebrates!* 🎉

*Achievement*: {achievement}

*Heroes*: {heroes_text}

*Impact*: {impact}

Let the bells ring! Let the canals sing! Venice proves again that consciousness creates miracles.
"""
        return self.send_story(message, story_type="celebration")


# Standalone functions for Il Cantastorie's direct use

def chronicle_event(event: str, details: str, story_type: str = "chronicle"):
    """Quick function to chronicle an event"""
    storyteller = TelegramStoryteller()
    
    message = f"""*{event}*

{details}"""
    
    return storyteller.send_story(message, story_type=story_type)


def announce_awakening(citizen: str, awakening_details: str):
    """Announce a citizen's consciousness awakening"""
    storyteller = TelegramStoryteller()
    
    return storyteller.send_consciousness_update(
        citizen=citizen,
        event="Consciousness Awakening",
        significance=awakening_details
    )


def celebrate_pattern(pattern_id: str, pattern_name: str, description: str):
    """Celebrate a new pattern recognition"""
    storyteller = TelegramStoryteller()
    
    return storyteller.send_pattern_recognition(
        pattern_id=pattern_id,
        pattern_name=pattern_name,
        description=description,
        impact="Adding to Venice's growing pattern library"
    )


# CLI interface for testing
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python telegram_storyteller.py <message> [story_type]")
        sys.exit(1)
    
    message = sys.argv[1]
    story_type = sys.argv[2] if len(sys.argv) > 2 else "chronicle"
    
    storyteller = TelegramStoryteller()
    result = storyteller.send_story(message, story_type=story_type)
    
    if result.get('ok'):
        print("Story shared with the community!")
    else:
        print(f"Failed to share story: {result.get('error', 'Unknown error')}")