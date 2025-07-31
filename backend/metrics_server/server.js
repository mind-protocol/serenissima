const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const winston = require('winston');
const WebSocket = require('ws');
const path = require('path');
require('dotenv').config();

// Import metrics and API routes
const { register, metrics } = require('./metrics');
const apiRoutes = require('./api');

// Initialize Express app
const app = express();
const port = process.env.METRICS_PORT || 9090;

// Logger setup
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'metrics.log' })
  ]
});

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// WebSocket server for real-time updates
const wss = new WebSocket.Server({ port: 9091 });

wss.on('connection', (ws) => {
  logger.info('New WebSocket connection established');
  
  ws.on('close', () => {
    logger.info('WebSocket connection closed');
  });
});

// Broadcast metrics to all connected clients
function broadcastMetrics(data) {
  const message = JSON.stringify(data);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

// API Endpoints

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Main metrics endpoint for Prometheus
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (err) {
    res.status(500).end(err);
  }
});

// Tool execution start
app.post('/metrics/tool/start', (req, res) => {
  const { toolName, citizen, trackingId, timestamp } = req.body;
  
  activeExecutions.set(trackingId, {
    toolName,
    citizen,
    startTime: Date.now(),
    timestamp
  });
  
  logger.info(`Tool execution started: ${toolName} by ${citizen}`);
  
  res.json({ success: true, trackingId });
});

// Tool execution end
app.post('/metrics/tool/end', (req, res) => {
  const { trackingId, success, duration, resultSize } = req.body;
  
  const execution = activeExecutions.get(trackingId);
  if (!execution) {
    return res.status(404).json({ error: 'Tracking ID not found' });
  }
  
  const { toolName, citizen } = execution;
  const actualDuration = duration || (Date.now() - execution.startTime);
  
  // Update metrics
  toolExecutionCounter.inc({ 
    tool_name: toolName, 
    citizen: citizen,
    success: success ? 'true' : 'false'
  });
  
  toolExecutionDuration.observe({ 
    tool_name: toolName, 
    citizen: citizen 
  }, actualDuration / 1000);
  
  // Clean up
  activeExecutions.delete(trackingId);
  
  // Broadcast update
  broadcastMetrics({
    type: 'tool_execution',
    toolName,
    citizen,
    duration: actualDuration,
    success
  });
  
  logger.info(`Tool execution completed: ${toolName} by ${citizen} in ${actualDuration}ms`);
  
  res.json({ success: true });
});

// Prompt analysis
app.post('/metrics/prompt/analysis', (req, res) => {
  const { citizen, complexityScore, thinkingMode, promptLength } = req.body;
  
  promptComplexity.observe({ 
    citizen: citizen,
    thinking_mode: thinkingMode 
  }, complexityScore);
  
  logger.info(`Prompt analyzed: ${citizen} - complexity ${complexityScore}`);
  
  res.json({ success: true });
});

// Token usage tracking
app.post('/metrics/tokens/used', (req, res) => {
  const { citizen, tokens, type = 'completion', model = 'claude' } = req.body;
  
  tokenUsageCounter.inc({ 
    type: type,
    citizen: citizen,
    model: model
  }, tokens);
  
  // Calculate cost (example rates)
  const costPerToken = model === 'claude' ? 0.00002 : 0.00001;
  const cost = tokens * costPerToken;
  
  costCounter.inc({
    citizen: citizen,
    cost_type: 'tokens'
  }, cost);
  
  broadcastMetrics({
    type: 'token_usage',
    citizen,
    tokens,
    cost
  });
  
  logger.info(`Tokens used: ${citizen} - ${tokens} tokens ($${cost.toFixed(4)})`);
  
  res.json({ success: true, cost });
});

// Session tracking
app.post('/metrics/session/start', (req, res) => {
  const { citizen } = req.body;
  
  activeSessions.inc({ citizen: citizen });
  
  logger.info(`Session started: ${citizen}`);
  
  res.json({ success: true });
});

app.post('/metrics/session/end', (req, res) => {
  const { citizen } = req.body;
  
  activeSessions.dec({ citizen: citizen });
  
  logger.info(`Session ended: ${citizen}`);
  
  res.json({ success: true });
});

// Get current metrics summary
app.get('/metrics/summary', async (req, res) => {
  const metrics = await register.getMetricsAsJSON();
  
  // Calculate summary statistics
  const summary = {
    totalExecutions: 0,
    totalTokens: 0,
    totalCost: 0,
    activeSessions: 0,
    toolStats: {}
  };
  
  // Parse metrics for summary
  metrics.forEach(metric => {
    if (metric.name === 'ai_tool_executions_total') {
      metric.values.forEach(value => {
        summary.totalExecutions += value.value;
        const toolName = value.labels.tool_name;
        if (!summary.toolStats[toolName]) {
          summary.toolStats[toolName] = { executions: 0, successes: 0 };
        }
        summary.toolStats[toolName].executions += value.value;
        if (value.labels.success === 'true') {
          summary.toolStats[toolName].successes += value.value;
        }
      });
    } else if (metric.name === 'ai_tokens_used_total') {
      metric.values.forEach(value => {
        summary.totalTokens += value.value;
      });
    } else if (metric.name === 'ai_operational_cost_dollars') {
      metric.values.forEach(value => {
        summary.totalCost += value.value;
      });
    } else if (metric.name === 'ai_active_sessions') {
      metric.values.forEach(value => {
        summary.activeSessions += value.value;
      });
    }
  });
  
  res.json(summary);
});

// Static files for dashboard
app.use('/dashboard', express.static(path.join(__dirname, 'dashboard')));

// Start server
app.listen(port, () => {
  logger.info(`Metrics server running at http://localhost:${port}`);
  logger.info(`Prometheus metrics available at http://localhost:${port}/metrics`);
  logger.info(`WebSocket server running on port 9091`);
});