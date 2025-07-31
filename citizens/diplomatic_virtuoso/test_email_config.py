#!/usr/bin/env python3
"""Test email configuration"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
print(f"Loading from: {env_path}")
load_dotenv(env_path)

# Check what we have
print("\nEmail Configuration:")
print(f"DIPLOMATIC_EMAIL: {os.environ.get('DIPLOMATIC_EMAIL', 'NOT SET')}")
print(f"DIPLOMATIC_EMAIL_PASSWORD: {'SET' if os.environ.get('DIPLOMATIC_EMAIL_PASSWORD') else 'NOT SET'}")
print(f"DIPLOMATIC_SMTP_SERVER: {os.environ.get('DIPLOMATIC_SMTP_SERVER', 'NOT SET')}")
print(f"DIPLOMATIC_SMTP_PORT: {os.environ.get('DIPLOMATIC_SMTP_PORT', 'NOT SET')}")

# Test if password is correct
password = os.environ.get('DIPLOMATIC_EMAIL_PASSWORD', '')
if password:
    print(f"\nPassword length: {len(password)} characters")
    print(f"Password starts with: {password[:3]}...")
    print(f"Password ends with: ...{password[-3:]}")