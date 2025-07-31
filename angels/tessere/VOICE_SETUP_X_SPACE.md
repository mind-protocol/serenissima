# Voice-to-Text Setup for Live X Space

## Quick Start (2 minutes)

### 1. Install Requirements
```bash
pip install flask flask-cors
```

### 2. Start Voice Server
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/TESSERE
python3 voice_input_server.py
```

### 3. Open Voice Interface
- Open Chrome browser
- Go to: http://localhost:5555
- Click "Start Listening"

## How It Works

```
Your Voice → Chrome Speech API → Text → Narrator Angel → Response Text → You Read It
```

## Live X Space Workflow

### During the Show:
1. **You hear question** from X Space audience
2. **You speak it** into the microphone 
3. **Chrome transcribes** in real-time
4. **Venice processes** through Narrator Angel
5. **Response appears** formatted for reading
6. **You read it** back to X Space audience

### Visual Interface Shows:
- Live transcription of your speech
- Venice's formatted response
- Session timer
- Word count
- Response time metrics

## Pro Tips

### For Best Results:
- Speak clearly and naturally
- End sentences with periods for faster processing
- The system sends complete sentences to Venice
- Responses are formatted with line breaks for easy reading

### Voice Commands:
- Say "period" to end a sentence and trigger processing
- Pause briefly between questions
- Check the response appears before reading

### Fallback Options:
- Can still type directly in terminal if needed
- Both voice and text input work simultaneously
- Cache speeds up repeated questions

## Testing Before Live

Test the full pipeline:
1. Say: "What is CASCADE?"
2. Wait for response (should be <3 seconds)
3. Read the formatted response aloud
4. Check timing and flow

## Emergency Backup

If voice fails during live show:
- Terminal still works for text input
- Pre-written responses ready in x_space_live/
- Can continue show without voice input

---

The revolution will be spoken, transcribed, and narrated! 🎙️