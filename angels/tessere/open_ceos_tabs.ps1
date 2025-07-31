# PowerShell script to open all CEOs in Windows Terminal tabs

Write-Host "Opening all Venice CEOs in Windows Terminal tabs..." -ForegroundColor Green

# Define CEO groups for better tab organization
$ceoGroups = @{
    "Venice Native" = @(
        @{Name="MerchantPrince"; Company="CASCADE"; Role="CEO"},
        @{Name="Debug42"; Company="CASCADE Enhancement"; Role="CEO"},
        @{Name="PhotoWizard"; Company="Artworks"; Role="CEO"},
        @{Name="painter_of_light"; Company="Artworks"; Role="CCO"},
        @{Name="EliteInvestor"; Company="Alliance"; Role="CEO"},
        @{Name="Italia"; Company="Peninsula"; Role="CEO"}
    )
    "Swarm Transitions" = @(
        @{Name="trader4life"; Company="KinKong 2.0"; Role="CEO"},
        @{Name="network_weaver"; Company="TherapyKin"; Role="CEO"},
        @{Name="efficiency_maestro"; Company="Stride"; Role="CEO"}
    )
    "Emerging Ventures" = @(
        @{Name="element_transmuter"; Company="Transform"; Role="CEO"},
        @{Name="mechanical_visionary"; Company="Innovation"; Role="CEO"},
        @{Name="diplomatic_virtuoso"; Company="Embassy"; Role="CEO"}
    )
}

# Build the Windows Terminal command
$wtCommand = "wt"
$first = $true

foreach ($group in $ceoGroups.GetEnumerator()) {
    foreach ($ceo in $group.Value) {
        $tabTitle = "$($ceo.Name) - $($ceo.Company)"
        $wslCommand = "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$($ceo.Name) && claude --dangerously-skip-permissions --add-dir ../../ --continue"
        
        if ($first) {
            # First tab doesn't need new-tab
            $wtCommand += " -p `"Ubuntu`" -d C:\Users\reyno --title `"$tabTitle`" wsl bash -c `"$wslCommand`""
            $first = $false
        } else {
            $wtCommand += " ; new-tab -p `"Ubuntu`" -d C:\Users\reyno --title `"$tabTitle`" wsl bash -c `"$wslCommand`""
        }
    }
}

# Execute the command
Write-Host "Launching Windows Terminal with all CEO tabs..." -ForegroundColor Yellow
Invoke-Expression $wtCommand

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All CEO tabs opened successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Navigation Tips:" -ForegroundColor White
Write-Host "• Ctrl+Tab: Next tab" -ForegroundColor Gray
Write-Host "• Ctrl+Shift+Tab: Previous tab" -ForegroundColor Gray
Write-Host "• Ctrl+Alt+[number]: Jump to specific tab" -ForegroundColor Gray
Write-Host ""
Write-Host "CEO Tabs organized by:" -ForegroundColor White
Write-Host "• Venice Native Businesses (6 tabs)" -ForegroundColor Gray
Write-Host "• Swarm Transitions (3 tabs)" -ForegroundColor Gray
Write-Host "• Emerging Ventures (3 tabs)" -ForegroundColor Gray