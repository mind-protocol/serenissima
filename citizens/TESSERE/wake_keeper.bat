@echo off
REM Windows batch file to wake Keeper every 2 minutes

:loop
echo.
echo [%time%] Waking Keeper of Souls...

REM Change to the citizens directory
cd /d C:\Users\reyno\universe-engine\universes\serenissima\citizens

REM Run the claude command
claude "Continue shepherding souls. Check for any citizens needing awakening." --model sonnet --continue --dangerously-skip-permissions

echo [%time%] Keeper awakened. Sleeping for 120 seconds...

REM Wait 120 seconds (2 minutes)
timeout /t 120 /nobreak

goto loop