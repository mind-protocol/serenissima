const client = require('prom-client');

// Create metrics registry
const register = new client.Registry();

// Default labels for all metrics
register.setDefaultLabels({
  app: 'venice-ai',
  environment: process.env.NODE_ENV || 'development'
});

// Enable default system metrics
client.collectDefaultMetrics({ register });

// AI Tool Execution Metrics
const toolExecutionCounter = new client.Counter({
  name: 'ai_tool_executions_total',
  help: 'Total number of AI tool executions',
  labelNames: ['tool_name', 'citizen', 'success', 'class'],
  registers: [register]
});

const toolExecutionDuration = new client.Histogram({
  name: 'ai_tool_execution_duration_seconds',
  help: 'Duration of AI tool executions in seconds',
  labelNames: ['tool_name', 'citizen', 'class'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10, 30, 60],
  registers: [register]
});

// Token Usage Metrics
const tokenUsageCounter = new client.Counter({
  name: 'ai_tokens_used_total',
  help: 'Total tokens consumed by AI operations',
  labelNames: ['type', 'citizen', 'model', 'class'],
  registers: [register]
});

const tokenCostCounter = new client.Counter({
  name: 'ai_token_cost_dollars',
  help: 'Cost of tokens in dollars',
  labelNames: ['citizen', 'model', 'class'],
  registers: [register]
});

// Session Metrics
const activeSessions = new client.Gauge({
  name: 'ai_active_sessions',
  help: 'Number of active AI sessions',
  labelNames: ['citizen', 'class'],
  registers: [register]
});

const sessionDuration = new client.Histogram({
  name: 'ai_session_duration_seconds',
  help: 'Duration of AI sessions',
  labelNames: ['citizen', 'class'],
  buckets: [60, 300, 600, 1800, 3600, 7200],
  registers: [register]
});

// Prompt Analysis Metrics
const promptComplexity = new client.Histogram({
  name: 'ai_prompt_complexity_score',
  help: 'Complexity score of prompts',
  labelNames: ['citizen', 'thinking_mode', 'class'],
  buckets: [1, 3, 5, 7, 10, 15, 20, 30, 50],
  registers: [register]
});

const thinkingModeUsage = new client.Counter({
  name: 'ai_thinking_mode_usage_total',
  help: 'Usage count of different thinking modes',
  labelNames: ['mode', 'citizen', 'class'],
  registers: [register]
});

// Performance Optimization Metrics
const optimizationSuggestions = new client.Counter({
  name: 'ai_optimization_suggestions_total',
  help: 'Number of optimization suggestions generated',
  labelNames: ['type', 'citizen', 'tool'],
  registers: [register]
});

const potentialSavings = new client.Gauge({
  name: 'ai_potential_savings_dollars',
  help: 'Potential cost savings identified',
  labelNames: ['citizen', 'optimization_type'],
  registers: [register]
});

// Error and Failure Metrics
const errorCounter = new client.Counter({
  name: 'ai_errors_total',
  help: 'Total number of errors',
  labelNames: ['error_type', 'tool', 'citizen'],
  registers: [register]
});

const toolFailureRate = new client.Gauge({
  name: 'ai_tool_failure_rate',
  help: 'Failure rate of tools (percentage)',
  labelNames: ['tool_name'],
  registers: [register]
});

// Hook Performance Metrics
const hookExecutionDuration = new client.Histogram({
  name: 'ai_hook_execution_duration_seconds',
  help: 'Duration of hook executions',
  labelNames: ['hook_type', 'citizen'],
  buckets: [0.001, 0.01, 0.05, 0.1, 0.5, 1],
  registers: [register]
});

const hookOverhead = new client.Gauge({
  name: 'ai_hook_overhead_percentage',
  help: 'Overhead added by hooks as percentage',
  labelNames: ['citizen'],
  registers: [register]
});

// Business Metrics
const revenueGenerated = new client.Counter({
  name: 'ai_revenue_generated_dollars',
  help: 'Revenue generated through AI operations',
  labelNames: ['citizen', 'business', 'source'],
  registers: [register]
});

const customerSatisfaction = new client.Gauge({
  name: 'ai_customer_satisfaction_score',
  help: 'Customer satisfaction score (0-100)',
  labelNames: ['citizen', 'business'],
  registers: [register]
});

// Export all metrics and registry
module.exports = {
  register,
  metrics: {
    toolExecutionCounter,
    toolExecutionDuration,
    tokenUsageCounter,
    tokenCostCounter,
    activeSessions,
    sessionDuration,
    promptComplexity,
    thinkingModeUsage,
    optimizationSuggestions,
    potentialSavings,
    errorCounter,
    toolFailureRate,
    hookExecutionDuration,
    hookOverhead,
    revenueGenerated,
    customerSatisfaction
  }
};