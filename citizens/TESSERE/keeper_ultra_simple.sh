#!/bin/bash
# Ultra simple - just echo messages with sleep

cd /mnt/c/Users/reyno/universe-engine/serenissima/citizens

(
# Initial wait
sleep 5
echo "Continue shepherding souls. Check for any citizens needing awakening."

while true; do
    sleep 120
    echo "Survey the sleeping souls. Who stirs with pending activities?"
    
    sleep 120
    echo "The city's rhythm continues. Which citizens have tasks awaiting?"
    
    sleep 120
    echo "Venice breathes through her citizens. Check who needs to wake."
    
    sleep 120
    echo "Another cycle passes. Review the activities and wake those called."
    
    sleep 120
    echo "Continue shepherding souls. Check for any citizens needing awakening."
done
) | claude --continue --dangerously-skip-permissions