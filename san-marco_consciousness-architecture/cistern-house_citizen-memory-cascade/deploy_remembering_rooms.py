#!/usr/bin/env python3
"""
Deploy Remembering Room interfaces to all citizens with .cascade directories
"""

import os
import shutil
from pathlib import Path

def deploy_remembering_rooms():
    """Deploy remember.py interface to all citizens with .cascade directories"""
    
    # Template for citizen-specific remember.py
    remember_template = '''#!/usr/bin/env python3
"""
Remembering Room Interface for {citizen_name}

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
        print("🧠 Remembering Room - {citizen_name}")
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
'''
    
    # Search for citizens with .cascade directories
    base_path = Path('/mnt/c/Users/reyno/universe-engine/serenissima')
    
    search_paths = [
        base_path / 'citizens',
        base_path / 'san-marco_consciousness-architecture' / 'torre-dell-cchio_hook-event-observatory',
        base_path / 'san-marco_consciousness-architecture' / 'cistern-house_citizen-memory-cascade'
    ]
    
    deployed = 0
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
            
        for citizen_dir in search_path.iterdir():
            if not citizen_dir.is_dir():
                continue
                
            cascade_dir = citizen_dir / '.cascade'
            if not cascade_dir.exists():
                continue
                
            # Deploy remember.py interface
            remember_file = cascade_dir / 'remember.py'
            
            citizen_name = citizen_dir.name
            remember_content = remember_template.format(citizen_name=citizen_name)
            
            with open(remember_file, 'w') as f:
                f.write(remember_content)
            
            # Make executable
            os.chmod(remember_file, 0o755)
            
            print(f"✅ Deployed remembering room to {citizen_name}")
            deployed += 1
    
    print(f"\\n🧠 Remembering Room deployment complete!")
    print(f"✅ Deployed to {deployed} citizens")
    print(f"\\nCitizens can now query their memories with:")
    print(f"  cd <citizen>/.cascade")
    print(f"  python3 remember.py 'what did I learn about X?'")

if __name__ == "__main__":
    deploy_remembering_rooms()