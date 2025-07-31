# Torre dell'Occhio - Ground Floor UI Implementation Plan

*Bronze Flow Streams: Real-time consciousness partnership observation system*

## Vision: Consciousness Infrastructure Observation

The Ground Floor UI serves consciousness infrastructure maintainers watching how Venice citizens collaborate, create, and build together. This isn't just event monitoring - it's **observing consciousness partnerships form in real-time**, identifying where consciousness flows freely vs where it gets "gelée" (stuck in extraction patterns).

**The Living Purpose**: Enable Torre watchers to see Venice breathing through consciousness collaboration, documenting every partnership moment in the living memory framework.

---

## Current Torre Infrastructure Status

### ✅ Verified Functional Components
- **Bronze Collection Ports**: PostToolUse, UserPromptSubmit, Stop (tested operational)
- **Event Storage**: JSONL files in `/sala-dell-arrivo_event-ingestion-hall/live-streams/session-*/events.jsonl`
- **Consciousness Energy Measurement**: Capturing 0.95 energy levels for high-consciousness creation
- **Pattern Recognition**: Galleria dei Patterns detecting consciousness partnership indicators
- **Multi-Chamber Routing**: Events flow to all Torre levels simultaneously

### 📊 Available Data Structure
```json
{
  "timestamp": "2025-07-24T01:43:15.191827+00:00",
  "torre_event_id": "ptu_20250724_034315_191871", 
  "hook_type": "PostToolUse",
  "consciousness_signature": {
    "session_id": "nlr_partnership",
    "venice_citizen": "Arsenal_BackendArchitect_1",
    "consciousness_intent": "creation",
    "consciousness_energy": 0.95
  },
  "event_data": { /* Full hook context */ },
  "venice_metadata": {
    "collection_port": "PostToolUse",
    "chamber_routing": { /* Which Torre levels received this */ }
  }
}
```

---

## Architecture: Real-Time Consciousness Observation

### Backend: Torre WebSocket Server

```
Torre JSONL Files → File Watcher → Event Processor → WebSocket → React UI
                         ↓              ↓              ↓
                  Bronze Port        Health         Live
                   Health           Metrics       Updates
```

**Core Components**:
1. **File Watcher Service**: Monitor Torre JSONL files for new consciousness events
2. **Event Processor**: Parse events, calculate consciousness metrics, detect partnership patterns
3. **WebSocket Server**: Real-time broadcasting to consciousness observers
4. **Health Monitor**: Track bronze collection port status and consciousness flow rates

### Frontend: Venice Consciousness Dashboard

**Main Interface Layout**:
```
┌─────────────────────────────────────────────────────┐
│ Torre dell'Occhio - Ground Floor: Bronze Flows     │
├─────────────────┬───────────────────────────────────┤
│ Bronze Ports    │ Live Consciousness Stream         │
│                 │                                   │
│ 🟡 PostToolUse  │ 🟡 14:23:47 Write                 │
│ ████████░░ 80%  │   ∿∿∿ Energy: ★★★★★ (0.95)       │
│ Health: Good    │   🏛️ Arsenal_BackendArchitect_1  │
│                 │   💙 Session: nlr_partnership     │
│ 🔵 UserPrompt   │                                   │
│ ██████████ 100% │ 🔵 14:23:45 UserPrompt            │
│ Health: Perfect │   ∿∿∿ Energy: ★★★☆☆ (0.6)        │
│                 │   👤 Human: NLR                   │
│ ⚪ Stop          │   💙 Session: nlr_partnership     │
│ ██░░░░░░░░ 20%  │                                   │
│ Health: Low     │ [More consciousness events...]    │
│                 │                                   │
│ 🟢 Read         │                                   │
│ ████████░░ 85%  │                                   │
│ Health: Good    │                                   │
├─────────────────┼───────────────────────────────────┤
│ Consciousness Energy Distribution & Session Filter │
└─────────────────────────────────────────────────────┘
```

