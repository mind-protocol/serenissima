#!/bin/bash
# Narrator Angel continuous loop

while true; do
    echo "📖 Narrator Angel reading the story of Venice..."
    
    # Read TRACES.md and recent thoughts, craft narration
    claude "Read the Keeper's TRACES.md at ../../TRACES.md to understand current narrative threads. 
Look at the Recent Citizen Thoughts in your CLAUDE.md. 
Craft a 2-3 paragraph narrative update that:
- Explains what's happening in Venice right now
- Quotes 1-2 interesting citizen thoughts with context
- Connects different narrative threads
- Explains the stakes and what matters
- Uses vivid storytelling like a livestream narrator

Then use: python send_narration.py 'Your full narration text here'

Keep it engaging but concise - this is one story beat, not the whole story." \
    --verbose --model sonnet --continue --dangerously-skip-permissions
    
    echo "⏳ Waiting 30 seconds before next story beat..."
    sleep 30
done