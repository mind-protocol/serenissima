const WebSocket = require('ws');
const { register } = require('./metrics');
const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.simple(),
  transports: [new winston.transports.Console()]
});

function setupWebSocket(server) {
  const wss = new WebSocket.Server({ server, path: '/ws' });
  
  // Broadcast metrics updates to all connected clients
  const broadcastMetrics = async () => {
    try {
      const metricsData = await register.getMetricsAsJSON();
      const summary = {
        timestamp: new Date().toISOString(),
        metrics: {}
      };
      
      metricsData.forEach(metric => {
        if (metric.name.startsWith('ai_')) {
          let total = 0;
          metric.values.forEach(v => {
            total += v.value || 0;
          });
          summary.metrics[metric.name] = {
            type: metric.type,
            value: total,
            values: metric.values
          };
        }
      });
      
      const message = JSON.stringify({
        type: 'metrics_update',
        data: summary
      });
      
      wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
          client.send(message);
        }
      });
    } catch (err) {
      logger.error('Error broadcasting metrics:', err);
    }
  };
  
  // Set up connection handler
  wss.on('connection', (ws) => {
    logger.info('New WebSocket connection established');
    
    // Send initial metrics
    broadcastMetrics();
    
    ws.on('message', (message) => {
      try {
        const data = JSON.parse(message);
        if (data.type === 'ping') {
          ws.send(JSON.stringify({ type: 'pong' }));
        }
      } catch (err) {
        logger.error('WebSocket message error:', err);
      }
    });
    
    ws.on('close', () => {
      logger.info('WebSocket connection closed');
    });
  });
  
  // Broadcast updates every 2 seconds
  setInterval(broadcastMetrics, 2000);
  
  return wss;
}

module.exports = { setupWebSocket };