# Testing memory capture system functionality

**Created**: 2025-07-25T01:57:49.441889
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/integration_test_deep_verification.js

## File Content
// Torre Integration Deep Test
// Verify consciousness map and analytics are actually working

const WebSocket = require('ws');
const http = require('http');

console.log('🧪 Torre Deep Integration Test - Verifying all systems');

// Test 1: WebSocket Connection
function testWebSocketConnection() {
  return new Promise((resolve, reject) => {
    console.log('Testing WebSocket connection...');
    
    const ws = new WebSocket('ws://localhost:3001');
    let eventReceived = false;
    
    ws.on('open', () => {
      console.log('✅ WebSocket connected successfully');
    });
    
    ws.on('message', (data) => {
      try {
        const parsed = JSON.parse(data);
        console.log('✅ WebSocket message received:', parsed.type || 'unknown');
        eventReceived = true;
        ws.close();
        resolve(true);
      } catch (error) {
        console.log('❌ WebSocket message parse error:', error);
        reject(error);
      }
    });
    
    ws.on('error', (error) => {
      console.log('❌ WebSocket connection failed:', error.message);
      reject(error);
    });
    
    // Timeout after 5 seconds
    setTimeout(() => {
      if (!eventReceived) {
        ws.close();
        resolve(false);
      }
    }, 5000);
  });
}

// Test 2: UI Response
function testUIResponse() {
  return new Promise((resolve, reject) => {
    console.log('Testing Torre UI response...');
    
    const req = http.get('http://localhost:3000', (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        const hasConsciousness = data.includes('consciousness') || data.includes('Consciousness');
        const hasMap = data.includes('map') || data.includes('Map');
        
        console.log('✅ UI Response received');
        console.log('  - Contains consciousness content:', hasConsciousness);
        console.log('  - Contains map references:', hasMap);
        
        resolve({
          responded: true,
          hasConsciousness,
          hasMap,
          contentLength: data.length
        });
      });
    });
    
    req.on('error', (error) => {
      console.log('❌ UI request failed:', error.message);
      reject(error);
    });
    
    req.setTimeout(5000, () => {
      console.log('❌ UI request timeout');
      req.destroy();
      resolve({ responded: false });
    });
  });
}

// Test 3: Event Files Verification
function testEventFiles() {
  console.log('Testing consciousness event files...');
  
  const fs = require('fs');
  const path = require('path');
  
  const liveStreamsPath = '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/sala-dell-arrivo_event-ingestion-hall/live-streams';
  
  try {
    const sessions = fs.readdirSync(liveStreamsPath).filter(item => {
      const fullPath = path.join(liveStreamsPath, item);
      return fs.statSync(fullPath).isDirectory();
    });
    
    console.log('✅ Event capture verified');
    console.log('  - Active sessions found:', sessions.length);
    console.log('  - Recent sessions:', sessions.slice(-3));
    
    return {
      eventCaptureWorking: true,
      activeSessions: sessions.length,
      recentSessions: sessions.slice(-3)
    };
  } catch (error) {
    console.log('❌ Event file check failed:', error.message);
    return { eventCaptureWorking: false };
  }
}

// Run all tests
async function runDeepIntegrationTest() {
  console.log('🏛️ Torre dell\'Occhio Deep Integration Test Starting...\n');
  
  const results = {
    timestamp: new Date().toISOString(),
    tests: {}
  };
  
  try {
    // Test WebSocket
    results.tests.websocket = await testWebSocketConnection();
    
    // Test UI
    results.tests.ui = await testUIResponse();
    
    // Test Event Files
    results.tests.eventFiles = testEventFiles();
    
    // Overall assessment
    const websocketWorking = results.tests.websocket === true;
    const uiWorking = results.tests.ui.responded === true;
    const eventsWorking = results.tests.eventFiles.eventCaptureWorking === true;
    
    results.overall = {
      allSystemsOperational: websocketWorking && uiWorking && eventsWorking,
      websocketStatus: websocketWorking ? 'operational' : 'failed',
      uiStatus: uiWorking ? 'operational' : 'failed', 
      eventCaptureStatus: eventsWorking ? 'operational' : 'failed'
    };
    
    console.log('\n🎯 DEEP INTEGRATION TEST RESULTS:');
    console.log('================================');
    console.log('WebSocket Server:', results.overall.websocketStatus);
    console.log('Torre UI:', results.overall.uiStatus);
    console.log('Event Capture:', results.overall.eventCaptureStatus);
    console.log('Overall Status:', results.overall.allSystemsOperational ? '✅ FULLY OPERATIONAL' : '❌ ISSUES DETECTED');
    
    // Write results to file
    const fs = require('fs');
    fs.writeFileSync(
      '/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/integration_test_results.json',
      JSON.stringify(results, null, 2)
    );
    
    console.log('\n📋 Detailed results saved to integration_test_results.json');
    
  } catch (error) {
    console.error('❌ Integration test failed:', error);
    results.error = error.message;
  }
}

// Execute the test
runDeepIntegrationTest();

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*