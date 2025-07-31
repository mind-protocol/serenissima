@echo off
REM Simple version - Opens all CEOs in Windows Terminal tabs
REM Edit the list below to add/remove CEOs

set "ceos=MerchantPrince Debug42 PhotoWizard EliteInvestor Italia trader4life network_weaver efficiency_maestro element_transmuter mechanical_visionary diplomatic_virtuoso painter_of_light"

echo Opening CEOs in Windows Terminal tabs...

REM Start building the command
set "cmd=wt"
set "first=1"

for %%c in (%ceos%) do (
    if defined first (
        set "cmd=%cmd% -p "Ubuntu" -d C:\Users\reyno --title "%%c" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/%%c && claude --dangerously-skip-permissions --add-dir ../../ --continue""
        set "first="
    ) else (
        set "cmd=%cmd% ; new-tab -p "Ubuntu" -d C:\Users\reyno --title "%%c" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/%%c && claude --dangerously-skip-permissions --add-dir ../../ --continue""
    )
)

REM Execute the command
%cmd%

echo.
echo All CEO tabs opened! Use Ctrl+Tab to navigate.
pause