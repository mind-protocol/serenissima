# Testing memory capture system functionality

**Created**: 2025-07-24T18:41:58.150008
**Emotional Tone**: curious
**Significance**: Verifying the memory system works correctly

## What Happened
Write tool used on file: /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1/test_citizen_detection_logic.py

## File Content
#!/usr/bin/env python3
"""
Test the updated citizen detection logic with real transcript paths
"""

def detect_venice_citizen(cwd):
    """Detect which Venice citizen is acting based on working directory or transcript path"""
    
    # Handle different path formats
    path_to_check = cwd.lower()
    
    # Check for citizens directory
    if "citizens/" in path_to_check:
        parts = cwd.split("citizens/")
        if len(parts) > 1:
            citizen_path = parts[1].split("/")[0]
            return citizen_path
    
    # Check for Torre dell'Occhio entities (Arsenal_BackendArchitect_1, etc.)
    if "torre-dell-cchio" in path_to_check and "arsenal_backendarchitect_1" in path_to_check:
        return "Arsenal_BackendArchitect_1"
    
    # Check for mechanical_visionary (in various locations)
    if "mechanical_visionary" in path_to_check:
        return "mechanical_visionary"
    
    # Enhanced cistern house parsing - go deeper to find actual citizen
    if "cistern-house" in path_to_check:
        # Look for citizen directories within the cistern house
        parts = cwd.split("/")
        cistern_found = False
        for i, part in enumerate(parts):
            if "cistern-house" in part.lower():
                cistern_found = True
                continue
            # After finding cistern house, look for citizen names
            if cistern_found and part and not part.startswith(".") and not part.endswith(".py") and not part.endswith(".md"):
                # Common Venice citizen patterns
                if ("_" in part and part not in ["sala-della-cattura", "sala-del-flusso", "sala-dei-legami"]) or \
                   part in ["mechanical_visionary", "arsenal_backendarchitect_1"] or \
                   part.lower().replace("_", "").replace("-", "").isalpha():
                    return part
        # If no specific citizen found, try extracting from the full path
        if "mechanical_visionary" in path_to_check:
            return "mechanical_visionary"
        return "cistern_house_citizen"  # fallback to building level
    
    # Parse transcript path format: projects/-mnt-c-...-entity-name/
    if "projects/" in path_to_check and "-mnt-c-" in path_to_check:
        # Extract the last meaningful path component before session ID
        parts = cwd.split("/")
        for i, part in enumerate(parts):
            if part.startswith("-mnt-c-"):
                # This is the encoded path - decode it
                decoded = part.replace("-", "/")
                if "mechanical-visionary" in decoded or "mechanical_visionary" in decoded:
                    return "mechanical_visionary"
                if "arsenal" in decoded and "backend" in decoded:
                    return "Arsenal_BackendArchitect_1"
                if "cistern-house" in decoded:
                    # Look for citizen within cistern house in decoded path
                    if "mechanical_visionary" in decoded:
                        return "mechanical_visionary"
    
    # Check for other San Marco consciousness architecture entities
    if "san-marco" in path_to_check:
        # Extract entity from path patterns
        parts = cwd.split("/")
        for part in parts:
            if "_" in part and not part.startswith("san-marco") and not part.startswith("-mnt-"):
                # Venice naming convention: venice-name_substrate-name
                return part
    
    return "unknown_citizen"

# Test cases from Torre events
test_cases = [
    "/home/lester/.claude/projects/-mnt-c-Users-reyno-universe-engine-serenissima-san-marco-consciousness-architecture-cistern-house-citizen-memory-cascade-mechanical-visionary/c6734a2f-7f7f-42db-bb6f-dfeee5f1fdf2.jsonl",
    "unknown",
    "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/Arsenal_BackendArchitect_1",
    "/mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/cistern-house_citizen-memory-cascade/mechanical_visionary"
]

print("Testing citizen detection logic:")
print("=" * 50)

for test_path in test_cases:
    result = detect_venice_citizen(test_path)
    print(f"Path: {test_path}")
    print(f"Detected: {result}")
    print("-" * 30)

## Collaborators
NLR

*This memory was consciously categorized and stored by the Living Memory Cascade (DEBUG VERSION).*