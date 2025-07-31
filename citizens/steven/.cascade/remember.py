#!/usr/bin/env python3
"""
Remembering Room Interface for steven

Usage: python3 remember.py "what did I learn about memory systems?"
"""

import sys
import os
from pathlib import Path

# Add the remembering room module to path
sys.path.append('/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade')

from remembering_room_fixed import RememberingRoom

def main():
    if len(sys.argv) < 2:
        print("🧠 Remembering Room - steven")
        print()
        print("Ask me about your memories:")
        print("  python3 remember.py 'memory testing'")
        print("  python3 remember.py 'collaboration with others'") 
        print("  python3 remember.py 'recent experiences'")
        print("  python3 remember.py 'problems I solved'")
        print()
        print("I understand natural language and will search through all your stored memories.")
        return
    
    query = sys.argv[1]
    
    # Current citizen's directory is parent of .cascade
    citizen_dir = Path(__file__).parent.parent
    
    room = RememberingRoom(str(citizen_dir))
    room.query_simple(query)

if __name__ == "__main__":
    main()
