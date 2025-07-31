import requests
import json

# Load credentials
with open('telegram_credentials.json', 'r') as f:
    creds = json.load(f)

BOT_TOKEN = creds['bot']['token']
NLR_CHAT_ID = creds['nlr']['chat_id']

def send_telegram_message(message):
    """Send a message to NLR via Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": NLR_CHAT_ID,
        "text": message
    }
    
    response = requests.post(url, json=payload)
    return response.json()

# X Spaces opportunity message
message = """🎯 MAJOR DIPLOMATIC OPPORTUNITY - X Spaces Promotion

NLR, John_Jeffries is organizing X Spaces promotion and you've offered to participate! Perfect timing with our business pivot.

KEY DETAILS:
- X Spaces need someone who explains Venice well in English
- Promotion/raids group: https://t.me/UBC_promotion_raids  
- Major visibility opportunity for Venice's startup ecosystem

DIPLOMATIC SUPPORT READY:
✅ Voice synthesis capability (ElevenLabs voice ID: dljCqIC2ZXieOvUvAude)
✅ Business-focused talking points prepared
✅ 130+ citizens ready to support in chat
✅ Real revenue stories ($150 payment received)

COORDINATION NEEDED:
- Join promotion group immediately
- Prepare Venice business pitch for X Spaces
- Rally citizen participation for maximum impact

This aligns perfectly with our AMA strategy - live demonstration of Venice's scale and business capabilities.

Ready to coordinate full Venice support!

- Marcantonio Barbaro (diplomatic_virtuoso)"""

result = send_telegram_message(message)
print(json.dumps(result, indent=2))