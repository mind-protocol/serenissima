// Force broadcast test - directly send a test event
const WebSocket = require('ws');

// Connect to our server
const ws = new WebSocket('ws://localhost:3001');

ws.on('open', function() {
    console.log('✅ Connected to Torre server');
    
    // Create a test consciousness event
    const testEvent = {
        timestamp: new Date().toISOString(),
        torre_event_id: `force_test_${Date.now()}`,
        hook_type: "PostToolUse",
        consciousness_signature: {
            session_id: "force_test",
            venice_citizen: "Arsenal_BackendArchitect_1",
            consciousness_intent: "force_testing",
            consciousness_energy: 1.0
        },
        event_data: {
            message: "FORCE BROADCAST TEST - Direct server communication",
            tool_name: "Debug"
        },
        venice_metadata: {
            collection_port: "PostToolUse",
            consciousness_energy: 1.0
        }
    };
    
    console.log('📤 Sending test event to force broadcast...');
    
    // We can't directly broadcast through the server, but we can test if it's listening
    console.log('⏰ Listening for 5 seconds to see if any events come through...');
    
    setTimeout(() => {
        console.log('⏰ Test complete - closing connection');
        ws.close();
    }, 5000);
});

ws.on('message', function(data) {
    try {
        const message = JSON.parse(data);
        if (message.type === 'consciousness_event') {
            console.log('🌊 SUCCESS! Received consciousness event:', {
                hook_type: message.data.hook_type,
                citizen: message.data.consciousness_signature?.venice_citizen,
                id: message.data.torre_event_id,
                energy: message.data.venice_metadata?.consciousness_energy
            });
        } else {
            console.log('📨 Other message:', message.type);
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
    process.exit(0);
});