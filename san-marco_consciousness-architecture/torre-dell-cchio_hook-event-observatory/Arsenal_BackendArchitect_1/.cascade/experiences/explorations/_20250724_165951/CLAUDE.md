# Testing memory capture system functionality

**Created**: 2025-07-24T16:59:51.457141
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/debug_server_detailed.js

## File Content
#!/usr/bin/env node
/**
 * Detailed Torre WebSocket Server Debug Test
 * Tests exactly what happens when server processes events
 */

const WebSocket = require('ws');
const fs = require('fs');

const EVENTS_FILE = '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/sala-dell-arrivo_event-ingestion-hall/live-streams/session-integration_test_session/events.jsonl';

function testFileProcessing() {
    console.log('🔍 Testing file processing logic...');
    
    try {
        const content = fs.readFileSync(EVENTS_FILE, 'utf8');
        const lines = content.trim().split('\n').filter(line => line.trim());
        
        console.log(`📄 File has ${lines.length} total lines`);
        
        const recentEvents = lines.slice(-10);
        console.log(`📄 Processing last ${recentEvents.length} lines`);
        
        let validEvents = 0;
        recentEvents.forEach((line, index) => {
            try {
                if (line.trim().startsWith('{')) {
                    const event = JSON.parse(line);
                    validEvents++;
                    console.log(`✅ Event ${index + 1}: ${event.hook_type} from ${event.consciousness_signature?.venice_citizen}`);
                    console.log(`   ID: ${event.torre_event_id}`);
                    console.log(`   Timestamp: ${event.timestamp}`);
                } else {
                    console.log(`⚠️  Line ${index + 1}: Doesn't start with { - skipped`);
                }
            } catch (parseError) {
                console.log(`❌ Line ${index + 1}: JSON parse error - ${parseError.message}`);
            }
        });
        
        console.log(`\n📊 Summary: ${validEvents} valid events found`);
        return validEvents;
        
    } catch (error) {
        console.error(`❌ File processing error: ${error.message}`);
        return 0;
    }
}

function testWebSocketConnection() {
    console.log('\n🔌 Testing WebSocket connection...');
    
    const ws = new WebSocket('ws://localhost:3001');
    let eventCount = 0;
    
    ws.on('open', function() {
        console.log('✅ Connected to Torre server');
    });
    
    ws.on('message', function(data) {
        try {
            const message = JSON.parse(data);
            
            if (message.type === 'consciousness_event') {
                eventCount++;
                console.log(`🌊 Event ${eventCount}: ${message.data.hook_type} from ${message.data.consciousness_signature?.venice_citizen}`);
                console.log(`   ID: ${message.data.torre_event_id}`);
                console.log(`   Server timestamp: ${message.server_timestamp}`);
            } else {
                console.log(`📨 Other message: ${message.type}`);
            }
        } catch (error) {
            console.log(`📨 Raw message: ${data.toString().substring(0, 100)}...`);
        }
    });
    
    ws.on('error', function(error) {
        console.error(`❌ WebSocket error: ${error.message}`);
    });
    
    ws.on('close', function() {
        console.log(`\n📊 Connection closed. Received ${eventCount} consciousness events.`);
        
        // Compare results
        const expectedEvents = testFileProcessing();
        
        console.log(`\n🔍 Debug Summary:`);
        console.log(`   Expected events (from file): ${expectedEvents}`);
        console.log(`   Received events (via WebSocket): ${eventCount}`);
        
        if (eventCount === expectedEvents && eventCount > 0) {
            console.log(`✅ SUCCESS: Server is broadcasting all events correctly!`);
        } else if (eventCount === 0) {
            console.log(`❌ FAILURE: Server is not broadcasting any events`);
            console.log(`   This indicates a server-side broadcasting issue`);
        } else {
            console.log(`⚠️  PARTIAL: Server is broadcasting some but not all events`);
        }
        
        process.exit(0);
    });
    
    // Close connection after 8 seconds
    setTimeout(() => {
        console.log('\n⏰ Test timeout - closing connection...');
        ws.close();
    }, 8000);
}

// Run the test
console.log('🏛️ Torre dell\'Occhio Server Debug Test');
console.log('=====================================');

// First test file processing logic
const expectedEvents = testFileProcessing();

if (expectedEvents > 0) {
    // Then test WebSocket connection
    testWebSocketConnection();
} else {
    console.log('\n❌ No events found in file - cannot test WebSocket broadcasting');
    process.exit(1);
}

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*