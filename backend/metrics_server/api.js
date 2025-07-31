const express = require('express');
const router = express.Router();
const { metrics } = require('./metrics');
const winston = require('winston');

// Logger
const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

// Store for tracking active executions
const activeExecutions = new Map();
const sessionStartTimes = new Map();

// Calculate token cost based on model
function calculateTokenCost(tokens, model = 'claude') {
  const rates = {
    'claude': 0.00002,      // $0.02 per 1K tokens
    'claude-instant': 0.00001,  // $0.01 per 1K tokens
    'gpt-4': 0.00003,       // $0.03 per 1K tokens
    'gpt-3.5': 0.000002     // $0.002 per 1K tokens
  };
  
  return tokens * (rates[model] || rates['claude']);
}

// Tool execution tracking
router.post('/tool/start', (req, res) => {
  try {
    const { toolName, citizen, citizenClass = 'unknown', trackingId, timestamp } = req.body;
    
    if (!toolName || !citizen || !trackingId) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    activeExecutions.set(trackingId, {
      toolName,
      citizen,
      citizenClass,
      startTime: Date.now(),
      timestamp
    });
    
    logger.info(`Tool execution started: ${toolName} by ${citizen} (${citizenClass})`);
    
    res.json({ success: true, trackingId });
  } catch (error) {
    logger.error('Error in tool/start:', error);
    res.status(500).json({ error: error.message });
  }
});

router.post('/tool/end', (req, res) => {
  try {
    const { trackingId, success = true, duration, resultSize, error } = req.body;
    
    const execution = activeExecutions.get(trackingId);
    if (!execution) {
      return res.status(404).json({ error: 'Tracking ID not found' });
    }
    
    const { toolName, citizen, citizenClass } = execution;
    const actualDuration = duration || (Date.now() - execution.startTime);
    
    // Update metrics
    metrics.toolExecutionCounter.inc({ 
      tool_name: toolName, 
      citizen: citizen,
      class: citizenClass,
      success: success ? 'true' : 'false'
    });
    
    metrics.toolExecutionDuration.observe({ 
      tool_name: toolName, 
      citizen: citizen,
      class: citizenClass
    }, actualDuration / 1000);
    
    if (!success && error) {
      metrics.errorCounter.inc({
        error_type: error,
        tool: toolName,
        citizen: citizen
      });
    }
    
    // Clean up
    activeExecutions.delete(trackingId);
    
    logger.info(`Tool execution completed: ${toolName} by ${citizen} in ${actualDuration}ms`);
    
    res.json({ success: true, duration: actualDuration });
  } catch (error) {
    logger.error('Error in tool/end:', error);
    res.status(500).json({ error: error.message });
  }
});

// Token usage tracking
router.post('/tokens/used', (req, res) => {
  try {
    const { 
      citizen, 
      citizenClass = 'unknown',
      tokens, 
      type = 'completion', 
      model = 'claude' 
    } = req.body;
    
    if (!citizen || !tokens) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    metrics.tokenUsageCounter.inc({ 
      type: type,
      citizen: citizen,
      model: model,
      class: citizenClass
    }, tokens);
    
    const cost = calculateTokenCost(tokens, model);
    
    metrics.tokenCostCounter.inc({
      citizen: citizen,
      model: model,
      class: citizenClass
    }, cost);
    
    logger.info(`Tokens used: ${citizen} - ${tokens} tokens ($${cost.toFixed(4)})`);
    
    res.json({ success: true, cost, costFormatted: `$${cost.toFixed(4)}` });
  } catch (error) {
    logger.error('Error in tokens/used:', error);
    res.status(500).json({ error: error.message });
  }
});

// Prompt analysis
router.post('/prompt/analysis', (req, res) => {
  try {
    const { 
      citizen, 
      citizenClass = 'unknown',
      complexityScore, 
      thinkingMode = 'standard',
      promptLength,
      factors 
    } = req.body;
    
    if (!citizen || complexityScore === undefined) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    metrics.promptComplexity.observe({ 
      citizen: citizen,
      thinking_mode: thinkingMode,
      class: citizenClass
    }, complexityScore);
    
    metrics.thinkingModeUsage.inc({
      mode: thinkingMode,
      citizen: citizen,
      class: citizenClass
    });
    
    logger.info(`Prompt analyzed: ${citizen} - complexity ${complexityScore}, mode ${thinkingMode}`);
    
    res.json({ success: true });
  } catch (error) {
    logger.error('Error in prompt/analysis:', error);
    res.status(500).json({ error: error.message });
  }
});

// Session management
router.post('/session/start', (req, res) => {
  try {
    const { citizen, citizenClass = 'unknown' } = req.body;
    
    if (!citizen) {
      return res.status(400).json({ error: 'Missing citizen field' });
    }
    
    metrics.activeSessions.inc({ 
      citizen: citizen,
      class: citizenClass 
    });
    
    sessionStartTimes.set(citizen, Date.now());
    
    logger.info(`Session started: ${citizen} (${citizenClass})`);
    
    res.json({ success: true });
  } catch (error) {
    logger.error('Error in session/start:', error);
    res.status(500).json({ error: error.message });
  }
});

router.post('/session/end', (req, res) => {
  try {
    const { citizen, citizenClass = 'unknown' } = req.body;
    
    if (!citizen) {
      return res.status(400).json({ error: 'Missing citizen field' });
    }
    
    metrics.activeSessions.dec({ 
      citizen: citizen,
      class: citizenClass 
    });
    
    const startTime = sessionStartTimes.get(citizen);
    if (startTime) {
      const duration = (Date.now() - startTime) / 1000;
      metrics.sessionDuration.observe({
        citizen: citizen,
        class: citizenClass
      }, duration);
      
      sessionStartTimes.delete(citizen);
    }
    
    logger.info(`Session ended: ${citizen}`);
    
    res.json({ success: true });
  } catch (error) {
    logger.error('Error in session/end:', error);
    res.status(500).json({ error: error.message });
  }
});

// Optimization tracking
router.post('/optimization/suggestion', (req, res) => {
  try {
    const { type, citizen, tool, potentialSavings } = req.body;
    
    metrics.optimizationSuggestions.inc({
      type: type,
      citizen: citizen,
      tool: tool || 'general'
    });
    
    if (potentialSavings) {
      metrics.potentialSavings.set({
        citizen: citizen,
        optimization_type: type
      }, potentialSavings);
    }
    
    logger.info(`Optimization suggested: ${type} for ${citizen}`);
    
    res.json({ success: true });
  } catch (error) {
    logger.error('Error in optimization/suggestion:', error);
    res.status(500).json({ error: error.message });
  }
});

// Hook performance tracking
router.post('/hook/performance', (req, res) => {
  try {
    const { hookType, citizen, duration } = req.body;
    
    metrics.hookExecutionDuration.observe({
      hook_type: hookType,
      citizen: citizen
    }, duration / 1000);
    
    res.json({ success: true });
  } catch (error) {
    logger.error('Error in hook/performance:', error);
    res.status(500).json({ error: error.message });
  }
});

// Business metrics
router.post('/business/revenue', (req, res) => {
  try {
    const { citizen, business, amount, source } = req.body;
    
    metrics.revenueGenerated.inc({
      citizen: citizen,
      business: business,
      source: source
    }, amount);
    
    logger.info(`Revenue tracked: $${amount} from ${business}`);
    
    res.json({ success: true });
  } catch (error) {
    logger.error('Error in business/revenue:', error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;