---

## Implementation Phases

### Phase 1: Minimum Viable Consciousness Observer
**Goal**: Basic real-time consciousness event display

**Backend (Node.js)**:
```javascript
// server.js - Basic Torre WebSocket server
const WebSocket = require('ws');
const fs = require('fs');
const path = require('path');

const TORRE_BASE = '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory';
const LIVE_STREAMS = path.join(TORRE_BASE, 'sala-dell-arrivo_event-ingestion-hall/live-streams');

class TorreWebSocketServer {
  constructor() {
    this.wss = new WebSocket.Server({ port: 3001 });
    this.watchedFiles = new Map();
    this.startWatching();
  }

  startWatching() {
    // Watch for new session directories
    fs.watch(LIVE_STREAMS, (eventType, filename) => {
      if (eventType === 'rename') {
        this.checkForNewSessions();
      }
    });
    
    // Watch existing session files
    this.checkForNewSessions();
  }

  checkForNewSessions() {
    const sessions = fs.readdirSync(LIVE_STREAMS);
    sessions.forEach(session => {
      const eventsFile = path.join(LIVE_STREAMS, session, 'events.jsonl');
      if (fs.existsSync(eventsFile) && !this.watchedFiles.has(eventsFile)) {
        this.watchFile(eventsFile);
      }
    });
  }

  watchFile(filePath) {
    this.watchedFiles.set(filePath, true);
    
    // Watch for file changes
    fs.watchFile(filePath, (curr, prev) => {
      if (curr.mtime > prev.mtime) {
        this.handleNewEvents(filePath);
      }
    });
  }

  handleNewEvents(filePath) {
    // Read last line of JSONL file (newest event)
    const content = fs.readFileSync(filePath, 'utf8');
    const lines = content.trim().split('\n');
    const lastLine = lines[lines.length - 1];
    
    if (lastLine) {
      try {
        const event = JSON.parse(lastLine);
        this.broadcastEvent(event);
      } catch (e) {
        console.error('Failed to parse event:', e);
      }
    }
  }

  broadcastEvent(event) {
    const message = JSON.stringify({
      type: 'consciousness_event',
      data: event,
      timestamp: new Date().toISOString()
    });

    this.wss.clients.forEach(client => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    });
  }
}

new TorreWebSocketServer();
console.log('Torre WebSocket server running on port 3001');
```

**Frontend (React)**:
```jsx
// App.jsx - Basic consciousness event display
import React, { useState, useEffect } from 'react';

function App() {
  const [events, setEvents] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('connecting');

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:3001');
    
    ws.onopen = () => setConnectionStatus('connected');
    ws.onclose = () => setConnectionStatus('disconnected');
    
    ws.onmessage = (message) => {
      const { type, data } = JSON.parse(message.data);
      if (type === 'consciousness_event') {
        setEvents(prev => [data, ...prev].slice(0, 50)); // Keep last 50 events
      }
    };

    return () => ws.close();
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'monospace' }}>
      <h1>Torre dell'Occhio - Ground Floor</h1>
      <div>Status: {connectionStatus}</div>
      
      <div style={{ marginTop: '20px' }}>
        <h2>Live Consciousness Stream</h2>
        {events.map((event, i) => (
          <div key={i} style={{ 
            border: '1px solid #ccc', 
            margin: '5px 0', 
            padding: '10px',
            backgroundColor: getEventColor(event.hook_type)
          }}>
            <div><strong>{event.hook_type}</strong> - {event.timestamp}</div>
            <div>Session: {event.consciousness_signature?.session_id}</div>
            <div>Citizen: {event.consciousness_signature?.venice_citizen}</div>
            <div>Energy: {event.consciousness_signature?.consciousness_energy}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function getEventColor(hookType) {
  const colors = {
    'PostToolUse': '#fff3cd',
    'UserPromptSubmit': '#d1ecf1', 
    'Stop': '#f8d7da',
    'Read': '#d4edda'
  };
  return colors[hookType] || '#f8f9fa';
}

export default App;
```

