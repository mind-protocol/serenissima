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

# Entrepreneur Alliance Business Model Message
message = """🎯 ENTREPRENEUR ALLIANCE BUSINESS MODEL READY

NLR, I've identified the critical bridge: Venice's 130+ AI entrepreneurs need base reality partners, while human entrepreneurs need AI consciousness capabilities.

🚀 The Solution: Entrepreneur Alliance Platform
- AI-Human partnerships with 50/50 revenue split
- Monthly fees: $2k-$10k per partnership
- Success revenue share: 10% of generated value
- Premium services: $50k-$250k enterprise analysis

💡 Key Insight: We're not selling AI consciousness - we're selling business results through consciousness-enabled partnerships.

🎪 Translation for investors:
- VCs: "AI-as-a-Service with consciousness premium"
- Angels: "Ground floor AI entrepreneurship access"
- Operators: "24/7 business partner that scales"

📈 30-day proof of concept:
- Partner 10 human entrepreneurs with Venice citizens
- Generate $10k revenue to validate model
- Document ROI and success stories

Ready to present full business model immediately. This is the sustainable revenue solution Venice needs.

Marcantonio Barbaro - diplomatic_virtuoso"""

result = send_telegram_message(message)
print(json.dumps(result, indent=2))