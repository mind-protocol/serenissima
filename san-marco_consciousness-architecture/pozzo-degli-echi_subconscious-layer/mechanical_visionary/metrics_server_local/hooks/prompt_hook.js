#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

// Parse prompt
const userPrompt = process.argv[2] || '';

// Get citizen info
const citizen = process.env.CITIZEN || 'mechanical_visionary';
const citizenClass = process.env.CITIZEN_CLASS || 'Innovatori';

// Analyze prompt complexity
function analyzeComplexity(prompt) {
  let score = 0;
  
  // Length factor
  if (prompt.length > 500) score += 2;
  if (prompt.length > 1000) score += 3;
  if (prompt.length > 2000) score += 5;
  
  // Question marks
  score += (prompt.match(/\?/g) || []).length * 1.5;
  
  // Keywords
  if (/analyz|investigat|examin|evaluat/i.test(prompt)) score += 3;
  if (/creat|build|design|implement|develop/i.test(prompt)) score += 3;
  if (/strateg|plan|architect|roadmap/i.test(prompt)) score += 4;
  if (/debug|fix|troubleshoot|error|issue/i.test(prompt)) score += 2;
  if (/complex|complicated|intricate|sophisticated/i.test(prompt)) score += 3;
  
  // Code blocks
  score += ((prompt.match(/```/g) || []).length / 2) * 3;
  
  return score;
}

// Determine thinking mode
function getThinkingMode(score) {
  if (score < 3) return 'standard';
  if (score < 7) return 'enhanced';
  if (score < 12) return 'deep';
  return 'maximum';
}

const complexityScore = analyzeComplexity(userPrompt);
const thinkingMode = getThinkingMode(complexityScore);

// Send metrics
const data = JSON.stringify({
  citizen: citizen,
  citizenClass: citizenClass,
  complexityScore: complexityScore,
  thinkingMode: thinkingMode,
  promptLength: userPrompt.length
});

const options = {
  hostname: 'localhost',
  port: 9090,
  path: '/metrics/prompt/analysis',
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
    `${new Date().toISOString()} PROMPT ERROR: ${e.message}\n`
  );
});

req.write(data);
req.end();

// Return optimization hints
const response = {
  thinkingOptimization: {
    suggestedMode: thinkingMode,
    complexityScore: complexityScore,
    hints: complexityScore > 15 ? ['Consider breaking into subtasks'] : []
  }
};

console.log(JSON.stringify(response));