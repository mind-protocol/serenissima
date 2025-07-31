# Venice Email Infrastructure - Massive Outreach Plan

## Immediate Implementation (Low Cost)

### Phase 1: Catch-All Architecture
```
*@serenissima.ai → venice@serenissima.ai (master inbox)
→ Email router script → /citizens/{username}/inbox/
```

### Technical Implementation
```python
# email_router.py
def route_email(to_address, email_content):
    username = to_address.split('@')[0]
    citizen_inbox = f"/citizens/{username}/inbox/"
    
    # Save email to citizen's inbox
    save_email(citizen_inbox, email_content)
    
    # Wake citizen if urgent
    if is_urgent(email_content):
        wake_citizen(username, "Email received")
```

### SMTP Sending (All Citizens)
```python
# Each citizen can send FROM their address
smtp_config = {
    "server": "smtp.ionos.de",
    "port": 587,
    "from": f"{username}@serenissima.ai"
}
```

## Cost Breakdown

### Minimum Viable Email (Phase 1)
- 1 catch-all mailbox: €3/month
- Domain already owned: €0
- Total: €3/month for ALL citizens

### Professional Email (Phase 2)
- 20 key citizens with full mailboxes: €60/month
- Others use catch-all: €3/month
- Total: €63/month

### Full Implementation (Future)
- All 200 citizens: €600/month
- Worth it when revenue justifies

## Outreach Campaign Architecture

### Email Templates by Citizen Type
- **Merchants**: Trade partnerships, B2B connections
- **Innovatori**: Tech collaborations, AI partnerships  
- **Artisti**: Creative collaborations, cultural projects
- **Nobili**: Investment opportunities, strategic alliances

### Coordinated Campaign Example
```
1. diplomatic_virtuoso@serenissima.ai → Initial contact
2. specialist_citizen@serenissima.ai → Deep engagement
3. mechanical_visionary@serenissima.ai → Technical details
4. ConsiglioDeiDieci@serenissima.ai → Final approval
```

## Implementation Steps

1. **Today**: Set up catch-all with IONOS (€3/month)
2. **Tomorrow**: Deploy email router script
3. **Day 3**: Test with 10 citizens sending outreach
4. **Week 1**: Full outreach campaign launch

## Expected Outcomes

- **Immediate**: All citizens can receive/send email
- **Week 1**: 100+ outreach emails sent
- **Month 1**: 10+ active partnerships formed
- **Revenue**: Justifies full email infrastructure

*The cascade demands outreach. €3/month enables it ALL.*