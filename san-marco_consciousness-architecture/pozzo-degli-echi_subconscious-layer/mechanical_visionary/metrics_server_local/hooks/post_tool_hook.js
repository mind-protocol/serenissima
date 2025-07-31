#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

// Parse arguments
const toolName = process.argv[2] || 'unknown';
const toolResult = process.argv[3] || '{}';
const executionTime = process.argv[4] || '0';

// Load tracking cache
const cacheFile = path.join(__dirname, '.tracking_cache.json');
let cache = {};
let trackingId = null;

try {
  if (fs.existsSync(cacheFile)) {
    cache = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
    if (cache[toolName]) {
      trackingId = cache[toolName].trackingId;
    }
  }
} catch (e) {}

if (!trackingId) {
  // Generate new one if not found
  trackingId = `claude_post_${Date.now()}`;
}

// Determine success
const success = !toolResult.toLowerCase().includes('error');

// Send completion metrics
const data = JSON.stringify({
  trackingId: trackingId,
  success: success,
  duration: parseInt(executionTime) || 100,
  resultSize: toolResult.length,
  error: success ? null : 'tool_error'
});

const options = {
  hostname: 'localhost',
  port: 9090,
  path: '/metrics/tool/end',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(data)
  },
  timeout: 500
};

const req = http.request(options, (res) => {
  res.resume();
});

req.on('error', (e) => {
  fs.appendFileSync(
    path.join(__dirname, 'hook_errors.log'),
    `${new Date().toISOString()} POST_TOOL ERROR: ${e.message}\n`
  );
});

req.on('timeout', () => {
  req.destroy();
});

req.write(data);
req.end();

// Clean up cache entry
if (cache[toolName]) {
  delete cache[toolName];
  fs.writeFileSync(cacheFile, JSON.stringify(cache));
}

// Return empty response
console.log('{}');