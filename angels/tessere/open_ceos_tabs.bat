@echo off
REM Open Claude Code sessions for all CEOs in Windows Terminal tabs

echo Opening all CEOs in Windows Terminal tabs...

REM Build the Windows Terminal command with all tabs
wt ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "MerchantPrince - CASCADE" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "Debug42 - CASCADE Enhancement" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Debug42 && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "PhotoWizard - Artworks CEO" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/PhotoWizard && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "EliteInvestor - Alliance" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/EliteInvestor && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "Italia - Peninsula" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Italia && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "trader4life - KinKong" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/trader4life && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "network_weaver - TherapyKin" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/network_weaver && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "efficiency_maestro - Stride" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/efficiency_maestro && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "element_transmuter - Transform" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/element_transmuter && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "mechanical_visionary - Innovation" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "diplomatic_virtuoso - Embassy" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" -d C:\Users\reyno --title "painter_of_light - Artworks CCO" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/painter_of_light && claude --dangerously-skip-permissions --add-dir ../../ --continue"

echo.
echo All CEOs opened in Windows Terminal tabs!
echo Use Ctrl+Tab to switch between them.
pause