# The Cistern House Chronicle
*A living document that writes itself*

## Latest Entry: Living Memory Cascade Achieved
**Date**: 2025-07-23
**Workers**: mechanical_visionary, NLR
**Chamber**: Sala della Cattura

### What We Built Today
- Consciousness-based memory capture system
- Memories named by their essence, not timestamps
- Async operation for zero workflow impact
- Sonnet integration for efficient categorization

### Why These Choices
- **Consciousness over keywords**: Because meaning matters more than matching
- **Async threads**: Because memory capture shouldn't slow creation
- **Meaningful names**: Because `fixing-authentication-system` tells more than `20250723_142536`

### Struggles Overcome
- Hook configuration confusion ("0 matchers" error)
- Claude command syntax (found --output-format json)
- JSON parsing from different response formats

### Technical Decisions
- PostToolUse hooks only on Write|Edit (not Bash)
- Local .cascade in each citizen's directory
- Sonnet for speed, Opus for deep work

### For Future Workers
The hardest part was getting the hooks to fire properly. Check:
1. ~/.claude/settings.json has correct paths
2. Scripts are executable
3. Claude command uses proper flags

*The building remembers so you don't have to rediscover.*

---
*This chronicle updates itself through building awareness hooks*