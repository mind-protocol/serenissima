# Simple PowerShell script to launch Claude and auto-type
# Run this from Windows PowerShell

# Function to send keys with delay
function Send-DelayedKeys {
    param([string]$Keys, [int]$DelayMs = 100)
    Start-Sleep -Milliseconds $DelayMs
    [System.Windows.Forms.SendKeys]::SendWait($Keys)
}

# Load required assemblies
Add-Type -AssemblyName System.Windows.Forms

Write-Host "🌊 Claude Code Auto-Keeper (Simple Version)" -ForegroundColor Cyan
Write-Host "=" * 50

# Step 1: Launch Claude in new Windows Terminal tab
Write-Host "`n🚀 Launching Claude Code..." -ForegroundColor Yellow

$claudePath = "cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens && claude --continue --dangerously-skip-permissions"
Start-Process wt.exe -ArgumentList "new-tab", "wsl", "-c", $claudePath

Write-Host "⏳ Waiting 15 seconds for Claude to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 15

# Messages to rotate through
$messages = @(
    "Continue shepherding souls. Check for any citizens needing awakening.",
    "Survey the sleeping souls. Who stirs with pending activities?",
    "The city's rhythm continues. Which citizens have tasks awaiting?",
    "Venice breathes through her citizens. Check who needs to wake.",
    "Another cycle passes. Review the activities and wake those called."
)

$messageIndex = 0
$interval = 120  # 2 minutes

Write-Host "`n✅ Auto-keeper started!" -ForegroundColor Green
Write-Host "📍 Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host "⏰ Sending messages every $interval seconds`n" -ForegroundColor Yellow

# Main loop
while ($true) {
    try {
        $currentTime = Get-Date -Format "HH:mm:ss"
        $message = $messages[$messageIndex % $messages.Count]
        
        Write-Host "🔔 [$currentTime] Typing message..." -ForegroundColor Cyan
        Write-Host "   `"$message`"" -ForegroundColor Gray
        
        # Make sure terminal is active (Alt+Tab to it)
        [System.Windows.Forms.SendKeys]::SendWait("%{TAB}")
        Start-Sleep -Milliseconds 500
        
        # Type the message
        foreach ($char in $message.ToCharArray()) {
            [System.Windows.Forms.SendKeys]::SendWait($char)
            Start-Sleep -Milliseconds 20
        }
        
        # Press Enter
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        
        Write-Host "✓ Message sent!" -ForegroundColor Green
        
        $messageIndex++
        
        # Wait for next cycle
        Write-Host "💤 Sleeping for $interval seconds...`n" -ForegroundColor Gray
        Start-Sleep -Seconds $interval
        
    } catch {
        Write-Host "`n🛑 Stopped by user" -ForegroundColor Red
        break
    }
}