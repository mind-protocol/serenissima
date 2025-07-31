# Testing memory capture system functionality

**Created**: 2025-07-24T16:09:41.000928
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/test_websocket.js

## File Content
// Quick WebSocket connection test
const WebSocket = require('ws');

console.log('🔍 Testing Torre WebSocket connection...');

const ws = new WebSocket('ws://localhost:3001');

ws.on('open', function() {
    console.log('✅ Connected to Torre consciousness server');
});

ws.on('message', function(data) {
    try {
        const message = JSON.parse(data);
        console.log('📨 Received message type:', message.type);
        
        if (message.type === 'consciousness_event') {
            console.log('🌊 Consciousness Event:', {
                hook_type: message.data.hook_type,
                citizen: message.data.consciousness_signature?.venice_citizen,
                timestamp: message.data.timestamp,
                id: message.data.torre_event_id
            });
        }
    } catch (error) {
        console.log('📨 Raw message:', data.toString());
    }
});

ws.on('error', function(error) {
    console.error('❌ WebSocket error:', error.message);
});

ws.on('close', function() {
    console.log('🔴 Connection closed');
});

// Keep alive for 10 seconds
setTimeout(() => {
    console.log('⏰ Test complete');
    ws.close();
    process.exit(0);
}, 10000);

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*