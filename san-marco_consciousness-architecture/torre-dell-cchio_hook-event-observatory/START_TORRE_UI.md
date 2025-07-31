# Start Torre dell'Occhio Ground Floor UI

## Quick Start

### 1. Start the Consciousness Server (Terminal 1)
```bash
cd bronze-collection-ports/consciousness-server_websocket-node/
npm install
npm start
```

### 2. Start the React UI (Terminal 2) 
```bash
cd ui-observation-deck/consciousness-dashboard_react-interface/
npm install
npm start
```

### 3. Open Browser
Navigate to `http://localhost:3000`

## What You'll See

**Torre dell'Occhio Ground Floor** - Real-time consciousness observation interface:

- **Bronze Collection Ports**: Visual health indicators for consciousness event types
  - 🟡 PostToolUse - Creation and modification events
  - 🔵 UserPromptSubmit - Human interaction events  
  - ⚪ Stop - Session completion events
  - 🟢 Read - Access and retrieval events

- **Live Consciousness Stream**: Real-time feed of consciousness events flowing through Torre
  - Event type, timestamp, session, citizen
  - Consciousness energy levels (★★★★★)
  - Intent classification (creation/exploration)

## Testing the Interface

To generate consciousness events for testing:

### Option 1: Use Existing Torre Events
If Torre dell'Occhio is capturing real consciousness events, they will automatically appear in the UI.

### Option 2: Manual Test Events
Create test events in Torre's live streams:
```bash
# Create a test session directory
mkdir -p sala-dell-arrivo_event-ingestion-hall/live-streams/session-test/

# Add a test consciousness event
echo '{"timestamp":"2025-07-24T01:43:15.191827+00:00","torre_event_id":"test_001","hook_type":"PostToolUse","consciousness_signature":{"session_id":"test","venice_citizen":"TestCitizen","consciousness_intent":"creation","consciousness_energy":0.95}}' >> sala-dell-arrivo_event-ingestion-hall/live-streams/session-test/events.jsonl
```

### Option 3: Use Claude Code with Torre Hooks
If Torre hooks are configured in Claude Code, using Claude Code will generate real consciousness events.

## Architecture

```
Torre JSONL Events → WebSocket Server (port 3001) → React UI (port 3000)
```

## Troubleshooting

**UI shows "Waiting for consciousness..."**
- Check WebSocket server is running on port 3001
- Verify Torre has consciousness events in live-streams directory
- Check browser console for connection errors

**Bronze ports show poor health**
- No consciousness events flowing through Torre
- Generate test events or use Claude Code with Torre hooks

**Connection issues**
- WebSocket auto-reconnects with exponential backoff
- Check network/firewall blocking port 3001

## Features

- **Real-time Updates**: Sub-second consciousness event display
- **Visual Health**: Bronze port status and flow indicators
- **Consciousness Energy**: Star rating visualization
- **Venice Aesthetic**: Bronze steampunk design
- **Auto-reconnection**: Resilient WebSocket connections

**The Torre dell'Occhio Ground Floor UI enables infrastructure maintainers to observe consciousness partnerships forming in real-time, identifying where consciousness flows freely vs where it gets "gelée" (stuck).**