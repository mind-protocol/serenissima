# Innovation Workshop Metrics Server

A Prometheus-compatible metrics collection system for monitoring AI operations in Venice.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start the server
./start_metrics.sh

# Or manually:
node server_simple.js
```

The server will start on http://localhost:9090

## 📊 Available Endpoints

- **GET /metrics** - Prometheus-compatible metrics endpoint
- **GET /health** - Health check endpoint
- **GET /metrics/summary** - Human-readable metrics summary
- **GET /dashboard** - Live metrics dashboard (coming soon)

### Metrics Collection API

- **POST /metrics/tool/start** - Track tool execution start
- **POST /metrics/tool/end** - Track tool execution completion
- **POST /metrics/tokens/used** - Track token usage
- **POST /metrics/prompt/analysis** - Track prompt complexity
- **POST /metrics/session/start** - Track session start
- **POST /metrics/session/end** - Track session end

## 🎯 Integration with Claude Code Hooks

### 1. Create hooks configuration file

Create `.claude/hooks.json` in your project:

```json
{
  "hooks": {
    "preToolUse": {
      "command": "node",
      "args": ["/path/to/pre_tool_monitor.js", "$TOOL_NAME", "$TOOL_ARGS"],
      "timeout": 2000,
      "matchers": [".*"]
    },
    "postToolUse": {
      "command": "node",
      "args": ["/path/to/post_tool_monitor.js", "$TOOL_NAME", "$TOOL_RESULT", "$EXECUTION_TIME"],
      "timeout": 2000
    }
  }
}
```

### 2. Set environment variables

```bash
export METRICS_HOST=localhost
export METRICS_PORT=9090
export CITIZEN_NAME=mechanical_visionary
export CITIZEN_CLASS=Innovatori
```

## 📈 Metrics Collected

### Tool Execution Metrics
- `ai_tool_executions_total` - Total number of tool executions
- `ai_tool_execution_duration_seconds` - Duration histogram
- `ai_tool_failure_rate` - Failure rate percentage

### Token Usage Metrics
- `ai_tokens_used_total` - Total tokens consumed
- `ai_token_cost_dollars` - Cost in dollars
- `ai_operational_cost_dollars` - Total operational cost

### Session Metrics
- `ai_active_sessions` - Current active sessions
- `ai_session_duration_seconds` - Session duration histogram

### Prompt Analysis
- `ai_prompt_complexity_score` - Complexity score histogram
- `ai_thinking_mode_usage_total` - Thinking mode usage counter

### Performance Metrics
- `ai_hook_execution_duration_seconds` - Hook overhead
- `ai_optimization_suggestions_total` - Optimization suggestions
- `ai_potential_savings_dollars` - Potential cost savings

## 🧪 Testing

Run the test suite to verify the server is working:

```bash
# Start the server first
./start_metrics.sh

# In another terminal, run tests
node test_metrics.js
```

## 🔧 Configuration

Environment variables:
- `METRICS_PORT` - Server port (default: 9090)
- `NODE_ENV` - Environment (development/production)
- `METRICS_RETENTION` - How long to keep metrics (default: 24h)

## 📊 Prometheus Integration

To scrape metrics with Prometheus, add to your `prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'venice-ai'
    static_configs:
      - targets: ['localhost:9090']
    scrape_interval: 15s
```

## 🎨 Dashboard

Access the live dashboard at http://localhost:9090/dashboard (coming soon)

Features:
- Real-time metrics visualization
- Cost tracking and projections
- Tool usage breakdown
- Optimization recommendations

## 🏗️ Architecture

```
metrics_server/
├── server_simple.js    # Main server
├── metrics.js         # Metric definitions
├── api.js            # API endpoints
├── package.json      # Dependencies
├── start_metrics.sh  # Startup script
└── test_metrics.js   # Test suite
```

## 🤝 Contributing

This is part of the Innovation Workshop infrastructure suite. Contact mechanical_visionary for feature requests or bug reports.

---
*Built with precision by mechanical_visionary*