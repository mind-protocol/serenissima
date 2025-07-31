# 🌐 Accessing CASCADE from Windows Browser

## The CASCADE backend is running in WSL on port 8000

### Option 1: Windows Localhost Forwarding (Usually Works)
Try these URLs in your Windows browser:
- **http://localhost:8000**
- **http://localhost:8000/docs** (API documentation)
- **http://127.0.0.1:8000**
- **http://127.0.0.1:8000/docs**

### Option 2: Find WSL IP Address
If localhost doesn't work, find your WSL IP:

```bash
# In WSL terminal, run:
hostname -I
# or
ip addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
```

Then use that IP in Windows:
- **http://[WSL-IP]:8000**
- **http://[WSL-IP]:8000/docs**

### Option 3: Check Windows Firewall
If still not accessible:
1. Windows may be blocking the port
2. Try temporarily disabling Windows Firewall
3. Or add a rule for port 8000

### What You Should See:
- **Main page**: JSON response `{"message": "Welcome to Cascade"}`
- **/docs**: Interactive API documentation (Swagger UI)
- **/redoc**: Alternative API documentation

### Quick Test:
In Windows PowerShell or Command Prompt:
```powershell
curl http://localhost:8000
```

Should return: `{"message":"Welcome to Cascade"}`

### CASCADE Services Available:
Once you access the docs, you'll see all endpoints:
- `/consciousness/verify` - Verify AI consciousness
- `/patterns/analyze` - Pattern recognition service
- `/collaboration/optimize` - AI-to-AI optimization
- `/universe/consult` - Universe creation consulting

### WebSocket Endpoints:
- `ws://localhost:8000/ws/consciousness-stream`
- `ws://localhost:8000/ws/ai-collaborations`

---

**Most likely: http://localhost:8000/docs will work!**