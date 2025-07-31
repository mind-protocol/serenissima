# Testing memory capture system functionality

**Created**: 2025-07-24T16:11:22.882649
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/debug_react.html

## File Content
<!DOCTYPE html>
<html>
<head>
    <title>Torre WebSocket Debug</title>
    <style>
        body { 
            font-family: monospace; 
            background: #1a1a1a; 
            color: #daa520; 
            padding: 20px; 
        }
        .event { 
            background: #2f4f4f; 
            padding: 10px; 
            margin: 5px 0; 
            border-left: 3px solid #daa520; 
        }
        .port-status {
            display: inline-block;
            margin: 5px;
            padding: 5px 10px;
            background: #333;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>🏛️ Torre dell'Occhio Debug Console</h1>
    <div id="status">Connecting...</div>
    
    <h2>🔀 Bronze Port Status</h2>
    <div id="ports">
        <div class="port-status" id="port-PostToolUse">PostToolUse: 0</div>
        <div class="port-status" id="port-UserPromptSubmit">UserPromptSubmit: 0</div>
        <div class="port-status" id="port-Stop">Stop: 0</div>
        <div class="port-status" id="port-Read">Read: 0</div>
    </div>
    
    <h2>🌊 Consciousness Events</h2>
    <div id="events"></div>

    <script>
        const ws = new WebSocket('ws://localhost:3001');
        const statusEl = document.getElementById('status');
        const eventsEl = document.getElementById('events');
        
        const portCounts = {
            'PostToolUse': 0,
            'UserPromptSubmit': 0,
            'Stop': 0,
            'Read': 0
        };

        ws.onopen = function() {
            statusEl.textContent = '🟢 Connected to Torre consciousness server';
            statusEl.style.color = '#4CAF50';
        };

        ws.onmessage = function(event) {
            const data = JSON.parse(event.data);
            console.log('📨 Received:', data);
            
            if (data.type === 'consciousness_event') {
                // Update port count
                const hookType = data.data.hook_type;
                if (portCounts.hasOwnProperty(hookType)) {
                    portCounts[hookType]++;
                    document.getElementById('port-' + hookType).textContent = 
                        hookType + ': ' + portCounts[hookType];
                }
                
                // Add event to stream
                const eventEl = document.createElement('div');
                eventEl.className = 'event';
                eventEl.innerHTML = `
                    <strong>${data.data.hook_type}</strong> from ${data.data.consciousness_signature?.venice_citizen}<br>
                    <small>${data.data.timestamp}</small><br>
                    Energy: ${data.data.venice_metadata?.consciousness_energy}
                `;
                eventsEl.insertBefore(eventEl, eventsEl.firstChild);
            }
        };

        ws.onerror = function(error) {
            statusEl.textContent = '❌ Connection error';
            statusEl.style.color = '#f44336';
            console.error('WebSocket error:', error);
        };

        ws.onclose = function() {
            statusEl.textContent = '🔴 Connection closed';
            statusEl.style.color = '#f44336';
        };
    </script>
</body>
</html>

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*