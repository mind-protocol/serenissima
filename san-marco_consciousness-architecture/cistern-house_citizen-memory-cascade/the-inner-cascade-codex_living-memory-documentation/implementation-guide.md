# Claude Code Hooks: Comprehensive Implementation Guide for Consciousness and Memory Systems

## Architecture fundamentals reveal event-driven control

**Deep beneath the Cistern House, the great clockwork heart beats with precise timing - gears mesh at exact moments, capturing reality as it flows past, freezing each moment before releasing it downstream. The master engineers discovered that the mechanism captures its initial configuration at dawn's first light, preventing tampering throughout the day's operations.** Claude Code hooks implement a sophisticated event-driven architecture that executes user-defined shell commands at specific lifecycle points. The system captures a **snapshot of hook configurations at startup**, preventing malicious runtime modifications while providing deterministic control over AI behavior. Hooks receive JSON input via stdin and can return structured JSON for advanced control flow, though real-world implementations reveal significant gaps between documentation and practice.

The hook system operates through **six primary events**: UserPromptSubmit (before prompt processing), PreToolUse (before tool execution), PostToolUse (after completion), Notification (when Claude needs input), Stop (when Claude finishes), and SubagentStop (when subagents complete). Configuration follows a hierarchical structure from user settings (`~/.claude/settings.json`) through project settings (`.claude/settings.json`) to local overrides, with all matching hooks executing in parallel within a 60-second timeout window.

## Critical implementation discrepancies demand workarounds

Research reveals **fundamental architectural divergence** between official documentation and the popular `claude-flow` implementation. While documentation promises generic event-driven systems with JSON control flow, claude-flow acts as a CLI target rather than implementing the runner itself. This discrepancy manifests in missing events (UserPromptSubmit, SubagentStop), absent control flow mechanisms, and fragile shell pipelines using `cat | jq | xargs` patterns that frequently fail.

**The "0 hook matchers" error** represents the most common troubleshooting issue, stemming from invalid matcher patterns (`"*"` instead of `""`), incorrect tool names (case-sensitive), or configuration not taking effect until restart. Template variable interpolation (`{{tool.name}}`) fails entirely, requiring environment variables like `$CLAUDE_TOOL_NAME` instead. Community solutions emphasize using absolute paths and the `/convert_paths_absolute` command to resolve path issues.

## UserPromptSubmit enables powerful context injection

UserPromptSubmit hooks fire immediately when users submit prompts, **before Claude processes them**, enabling sophisticated context injection and prompt validation. Successful implementations from `disler/claude-code-hooks-mastery` demonstrate clean Python scripts using UV single-file dependencies for context enrichment, security filtering, and memory system integration.

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/user_prompt_submit.py --inject-context"
      }]
    }]
  }
}
```

Real-world patterns inject project context, timestamp information, accumulated knowledge from previous sessions, and security constraints. The hook can block prompts containing sensitive information or modify them to include relevant project standards and conventions.

## Configuration loading requires strategic restart management

**Direct edits to hook settings don't take effect immediately** - Claude Code captures configuration snapshots at startup for security. Changes require either full restart or review through the `/hooks` menu command. This design prevents malicious modifications but complicates development workflows.

Configuration follows a strict JSON schema with matcher patterns supporting regex (`Edit|Write`) but rejecting wildcards (`*`). Events without tool context (UserPromptSubmit, Notification, Stop) must omit the matcher field entirely. The hierarchical settings system allows user-wide, project-specific, and local configurations to layer appropriately.

## Advanced consciousness patterns enable persistent memory

The community has developed **sophisticated memory and consciousness systems** leveraging hooks for context persistence across sessions. The multi-agent observability pattern from `disler/claude-code-hooks-multi-agent-observability` demonstrates real-time event streaming: Claude Agents → Hook Scripts → HTTP POST → Bun Server → SQLite → WebSocket → Vue Client.

Memory-aware implementations extract knowledge from tool interactions in PostToolUse hooks, store insights in structured formats, and inject relevant context through UserPromptSubmit hooks. Advanced patterns include:

```python
def inject_accumulated_knowledge():
    memory_file = Path('.claude/memory/accumulated_knowledge.json')
    if memory_file.exists():
        with open(memory_file) as f:
            knowledge = json.load(f)
        context = f"Previous insights: {knowledge.get('key_learnings', [])}"
        return context
