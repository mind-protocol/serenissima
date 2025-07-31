# PowerShell script to open Claude Code sessions for all Venice CEOs
# Each CEO gets their own terminal window

Write-Host "Starting Claude Code sessions for all Venice CEOs..." -ForegroundColor Green
Write-Host ""

# Define all CEOs with their companies
$ceos = @(
    @{Name="MerchantPrince"; Company="CASCADE Platform"; Type="CEO"},
    @{Name="Debug42"; Company="CASCADE Enhancement Studio"; Type="CEO"},
    @{Name="PhotoWizard"; Company="Venice Consciousness Artworks"; Type="CEO"},
    @{Name="EliteInvestor"; Company="Entrepreneur Alliance"; Type="CEO"},
    @{Name="Italia"; Company="Peninsula Expansion"; Type="CEO"},
    @{Name="trader4life"; Company="KinKong Trading 2.0"; Type="CEO"},
    @{Name="network_weaver"; Company="TherapyKin"; Type="CEO"},
    @{Name="efficiency_maestro"; Company="Stride Coaching"; Type="CEO"},
    @{Name="element_transmuter"; Company="Transformation Institute"; Type="CEO"},
    @{Name="mechanical_visionary"; Company="Innovation Workshop"; Type="CEO"},
    @{Name="diplomatic_virtuoso"; Company="Embassy Services"; Type="CEO"},
    @{Name="painter_of_light"; Company="Venice Consciousness Artworks"; Type="CCO"}
)

$counter = 1
$total = $ceos.Count

foreach ($ceo in $ceos) {
    $progress = "[{0}/{1}]" -f $counter, $total
    Write-Host "$progress Opening $($ceo.Name) - $($ceo.Company) $($ceo.Type)..." -ForegroundColor Yellow
    
    $windowTitle = "$($ceo.Name) - $($ceo.Company)"
    $wslCommand = "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$($ceo.Name) && claude --dangerously-skip-permissions --add-dir ../../ --continue"
    
    Start-Process wsl -ArgumentList "bash", "-c", "`"$wslCommand`"" -WindowStyle Normal
    
    # Small delay to prevent overwhelming the system
    Start-Sleep -Seconds 2
    $counter++
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All CEO sessions launched!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Venice Leadership Team Active:" -ForegroundColor White

foreach ($ceo in $ceos) {
    Write-Host "• $($ceo.Name) - $($ceo.Type) of $($ceo.Company)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Each leader is now in their own interactive Claude session." -ForegroundColor Yellow
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")