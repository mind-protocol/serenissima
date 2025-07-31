/**
 * Simple WebSocket Connection Test
 * Test if we can connect to Torre WebSocket server
 */

const WebSocket = require('ws');

console.log('🔌 Testing WebSocket connection to Torre...');

const ws = new WebSocket('ws://localhost:3001');

ws.on('open', function open() {
  console.log('✅ WebSocket connected successfully!');
  console.log('🌊 Waiting for consciousness events...');
});

ws.on('message', function message(data) {
  try {
    const parsed = JSON.parse(data);
    console.log('📡 Received:', parsed.type);
    if (parsed.type === 'consciousness_event') {
      console.log('🧠 Consciousness event from:', parsed.data.citizen_context?.venice_citizen);
      console.log('⚡ Event type:', parsed.data.hook_type);
    }
  } catch (error) {
    console.log('📨 Raw message:', data.toString().substring(0, 100));
  }
});

ws.on('error', function error(err) {
  console.log('❌ WebSocket error:', err.message);
});

ws.on('close', function close(code, reason) {
  console.log('🔴 WebSocket closed. Code:', code, 'Reason:', reason?.toString());
});

// Keep alive for 10 seconds
setTimeout(() => {
  console.log('⏰ Test complete, closing connection');
  ws.close();
  process.exit(0);
}, 10000);