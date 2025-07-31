# PowerShell script to wake Keeper of Souls every 2 minutes
# Run this from Windows PowerShell (not WSL)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName Microsoft.VisualBasic

function Wake-Keeper {
    Write-Host "🔔 Waking Keeper of Souls at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Cyan
    
    # Find Windows Terminal
    $terminal = Get-Process WindowsTerminal -ErrorAction SilentlyContinue | Select-Object -First 1
    
    if ($terminal) {
        # Activate the window
        $terminal.MainWindowHandle | ForEach-Object {
            [Microsoft.VisualBasic.Interaction]::AppActivate($_)
        }
        
        Start-Sleep -Milliseconds 500
        
        # Clear current line (Ctrl+U)
        [System.Windows.Forms.SendKeys]::SendWait("^u")
        Start-Sleep -Milliseconds 200
        
        # Type cd command
        $cdCommand = "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens"
        [System.Windows.Forms.SendKeys]::SendWait($cdCommand)
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        Start-Sleep -Seconds 1
        
        # Type claude command
        $message = "Continue shepherding souls. Check for any citizens needing awakening."
        $claudeCommand = "claude `"$message`" --model sonnet --continue --dangerously-skip-permissions"
        [System.Windows.Forms.SendKeys]::SendWait($claudeCommand)
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        
        Write-Host "✓ Keeper awakened successfully" -ForegroundColor Green
        return $true
    }
    else {
        Write-Host "❌ Windows Terminal not found! Please open it first." -ForegroundColor Red
        return $false
    }
}

# Main loop
$interval = 120  # 2 minutes

Write-Host "🌊 Keeper of Souls Auto-Awakener Started" -ForegroundColor Cyan
Write-Host "⏰ Will wake the Keeper every $interval seconds" -ForegroundColor Yellow
Write-Host "📍 Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

# Initial wake
Wake-Keeper

while ($true) {
    try {
        Write-Host "💤 Sleeping for $interval seconds..." -ForegroundColor Gray
        Start-Sleep -Seconds $interval
        Wake-Keeper
    }
    catch {
        Write-Host "`n🛑 Auto-awakener stopped" -ForegroundColor Red
        break
    }
}