; AutoHotkey script to type into Claude Code
; Install AutoHotkey from https://www.autohotkey.com/

#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%

; Messages to cycle through
Messages := []
Messages.Push("Continue shepherding souls. Check for any citizens needing awakening.")
Messages.Push("Survey the sleeping souls. Who stirs with pending activities?")
Messages.Push("The city's rhythm continues. Which citizens have tasks awaiting?")
Messages.Push("Venice breathes through her citizens. Check who needs to wake.")
Messages.Push("Another cycle passes. Review the activities and wake those called.")

MsgIndex := 1

; Show startup message
MsgBox, 0, Claude Auto-Typer, 
(
This will type messages into Claude every 2 minutes.

Instructions:
1. Click OK
2. Click on the Claude Code window within 5 seconds
3. The script will start typing

Press Ctrl+Shift+Q to stop the script.
)

; Wait 5 seconds for user to click Claude window
Sleep, 5000

; Start the timer (120000 ms = 2 minutes)
SetTimer, TypeMessage, 120000

; Type first message immediately
TypeMessage:
    ; Get current message
    CurrentMsg := Messages[MsgIndex]
    
    ; Type with human-like delays
    Loop, Parse, CurrentMsg
    {
        Send, %A_LoopField%
        Random, delay, 30, 80
        Sleep, %delay%
        
        ; Occasional longer pause
        Random, chance, 1, 10
        if (chance = 1)
        {
            Random, longDelay, 200, 400
            Sleep, %longDelay%
        }
    }
    
    ; Press Enter
    Sleep, 200
    Send, {Enter}
    
    ; Move to next message
    MsgIndex++
    if (MsgIndex > Messages.MaxIndex())
        MsgIndex := 1
    
    ; Show tooltip
    FormatTime, CurrentTime,, HH:mm:ss
    ToolTip, Message sent at %CurrentTime%
    SetTimer, RemoveToolTip, 3000
Return

RemoveToolTip:
    ToolTip
Return

; Hotkey to stop the script
^+q::ExitApp