const WebSocket = require('ws');

console.log('Testing WebSocket connection...');

const ws = new WebSocket('ws://localhost:3001');

ws.on('open', () => {
    console.log('✅ Connected!');
    ws.close();
});

ws.on('error', (error) => {
    console.log('❌ Error:', error.message);
    console.log('Error code:', error.code);
});

ws.on('close', (code, reason) => {
    console.log('🔴 Closed:', code, reason?.toString());
    process.exit(0);
});

// Force timeout
setTimeout(() => {
    console.log('⏰ Timeout - force exit');
    process.exit(1);
}, 3000);