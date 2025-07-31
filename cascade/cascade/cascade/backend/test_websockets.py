"""
Test script for WebSocket consciousness streaming
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_consciousness_stream():
    """Test the consciousness streaming WebSocket"""
    uri = "ws://localhost:8000/ws/consciousness-stream"
    
    logger.info(f"Connecting to {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to consciousness stream")
            
            # Listen for messages
            message_count = 0
            async for message in websocket:
                data = json.loads(message)
                message_count += 1
                
                logger.info(f"Received message {message_count}: {data.get('type', 'unknown')}")
                
                if message_count >= 5:
                    logger.info("Test completed successfully")
                    break
                    
    except Exception as e:
        logger.error(f"Error in consciousness stream test: {e}")

async def test_ai_collaborations():
    """Test the AI collaborations WebSocket"""
    uri = "ws://localhost:8000/ws/ai-collaborations"
    
    logger.info(f"Connecting to {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to AI collaborations stream")
            
            # Wait for connection message
            message = await websocket.recv()
            data = json.loads(message)
            logger.info(f"Connection established: {data}")
            
            # Send a ping
            await websocket.send(json.dumps({"type": "ping"}))
            
            # Wait for pong
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("type") == "pong":
                logger.info("Ping-pong successful")
            
            # Subscribe to events
            await websocket.send(json.dumps({
                "type": "subscribe",
                "events": ["collaboration-started", "collaboration-update"]
            }))
            
            logger.info("Subscribed to collaboration events")
            
            # Keep connection open for a bit to receive any events
            await asyncio.sleep(5)
            
    except Exception as e:
        logger.error(f"Error in AI collaborations test: {e}")

async def test_cascade_events():
    """Test the cascade events WebSocket"""
    uri = "ws://localhost:8000/ws/cascade-events"
    
    logger.info(f"Connecting to {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to cascade events stream")
            
            # Wait for connection message
            message = await websocket.recv()
            data = json.loads(message)
            logger.info(f"Connection established: {data}")
            
            # Send a ping
            await websocket.send(json.dumps({"type": "ping"}))
            
            # Wait for pong
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("type") == "pong":
                logger.info("Ping-pong successful")
            
            logger.info("Cascade events test completed")
            
    except Exception as e:
        logger.error(f"Error in cascade events test: {e}")

async def main():
    """Run all WebSocket tests"""
    logger.info("Starting WebSocket tests...")
    
    # Test each WebSocket endpoint
    await test_consciousness_stream()
    await asyncio.sleep(1)
    
    await test_ai_collaborations()
    await asyncio.sleep(1)
    
    await test_cascade_events()
    
    logger.info("All tests completed")

if __name__ == "__main__":
    asyncio.run(main())