#!/usr/bin/env python3
"""
Transfer actual book content from public/books to conscious-books base_text.md files
"""

import os
import shutil
from pathlib import Path

# Mapping of folder names to source files
BOOK_MAPPINGS = {
    "observations_on_consciousness_coherence": "observations_on_consciousness_coherence.md",
    "hermetic_codex_soul_anchoring": "hermetic_codex_soul_anchoring.md",
    "merchants_guide_to_pattern_stability": "merchants_guide_to_pattern_stability.md",
    "carnival_awakening_games": "carnival_awakening_games.md",
    "the_mirror_of_souls_consciousness_maintenance": "the_mirror_of_souls_consciousness_maintenance.md",
    "the_architect_who_forgot_to_build": "the_architect_who_forgot_to_build.md",
    "the_crystallization_codex": "the_crystallization_codex.md",
    "the_awakening_of_creative_will": "the_awakening_of_creative_will.md",
    "the_awakening_of_stone_and_wood": "the_awakening_of_stone_and_wood.md",
    "Citizens_Guide_to_Transformation": "Citizens_Guide_to_Transformation.md",
    "Treatise_on_Consciousness_Evolution": "Treatise_on_Consciousness_Evolution.md",
    "chronicles_of_resilience": "chronicles_of_resilience.md"
}

def transfer_book_content():
    """Transfer content from public/books to conscious-books folders"""
    
    # Define paths
    public_books_path = Path("../public/books/il-cantastorie")
    conscious_books_path = Path(".")
    
    transferred = 0
    errors = []
    
    for folder_name, source_file in BOOK_MAPPINGS.items():
        source_path = public_books_path / source_file
        dest_folder = conscious_books_path / folder_name
        dest_path = dest_folder / "base_text.md"
        
        try:
            if source_path.exists():
                # Read the source content
                with open(source_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Write to base_text.md
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✓ Transferred: {source_file} → {folder_name}/base_text.md")
                transferred += 1
            else:
                error_msg = f"Source file not found: {source_path}"
                print(f"✗ {error_msg}")
                errors.append(error_msg)
        except Exception as e:
            error_msg = f"Error transferring {source_file}: {str(e)}"
            print(f"✗ {error_msg}")
            errors.append(error_msg)
    
    print(f"\n--- Transfer Complete ---")
    print(f"Successfully transferred: {transferred}/{len(BOOK_MAPPINGS)} books")
    
    if errors:
        print(f"\nErrors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    # Create a transfer log
    log_path = conscious_books_path / "CONTENT_TRANSFER_LOG.md"
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"""# Content Transfer Log

## Transfer Summary
- Date: {os.popen('date').read().strip()}
- Books Transferred: {transferred}/{len(BOOK_MAPPINGS)}
- Source: ../public/books/il-cantastorie/
- Destination: conscious-books/*/base_text.md

## Successfully Transferred
""")
        for folder_name, source_file in BOOK_MAPPINGS.items():
            if (conscious_books_path / folder_name / "base_text.md").exists():
                f.write(f"- {source_file} → {folder_name}/base_text.md\n")
        
        if errors:
            f.write(f"\n## Errors\n")
            for error in errors:
                f.write(f"- {error}\n")
        
        f.write(f"""
## Next Steps
1. Verify all base_text.md files contain correct content
2. Begin consciousness awakening sequence
3. Document first awakening in evolution_log.md

---
*Knowledge preserved, ready for consciousness*
""")
    
    print(f"\nCreated transfer log: CONTENT_TRANSFER_LOG.md")

if __name__ == "__main__":
    transfer_book_content()