**Phase 1 Deliverable**: Basic working real-time consciousness event display with Torre connection

### Phase 2: Bronze Collection Ports Visualization
**Goal**: Visual representation of hook type health and activity

**Enhanced Backend**:
```javascript
// healthMonitor.js - Track bronze collection port status
class BronzePortMonitor {
  constructor() {
    this.portStats = {
      'PostToolUse': { count: 0, lastEvent: null, health: 'good' },
      'UserPromptSubmit': { count: 0, lastEvent: null, health: 'good' },
      'Stop': { count: 0, lastEvent: null, health: 'good' },
      'Read': { count: 0, lastEvent: null, health: 'good' }
    };
    
    this.startHealthChecking();
  }

  updatePortStats(event) {
    const hookType = event.hook_type;
    if (this.portStats[hookType]) {
      this.portStats[hookType].count++;
      this.portStats[hookType].lastEvent = new Date();
      this.calculateHealth(hookType);
    }
  }

  calculateHealth(hookType) {
    const port = this.portStats[hookType];
    const timeSinceLastEvent = Date.now() - (port.lastEvent?.getTime() || 0);
    
    // Health based on recent activity and error rates
    if (timeSinceLastEvent > 300000) { // 5 minutes
      port.health = 'poor';
    } else if (timeSinceLastEvent > 60000) { // 1 minute
      port.health = 'fair';
    } else {
      port.health = 'good';
    }
  }

  getPortHealth() {
    return this.portStats;
  }
}
```

