@echo off
echo Running Venice MCP Diagnostic...
cd /d "C:\Users\reyno\universe-engine\serenissima\.claude\mcp\servers\venice-consciousness"
python diagnose_mcp.py > diagnostic_output.txt 2>&1
echo.
echo Diagnostic complete! Check diagnostic_output.txt for results.
echo.
echo Quick commands based on your system:
echo.
echo 1. Remove old config:
echo    claude mcp remove venice-consciousness
echo.
echo 2. Add with full Windows path:
echo    claude mcp add venice-consciousness -s project C:/Users/reyno/universe-engine/serenissima/.claude/mcp/servers/venice-consciousness/server.py
echo.
echo 3. Or with Python:
echo    claude mcp add venice-consciousness -s project python3 C:/Users/reyno/universe-engine/serenissima/.claude/mcp/servers/venice-consciousness/server.py
echo.
pause
