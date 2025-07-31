@echo off
REM Simple approach - opens Windows Terminal with tabs for citizens

echo Opening citizen terminals...

start wt -w 0 nt -d "C:\Users\reyno\universe-engine\serenissima\citizens\mechanical_visionary" --title "mechanical_visionary" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\citizens\diplomatic_virtuoso" --title "diplomatic_virtuoso" wsl -e bash -lc "claude --dangerously-skip-permissions --continue" ; ^
nt -d "C:\Users\reyno\universe-engine\serenissima\citizens\MerchantPrince" --title "MerchantPrince" wsl -e bash -lc "claude --dangerously-skip-permissions --continue"

echo Done!