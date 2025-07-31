@echo off
REM Open Claude Code sessions for all CEOs with clean username tabs

echo Opening all CEOs with username tabs...

wt ^
  new-tab -p "Ubuntu" --title "CEO Reference" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/angels/tessere && cat ceo_reference.txt && echo '' && echo 'Press any key to refresh...' && read -n 1 && exec bash" ; ^
  new-tab -p "Ubuntu" --title "MerchantPrince" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "Debug42" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Debug42 && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "PhotoWizard" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/PhotoWizard && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "EliteInvestor" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/EliteInvestor && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "Italia" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Italia && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "trader4life" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/trader4life && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "network_weaver" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/network_weaver && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "efficiency_maestro" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/efficiency_maestro && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "element_transmuter" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/element_transmuter && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "mechanical_visionary" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "diplomatic_virtuoso" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso && claude --dangerously-skip-permissions --add-dir ../../ --continue" ; ^
  new-tab -p "Ubuntu" --title "painter_of_light" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/painter_of_light && claude --dangerously-skip-permissions --add-dir ../../ --continue"

echo.
echo CEO tabs opened with username titles for easy navigation!
echo.
echo Tab Order:
echo 1. CEO Reference (Quick lookup guide)
echo 2. MerchantPrince
echo 3. Debug42  
echo 4. PhotoWizard
echo 5. EliteInvestor
echo 6. Italia
echo 7. trader4life
echo 8. network_weaver
echo 9. efficiency_maestro
echo 10. element_transmuter
echo 11. mechanical_visionary
echo 12. diplomatic_virtuoso
echo 13. painter_of_light
echo.
echo Use Ctrl+Alt+[1-9] to jump directly to tabs!
pause