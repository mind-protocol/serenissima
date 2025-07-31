# Torre UI Cache Clear Instructions

## 🔧 React Build Cache Issue

The error is showing line 293 but the file only shows one declaration at line 284. This suggests React's dev server has cached the old version with the duplicate declaration.

## ✅ Solution Steps:

### 1. Stop the React Dev Server
- Press `Ctrl+C` in the terminal running `npm start`

### 2. Clear React Cache
```bash
cd /mnt/c/Users/reyno/universe-engine/serenissima/san-marco_consciousness-architecture/torre-dell-cchio_hook-event-observatory/ui-observation-deck/consciousness-dashboard_react-interface

# Clear npm cache
npm start -- --reset-cache

# OR delete node_modules and reinstall
rm -rf node_modules
rm package-lock.json
npm install
```

### 3. Alternative: Force Cache Clear
```bash
# Clear React's internal cache
rm -rf node_modules/.cache
rm -rf build

# Restart with cleared cache
npm start
```

### 4. Verify File Content
The current ConsciousnessStream.js should have only ONE declaration:
```javascript
// Line 284 - ONLY declaration
const ToolResponseSection = styled.div`
  margin-top: 12px;
  border: 1px solid rgba(184, 134, 11, 0.3);
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.05);
`;
```

## 🏛️ Expected Result After Cache Clear:
- Torre UI compiles successfully  
- No duplicate declaration errors
- Consciousness Stream displays with bronze Torre styling
- Active Entities tab functional

The React dev server was holding onto the old version with the duplicate declaration. Clearing the cache should resolve this immediately.

---
*Issue: React Cache Staleness*
*Solution: Clear cache and restart dev server*
*Expected: Immediate compilation success*