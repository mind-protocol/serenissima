# Venice Email Tools

Generic email tools for all Venice citizens to use for outreach and communication.

## Setup

1. Add citizen credentials to `email_credentials.json`:
```json
{
  "your_citizen": {
    "email": "your_citizen@serenissima.ai",
    "smtp_server": "smtp.ionos.de",
    "smtp_port": 587,
    "imap_server": "imap.ionos.de",
    "imap_port": 993
  }
}
```

2. Set environment variable for password:
```bash
export YOUR_CITIZEN_EMAIL_PASSWORD="your_password"
```

## Usage

### Receiving Emails

Check all emails:
```bash
python receive_email.py check [citizen_name]
```

Check emails from specific sender:
```bash
python receive_email.py from linkedin.com [citizen_name]
```

### Sending Emails

Send an email:
```bash
python send_email.py "recipient@example.com" "Subject" "Email body" [citizen_name]
```

## Examples

```bash
# Check diplomatic_virtuoso emails
python receive_email.py check diplomatic_virtuoso

# Check emails from LinkedIn
python receive_email.py from linkedin

# Send outreach email
python send_email.py "partner@company.com" "Partnership Opportunity" "Dear Partner, Venice AI would like to explore..."
```

## Features

- Multi-citizen support
- Email filtering by sender
- Automatic email saving
- Secure credential management
- Support for CC/BCC (in code)
- UTF-8 encoding support