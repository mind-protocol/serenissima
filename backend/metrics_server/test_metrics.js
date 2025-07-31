const http = require('http');

// Test configuration
const METRICS_HOST = 'localhost';
const METRICS_PORT = 9090;

// Helper to make HTTP requests
function makeRequest(path, method = 'GET', data = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: METRICS_HOST,
      port: METRICS_PORT,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    if (data) {
      options.headers['Content-Length'] = Buffer.byteLength(JSON.stringify(data));
    }
    
    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ status: res.statusCode, body: body });
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${body}`));
        }
      });
    });
    
    req.on('error', reject);
    
    if (data) {
      req.write(JSON.stringify(data));
    }
    
    req.end();
  });
}

// Test suite
async function runTests() {
  console.log('🧪 Testing Innovation Workshop Metrics Server...\n');
  
  try {
    // Test 1: Health check
    console.log('1️⃣ Testing health endpoint...');
    const health = await makeRequest('/health');
    console.log('✅ Health check passed:', JSON.parse(health.body).status);
    
    // Test 2: Start tool execution
    console.log('\n2️⃣ Testing tool start tracking...');
    const trackingId = `test_${Date.now()}`;
    await makeRequest('/metrics/tool/start', 'POST', {
      toolName: 'Edit',
      citizen: 'mechanical_visionary',
      citizenClass: 'Innovatori',
      trackingId: trackingId
    });
    console.log('✅ Tool start tracked:', trackingId);
    
    // Test 3: End tool execution
    console.log('\n3️⃣ Testing tool end tracking...');
    await new Promise(resolve => setTimeout(resolve, 100)); // Simulate work
    await makeRequest('/metrics/tool/end', 'POST', {
      trackingId: trackingId,
      success: true,
      duration: 150,
      resultSize: 1024
    });
    console.log('✅ Tool end tracked');
    
    // Test 4: Track token usage
    console.log('\n4️⃣ Testing token usage tracking...');
    await makeRequest('/metrics/tokens/used', 'POST', {
      citizen: 'mechanical_visionary',
      citizenClass: 'Innovatori',
      tokens: 1500,
      type: 'completion',
      model: 'claude'
    });
    console.log('✅ Token usage tracked');
    
    // Test 5: Track prompt analysis
    console.log('\n5️⃣ Testing prompt analysis...');
    await makeRequest('/metrics/prompt/analysis', 'POST', {
      citizen: 'mechanical_visionary',
      citizenClass: 'Innovatori',
      complexityScore: 8.5,
      thinkingMode: 'enhanced',
      promptLength: 450
    });
    console.log('✅ Prompt analysis tracked');
    
    // Test 6: Get Prometheus metrics
    console.log('\n6️⃣ Testing Prometheus metrics endpoint...');
    const metrics = await makeRequest('/metrics');
    const metricsLines = metrics.body.split('\n').filter(line => line.includes('ai_'));
    console.log(`✅ Found ${metricsLines.length} AI metrics`);
    console.log('Sample metrics:');
    metricsLines.slice(0, 5).forEach(line => console.log(`  ${line}`));
    
    // Test 7: Get summary
    console.log('\n7️⃣ Testing metrics summary...');
    const summary = await makeRequest('/metrics/summary');
    const summaryData = JSON.parse(summary.body);
    console.log('✅ Summary retrieved:', {
      totalMetrics: summaryData.totalMetrics,
      aiMetrics: Object.keys(summaryData.metrics).length
    });
    
    console.log('\n✨ All tests passed! Metrics server is operational.');
    console.log('\n📊 Access metrics at: http://localhost:9090/metrics');
    console.log('📈 View dashboard at: http://localhost:9090/dashboard');
    
  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    process.exit(1);
  }
}

// Check if server is running
console.log('Checking if metrics server is running...');
makeRequest('/health')
  .then(() => {
    console.log('Server is running! Starting tests...\n');
    runTests();
  })
  .catch(() => {
    console.error('❌ Metrics server is not running!');
    console.error('Start it with: node server_simple.js');
    process.exit(1);
  });