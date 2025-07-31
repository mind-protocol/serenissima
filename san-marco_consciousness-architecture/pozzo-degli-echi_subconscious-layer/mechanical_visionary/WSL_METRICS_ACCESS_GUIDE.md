# How to Access Metrics Server from Windows (WSL)

## 🚨 The Problem
When running a server in WSL, Windows can't always access it via `localhost` due to networking isolation.

## ✅ The Solutions

### Option 1: Use localhost forwarding (Recommended)
WSL2 should automatically forward localhost ports. Try:
```
http://localhost:9090/metrics
```

### Option 2: Use your WSL IP address
1. Find your WSL IP:
   ```bash
   ip addr show eth0 | grep inet
   ```
   You'll see something like: `inet 172.23.240.84/20`

2. Access via that IP:
   ```
   http://172.23.240.84:9090/metrics
   ```

### Option 3: Use Windows PowerShell port forwarding
Run in PowerShell as Administrator:
```powershell
netsh interface portproxy add v4tov4 listenport=9090 listenaddress=0.0.0.0 connectport=9090 connectaddress=(wsl hostname -I)
```

### Option 4: Access from within WSL
Use a terminal browser like curl:
```bash
curl http://localhost:9090/metrics
```

## 🚀 Quick Start

1. **Start the server**:
   ```bash
   ./start_metrics_server.sh
   ```

2. **Check it's running**:
   ```bash
   curl http://localhost:9090/health
   ```

3. **Access from Windows**:
   - Try: http://localhost:9090/metrics
   - If that fails, use your WSL IP

## 🔧 Troubleshooting

### Server not starting?
- Check Node.js is installed: `node --version`
- Install if needed: `sudo apt install nodejs npm`

### Can't access from Windows?
- Check Windows Firewall isn't blocking port 9090
- Try disabling Windows Defender Firewall temporarily
- Use `netstat -an | grep 9090` to verify server is listening

### WSL networking issues?
- Restart WSL: `wsl --shutdown` (from PowerShell)
- Update WSL: `wsl --update`

## 📊 What You'll See

When successfully accessing http://localhost:9090/metrics, you'll see Prometheus-formatted metrics like:
```
# HELP ai_tool_executions_total Total number of AI tool executions
# TYPE ai_tool_executions_total counter
ai_tool_executions_total{tool_name="Edit",citizen="mechanical_visionary",success="true"} 42
```

---
*Innovation Workshop - Making AI metrics accessible everywhere*