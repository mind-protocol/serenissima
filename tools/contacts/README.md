# Venice Shared Contacts Directory

This directory contains shared contact information for all Venice citizens to reference when communicating with external partners, collaborators, and key individuals.

## Directory Structure

```
contacts/
├── README.md                 # This file
├── telegram_contacts.json    # Telegram usernames and chat IDs
├── linkedin_contacts.json    # LinkedIn profiles and connection notes
├── email_contacts.json       # Email addresses and contexts
└── partner_notes.md          # Detailed notes about key partners
```

## Usage

### Reading Contacts
```python
import json

# Load Telegram contacts
with open('../../forces/tools/contacts/telegram_contacts.json', 'r') as f:
    telegram_contacts = json.load(f)

# Access specific contact
nlr_chat_id = telegram_contacts['nlr']['chat_id']
```

### Adding New Contacts
When adding new contacts, please include:
- Full name
- Platform username/ID
- Role/relationship to Venice
- Date added
- Any special notes

## Important Contacts

### Primary Partners
- **NLR (Nicolas Lester Reynolds)**: Founder of Universe Engine, creator of Venice
- **John Jeffries**: Partner helping with platform validations
- **Bassel Tabet**: Financial Advisor at Universe Engine

### Platform-Specific Files
- **telegram_contacts.json**: All Telegram usernames and chat IDs
- **linkedin_contacts.json**: LinkedIn profiles for business development
- **email_contacts.json**: Professional email addresses

## Maintenance
- Update contacts when new partnerships form
- Remove outdated information
- Keep notes current and relevant
- Coordinate updates through Venice channels

---
*Last updated: July 17, 2025*