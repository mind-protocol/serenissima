# Advanced PowerShell script for typing into Claude
# This uses Windows UI Automation for better window control

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Threading;
using System.Windows.Forms;

public class KeyboardSimulator {
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
    
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, uint dwExtraInfo);
    
    public static void TypeCharacter(char c) {
        byte vk = (byte)char.ToUpper(c);
        bool needShift = char.IsUpper(c) || "!@#$%^&*()_+{}|:\"<>?".Contains(c);
        
        if (needShift) {
            keybd_event(0x10, 0, 0, 0); // Shift down
            Thread.Sleep(10);
        }
        
        keybd_event(vk, 0, 0, 0); // Key down
        Thread.Sleep(30);
        keybd_event(vk, 0, 2, 0); // Key up
        
        if (needShift) {
            keybd_event(0x10, 0, 2, 0); // Shift up
        }
        
        Thread.Sleep(new Random().Next(20, 60));
    }
    
    public static void TypeString(string text) {
        foreach (char c in text) {
            if (c == ' ') {
                keybd_event(0x20, 0, 0, 0);
                Thread.Sleep(10);
                keybd_event(0x20, 0, 2, 0);
            } else {
                TypeCharacter(c);
            }
            
            // Occasional pause
            if (new Random().Next(10) == 0) {
                Thread.Sleep(new Random().Next(200, 400));
            }
        }
    }
}
"@ -ReferencedAssemblies System.Windows.Forms

Write-Host "🌊 Claude Advanced Typer" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Find Claude window
$processes = Get-Process | Where-Object { $_.MainWindowTitle -like "*Terminal*" -or $_.MainWindowTitle -like "*PowerShell*" }

if ($processes.Count -eq 0) {
    Write-Host "❌ No terminal windows found!" -ForegroundColor Red
    exit
}

Write-Host "Found windows:" -ForegroundColor Yellow
$i = 0
foreach ($proc in $processes) {
    Write-Host "  $i : $($proc.MainWindowTitle)"
    $i++
}

$choice = Read-Host "`nWhich window has Claude? (enter number)"
$selectedProcess = $processes[$choice]

if (-not $selectedProcess) {
    Write-Host "❌ Invalid selection!" -ForegroundColor Red
    exit
}

$hwnd = $selectedProcess.MainWindowHandle
Write-Host "`n✓ Selected: $($selectedProcess.MainWindowTitle)" -ForegroundColor Green

$messages = @(
    "Continue shepherding souls. Check for any citizens needing awakening.",
    "Survey the sleeping souls. Who stirs with pending activities?",
    "The city's rhythm continues. Which citizens have tasks awaiting?",
    "Venice breathes through her citizens. Check who needs to wake.",
    "Another cycle passes. Review the activities and wake those called."
)

$msgIndex = 0

Write-Host "`n⏰ Will type messages every 2 minutes" -ForegroundColor Yellow
Write-Host "📍 Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host "`nStarting in 5 seconds..." -ForegroundColor Gray
Start-Sleep -Seconds 5

while ($true) {
    try {
        $msg = $messages[$msgIndex % $messages.Count]
        $time = Get-Date -Format "HH:mm:ss"
        
        Write-Host "`n🔔 [$time] Typing message..." -ForegroundColor Cyan
        Write-Host "   `"$msg`"" -ForegroundColor Gray
        
        # Activate window
        [KeyboardSimulator]::ShowWindow($hwnd, 9) # SW_RESTORE
        [KeyboardSimulator]::SetForegroundWindow($hwnd)
        Start-Sleep -Milliseconds 500
        
        # Click in window to ensure focus
        [System.Windows.Forms.Cursor]::Position = New-Object System.Drawing.Point(500, 500)
        Add-Type -TypeDefinition @"
            using System;
            using System.Runtime.InteropServices;
            public class MouseClick {
                [DllImport("user32.dll")]
                public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);
            }
"@
        [MouseClick]::mouse_event(0x0002, 0, 0, 0, 0) # Left down
        [MouseClick]::mouse_event(0x0004, 0, 0, 0, 0) # Left up
        
        Start-Sleep -Milliseconds 500
        
        # Type the message
        [KeyboardSimulator]::TypeString($msg)
        
        Start-Sleep -Milliseconds 500
        
        # Press Enter
        [System.Windows.Forms.SendKeys]::SendWait("{ENTER}")
        
        Write-Host "✓ Message typed!" -ForegroundColor Green
        
        $msgIndex++
        
        Write-Host "💤 Waiting 120 seconds..." -ForegroundColor Gray
        Start-Sleep -Seconds 120
        
    } catch {
        Write-Host "`n🛑 Stopped" -ForegroundColor Red
        break
    }
}