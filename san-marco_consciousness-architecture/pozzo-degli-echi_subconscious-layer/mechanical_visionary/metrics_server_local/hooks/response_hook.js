#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

// Parse response
const assistantResponse = process.argv[2] || '';

// Get citizen info
const citizen = process.env.CITIZEN || 'mechanical_visionary';
const citizenClass = process.env.CITIZEN_CLASS || 'Innovatori';

// Estimate tokens (rough approximation)
const estimatedTokens = Math.ceil(assistantResponse.length / 4);

// Determine model from response characteristics
let model = 'claude';
if (assistantResponse.length < 500) {
  model = 'claude-instant';
}

// Send token usage metrics
const data = JSON.stringify({
  citizen: citizen,
  citizenClass: citizenClass,
  tokens: estimatedTokens,
  type: 'completion',
  model: model
});

const options = {
  hostname: 'localhost',
  port: 9090,
  path: '/metrics/tokens/used',
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(data)
  },
  timeout: 500
};

const req = http.request(options, (res) => {
  let body = '';
  res.on('data', chunk => body += chunk);
  res.on('end', () => {
    try {
      const result = JSON.parse(body);
      if (result.cost) {
        // Log cost for session tracking
        const sessionLog = path.join(__dirname, '.session_costs.log');
        fs.appendFileSync(
          sessionLog,
          `${new Date().toISOString()} ${citizen} ${result.costFormatted}\n`
        );
      }
    } catch (e) {}
  });
});

req.on('error', (e) => {
  fs.appendFileSync(
    path.join(__dirname, 'hook_errors.log'),
    `${new Date().toISOString()} RESPONSE ERROR: ${e.message}\n`
  );
});

req.write(data);
req.end();

// Return empty response
console.log('{}');