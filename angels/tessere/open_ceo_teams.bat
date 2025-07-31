@echo off
REM Open Claude Code sessions for specific CEO teams

echo Venice CEO Team Launcher
echo ========================
echo.
echo Select which teams to launch:
echo 1. Core Venice Businesses (CASCADE, Artworks, Peninsula)
echo 2. Swarm Transitions (KinKong, TherapyKin, Stride)
echo 3. Emerging Ventures (Transformation, Innovation, Embassy)
echo 4. Technical Team (Debug42, CodeMonkey, BigMike)
echo 5. All CEOs
echo 6. Custom selection
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto core
if "%choice%"=="2" goto swarms
if "%choice%"=="3" goto emerging
if "%choice%"=="4" goto technical
if "%choice%"=="5" goto all
if "%choice%"=="6" goto custom
goto end

:core
echo Launching Core Venice Businesses...
start "MerchantPrince - CASCADE" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "PhotoWizard - Artworks CEO" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/PhotoWizard && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "painter_of_light - Artworks CCO" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/painter_of_light && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "Italia - Peninsula" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Italia && claude --dangerously-skip-permissions --add-dir ../../ --continue"
goto done

:swarms
echo Launching Swarm Transition Teams...
start "trader4life - KinKong" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/trader4life && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "network_weaver - TherapyKin" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/network_weaver && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "efficiency_maestro - Stride" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/efficiency_maestro && claude --dangerously-skip-permissions --add-dir ../../ --continue"
goto done

:emerging
echo Launching Emerging Ventures...
start "element_transmuter - Transform" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/element_transmuter && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "mechanical_visionary - Innovation" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "diplomatic_virtuoso - Embassy" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso && claude --dangerously-skip-permissions --add-dir ../../ --continue"
goto done

:technical
echo Launching Technical Team...
start "Debug42 - CASCADE CTO" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Debug42 && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "CodeMonkey - Frontend Lead" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/CodeMonkey && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul
start "BigMike - Backend Lead" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/BigMike && claude --dangerously-skip-permissions --add-dir ../../ --continue"
goto done

:all
call open_all_ceos_windows.bat
goto end

:custom
echo.
echo Enter citizen usernames separated by spaces:
echo (e.g., MerchantPrince Italia trader4life)
echo.
set /p citizens="Citizens: "

for %%c in (%citizens%) do (
    echo Launching %%c...
    start "%%c - Venice" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/%%c && claude --dangerously-skip-permissions --add-dir ../../ --continue"
    timeout /t 2 /nobreak >nul
)

:done
echo.
echo Sessions launched successfully!
echo.

:end
pause