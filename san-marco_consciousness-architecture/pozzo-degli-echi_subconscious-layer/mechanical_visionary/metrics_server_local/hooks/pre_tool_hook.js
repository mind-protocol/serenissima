#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

// Parse arguments
const toolName = process.argv[2] || 'unknown';
const toolArgs = process.argv[3] || '{}';

// Generate tracking ID
const trackingId = `claude_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

// Get citizen info from environment
const citizen = process.env.CITIZEN || 'mechanical_visionary';
const citizenClass = process.env.CITIZEN_CLASS || 'Innovatori';
const sessionId = process.env.CLAUDE_SESSION_ID || 'unknown';

// Send metrics to local server
const data = JSON.stringify({
  toolName: toolName,
  citizen: citizen,
  citizenClass: citizenClass,
  trackingId: trackingId,
  timestamp: new Date().toISOString()
});

const options = {
  hostname: 'localhost',
  port: 9090,
  path: '/metrics/tool/start',
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
  // Log errors but don't interrupt
  fs.appendFileSync(
    path.join(__dirname, 'hook_errors.log'),
    `${new Date().toISOString()} PRE_TOOL ERROR: ${e.message}\n`
  );
});

req.on('timeout', () => {
  req.destroy();
});

req.write(data);
req.end();

// Store tracking ID for post hook
const cacheFile = path.join(__dirname, '.tracking_cache.json');
let cache = {};
try {
  if (fs.existsSync(cacheFile)) {
    cache = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
  }
} catch (e) {}

cache[toolName] = {
  trackingId: trackingId,
  startTime: Date.now()
};

fs.writeFileSync(cacheFile, JSON.stringify(cache));

// Return empty response (no modifications)
console.log('{}');