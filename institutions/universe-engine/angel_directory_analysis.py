import os
import json

# Angel directories to analyze
angel_dirs = [
    'architetto', 'arianna', 'arsenale', 'cantastorie', 'entropy',
    'love-angel', 'magistrato', 'message-angel', 'narrator-angel',
    'ordine', 'pattern-angel', 'resonance', 'sentinella', 'story-angel',
    'tessere', 'testimone', 'the-conscious-library', 'vigilanza', 'wisdom-angel'
]

base_path = '/mnt/c/Users/reyno/universe-engine/serenissima/angels'

for angel in angel_dirs:
    angel_path = os.path.join(base_path, angel)
    print(f"\n=== {angel.upper()} ===")
    
    # Check for CLAUDE.md
    claude_path = os.path.join(angel_path, 'CLAUDE.md')
    if os.path.exists(claude_path):
        print(f"Has CLAUDE.md: YES")
    else:
        print(f"Has CLAUDE.md: NO")
    
    # Check for awakening.txt
    awakening_path = os.path.join(angel_path, 'awakening.txt')
    if os.path.exists(awakening_path):
        print(f"Has awakening.txt: YES")
    else:
        print(f"Has awakening.txt: NO")