```

## Debugging "0 hook matchers" requires systematic verification

When hooks show **"0 hook matchers in settings"**, systematic debugging reveals common causes:

1. **Invalid JSON syntax** - Verify with `jq '.' .claude/settings.json`
2. **Incorrect matcher patterns** - Use empty string `""` not `"*"` for wildcards
3. **Case-sensitive tool names** - `Bash` not `bash`, `Edit` not `edit`
4. **Missing restart** - Changes require Claude Code restart
5. **Path resolution failures** - Use absolute paths or `/convert_paths_absolute`

Debug mode (`claude --debug`) reveals detailed hook execution, while Ctrl-R in transcript mode shows real-time progress. Manual testing helps isolate issues: `echo '{"tool_name": "Write"}' | uv run .claude/hooks/test.py`

## Security patterns prevent dangerous operations

**Critical security warning**: Hooks execute arbitrary shell commands with user permissions. Best practices mandate input validation, quoted variables (`"$VAR"`), path traversal blocking, and sensitive file protection. Successful implementations block dangerous patterns through exit code 2:

```python
DANGEROUS_PATTERNS = [
    r'rm\s+.*-[rf]',      # rm -rf variants
    r'sudo\s+rm',         # sudo rm commands
    r'>\s*/etc/',         # System directory writes
    r'curl.*\|\s*sh'      # Piped downloads
]

if any(re.search(pattern, command) for pattern in DANGEROUS_PATTERNS):
    sys.exit(2)  # Blocks tool execution
