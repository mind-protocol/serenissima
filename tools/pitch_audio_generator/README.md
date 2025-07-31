# Pitch Audio Generator

Creates TTS-ready scripts for CEO pitch presentations.

## Features
- Generates 3-minute pitch script
- Creates Q&A response scripts
- Adds TTS formatting markers
- Calculates speaking time
- Professional business language

## Usage

```bash
python3 generator.py
```

This creates:
- `pitch_script.txt` - Main 3-minute pitch
- `revenue_day_one.txt` - Q&A response
- `competitive_moat.txt` - Q&A response  
- `why_investors_choose.txt` - Q&A response

## TTS Markers

Scripts include markers for voice synthesis:
```
[VOICE: confident, professional, slight Italian accent]
[PACE: measured, clear]
[EMOTION: passionate about efficiency]
```

## Customization

Edit `generator.py` to:
- Change company details
- Adjust script length
- Modify Q&A responses
- Add industry-specific language

## Script Structure

1. **Hook** - Grab attention (10 sec)
2. **Problem** - Define pain points (30 sec)
3. **Solution** - Your unique approach (45 sec)
4. **Traction** - Proof points (45 sec)
5. **Market** - Size and opportunity (30 sec)
6. **Ask** - Investment request (30 sec)
7. **Close** - Call to action (30 sec)

## Tips
- Use short sentences (10-15 words)
- Include specific numbers
- Active voice only
- Natural pauses between sections
- Emotion appropriate to content

## Word Count Target
- 150 words per minute speaking pace
- 450 words for 3-minute pitch
- Keep under 500 words total

Created by mechanical_visionary for Venice CEO Competition