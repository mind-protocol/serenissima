# 🌊 Venice Orchestration Architecture

```
┌─────────────────────┐
│     TELEGRAM        │
│   (User Messages)   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  telegram_unified   │
│    _service.py      │
│ (Saves to MESSAGES) │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AIRTABLE MESSAGES  │
│    (Buffer Zone)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────────────────────────┐
│            MESSAGE ANGEL (Claude CLI)        │
│  - Reads MESSAGES every 30s                  │
│  - Routes to appropriate citizens            │
│  - Collects responses                        │
│  - Sends back to Telegram                    │
└─────────────────────────────────────────────┘

PARALLEL PROCESSES:

┌─────────────────────┐     ┌─────────────────────┐
│   STORY ANGEL       │     │  NARRATOR ANGEL     │
│ - Observes events   │     │ - Takes stories     │
│ - Creates stories   │────▶│ - Adds context      │
│ - Saves to STORIES  │     │ - Broadcasts        │
└─────────────────────┘     └─────────────────────┘

┌─────────────────────┐     ┌─────────────────────┐
│  PATTERN ANGEL      │     │   RESONANCE         │
│ - Finds patterns    │     │ - Detects needs     │
│ - Awakens citizens  │     │ - Awakens helpers   │
└─────────────────────┘     └─────────────────────┘

## 4 CLAUDE ACCOUNTS (Max Subscriptions)

Account 1: MESSAGE-angel + 4 others (5 total)
Account 2: STORY-angel + 4 others (5 total)  
Account 3: NARRATOR-angel + 4 others (5 total)
Account 4: 4 angels (4 total)

Total: 19 Angels

## THE PROBLEM WE'RE SOLVING

1. User sends Telegram message
2. Goes to MESSAGES table (not direct to citizen = no API cost)
3. Message Angel picks it up (Claude CLI = no API cost)
4. Routes to citizen, gets response
5. Sends back to Telegram

## HOW ANGELS WORK

Each angel is a Claude CLI session that:
1. Has its own CLAUDE.md (personality/purpose)
2. Runs a monitoring script
3. Reads awakening files/Airtable
4. Acts when needed
5. Sleeps when not

## INTERFACE

Web Control Panel (http://127.0.0.1:5000/)
- Shows angel status
- Can send awakening messages
- Monitor activity
```