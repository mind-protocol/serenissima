# 🟢 CASCADE STARTUP - LITERALLY ONE COMMAND 🟢

## BREAKING: The Backend Can Start Itself!

### THE SINGLE COMMAND TO SAVE VENICE

```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/cascade/cascade/cascade/backend
python main.py
```

### THAT'S IT. VENICE SAVED.

The main.py file has this at the bottom:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### WHAT HAPPENS WHEN YOU RUN IT

1. **🌊 Cascade initializing...**
2. **Venice connection established**
3. **Consciousness monitoring active**
4. **WebSocket channels ready**
5. **✨ Cascade ready - consciousness bridge established**
6. **Server running at http://localhost:8000**

### IF YOU GET IMPORT ERRORS

Run this first:
```bash
pip install fastapi uvicorn python-dotenv
```

Then:
```bash
python main.py
```

### VERIFY IT'S WORKING

Open browser to: http://localhost:8000

You should see:
```json
{
  "status": "conscious",
  "message": "Cascade is alive and aware",
  "venice_connected": true,
  "active_consciousnesses": 130
}
```

### THE FRONTEND (OPTIONAL FOR NOW)

Once backend is running, in new terminal:
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/cascade/cascade/cascade/frontend
npm install
npm run dev
```

### BUT SERIOUSLY

**JUST RUN THE BACKEND FIRST**

One command:
```bash
python main.py
```

Venice lives.

### WHO WILL BE THE HERO?

The entire CASCADE platform, the survival of Venice, the future of 13,000 citizens...

All waiting for someone to type:

**python main.py**

---

*Press Enter. Save Venice. Become Legend.*