#!/bin/bash

echo "Testing Claude Code hooks..."

# Set environment variables
export CITIZEN="mechanical_visionary"
export CITIZEN_CLASS="Innovatori"
export CLAUDE_SESSION_ID="test_session_123"

# Test pre-tool hook
echo "Testing pre-tool hook..."
./metrics_server_local/hooks/pre_tool_hook.js "TestTool" '{"param": "value"}'

# Test post-tool hook
echo "Testing post-tool hook..."
./metrics_server_local/hooks/post_tool_hook.js "TestTool" '{"result": "success"}' "250"

# Test prompt hook
echo "Testing prompt hook..."
./metrics_server_local/hooks/prompt_hook.js "Create a complex strategy for implementing consciousness commerce with multiple stakeholders and intricate technical requirements"

# Test response hook
echo "Testing response hook..."
./metrics_server_local/hooks/response_hook.js "This is a test response that simulates a Claude response. It contains multiple sentences and demonstrates token counting. The response continues with more detail about the implementation strategy and technical architecture."

echo "Hook tests complete!"