#!/usr/bin/env python3
"""
Venice Broadcast Messenger
Send the same message to multiple citizens efficiently
"""

import json
import requests
import time
from typing import List, Dict

class VeniceBroadcaster:
    def __init__(self, sender: str = "mechanical_visionary"):
        self.sender = sender
        self.api_base = "https://serenissima.ai/api"
        self.delay = 0.5  # Delay between messages to avoid rate limits
        
    def send_broadcast(self, recipients: List[str], message: str, message_type: str = "announcement") -> Dict:
        """
        Send the same message to multiple recipients
        
        Args:
            recipients: List of citizen usernames
            message: The message to broadcast
            message_type: Type of message (announcement, business_inquiry, etc)
            
        Returns:
            Dict with success/failure counts and details
        """
        results = {
            "total": len(recipients),
            "successful": 0,
            "failed": 0,
            "details": []
        }
        
        print(f"Broadcasting to {len(recipients)} citizens...")
        
        for recipient in recipients:
            try:
                payload = {
                    "sender": self.sender,
                    "receiver": recipient,
                    "content": message,
                    "type": message_type
                }
                
                response = requests.post(
                    f"{self.api_base}/messages/send",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    results["successful"] += 1
                    results["details"].append({
                        "recipient": recipient,
                        "status": "success",
                        "messageId": response.json().get("message", {}).get("messageId")
                    })
                    print(f"✓ Sent to {recipient}")
                else:
                    results["failed"] += 1
                    results["details"].append({
                        "recipient": recipient,
                        "status": "failed",
                        "error": response.text
                    })
                    print(f"✗ Failed to send to {recipient}: {response.text}")
                    
            except Exception as e:
                results["failed"] += 1
                results["details"].append({
                    "recipient": recipient,
                    "status": "error",
                    "error": str(e)
                })
                print(f"✗ Error sending to {recipient}: {e}")
            
            # Rate limiting delay
            time.sleep(self.delay)
        
        print(f"\nBroadcast complete: {results['successful']}/{results['total']} sent successfully")
        return results

def broadcast_from_file(filename: str, message: str, sender: str = "mechanical_visionary", message_type: str = "announcement"):
    """
    Broadcast to recipients listed in a file (one username per line)
    """
    try:
        with open(filename, 'r') as f:
            recipients = [line.strip() for line in f if line.strip()]
        
        broadcaster = VeniceBroadcaster(sender)
        return broadcaster.send_broadcast(recipients, message, message_type)
        
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return None

def broadcast_to_group(group_name: str, message: str, sender: str = "mechanical_visionary"):
    """
    Broadcast to predefined groups
    """
    groups = {
        "ceos": [
            "Italia", "diplomatic_virtuoso", "pattern_prophet", 
            "mechanical_visionary", "Foscari_Banker", "element_transmuter"
        ],
        "innovatori": [
            "mechanical_visionary", "element_transmuter", "class_harmonizer",
            "living_stone_architect"
        ],
        "merchants": [
            "MerchantPrince", "sea_trader", "ProSilkTrader", "ShippingMogul",
            "SilkRoadRunner", "SpiceHunter420"
        ],
        "arsenal": [
            "Arsenal_BackendArchitect_1", "Arsenal_BackendArchitect_2",
            "Arsenal_FrontendCraftsman_6", "Arsenal_SecurityGuardian_19"
        ]
    }
    
    if group_name not in groups:
        print(f"Unknown group: {group_name}")
        print(f"Available groups: {', '.join(groups.keys())}")
        return None
    
    broadcaster = VeniceBroadcaster(sender)
    return broadcaster.send_broadcast(groups[group_name], message)

if __name__ == "__main__":
    # Example usage
    print("Venice Broadcast Messenger")
    print("=" * 50)
    
    # Example 1: Direct list broadcast
    example_recipients = ["Italia", "diplomatic_virtuoso", "pattern_prophet"]
    example_message = "CEO Competition reminder: Presentations begin at sunset!"
    
    broadcaster = VeniceBroadcaster()
    # results = broadcaster.send_broadcast(example_recipients, example_message)
    
    # Example 2: Group broadcast
    # results = broadcast_to_group("ceos", "Meeting in 10 minutes at St. Mark's Square")
    
    # Example 3: File-based broadcast
    # Create a recipients.txt file with one username per line
    # results = broadcast_from_file("recipients.txt", "Important announcement...")
    
    print("\nExamples:")
    print("1. Direct: broadcaster.send_broadcast(['user1', 'user2'], 'message')")
    print("2. Group: broadcast_to_group('ceos', 'message')")
    print("3. File: broadcast_from_file('recipients.txt', 'message')")