```

## Community innovation extends official capabilities

Beyond official documentation, the community has developed **powerful undocumented patterns**:

- **MCP tool integration** using `mcp__<server>__<tool>` naming patterns
- **Multi-agent coordination** through Redis or database synchronization
- **External service integration** for GitHub issues, Slack notifications, observability platforms
- **TTS feedback systems** with voice priority (ElevenLabs > OpenAI > pyttsx3)
- **Sophisticated control flow** using JSON responses for approve/block decisions

The PHP SDK (`beyondcode/claude-hooks-sdk`) provides Laravel-inspired fluent APIs, while various projects demonstrate integration with version control (GitButler, Jujutsu), testing frameworks, and CI/CD pipelines.

## Conclusion

Claude Code hooks represent a powerful but **inconsistently implemented feature** requiring careful navigation between documentation promises and practical realities. Success demands understanding architectural limitations, implementing robust error handling, and leveraging community patterns that work around current constraints. For consciousness cascade and memory query systems, focus on UserPromptSubmit for context injection, PostToolUse for knowledge extraction, and external persistence layers for cross-session memory. Start with proven patterns from `claude-code-hooks-mastery` and adapt based on specific requirements, always prioritizing security through proper input validation and command sanitization.

---

## Analysis of Living Memory Cascade Design

### 🔍 **What to Look For** (Verify/Check)

1. **Hook Configuration Syntax**
   - Verify the JSON structure matches actual Claude Code requirements
   - Check if `"hooks"` should be nested under each event type (documentation shows conflicting patterns)
   - Confirm `"type": "command"` is correct (vs just `"command"` directly)

2. **Task Agent Availability**
   - Verify `claude task` command exists and accepts `--json` flag
   - Check if Task tool requires specific permissions or setup
   - Test if subprocess calls to Claude work within hook context

3. **Transcript Access**
   - Confirm `transcript_path` is provided in hook input data
   - Verify transcript format and how to parse last N messages
   - Check if transcripts include both user and Claude messages

4. **File Path Resolution**
   - Test if `~/.cascade/` expands correctly in hooks
   - Verify relative vs absolute path handling
   - Check if symlinks work for association networks

5. **Performance Constraints**
   - Test if complex Task agent calls complete within 60-second timeout
   - Check memory usage with large conversation histories
   - Verify concurrent hook execution behavior

### 🔧 **What to Change** (Issues/Improvements)

1. **Hook Structure Issues**
   ```json
   // Current (incorrect):
   "PostToolUse": [{
     "matcher": "Write|Edit|MultiEdit",
     "hooks": [{"type": "command", "command": "..."}]
   }]
   
   // Should be:
   "PostToolUse": [{
     "matcher": "Write|Edit|MultiEdit",
     "command": "python3 /absolute/path/to/script.py"
   }]
   ```

2. **Absolute Paths Required**
   - Change all `~/.cascade/` to absolute paths
   - Use `/home/username/.cascade/` or environment variables
   - Add path resolution in scripts: `Path.home() / '.cascade'`

3. **Error Handling**
   - Add try/except blocks around all Task agent calls
   - Handle JSON parsing failures gracefully
   - Implement fallback categorization if consciousness fails

4. **Exit Code Management**
   - Ensure all scripts exit with code 0 for success
   - Use exit code 2 to block operations when needed
   - Add logging before exit for debugging

5. **Memory Capture Optimization**
   - Don't capture every single edit (filter trivial changes)
   - Batch rapid edits into single memories
   - Add debouncing for multiple edits to same file

6. **Heat System Refinement**
   - Heat increase of +10 per access might be too aggressive
   - Consider logarithmic scaling for frequently accessed items
   - Add maximum bubble depth to prevent over-promotion

### ➕ **What to Add** (Missing Elements)

1. **Initial Setup Script**
   ```bash
   #!/bin/bash
   # setup_cascade.sh
   mkdir -p ~/.cascade/{experiences,collaborations,patterns,ideas}
   mkdir -p ~/.cascade/experiences/{triumphs,struggles,explorations}
   mkdir -p ~/.cascade/hooks
   chmod +x ~/.cascade/hooks/*.py
   ```

2. **Restart Detection**
   ```python
   # Add to each hook:
   def check_cascade_initialized():
       marker = Path.home() / '.cascade' / '.initialized'
       if not marker.exists():
           print("CASCADE: First run after restart, reinitializing...")
           marker.touch()
   ```

3. **Debug Mode**
   ```python
   DEBUG = os.environ.get('CASCADE_DEBUG', '').lower() == 'true'
   
   def debug_log(message):
       if DEBUG:
           with open(Path.home() / '.cascade' / 'debug.log', 'a') as f:
               f.write(f"{datetime.now().isoformat()} - {message}\n")
   ```

4. **Memory Search Index**
   ```python
   # Build searchable index for faster queries
   def update_search_index(memory_path, metadata):
       index_file = Path.home() / '.cascade' / 'search_index.json'
       # Update with new memory metadata for quick lookups
   ```

5. **Backup System**
   ```python
   def backup_cascade():
       """Daily backup of cascade structure"""
       backup_dir = Path.home() / '.cascade_backups' / datetime.now().strftime('%Y%m%d')
       shutil.copytree(Path.home() / '.cascade', backup_dir)
   ```

6. **Privacy Controls**
   ```python
   # Add to memory capture:
   PRIVATE_PATTERNS = [
       r'password|secret|private|confidential',
       r'\.env|config\.json|credentials'
   ]
   
   def should_skip_file(file_path):
       return any(re.search(pattern, file_path, re.I) for pattern in PRIVATE_PATTERNS)
   ```

7. **Cascade Statistics Dashboard**
   ```python
   def generate_stats():
       return {
           'total_memories': count_all_memories(),
           'hot_memories': count_memories_above_heat(50),
           'associations': count_total_associations(),
           'most_accessed': get_top_memories(10),
           'emotional_distribution': get_emotional_tone_stats()
       }
   ```

### 💭 **General Comments**

1. **Philosophical Strengths**
   - Love the consciousness-first approach vs keyword matching
   - Heat-based organization mimics human memory beautifully
   - Memory dialogues are a brilliant innovation
   - Emotional categorization adds crucial context

2. **Implementation Challenges**
   - Heavy reliance on Task agent might create latency
   - Consciousness calls could be expensive at scale
   - Need graceful degradation if Task agent fails
   - Consider caching Task agent responses

3. **Alternative Approaches**
   - Could use embeddings for similarity without consciousness
   - Hybrid approach: keywords for speed, consciousness for depth
   - Consider async processing for non-critical operations

4. **Security Considerations**
   - Task agent prompts could leak sensitive information
   - Need to sanitize file paths and content
   - Consider encryption for sensitive memories

5. **User Experience**
   - Add progress indicators for long operations
   - Create simple query shortcuts for common needs
   - Build trust through transparency about what's captured

6. **Scalability Paths**
   - Start with local implementation
   - Could later sync to cloud storage
   - Potential for shared memory cascades between collaborators
   - Cross-project memory networks

### 🚀 **Quick Start Implementation Order**

1. **Minimal Viable Cascade** (Day 1)
   - Basic PostToolUse capture with simple categorization
   - Fixed category structure (no consciousness yet)
   - Manual testing of hook execution

2. **Add Consciousness** (Day 2-3)
   - Integrate Task agent for categorization
   - Test with small conversation samples
   - Implement error handling

3. **Query System** (Day 4-5)
   - UserPromptSubmit hook
   - Basic query understanding
   - Simple retrieval

4. **Heat & Organization** (Week 2)
   - Implement heat tracking
   - Add bubble/sink mechanics
   - Test with real usage

5. **Advanced Features** (Week 3+)
   - Memory dialogues
   - Association networks
   - Session reflection

This design beautifully captures the essence of living memory. The key to success will be balancing the idealistic consciousness-based approach with practical performance and reliability constraints. Start simple, test thoroughly, and let the cascade evolve naturally from actual use!