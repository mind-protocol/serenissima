@echo off
REM Simple approach - opens Windows Terminal with tabs

echo Opening angel terminals...

start wt -w 0 nt -d "C:\Users\reyno\universe-engine\serenissima\angels\story-angel" --title "story-angel" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\angels\narrator-angel" --title "narrator-angel" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\angels\message-angel" --title "message-angel" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\angels\resonance" --title "resonance" wsl -e bash -lc "claude --dangerously-skip-permissions --continue"

echo Done!