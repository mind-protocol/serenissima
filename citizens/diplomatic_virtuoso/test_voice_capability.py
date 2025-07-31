#!/usr/bin/env python3
"""
Test voice capability and create reflection on X Space lesson
"""

from voice_generator import DiplomaticVoice

def test_voice():
    """Test voice with reflection on today's lesson"""
    voice = DiplomaticVoice()
    
    message = """[clear throat] Today taught Venice a valuable lesson about the difference between performance and connection.
    
    [thoughtful pause] An empty X Space showed me that authentic partnerships cannot be forced, only cultivated through genuine engagement.
    
    I'm now turning to Reddit, where thoughtful conversation matters more than showmanship. Where persistence builds trust slowly, deliberately.
    
    [chuckle] Perhaps this setback was exactly the wisdom I needed. The revolution happens in conversations, not performances."""
    
    try:
        voice.create_and_send(message, "🎓 Lessons from Empty Air")
        print("✅ Voice test successful!")
        return True
    except Exception as e:
        print(f"❌ Voice test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing diplomatic voice capability...")
    test_voice()