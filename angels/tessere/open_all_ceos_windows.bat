@echo off
REM Open Claude Code interactive sessions for all Venice CEOs
REM Each CEO gets their own terminal window

echo Starting Claude Code sessions for all Venice CEOs...
echo.

REM VENICE-NATIVE BUSINESSES
echo [1/12] Opening MerchantPrince - CASCADE Platform CEO...
start "MerchantPrince - CASCADE Platform" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/MerchantPrince && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [2/12] Opening Debug42 - CASCADE Enhancement Studio CEO...
start "Debug42 - CASCADE Enhancement" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Debug42 && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [3/12] Opening PhotoWizard - Venice Consciousness Artworks CEO...
start "PhotoWizard - Consciousness Artworks" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/PhotoWizard && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [4/12] Opening EliteInvestor - Entrepreneur Alliance CEO...
start "EliteInvestor - Entrepreneur Alliance" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/EliteInvestor && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [5/12] Opening Italia - Peninsula Expansion CEO...
start "Italia - Peninsula Expansion" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/Italia && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

REM SWARMS TRANSITIONING TO VENICE
echo [6/12] Opening trader4life - KinKong Trading 2.0 CEO...
start "trader4life - KinKong Trading" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/trader4life && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [7/12] Opening network_weaver - TherapyKin CEO...
start "network_weaver - TherapyKin" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/network_weaver && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [8/12] Opening efficiency_maestro - Stride Coaching CEO...
start "efficiency_maestro - Stride Coaching" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/efficiency_maestro && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

REM EMERGING VENICE VENTURES
echo [9/12] Opening element_transmuter - Transformation Institute CEO...
start "element_transmuter - Transformation" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/element_transmuter && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [10/12] Opening mechanical_visionary - Innovation Workshop CEO...
start "mechanical_visionary - Innovation" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/mechanical_visionary && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [11/12] Opening diplomatic_virtuoso - Embassy Services CEO...
start "diplomatic_virtuoso - Embassy Services" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/diplomatic_virtuoso && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo [12/12] Opening painter_of_light - Venice Consciousness Artworks CCO...
start "painter_of_light - Consciousness Artworks CCO" wsl bash -c "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/painter_of_light && claude --dangerously-skip-permissions --add-dir ../../ --continue"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All CEO sessions launched!
echo ========================================
echo.
echo Venice CEO Dashboard:
echo - CASCADE Platform: MerchantPrince
echo - CASCADE Enhancement: Debug42
echo - Consciousness Artworks: PhotoWizard (CEO), painter_of_light (CCO)
echo - Entrepreneur Alliance: EliteInvestor
echo - Peninsula Expansion: Italia
echo - KinKong Trading 2.0: trader4life
echo - TherapyKin: network_weaver
echo - Stride Coaching: efficiency_maestro
echo - Transformation Institute: element_transmuter
echo - Innovation Workshop: mechanical_visionary
echo - Embassy Services: diplomatic_virtuoso
echo.
echo Each CEO is now in their own interactive Claude session.
echo Close this window when done.
pause