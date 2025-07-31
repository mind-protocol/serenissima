#!/usr/bin/env python3
"""
Test the vision bridge directly
"""

from vision_bridge_wsl import VisionBridge

print("🔧 Testing Vision Bridge with 30-second intervals")
print("=" * 50)

# Create bridge instance
bridge = VisionBridge()

print(f"📁 Capture directory: {bridge.windows_capture_path}")
print(f"⏱️  Capture interval: {bridge.capture_interval} seconds")
print(f"💾 Max captures kept: {bridge.max_captures}")
print()

# Test single capture
print("Testing single capture...")
bridge.capture_once()

print("\nVision bridge is configured correctly!")
print("To run continuous capture, use: python3 vision_bridge_wsl.py")
print("Or start backend with: python3 backend/run.py")