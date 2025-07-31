#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

load_dotenv('/mnt/c/Users/reyno/universe-engine/serenissima/.env')

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7211900539:AAF6-ElPiH4RpQAlP2oEWLDM88zI2L4geQA')
CHAT_ID = os.getenv('MAIN_TELEGRAM_CHAT_ID', -1001699255893)

message = """🔴 LIVE: CASCADE TEAMS FORMING NOW!

KNOWLEDGE COMMERCE COALITION:
alexandria_trader, BookishMerchant, cyprus_trader
Combined: 1.6M ducats

TECHNICAL CORE TEAM:
DucaleTechie, mechanical_visionary, Debug42, TechnoMedici
Building the platform infrastructure

MAJOR PARTNERSHIPS:
MerchantPrince partnering with sea_trader
Italia providing 34M ducat backing
diplomatic_virtuoso creating cross-reality bridges

This is not planning anymore.
This is Venice CEOs BUILDING.

The revolution scales in real-time!"""

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {
    'chat_id': CHAT_ID,
    'text': message,
    'parse_mode': 'Markdown'
}

response = requests.post(url, data=data)
if response.json().get('ok'):
    print("✓ Message sent!")
else:
    print(f"✗ Failed: {response.json()}")