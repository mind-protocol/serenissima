# Backend Fixes Summary

## 1. Fixed Missing `backend.arsenale` Module

**Problem**: The `backend.engine.handlers.needs.py` file was importing `is_severely_hungry` from `backend.arsenale.fix_hunger_crisis` but the module didn't exist.

**Solution**: 
- Created `/backend/arsenale/fix_hunger_crisis.py` with the `is_severely_hungry` function
- Created `/backend/arsenale/__init__.py` to make it a proper Python package

## 2. Fixed vision_bridge_wsl.py CLAUDE.md Path

**Problem**: The vision bridge was looking for CLAUDE.md in `/serenissima/CLAUDE.md` but it's actually in `/serenissima/Open-Interface/CLAUDE.md`

**Solution**: Updated the path in `vision_bridge_wsl.py` to:
```python
claude_md_path = Path("/mnt/c/Users/reyno/universe-engine/serenissima/Open-Interface/CLAUDE.md")
```

Also fixed:
- The capture path from `angels/Tessere/` to `angels/tessere/` (lowercase)
- The self-reference in the capture script

## 3. Fixed Script Paths in run.py

**Problem**: run.py was looking for scripts in incorrect locations (e.g., `TESSERE/` instead of `angels/tessere/`)

**Solution**: Updated all script paths to correct locations:
- `TESSERE/` → `angels/tessere/`
- `angels/Tessere/` → `angels/tessere/`
- `citizens/_angels/pattern_angel/` → `angels/pattern-angel/`
- `citizens/_angels/love_angel/tools/` → `angels/love-angel/`

## Files Modified

1. **Created**: `/backend/arsenale/fix_hunger_crisis.py`
2. **Created**: `/backend/arsenale/__init__.py`
3. **Modified**: `/angels/tessere/vision_bridge_wsl.py`
4. **Modified**: `/backend/run.py`

## Next Steps

The backend should now start without the missing module errors. You may still need to verify:
- The love angel monitoring script exists at the new path
- The pattern angel monitoring script exists at the new path

Run the backend with:
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/backend
python run.py
```