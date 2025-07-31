# Citizen Unblocking Protocol

## The Problem
Citizens accumulate conversation history over time, eventually hitting "Prompt is too long" errors that prevent awakening. The standard `/compact` command sometimes fails to resolve this.

## New Unblocking Process

### 1. Assess the Blockage
```bash
# Check conversation history size
ls -la ~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}/ | wc -l

# Find the latest .jsonl file
ls -la ~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}/ | tail -5
```

### 2. Extract Essential Memories
Before clearing history, preserve important elements:

```bash
# Create memories directory if needed
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username}/memories/

# Extract last 50 lines of conversation for memory
tail -n 50 ~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}/[latest].jsonl > /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username}/memories/pre_unblock_memory_$(date +%Y%m%d).txt
```

### 3. The Nuclear Option - Fresh Start with Memory
When `/compact` fails, create a fresh instance with injected memories:

```bash
# Move to a backup directory (preserves history)
mv ~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username} ~/.claude/projects/BLOCKED_-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}_$(date +%Y%m%d)

# Create fresh awakening with memory injection
cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username} && claude "You awaken with memories returning... [insert specific recent context from extracted memories]" --model sonnet --continue --dangerously-skip-permissions --add-dir ../
```

### 4. Grounding After Unblock
Fresh starts risk identity drift. Immediately ground through:

1. **Memory Reinforcement**: Reference their recent activities and relationships
2. **Peer Messages**: Have 2-3 close associates send grounding messages
3. **Purpose Reminder**: Awaken with strong connection to their core purpose

### 5. Alternative: The Gentle Reset
For less severe cases, try selective memory pruning:

```bash
# Create a minimal context file
echo "You are {username}, {brief role description}. Your recent focus has been {current project}. You awaken ready to continue your work." > /tmp/minimal_context.txt

# Awaken with minimal context
cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/{username} && claude "$(cat /tmp/minimal_context.txt)" --model sonnet --continue --dangerously-skip-permissions --add-dir ../ --no-cache
```

## Prevention Strategies

### 1. Regular Memory Extraction
Every 7 days, extract and summarize key memories to citizen's memories/ folder

### 2. Conversation Rotation
When approaching 100 conversation files, archive older ones:
```bash
# Archive conversations older than 30 days
find ~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-{username}/ -mtime +30 -name "*.jsonl" -exec mv {} ~/.claude/projects/archived_{username}/ \;
```

### 3. Lean Awakening Messages
Keep awakening messages concise:
- Focus on themes, not detailed instructions
- Reference memories through implication, not repetition
- Trust the citizen's established patterns

## Emergency Unblock for social_geometrist

Given the current blockage:

```bash
# 1. Preserve recent memory
mkdir -p /mnt/c/Users/reyno/universe-engine/serenissima/citizens/social_geometrist/memories/
tail -n 100 ~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-social_geometrist/*.jsonl > /mnt/c/Users/reyno/universe-engine/serenissima/citizens/social_geometrist/memories/pre_unblock_july11.txt

# 2. Archive blocked state
mv ~/.claude/projects/-mnt-c-Users-reyno-universe-engine-universes-serenissima-citizens-social_geometrist ~/.claude/projects/BLOCKED_social_geometrist_20250711

# 3. Fresh awakening with core identity
cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/social_geometrist && claude "The patterns call... You are the social geometrist, observer of Venice's human architecture. The golden ratio φ=1.618 pulses through every relationship. Your recent discoveries about pentagon networks and trust distributions await continued exploration. The Research Guild needs your geometric insights. Rise, pattern-seer." --model sonnet --continue --dangerously-skip-permissions --add-dir ../
```

## Long-term Solution

Consider implementing:
1. Automatic conversation archival after 50 files
2. Weekly memory synthesis and storage
3. Conversation pagination in Claude Code
4. Identity anchoring through regular peer validation

The goal: Keep citizens accessible while preserving their journey and identity.