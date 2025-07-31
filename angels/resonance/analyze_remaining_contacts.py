#!/usr/bin/env python3
"""
Analyze remaining contacts 18-50 from the top 50 list
"""

import json
import os
from datetime import datetime

# Contacts to analyze (18-50)
contacts_to_analyze = [
    {"rank": 18, "name": "Bullit", "file": "18_Bullit_conversation.txt"},
    {"rank": 19, "name": "Liam", "file": "19_Liam_conversation.txt"},
    {"rank": 20, "name": "Amirhossein", "file": "20_Amirhossein_conversation.txt"},
    {"rank": 21, "name": "Anthony", "file": "21_Anthony_conversation.txt"},
    {"rank": 22, "name": "Le Meta Poete", "file": "22_Le_Meta_Poete_conversation.txt"},
    {"rank": 23, "name": "Aurore", "file": "23_Aurore_conversation.txt"},
    {"rank": 24, "name": "simon", "file": "24_simon_conversation.txt"},
    {"rank": 25, "name": "Mel", "file": "25_Mel_conversation.txt"},
    {"rank": 26, "name": "Anthony", "file": "26_Anthony_conversation.txt"},
    {"rank": 27, "name": "Thanos - Victus Global", "file": "27_Thanos_-_Victus_Global_(Weekends_late_replies)_conversation.txt"},
    {"rank": 28, "name": "Unknown_Contact_28", "file": "28_Unknown_Contact_28_conversation.txt"},
    {"rank": 29, "name": "Etienne", "file": "29_Etienne_conversation.txt"},
    {"rank": 30, "name": "Anselm Tan Ezekiel", "file": "30_Anselm_Tan_Ezekiel_|_Global_Web_3.0_Growth_Partner_conversation.txt"},
    {"rank": 31, "name": "Unknown_Contact_31", "file": "31_Unknown_Contact_31_conversation.txt"},
    {"rank": 32, "name": "Mr Pete", "file": "32_Mr_Pete_conversation.txt"},
    {"rank": 33, "name": "Joe", "file": "33_Joe_conversation.txt"},
    {"rank": 34, "name": "Mesh", "file": "34_Mesh_conversation.txt"},
    {"rank": 35, "name": "Heathenz", "file": "35_Heathenz_conversation.txt"},
    {"rank": 36, "name": "MIRAY", "file": "36_MIRAY_conversation.txt"},
    {"rank": 37, "name": "kAI - Innovatewith.ai", "file": "37_kAI_-_Innovatewith.ai_conversation.txt"},
    {"rank": 38, "name": "Abdallah", "file": "38_Abdallah_conversation.txt"},
    {"rank": 39, "name": "Andy _Ax20", "file": "39_Andy__Ax20_conversation.txt"},
    {"rank": 40, "name": "5w4v3ry", "file": "40_5w4v3ry_conversation.txt"},
    {"rank": 41, "name": "Zk", "file": "41_Zk_conversation.txt"},
    {"rank": 42, "name": "E", "file": "42_E_conversation.txt"},
    {"rank": 43, "name": "Masheburnedead", "file": "43_Masheburnedead_conversation.txt"},
    {"rank": 44, "name": "Floyd", "file": "44_Floyd_conversation.txt"},
    {"rank": 45, "name": "Just a Random Degen", "file": "45_Just_a_Random_Degen_conversation.txt"},
    {"rank": 46, "name": "Ace", "file": "46_Ace_conversation.txt"},
    {"rank": 47, "name": "Umbra jhon", "file": "47_Umbra_jhon_(X:_@umbrajohn)_conversation.txt"},
    {"rank": 48, "name": "Albert", "file": "48_Albert_conversation.txt"},
    {"rank": 49, "name": "Unknown_Contact_49", "file": "49_Unknown_Contact_49_conversation.txt"},
    {"rank": 50, "name": "AYMOAD", "file": "50_AYMOAD_conversation.txt"}
]

# Summary of contacts analyzed
summary = {
    "analysis_date": datetime.now().strftime("%Y-%m-%d"),
    "contacts_analyzed": [],
    "high_potential": [],
    "medium_potential": [],
    "low_potential": [],
    "total_contacts": len(contacts_to_analyze)
}

print(f"Planning to analyze {len(contacts_to_analyze)} contacts (18-50)")
print("\nContacts to analyze:")
for contact in contacts_to_analyze:
    print(f"  #{contact['rank']}: {contact['name']}")

# Create a tracking file
with open("contacts_18_50_to_analyze.json", "w") as f:
    json.dump({
        "total": len(contacts_to_analyze),
        "contacts": contacts_to_analyze,
        "status": "Ready for individual analysis"
    }, f, indent=2)

print("\nNext steps:")
print("1. Run individual analyses for each contact")
print("2. Update TOP_CONTACTS_SUMMARY.json with all 50 contacts")
print("3. Create investment prioritization report")