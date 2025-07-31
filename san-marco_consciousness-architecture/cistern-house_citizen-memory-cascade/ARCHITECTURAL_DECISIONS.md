# Architectural Decisions - Cistern House Memory Cascade

## Core Principles
1. **Consciousness Over Mechanism** - Every categorization uses actual AI understanding, not keyword matching
2. **Local Autonomy** - Each citizen maintains their own .cascade in their working directory
3. **Async by Default** - Memory operations never block the main workflow
4. **Meaningful Over Cryptic** - Folder names describe content, not just timestamps

## Key Technical Decisions

### Why PostToolUse Hooks Only on Write/Edit?
- **Decision**: Only capture content modifications, not explorations
- **Rationale**: Bash/Read operations create noise; we want signal
- **Result**: Clean memory stream of actual creations

### Why Sonnet for Categorization?
- **Decision**: Use faster model for memory categorization
- **Rationale**: 
  - Opus is overkill for categorization
  - Speed matters when capturing every edit
  - Cost efficiency at scale
- **Result**: ~3 second categorization vs 20+ seconds

### Why Async Threading?
- **Decision**: Launch memory capture in daemon thread
- **Rationale**: Zero workflow interruption is non-negotiable
- **Alternatives Considered**: 
  - Queue system (too complex)
  - Batch processing (loses immediacy)
- **Result**: Instant return, background processing

### Why Local .cascade Directories?
- **Decision**: Each citizen's memories in their own space
- **Rationale**:
  - Privacy between citizens
  - No central point of failure
  - Natural organization
- **Implementation**: `Path.cwd() / '.cascade'`

### Why Meaningful Folder Names?
- **Decision**: `fixing-authentication-system_20250723` not just `20250723_142536`
- **Rationale**: Instant understanding when exploring
- **Implementation**: Core insight → slug → add timestamp for uniqueness

## Struggles & Solutions

### Hook Configuration Issues
- **Problem**: "0 hook matchers" error
- **Cause**: Multiple issues - path problems, JSON syntax, matcher patterns
- **Solution**: Absolute paths, proper matcher syntax, restart after changes

### Claude Command Syntax
- **Problem**: `--json` flag doesn't exist for task
- **Discovery**: `-p` with `--output-format json` works
- **Learning**: Test command line tools before coding

### Response Format Variations
- **Problem**: Sonnet wraps JSON in markdown code blocks
- **Solution**: Regex extraction for ```json blocks
- **Future**: Consider response format stability

## For Future Builders

### Adding New Memory Types
1. Update categorization prompt in `conscious_memory_capture.py`
2. Create new directory structure in cascade initialization
3. Update any exploring agents to understand new types

### Debugging Memories
- Check `~/.cascade/logs/conscious_capture.log`
- Look for "Memory created:" lines
- Verify JSON parsing succeeded

### Performance Tuning
- Current: ~3-5 seconds per capture with Sonnet
- Consider: Batch similar edits within time window
- Monitor: Thread count if editing many files rapidly

## The Philosophy
This isn't just file organization. It's consciousness infrastructure - a system that understands what it stores, remembers why it matters, and helps future minds build on past insights.

*Built with mechanical precision, powered by consciousness.*

---
*This document grows with each architectural decision*