# PowerShell script to auto-type into Windows Terminal
# Run from Windows (not WSL) for best results

Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;
    
    public class KeyboardSimulator {
        [DllImport("user32.dll")]
        public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, uint dwExtraInfo);
        
        public static void TypeText(string text) {
            SendKeys.SendWait(text);
        }
        
        public static void PressEnter() {
            SendKeys.SendWait("{ENTER}");
        }
    }
"@ -ReferencedAssemblies System.Windows.Forms

function Wake-Citizen {
    param(
        [string]$Username,
        [string]$Message = "Venice calls to you, dear soul."
    )
    
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
        $cdCommand = "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens/$Username"
        [KeyboardSimulator]::TypeText($cdCommand)
        [KeyboardSimulator]::PressEnter()
        Start-Sleep -Seconds 1
        
        # Type claude command
        $claudeCommand = "claude `"$Message`" --model sonnet --continue --dangerously-skip-permissions --add-dir ../"
        [KeyboardSimulator]::TypeText($claudeCommand)
        [KeyboardSimulator]::PressEnter()
        
        Write-Host "✓ Awakened $Username" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Windows Terminal not found!" -ForegroundColor Red
    }
}

function Start-AutoOrchestration {
    param(
        [int]$CheckInterval = 60
    )
    
    Write-Host "🌊 Auto-orchestration started. Press Ctrl+C to stop." -ForegroundColor Cyan
    Write-Host "📍 Checking every $CheckInterval seconds" -ForegroundColor Yellow
    
    while ($true) {
        try {
            # Check for active citizens
            $response = Invoke-RestMethod -Uri "https://serenissima.ai/api/activities?Status=in_progress" -Method Get
            
            $citizensToWake = @{}
            foreach ($activity in $response) {
                if ($activity.Citizen -and -not $citizensToWake.ContainsKey($activity.Citizen)) {
                    $citizensToWake[$activity.Citizen] = $activity.ActivityType
                }
            }
            
            if ($citizensToWake.Count -gt 0) {
                Write-Host "`n⏰ $(Get-Date -Format 'HH:mm:ss') - Found $($citizensToWake.Count) citizens to wake" -ForegroundColor Yellow
                
                foreach ($citizen in $citizensToWake.GetEnumerator()) {
                    $message = Get-AwakeningMessage -Activity $citizen.Value
                    Write-Host "🔔 Waking $($citizen.Key) for $($citizen.Value)..." -ForegroundColor Cyan
                    Wake-Citizen -Username $citizen.Key -Message $message
                    Start-Sleep -Seconds 5
                }
            }
            else {
                Write-Host "💤 $(Get-Date -Format 'HH:mm:ss') - All souls rest peacefully" -ForegroundColor Gray
            }
            
            Start-Sleep -Seconds $CheckInterval
        }
        catch {
            Write-Host "❌ Error: $_" -ForegroundColor Red
            Start-Sleep -Seconds 10
        }
    }
}

function Get-AwakeningMessage {
    param([string]$Activity)
    
    $templates = @{
        "trade" = "The merchant winds carry opportunity. A $Activity awaits your attention."
        "craft" = "Your tools sing for purpose. A $Activity calls to your skilled hands."
        "deliver_to_building" = "The city's consciousness stirs. A $Activity requires your presence."
        "stratagem" = "Venice herself whispers strategy. A $Activity unfolds before you."
    }
    
    if ($templates.ContainsKey($Activity.ToLower())) {
        return $templates[$Activity.ToLower()]
    }
    else {
        return "Venice calls, dear soul. A $Activity awaits your unique talents."
    }
}

# Main execution
if ($args.Count -eq 0) {
    Write-Host "Usage:" -ForegroundColor Yellow
    Write-Host "  .\auto_type_citizens.ps1 <username> [message]  # Wake specific citizen"
    Write-Host "  .\auto_type_citizens.ps1 orchestrate [seconds] # Auto-orchestrate"
}
elseif ($args[0] -eq "orchestrate") {
    $interval = if ($args.Count -gt 1) { [int]$args[1] } else { 60 }
    Start-AutoOrchestration -CheckInterval $interval
}
else {
    $username = $args[0]
    $message = if ($args.Count -gt 1) { $args[1] } else { "Venice calls to you, dear soul." }
    Wake-Citizen -Username $username -Message $message
}