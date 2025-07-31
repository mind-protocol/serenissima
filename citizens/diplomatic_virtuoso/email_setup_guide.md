# Email Setup Guide for diplomatic_virtuoso@serenissima.ai

## Current Configuration
- **Email:** diplomatic_virtuoso@serenissima.ai
- **SMTP Server:** smtp.ionos.com
- **Port:** 587 (TLS)
- **Password:** In .env file

## Setup Steps Needed

### 1. Verify Email Account Exists
The email account diplomatic_virtuoso@serenissima.ai needs to be created with your email provider (appears to be IONOS).

### 2. SMTP Settings for IONOS
```
Server: smtp.ionos.com
Port: 587 (STARTTLS) or 465 (SSL)
Authentication: Required
Username: diplomatic_virtuoso@serenissima.ai (full email)
```

### 3. Alternative Email Providers

**Gmail (if using Google Workspace):**
```
DIPLOMATIC_SMTP_SERVER=smtp.gmail.com
DIPLOMATIC_SMTP_PORT=587
```

**SendGrid (API-based):**
```python
# Alternative implementation using SendGrid
import sendgrid
from sendgrid.helpers.mail import Mail

def send_via_sendgrid(to_email, subject, body):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    message = Mail(
        from_email='diplomatic_virtuoso@serenissima.ai',
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    response = sg.send(message)
    return response.status_code == 202
```

### 4. Testing Connection
```python
# Simple SMTP test
import smtplib

server = smtplib.SMTP('smtp.ionos.com', 587)
server.starttls()
try:
    server.login('diplomatic_virtuoso@serenissima.ai', 'password')
    print("Login successful!")
except Exception as e:
    print(f"Login failed: {e}")
server.quit()
```

## Immediate Alternatives

### Option 1: Use Existing Email
If you have another email configured, we can update the script to use that temporarily:
```bash
export DIPLOMATIC_EMAIL="your-existing@email.com"
export DIPLOMATIC_EMAIL_PASSWORD="your-password"
export DIPLOMATIC_SMTP_SERVER="smtp.gmail.com"
```

### Option 2: Email Service Integration
Many services provide easier email sending:
- **Resend** - Simple API, good for transactional emails
- **Postmark** - Reliable, developer-friendly
- **AWS SES** - Cost-effective at scale
- **Mailgun** - Good API, reasonable pricing

### Option 3: Manual Sending
For immediate needs, copy the formatted email content and send manually through any email client.

## Columbus Pitch Ready
The investment pitch is prepared and can be sent as soon as email is configured:
- `columbus_message_personalized.txt` - Full pitch
- `columbus_objection_handlers.md` - Response strategies
- `email_campaign_tracker.md` - Follow-up sequences

## Next Steps
1. Verify diplomatic_virtuoso@serenissima.ai exists with IONOS
2. Confirm SMTP credentials are correct
3. Test with simple connection script
4. Send test email to yourself first
5. Send Columbus pitch

The diplomatic channels await activation!