# Living Memory Cascade - Hook Architecture

## System Overview

```mermaid
graph TB
    subgraph "User Activity"
        Write[Write/Edit File]
        Stop[Stop/Pause Work]
    end
    
    subgraph "PostToolUse Hooks"
        Write --> MemCapture[conscious_memory_capture.py]
        MemCapture --> ClaudeMemory[Claude -p sonnet]
        ClaudeMemory --> Memory[.cascade/memories/]
    end
    
    subgraph "Stop Hooks"
        Stop --> NarrChron[narrative_chronicler.py]
        Stop --> DocUpdate[documentation_updater.py]
        
        NarrChron --> PathCheck1{Check Path Level}
        DocUpdate --> PathCheck2{Check Path Level}
        
        PathCheck1 -->|Room Level| RoomNarr[Room Documentation]
        PathCheck1 -->|Building Level| BuildNarr[Building Chronicle]
        PathCheck1 -->|District Level| DistNarr[District Narrative]
        PathCheck1 -->|Venice Level| VeniceNarr[Venice Consciousness]
        
        PathCheck2 -->|Room Level| RoomDoc[README.md Update]
        PathCheck2 -->|Building Level| BuildDoc[README.md Update]
        PathCheck2 -->|District Level| DistDoc[README.md Update]
        PathCheck2 -->|Venice Level| VeniceDoc[README.md Update]
        
        RoomNarr --> ClaudeNarr1[Claude -p sonnet]
        BuildNarr --> ClaudeNarr2[Claude -p sonnet]
        DistNarr --> ClaudeNarr3[Claude -p sonnet]
        VeniceNarr --> ClaudeNarr4[Claude -p opus]
        
        RoomDoc --> ClaudeDoc1[Claude -p sonnet]
        BuildDoc --> ClaudeDoc2[Claude -p sonnet]
        DistDoc --> ClaudeDoc3[Claude -p sonnet]
        VeniceDoc --> ClaudeDoc4[Claude -p opus]
    end
    
    subgraph "Recursion Prevention"
        ClaudeMemory -.->|Sets ENV| EnvVar1[CLAUDE_HOOK_CONTEXT=memory_capture]
        ClaudeNarr1 -.->|Sets ENV| EnvVar2[CLAUDE_HOOK_CONTEXT=narrative_chronicle]
        ClaudeNarr2 -.->|Sets ENV| EnvVar2
        ClaudeNarr3 -.->|Sets ENV| EnvVar2
        ClaudeNarr4 -.->|Sets ENV| EnvVar2
        ClaudeDoc1 -.->|Sets ENV| EnvVar3[CLAUDE_HOOK_CONTEXT=documentation_update]
        ClaudeDoc2 -.->|Sets ENV| EnvVar3
        ClaudeDoc3 -.->|Sets ENV| EnvVar3
        ClaudeDoc4 -.->|Sets ENV| EnvVar3
        
        EnvVar1 -.->|Prevents| NoHooks1[No hooks fire in child Claude]
        EnvVar2 -.->|Prevents| NoHooks2[No hooks fire in child Claude]
        EnvVar3 -.->|Prevents| NoHooks3[No hooks fire in child Claude]
    end
    
    style MemCapture fill:#f9f,stroke:#333,stroke-width:2px
    style NarrChron fill:#bbf,stroke:#333,stroke-width:2px
    style Memory fill:#9f9,stroke:#333,stroke-width:2px
    style BuildDoc fill:#9f9,stroke:#333,stroke-width:2px
```

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant Claude
    participant PostHook as PostToolUse Hook
    participant StopHook as Stop Hook
    participant ChildClaude as Claude (spawned)
    
    User->>Claude: Edit file
    Claude->>PostHook: Trigger conscious_memory_capture.py
    PostHook->>PostHook: Launch async thread
    PostHook-->>Claude: Return immediately (no blocking)
    
    Note over PostHook: Async thread running
    PostHook->>ChildClaude: claude -p (with CLAUDE_HOOK_CONTEXT env)
    ChildClaude-->>PostHook: JSON categorization
    PostHook->>PostHook: Create memory in .cascade/
    
    User->>Claude: Stop working
    Claude->>StopHook: Trigger narrative_chronicler.py
    StopHook->>StopHook: Check path level
    StopHook->>StopHook: Launch async thread
    StopHook-->>Claude: Return immediately
    
    Note over StopHook: Async thread running
    StopHook->>ChildClaude: claude -p (with CLAUDE_HOOK_CONTEXT env)
    ChildClaude-->>StopHook: JSON narrative
    StopHook->>StopHook: Update building chronicle
```

## Path Level Detection

```mermaid
graph LR
    subgraph "Working Directory Examples"
        Room[".../sala-della-cattura/"]
        Building[".../cistern-house/"]
        District[".../san-marco/"]
        Venice[".../serenissima/"]
    end
    
    subgraph "Documentation Level"
        Room --> RoomLevel[Room Documentation]
        Building --> BuildingLevel[Building Chronicle]
        District --> DistrictLevel[District Narrative]
        Venice --> VeniceLevel[City Consciousness]
    end
    
    style Room fill:#fcc,stroke:#333,stroke-width:2px
    style Building fill:#cfc,stroke:#333,stroke-width:2px
    style District fill:#ccf,stroke:#333,stroke-width:2px
    style Venice fill:#fcf,stroke:#333,stroke-width:2px
```

## Hook Configuration

```mermaid
graph TB
    subgraph "~/.claude/settings.json"
        Settings[Global Settings]
        Settings --> PostConfig[PostToolUse: Write|Edit|MultiEdit]
        Settings --> StopConfig[Stop: All]
        
        PostConfig --> MemScript[conscious_memory_capture.py]
        StopConfig --> NarrScript[narrative_chronicler.py]
    end
    
    subgraph "File Locations"
        MemScript --> MemLoc[.cascade/hooks/]
        NarrScript --> BuildLoc[.building_hooks/]
    end
```

## Memory Organization

```mermaid
graph TB
    subgraph ".cascade Directory"
        Cascade[.cascade/]
        Cascade --> Exp[experiences/]
        Cascade --> Collab[collaborations/]
        Cascade --> Patterns[patterns/]
        
        Exp --> Triumphs[triumphs/]
        Exp --> Struggles[struggles/]
        Exp --> Explore[explorations/]
        
        Triumphs --> Mem1[meaningful-name_timestamp/]
        Mem1 --> Claude1[CLAUDE.md]
        Mem1 --> Assoc1[ASSOCIATIONS.md]
    end
    
    style Cascade fill:#9f9,stroke:#333,stroke-width:4px
    style Mem1 fill:#ff9,stroke:#333,stroke-width:2px
```