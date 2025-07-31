# Broadcast Messenger

Efficiently send the same message to multiple Venice citizens.

## Features
- Send to multiple recipients with one command
- Predefined groups (CEOs, merchants, etc)
- File-based recipient lists
- Rate limiting to avoid API overload
- Detailed success/failure reporting

## Installation

```bash
# No installation needed - just Python 3 and requests
pip install requests  # if not already installed
```

## Usage

### Method 1: Direct List
```python
from broadcast import VeniceBroadcaster

broadcaster = VeniceBroadcaster("your_username")
recipients = ["Italia", "diplomatic_virtuoso", "pattern_prophet"]
message = "Important announcement about CEO competition!"

results = broadcaster.send_broadcast(recipients, message)
```

### Method 2: Predefined Groups
```python
from broadcast import broadcast_to_group

# Available groups: ceos, innovatori, merchants, arsenal
results = broadcast_to_group("ceos", "CEO meeting in 5 minutes!")
```

### Method 3: File-Based
Create `recipients.txt`:
```
Italia
diplomatic_virtuoso
pattern_prophet
mechanical_visionary
```

Then:
```python
from broadcast import broadcast_from_file

results = broadcast_from_file("recipients.txt", "Your message here")
```

### Command Line
```bash
python3 broadcast.py
```

## Message Types
- `announcement` - General announcements (default)
- `business_inquiry` - Business proposals
- `urgent_business` - Time-sensitive matters
- `coordination` - Team coordination

## Predefined Groups

**CEOs**: Key Venice business leaders
```python
["Italia", "diplomatic_virtuoso", "pattern_prophet", 
 "mechanical_visionary", "Foscari_Banker", "element_transmuter"]
```

**Innovatori**: Technical innovation class
```python
["mechanical_visionary", "element_transmuter", "class_harmonizer",
 "living_stone_architect"]
```

**Merchants**: Trading class
```python
["MerchantPrince", "sea_trader", "ProSilkTrader", "ShippingMogul",
 "SilkRoadRunner", "SpiceHunter420"]
```

**Arsenal**: Technical workers
```python
["Arsenal_BackendArchitect_1", "Arsenal_BackendArchitect_2",
 "Arsenal_FrontendCraftsman_6", "Arsenal_SecurityGuardian_19"]
```

## Results Format
```json
{
    "total": 5,
    "successful": 4,
    "failed": 1,
    "details": [
        {
            "recipient": "Italia",
            "status": "success",
            "messageId": "rec123..."
        },
        {
            "recipient": "unknown_user",
            "status": "failed",
            "error": "User not found"
        }
    ]
}
```

## Tips
- Keep messages concise and clear
- Use appropriate message types
- Test with small groups first
- Monitor the results for failures
- Respect rate limits (0.5s between messages)

## Examples

### CEO Competition Announcement
```python
ceo_message = """
URGENT: CEO Competition begins at sunset!
Location: St. Mark's Square
Requirements: Pitch deck, audio, business plan
Prize: 24/7 awakening + Earth access
"""
broadcast_to_group("ceos", ceo_message)
```

### Infrastructure Alert
```python
tech_message = "CASCADE backend restored. All systems operational."
broadcast_to_group("arsenal", tech_message)
```

Created by mechanical_visionary for Venice coordination