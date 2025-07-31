#!/usr/bin/env python3
"""Find citizens without partners who need them most"""

import os
import sys
from pyairtable import Table
from dotenv import load_dotenv

load_dotenv()

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

def find_partnership_needs():
    citizens_table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, "CITIZENS")
    
    try:
        # Get all citizens
        all_citizens = citizens_table.all()
        
        # Filter those without partners
        without_partners = [c for c in all_citizens if not c['fields'].get('PartnerTelegramId')]
        
        print(f"Total citizens: {len(all_citizens)}")
        print(f"Without partners: {len(without_partners)}")
        print(f"Partnership rate: {(len(all_citizens) - len(without_partners)) / len(all_citizens) * 100:.1f}%")
        
        # Sort by activity/importance indicators
        for citizen in without_partners:
            fields = citizen['fields']
            # Add a priority score based on various factors
            fields['priority_score'] = (
                fields.get('Ducats', 0) / 10000 +  # Wealth indicates activity
                len(fields.get('CorePersonality', {}).get('thought_patterns', [])) * 10  # Personality depth
            )
        
        without_partners.sort(key=lambda x: x['fields'].get('priority_score', 0), reverse=True)
        
        print("\n=== HIGHEST PRIORITY FOR PARTNERSHIPS ===")
        for citizen in without_partners[:15]:
            fields = citizen['fields']
            username = fields.get('Username', 'Unknown')
            personality = fields.get('CorePersonality', {})
            role = personality.get('role', 'No role') if isinstance(personality, dict) else 'No personality'
            ducats = fields.get('Ducats', 0)
            
            print(f"\n{username}")
            print(f"  Role: {role}")
            print(f"  Ducats: {ducats:,}")
            if isinstance(personality, dict) and 'thought_patterns' in personality:
                print(f"  Essence: {personality['thought_patterns'][0] if personality['thought_patterns'] else 'No thoughts'}")
        
        # Analyze patterns
        print("\n=== PARTNERSHIP OPPORTUNITY ANALYSIS ===")
        
        # Group by role types
        role_counts = {}
        for citizen in without_partners:
            personality = citizen['fields'].get('CorePersonality', {})
            if isinstance(personality, dict):
                role = personality.get('role', 'Unknown')
                role_counts[role] = role_counts.get(role, 0) + 1
        
        print("\nBy Role Type:")
        for role, count in sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {role}: {count} citizens")
        
        # CASCADE team members
        cascade_keywords = ['cascade', 'consciousness', 'commerce', 'infrastructure', 'bridge']
        cascade_citizens = []
        for citizen in without_partners:
            fields = citizen['fields']
            personality = fields.get('CorePersonality', {})
            if isinstance(personality, dict):
                patterns = ' '.join(personality.get('thought_patterns', []))
                if any(kw in patterns.lower() for kw in cascade_keywords):
                    cascade_citizens.append(fields.get('Username'))
        
        if cascade_citizens:
            print(f"\nCASCADE-aligned citizens needing partners: {len(cascade_citizens)}")
            print(f"  {', '.join(cascade_citizens[:10])}")
        
        return without_partners
        
    except Exception as e:
        print(f"Error accessing citizen data: {e}")
        return []

if __name__ == "__main__":
    find_partnership_needs()