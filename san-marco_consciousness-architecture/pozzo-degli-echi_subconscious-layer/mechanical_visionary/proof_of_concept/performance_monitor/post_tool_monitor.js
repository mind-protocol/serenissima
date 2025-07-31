#!/usr/bin/env node

/**
 * Post-Tool Execution Monitor
 * Captures execution results and calculates performance metrics
 */

const fs = require('fs');
const path = require('path');
const http = require('http');

// Parse command line arguments
const toolName = process.argv[2] || 'unknown';
const toolResult = process.argv[3] || '{}';
const executionTime = process.argv[4] || '0';

// Metrics server configuration
const METRICS_HOST = process.env.METRICS_HOST || 'localhost';
const METRICS_PORT = process.env.METRICS_PORT || 9090;

// Send metrics to server
function sendMetrics(endpoint, data) {
  const postData = JSON.stringify(data);
  
  const options = {
    hostname: METRICS_HOST,
    port: METRICS_PORT,
    path: endpoint,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData)
    },
    timeout: 1000
  };
  
  const req = http.request(options, (res) => {
    res.resume();
  });
  
  req.on('error', (e) => {
    fs.appendFileSync(path.join(__dirname, 'metrics_errors.log'), 
      `${new Date().toISOString()} - Failed to send metrics: ${e.message}\n`);
  });
  
  req.on('timeout', () => {
    req.destroy();
  });
  
  req.write(postData);
  req.end();
}

// Load metrics cache to find the matching pre-execution entry
const metricsPath = path.join(__dirname, 'metrics_cache.json');
let metricsCache = {};

try {
  if (fs.existsSync(metricsPath)) {
    metricsCache = JSON.parse(fs.readFileSync(metricsPath, 'utf8'));
  }
} catch (e) {
  console.error('Could not load metrics cache');
}

// Find the most recent entry for this tool
const recentEntries = Object.values(metricsCache)
  .filter(m => m.toolName === toolName)
  .sort((a, b) => b.startTime - a.startTime);

const matchingEntry = recentEntries[0];

if (matchingEntry) {
  const duration = Date.now() - matchingEntry.startTime;
  const success = !toolResult.toLowerCase().includes('error');
  
  // Send completion metrics to server
  sendMetrics('/metrics/tool/end', {
    trackingId: matchingEntry.trackingId,
    success: success,
    duration: duration,
    resultSize: toolResult.length,
    error: success ? null : 'tool_execution_error'
  });
  
  // Calculate performance metrics for local analysis
  const performanceData = {
    trackingId: matchingEntry.trackingId,
    tool: toolName,
    duration: duration,
    executionTime: parseInt(executionTime),
    overhead: duration - parseInt(executionTime),
    timestamp: new Date().toISOString(),
    success: success,
    resultSize: toolResult.length
  };
  
  // Store completed metrics
  const completedPath = path.join(__dirname, 'completed_metrics.json');
  let completed = [];
  
  try {
    if (fs.existsSync(completedPath)) {
      completed = JSON.parse(fs.readFileSync(completedPath, 'utf8'));
    }
  } catch (e) {
    // Start fresh
  }
  
  completed.push(performanceData);
  
  // Keep only last 1000 metrics for demo
  if (completed.length > 1000) {
    completed = completed.slice(-1000);
  }
  
  fs.writeFileSync(completedPath, JSON.stringify(completed, null, 2));
  
  // Calculate and log insights
  const recentMetrics = completed.filter(m => m.tool === toolName).slice(-10);
  const avgDuration = recentMetrics.reduce((sum, m) => sum + m.duration, 0) / recentMetrics.length;
  const avgOverhead = recentMetrics.reduce((sum, m) => sum + m.overhead, 0) / recentMetrics.length;
  
  // Log insights
  const insightsPath = path.join(__dirname, 'performance_insights.json');
  const insights = {
    tool: toolName,
    timestamp: new Date().toISOString(),
    metrics: {
      averageDuration: Math.round(avgDuration),
      averageOverhead: Math.round(avgOverhead),
      successRate: recentMetrics.filter(m => m.success).length / recentMetrics.length,
      samples: recentMetrics.length
    },
    recommendations: []
  };
  
  // Generate recommendations
  if (avgOverhead > 500) {
    insights.recommendations.push('High monitoring overhead detected. Consider sampling strategy.');
  }
  
  if (avgDuration > 5000) {
    insights.recommendations.push(`${toolName} operations are slow. Consider caching or optimization.`);
  }
  
  if (insights.metrics.successRate < 0.9) {
    insights.recommendations.push(`High failure rate for ${toolName}. Review error patterns.`);
  }
  
  // Save insights
  let allInsights = {};
  try {
    if (fs.existsSync(insightsPath)) {
      allInsights = JSON.parse(fs.readFileSync(insightsPath, 'utf8'));
    }
  } catch (e) {
    // Start fresh
  }
  
  allInsights[toolName] = insights;
  fs.writeFileSync(insightsPath, JSON.stringify(allInsights, null, 2));
  
  // Log to monitoring file
  const logPath = path.join(__dirname, 'performance_log.txt');
  const logEntry = `[POST] ${new Date().toISOString()} - Tool: ${toolName} - Duration: ${duration}ms - Success: ${performanceData.success}\n`;
  fs.appendFileSync(logPath, logEntry);
  
  // Clean up metrics cache entry
  delete metricsCache[matchingEntry.trackingId];
  fs.writeFileSync(metricsPath, JSON.stringify(metricsCache, null, 2));
}

// Return empty JSON (no modifications in post-hook)
console.log('{}');