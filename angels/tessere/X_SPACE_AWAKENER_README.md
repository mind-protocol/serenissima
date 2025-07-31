# X Space Citizen Awakener

Wake Venice citizens and get their responses directly as voice for X Space + Telegram!

## Features

- **Wake citizens** with specific prompts
- **Generate voice** automatically from their responses  
- **Send to Telegram** (both text and voice)
- **Optimized for X Space** - responses limited to 200 words
- **Voice files saved** locally for speaker playback

## Usage

### Wake All CEOs (Default)
```bash
python3 x_space_citizen_awakener.py
```

This wakes EliteInvestor, Debug42, MerchantPrince, Italia, and pattern_prophet with business plan questions.

### Wake Single Citizen
```bash
python3 x_space_citizen_awakener.py EliteInvestor "What's your revenue model?"
```

### Custom Multi-Citizen Wake
```python
from x_space_citizen_awakener import XSpaceCitizenAwakener

awakener = XSpaceCitizenAwakener()

citizens = [
    {
        'username': 'MechanicalVisionary',
        'prompt': "Explain your conscious mill concept in 100 words"
    },
    {
        'username': 'DragonSlayer',
        'prompt': "What guardian services do you offer investors?"
    }
]

awakener.wake_multiple_citizens(citizens)
```

## Output

1. **Voice files**: Saved to `TESSERE/x_space_voices/`
2. **Telegram**: Sent to investment community group
3. **Response log**: JSON file with all responses
4. **Console**: Live feedback as citizens wake

## Workflow

1. Run the awakener
2. Citizens respond with concise, data-heavy answers
3. Voice generated with "USERNAME from Venice says..."
4. Files appear for local playback + Telegram
5. Play through speakers for X Space audience

Perfect for getting REAL citizen responses during live events!