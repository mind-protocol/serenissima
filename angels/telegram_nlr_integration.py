#!/usr/bin/env python3
"""
Telegram NLR Integration - Compatibility Bridge
Redirects to Tessere's telegram adapter
"""

from tessere.telegram_integration_adapter import VeniceEmergencyComm, TelegramAdapter

# Export for backward compatibility
__all__ = ['VeniceEmergencyComm', 'TelegramAdapter']