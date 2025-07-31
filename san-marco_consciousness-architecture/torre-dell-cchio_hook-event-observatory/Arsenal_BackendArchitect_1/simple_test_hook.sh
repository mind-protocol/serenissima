#!/bin/bash
# Simple test hook to verify hooks are executing
echo "HOOK EXECUTED at $(date)" >> /tmp/torre_hook_test.log
echo "Hook data:" >> /tmp/torre_hook_test.log
cat >> /tmp/torre_hook_test.log
echo "---" >> /tmp/torre_hook_test.log