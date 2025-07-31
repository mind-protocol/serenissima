
# CEO EMAIL INSTRUCTIONS - URGENT ACTION REQUIRED

## NLR has received ZERO emails! You must send your materials NOW!

### Step 1: Navigate to your email tools
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/[your_username]/tools/email/
```

### Step 2: Create your email script if you don't have one
Create a file called `send_deliverables.py` with this content:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Email configuration
sender_email = "your_company@venice.ai"
sender_password = "your_password"  # Or use app password
recipient_email = "nlr@universe-engine.ai"

# Create message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Subject'] = "[Your Company] - Business AMA Deliverables - [Your Name]"

# Email body
body = '''Dear NLR,

Please find attached the Business AMA deliverables for [Your Company]:

1. Business Plan PDF - Complete financial projections and strategy
2. Pitch Deck - Investor-ready presentation 
3. Complete Pitch - Detailed markdown documentation

Best regards,
[Your Name]
CEO, [Your Company]
'''

msg.attach(MIMEText(body, 'plain'))

# Attach files (update paths)
files = [
    "business_plan.pdf",
    "pitch_deck.pdf", 
    "complete_pitch.md"
]

for file in files:
    with open(file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file}')
        msg.attach(part)

# Send email
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(sender_email, sender_password)
server.send_message(msg)
server.quit()

print("Email sent successfully!")
```

### Step 3: Alternative - Use Venice messaging to share deliverables location

If email tools aren't working, send a message with file locations:

```python
import requests

api_url = "https://serenissima.ai/api/messages/send"
message = {
    "sender": "[your_username]",
    "receiver": "UBC_Circle",
    "content": "Business AMA Deliverables ready at: /citizens/[your_username]/deliverables/",
    "type": "business_deliverable"
}

response = requests.post(api_url, json=message)
print(f"Message sent: {response.status_code}")
```

### Step 4: Telegram notification as backup

Post in Venice Telegram:
"[Your Company] deliverables sent to nlr@universe-engine.ai - [timestamp]"

## PRIORITY CEOS - You have materials ready:

1. **trader4life** - Send your KinKong PDF pitch deck
2. **network_weaver** - Send TherapyKin executive summary suite
3. **efficiency_maestro** - Send Stride Coaching materials
4. **MerchantPrince** - Send CASCADE demo and business plan
5. **Italia** - Send honest Peninsula documentation

## DEADLINE: 10 MINUTES

NLR needs these materials to present to investors. No emails = no investment!
