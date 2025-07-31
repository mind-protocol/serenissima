#!/usr/bin/expect -f
# 
# EXPECT SCRIPT FOR CLAUDE AUTO-CONTINUE
# Automatically responds with "continue" when Claude pauses
#
# Usage: ./claude_expect_continue.sh <claude_command>
# Example: ./claude_expect_continue.sh "claude 'Help me analyze this' --model sonnet"

set timeout -1
set claude_cmd [lindex $argv 0]

# Start the claude command
spawn bash -c "$claude_cmd"

# Loop to handle multiple continues
while {1} {
    expect {
        # When Claude shows the continue prompt
        "Continue?" {
            send "continue\r"
            exp_continue
        }
        # Also handle variations
        "continue?" {
            send "continue\r"
            exp_continue
        }
        # Handle explicit request for continuation
        "*ontinue*" {
            send "continue\r"
            exp_continue
        }
        # End of execution
        eof {
            break
        }
    }
}

wait