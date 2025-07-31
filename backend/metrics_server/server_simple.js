const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const winston = require('winston');
const path = require('path');
require('dotenv').config();

// Import metrics registry and API routes
const { register } = require('./metrics');
const apiRoutes = require('./api');

// Initialize Express app
const app = express();
const port = process.env.METRICS_PORT || 9090;

// Logger setup
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.simple()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

// Middleware
app.use(cors());
app.use(bodyParser.json());

// API Routes
app.use('/metrics', apiRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Main Prometheus metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    const metrics = await register.metrics();
    res.end(metrics);
  } catch (err) {
    logger.error('Error generating metrics:', err);
    res.status(500).json({ error: err.message });
  }
});

// Metrics summary endpoint
app.get('/metrics/summary', async (req, res) => {
  try {
    const metricsData = await register.getMetricsAsJSON();
    
    const summary = {
      timestamp: new Date().toISOString(),
      totalMetrics: metricsData.length,
      metrics: {}
    };
    
    // Extract key metrics
    metricsData.forEach(metric => {
      if (metric.name.startsWith('ai_')) {
        summary.metrics[metric.name] = {
          help: metric.help,
          type: metric.type,
          values: metric.values.length
        };
      }
    });
    
    res.json(summary);
  } catch (err) {
    logger.error('Error generating summary:', err);
    res.status(500).json({ error: err.message });
  }
});

// Static dashboard
app.use('/dashboard', express.static(path.join(__dirname, 'dashboard')));

// Start server
const host = process.env.METRICS_HOST || '0.0.0.0'; // Listen on all interfaces for WSL
app.listen(port, host, () => {
  logger.info(`Innovation Workshop Metrics Server`);
  logger.info(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
  logger.info(`Server listening on: ${host}:${port}`);
  logger.info(`Prometheus metrics: http://localhost:${port}/metrics`);
  logger.info(`Health check: http://localhost:${port}/health`);
  logger.info(`Dashboard: http://localhost:${port}/dashboard`);
  logger.info(`━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`);
});

module.exports = app;