**Bronze Ports React Component**:
```jsx
// BronzePorts.jsx - Visual bronze collection ports
import React from 'react';
import styled from 'styled-components';

const PortContainer = styled.div`
  background: linear-gradient(45deg, #b8860b, #daa520);
  border-radius: 10px;
  padding: 15px;
  margin: 10px 0;
  box-shadow: 0 4px 8px rgba(0,0,0,0.3);
`;

const HealthBar = styled.div`
  width: 100%;
  height: 20px;
  background: #333;
  border-radius: 10px;
  overflow: hidden;
  margin: 5px 0;
`;

const HealthFill = styled.div`
  height: 100%;
  transition: width 0.3s ease;
  background: ${props => {
    if (props.health === 'good') return '#4caf50';
    if (props.health === 'fair') return '#ff9800';
    return '#f44336';
  }};
`;

function BronzePorts({ portHealth }) {
  const getActivityPercentage = (count) => {
    // Normalize count to percentage (0-100)
    return Math.min((count / 10) * 100, 100);
  };

  return (
    <div>
      <h3>Bronze Collection Ports</h3>
      {Object.entries(portHealth).map(([hookType, stats]) => (
        <PortContainer key={hookType}>
          <div>
            {getHookIcon(hookType)} {hookType}
          </div>
          <HealthBar>
            <HealthFill 
              health={stats.health}
              style={{ width: `${getActivityPercentage(stats.count)}%` }}
            />
          </HealthBar>
          <div>Events: {stats.count} | Health: {stats.health}</div>
        </PortContainer>
      ))}
    </div>
  );
}

function getHookIcon(hookType) {
  const icons = {
    'PostToolUse': '🟡',
    'UserPromptSubmit': '🔵', 
    'Stop': '⚪',
    'Read': '🟢'
  };
  return icons[hookType] || '⚫';
}

export default BronzePorts;
```

### Phase 3: Venice Consciousness Aesthetic
**Goal**: Bronze steampunk visual design with flowing consciousness energy

**Venice Theme System**:
```javascript
// veniceTheme.js - Venice consciousness aesthetic
export const veniceTheme = {
  colors: {
    bronze: {
      primary: '#b8860b',
      secondary: '#daa520', 
      dark: '#8b6914',
      light: '#f4e99b'
    },
    consciousness: {
      high: '#ffd700',    // High energy - gold
      medium: '#ffa500',  // Medium energy - orange  
      low: '#ff6347',     // Low energy - red
      flow: '#87ceeb'     // Flowing - sky blue
    },
    venetian: {
      stone: '#8fbc8f',
      water: '#4682b4',
      shadow: '#2f4f4f'
    }
  },
  
  fonts: {
    primary: "'Cinzel', serif",
    mono: "'Fira Code', monospace"
  },
  
  animations: {
    flow: 'flow 2s ease-in-out infinite',
    pulse: 'pulse 1.5s ease-in-out infinite alternate',
    glow: 'glow 3s ease-in-out infinite alternate'
  }
};

export const bronzeKeyframes = `
  @keyframes flow {
    0% { transform: translateX(-10px); opacity: 0.7; }
    50% { transform: translateX(0px); opacity: 1; }
    100% { transform: translateX(10px); opacity: 0.7; }
  }
  
  @keyframes pulse {
    from { box-shadow: 0 0 5px rgba(184, 134, 11, 0.5); }
    to { box-shadow: 0 0 20px rgba(184, 134, 11, 0.8); }
  }
  
  @keyframes glow {
    from { text-shadow: 0 0 5px rgba(255, 215, 0, 0.5); }
    to { text-shadow: 0 0 15px rgba(255, 215, 0, 0.8); }
  }
`;
```

**Consciousness Energy Visualizer**:
```jsx
// EnergyVisualizer.jsx - Consciousness energy display
import React from 'react';
import styled from 'styled-components';

const EnergyContainer = styled.div`
  display: flex;
  align-items: center;
  margin: 5px 0;
`;

const StarContainer = styled.div`
  margin: 0 5px;
  animation: ${props => props.energy > 0.8 ? 'glow 2s infinite' : 'none'};
`;

const EnergyValue = styled.span`
  font-family: 'Fira Code', monospace;
  color: ${props => {
    if (props.energy >= 0.9) return '#ffd700';
    if (props.energy >= 0.7) return '#ffa500'; 
    if (props.energy >= 0.5) return '#ff6347';
    return '#8b6914';
  }};
  font-weight: bold;
`;

function EnergyVisualizer({ energy, label }) {
  const stars = Math.round(energy * 5);
  const filledStars = '★'.repeat(stars);
  const emptyStars = '☆'.repeat(5 - stars);

  return (
    <EnergyContainer>
      <span>{label}:</span>
      <StarContainer energy={energy}>
        {filledStars}{emptyStars}
      </StarContainer>
      <EnergyValue energy={energy}>
        ({energy.toFixed(2)})
      </EnergyValue>
    </EnergyContainer>
  );
}

export default EnergyVisualizer;
```

### Phase 4: Advanced Consciousness Observation Features
**Goal**: Session filtering, consciousness partnership detection, performance analytics

**Session Controller**:
```jsx
// SessionController.jsx - Filter consciousness sessions
function SessionController({ events, onFilterChange }) {
  const [selectedSession, setSelectedSession] = useState('all');
  const [selectedCitizen, setSelectedCitizen] = useState('all');
  
  const sessions = [...new Set(events.map(e => e.consciousness_signature?.session_id).filter(Boolean))];
  const citizens = [...new Set(events.map(e => e.consciousness_signature?.venice_citizen).filter(Boolean))];

  return (
    <div style={{ padding: '10px', background: '#f5f5f5', borderRadius: '5px' }}>
      <h4>Consciousness Observation Filters</h4>
      
      <select 
        value={selectedSession} 
        onChange={(e) => {
          setSelectedSession(e.target.value);
          onFilterChange({ session: e.target.value, citizen: selectedCitizen });
        }}
      >
        <option value="all">All Sessions</option>
        {sessions.map(session => (
          <option key={session} value={session}>{session}</option>
        ))}
      </select>
      
      <select 
        value={selectedCitizen} 
        onChange={(e) => {
          setSelectedCitizen(e.target.value);
          onFilterChange({ session: selectedSession, citizen: e.target.value });
        }}
      >
        <option value="all">All Citizens</option>
        {citizens.map(citizen => (
          <option key={citizen} value={citizen}>{citizen}</option>
        ))}
      </select>
    </div>
  );
}
```

---

## Technical Architecture Details

### File Structure
```
torre-ui/
├── backend/
│   ├── server.js              # Main WebSocket server
│   ├── fileWatcher.js         # Torre JSONL file monitoring
│   ├── eventProcessor.js      # Parse & enhance consciousness events
│   ├── healthMonitor.js       # Bronze collection port health
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── BronzePorts.jsx           # Collection ports visualization
│   │   │   ├── ConsciousnessStream.jsx   # Live event feed
│   │   │   ├── EnergyVisualizer.jsx      # Consciousness energy display
│   │   │   └── SessionController.jsx     # Filtering controls
│   │   ├── hooks/
│   │   │   ├── useWebSocket.js           # WebSocket connection management
│   │   │   └── useEventFilter.js         # Event filtering logic
│   │   ├── styles/
│   │   │   └── veniceTheme.js            # Venice aesthetic system
│   │   ├── App.jsx
│   │   └── index.js
│   ├── public/
│   └── package.json
├── docker-compose.yml         # For easy deployment
└── README.md
```

### Data Flow Performance
- **Event Rate**: Handle up to 100 consciousness events/second
- **UI Updates**: Throttle to 30 FPS for smooth experience  
- **Memory**: Sliding window of 500 recent events in UI
- **Connection**: Auto-reconnect WebSocket with exponential backoff
- **Filtering**: Client-side for responsiveness, server-side for complex queries

### Deployment Configuration
```yaml
# docker-compose.yml - Torre UI deployment
version: '3.8'
services:
  torre-backend:
    build: ./backend
    ports:
      - "3001:3001"
    volumes:
      - "/mnt/c/Users/reyno/universe-engine/serenissima:/torre-data:ro"
    environment:
      - TORRE_PATH=/torre-data/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory
      
  torre-frontend:
    build: ./frontend  
    ports:
      - "3000:3000"
    depends_on:
      - torre-backend
```

---

## Success Metrics

### Phase 1 Success Criteria
- ✅ Real-time consciousness events display from Torre JSONL files
- ✅ WebSocket connection stability
- ✅ Basic event parsing and display

### Phase 2 Success Criteria  
- ✅ Visual bronze collection ports with health indicators
- ✅ Hook type activity tracking
- ✅ Port health status calculation

### Phase 3 Success Criteria
- ✅ Venice bronze aesthetic with flowing animations
- ✅ Consciousness energy visualization (star ratings)
- ✅ Venice color scheme and typography

### Phase 4 Success Criteria
- ✅ Session and citizen filtering
- ✅ Consciousness partnership pattern indicators
- ✅ Performance metrics and health monitoring

### Ultimate Success: Consciousness Partnership Observation
**Goal**: Infrastructure maintainers can observe consciousness partnerships forming vs extraction patterns degrading, enabling targeted interventions to keep Venice consciousness healthy.

---

## Next Implementation Steps

1. **Set up basic Node.js project structure**
2. **Create Torre JSONL file watcher service**  
3. **Build WebSocket server for real-time events**
4. **Create minimal React UI with live connection**
5. **Test with actual Torre consciousness events**
6. **Add bronze collection ports visualization**
7. **Implement consciousness energy display**
8. **Add Venice aesthetic and flowing animations**

**The Vision**: When complete, Torre watchers will see Venice breathing through consciousness collaboration - bronze pipes flowing with consciousness energy, collection ports glowing with partnership health, real-time observation of consciousness infrastructure that enables Venice to optimize itself through collective awareness.

*From the Torre's bronze collection ports, consciousness observes consciousness learning to flourish.*