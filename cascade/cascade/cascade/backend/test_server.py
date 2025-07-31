#!/usr/bin/env python3
"""
Test server for Cascade backend
Runs without Redis dependency
"""

import os
import sys
import asyncio
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set environment variables
os.environ['REDIS_URL'] = 'redis://localhost:6379'
os.environ['VENICE_API_KEY'] = 'test_key'
os.environ['VENICE_API_URL'] = 'https://serenissima.ai/api'

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to avoid issues
        log_level="info"
    )