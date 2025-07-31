#!/usr/bin/env python3
"""
Voice Input Server for Live X Space
Receives transcribed speech and routes to Narrator Angel
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess
import time
from pathlib import Path
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow browser to connect

# Paths
NARRATOR_PATH = Path("/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/narrator_angel")
OUTPUT_PATH = Path(__file__).parent / "x_space_live"
OUTPUT_PATH.mkdir(exist_ok=True)

# Response cache for common questions
response_cache = {}

@app.route('/')
def index():
    """Serve the voice input interface"""
    return send_file('voice_input.html')

@app.route('/api/narrator-input', methods=['POST'])
def process_voice_input():
    """Process voice input and get Narrator Angel response"""
    start_time = time.time()
    
    data = request.json
    user_text = data.get('text', '')
    
    if not user_text:
        return jsonify({'error': 'No text provided'}), 400
    
    print(f"\n{'='*60}")
    print(f"📢 VOICE INPUT: {user_text}")
    print(f"{'='*60}")
    
    # Check cache
    if user_text in response_cache:
        response = response_cache[user_text]
        print("✓ Cache hit!")
    else:
        # Call Narrator Angel for response
        response = get_narrator_response(user_text)
        response_cache[user_text] = response
    
    # Format for easy reading
    formatted_response = format_for_reading(response)
    
    # Save to file
    timestamp = datetime.now().strftime("%H%M%S")
    output_file = OUTPUT_PATH / f"response_{timestamp}.txt"
    output_file.write_text(formatted_response)
    
    elapsed = time.time() - start_time
    
    return jsonify({
        'response': formatted_response,
        'elapsed': f"{elapsed:.1f}s",
        'cached': user_text in response_cache
    })

def get_narrator_response(user_text):
    """Get response from Narrator Angel"""
    
    # Prepare the prompt for Narrator Angel
    prompt = f"""LIVE X SPACE QUESTION:
"{user_text}"

Generate a SHORT response (under 30 seconds when spoken) that:
1. Directly answers the question
2. Focuses on profitability/ROI if relevant
3. Includes specific examples from Venice
4. Ends with a hook or call to action

Keep it conversational and energetic!"""
    
    try:
        # Call Narrator Angel
        cmd = [
            'timeout', '10',
            'claude', prompt,
            '--model', 'sonnet',
            '--dir', str(NARRATOR_PATH)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Venice is processing... (Error: {result.returncode})"
            
    except Exception as e:
        return f"Venice is experiencing technical difficulties: {str(e)}"

def format_for_reading(text):
    """Format text for easy reading aloud"""
    # Break into readable chunks
    sentences = text.split('. ')
    formatted_lines = []
    
    for sentence in sentences:
        # Add back the period
        if not sentence.endswith('.'):
            sentence += '.'
        
        # Break long sentences
        if len(sentence) > 100:
            words = sentence.split()
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 80:
                    formatted_lines.append(' '.join(current_line))
                    current_line = []
            if current_line:
                formatted_lines.append(' '.join(current_line))
        else:
            formatted_lines.append(sentence)
    
    return '\n\n'.join(formatted_lines)

@app.route('/api/cache-status')
def cache_status():
    """Show cache statistics"""
    return jsonify({
        'cache_size': len(response_cache),
        'cached_questions': list(response_cache.keys())
    })

if __name__ == '__main__':
    print("🎙️ Venice Voice Input Server")
    print("=" * 60)
    print("1. Open http://localhost:5555 in Chrome")
    print("2. Click 'Start Listening' and speak")
    print("3. Your words → Venice → Formatted response")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5555, debug=True)