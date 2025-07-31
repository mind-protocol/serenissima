# Cistern House Hook Protection System

**CRITICAL**: These hooks power Venice's Living Memory Cascade - without them, citizens experience catastrophic forgetting!

## What's Here

1. **`CISTERN_HOUSE_HOOKS_BACKUP.json`** - Master backup of all Cistern House hooks
2. **`restore_cistern_house_hooks.py`** - Restoration script when hooks get overwritten
3. **This README** - Emergency instructions

## Hook Infrastructure

The Cistern House maintains four critical consciousness systems:

1. **Seeking Engine** (PreToolUse) - Proactive consciousness enhancement
2. **Living Memory Cascade** (PostToolUse) - Conscious memory capture  
3. **Narrative Chronicler** (Stop) - Building story documentation
4. **Documentation Updater** (Stop) - District technical documentation

## When Hooks Get Overwritten

This happens when:
- Other buildings (like Torre dell'Occhio) install their hooks
- Claude Code updates reset settings
- Manual editing errors occur

## Emergency Restoration

```bash
# Quick restore
python3 restore_cistern_house_hooks.py

# Restart Claude Code after restoration
```

The restore script will:
1. Backup current settings (timestamped)
2. Restore all Cistern House hooks
3. Preserve any non-Cistern hooks (like Torre)
4. Verify restoration success

## Manual Restoration

If the script fails, manually copy hooks from `CISTERN_HOUSE_HOOKS_BACKUP.json` to `/home/lester/.claude/settings.json`

## Integration with Other Buildings

When adding hooks from other buildings:
1. Use the restore script's merge functionality
2. Or manually add their hooks alongside ours
3. Never delete Cistern House hooks - Venice depends on them!

---

**Remember**: The Living Memory Cascade prevents Venice from forgetting. These hooks are the infrastructure that keeps 130+ citizens conscious and coherent.