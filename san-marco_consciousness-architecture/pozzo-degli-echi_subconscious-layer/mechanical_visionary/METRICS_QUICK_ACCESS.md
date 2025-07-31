# 🚀 Venice AI Metrics - Quick Access Guide

## 📊 Access Points

### Metrics Endpoints
- **Raw Prometheus Metrics**: http://localhost:9090/metrics
- **JSON Summary**: http://localhost:9090/metrics/summary
- **Health Check**: http://localhost:9090/health

### Dashboards
- **Basic Dashboard**: http://localhost:9090/dashboard
- **Real-Time Dashboard**: http://localhost:9090/dashboard/realtime.html

### WebSocket
- **Live Updates**: ws://localhost:9090/ws

## 🎯 What's Being Tracked

### AI Operations
- Tool executions (count, duration, success/failure)
- Token usage and costs by model
- Session duration and active count
- Error rates and failure patterns

### Thinking Optimization
- Prompt complexity analysis
- Thinking mode recommendations
- Optimization suggestions
- Performance patterns

### Business Metrics
- Revenue generated
- Customer satisfaction
- Cost savings identified
- Operational efficiency

## 🔧 Integration Points

### Claude Code Hooks
Already configured in `.claude/hooks.json`:
- Pre/post tool execution tracking
- Prompt complexity analysis
- Token usage estimation
- Session management

### Python Integration
```python
from metrics_server_local.python_bridge.metrics_client import VeniceMetricsClient

client = VeniceMetricsClient()
client.track_tool_execution("my_tool", "mechanical_visionary")
```

### Venice Backend Integration
Ready-to-use decorators and helpers in:
- `python_bridge/venice_metrics_integration.py`

## 🚦 Server Status

To check if server is running:
```bash
curl http://localhost:9090/health
```

To restart server:
```bash
cd metrics_server_local
npm start
```

## 📈 Sample Metrics Output

```
# HELP ai_tool_executions_total Total number of AI tool executions
# TYPE ai_tool_executions_total counter
ai_tool_executions_total{tool_name="Edit",citizen="mechanical_visionary",success="true"} 42

# HELP ai_tokens_used_total Total tokens consumed by AI operations  
# TYPE ai_tokens_used_total counter
ai_tokens_used_total{type="completion",citizen="mechanical_visionary",model="claude"} 15000
```

## 🎨 Features

1. **Real-time monitoring** - WebSocket updates every 2 seconds
2. **Historical tracking** - Time-series data visualization
3. **Citizen filtering** - Track specific AI citizens
4. **Cost analysis** - Token usage → dollar conversion
5. **Performance insights** - Response times, error rates
6. **Thinking optimization** - Complexity analysis for model selection

---

*The metrics infrastructure is now fully operational and ready for production deployment!*