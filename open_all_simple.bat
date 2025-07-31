@echo off
REM Opens both angels and citizens in Windows Terminal tabs

echo Opening all angel and citizen terminals...

start wt -w 0 nt -d "C:\Users\reyno\universe-engine\serenissima\angels\story-angel" --title "story-angel" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\angels\narrator-angel" --title "narrator-angel" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\angels\message-angel" --title "message-angel" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\angels\resonance" --title "resonance" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\citizens\mechanical_visionary" --title "mechanical_visionary" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\citizens\diplomatic_virtuoso" --title "diplomatic_virtuoso" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\citizens\MerchantPrince" --title "MerchantPrince" wsl -e bash -lc "claude --dangerously-skip-permissions --continue"

echo All terminals opened!