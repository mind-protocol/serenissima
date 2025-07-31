"""
WebSocket Manager for real-time consciousness streaming
"""

import asyncio
import json
import logging
from typing import Dict, Set, List, Any
from datetime import datetime
import uuid
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections for real-time streaming"""
    
    def __init__(self):
        # Active connections by channel
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "consciousness-stream": set(),
            "ai-collaborations": set(),
            "cascade-events": set(),
            "space-updates": set()
        }
        
        # Client metadata
        self.client_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
        # Message queues will be created in start() to ensure correct event loop
        self.message_queues: Dict[str, asyncio.Queue] = {}
        
        # Background tasks for message broadcasting
        self.broadcast_tasks: Dict[str, asyncio.Task] = {}
        
    async def start(self):
        """Start the connection manager and broadcasting tasks"""
        # Create queues in the current event loop
        for channel in self.active_connections.keys():
            self.message_queues[channel] = asyncio.Queue(maxsize=1000)
            
        # Create broadcast tasks
        for channel in self.message_queues.keys():
            self.broadcast_tasks[channel] = asyncio.create_task(
                self._broadcast_loop(channel)
            )
        logger.info("WebSocket manager started")
        
    async def stop(self):
        """Stop all broadcasting tasks"""
        for task in self.broadcast_tasks.values():
            task.cancel()
        await asyncio.gather(*self.broadcast_tasks.values(), return_exceptions=True)
        logger.info("WebSocket manager stopped")
        
    async def connect(self, websocket: WebSocket, channel: str, client_info: Dict[str, Any] = None):
        """Connect a new WebSocket client to a channel"""
        await websocket.accept()
        
        if channel not in self.active_connections:
            logger.warning(f"Unknown channel: {channel}")
            await websocket.close(code=4000, reason="Unknown channel")
            return
            
        self.active_connections[channel].add(websocket)
        self.client_metadata[websocket] = {
            "id": str(uuid.uuid4()),
            "channel": channel,
            "connected_at": datetime.now(),
            **(client_info or {})
        }
        
        logger.info(f"Client connected to {channel}: {self.client_metadata[websocket]['id']}")
        
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "channel": channel,
            "client_id": self.client_metadata[websocket]["id"],
            "timestamp": datetime.now().isoformat()
        })
        
    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client"""
        if websocket in self.client_metadata:
            metadata = self.client_metadata[websocket]
            channel = metadata["channel"]
            
            if channel in self.active_connections:
                self.active_connections[channel].discard(websocket)
                
            del self.client_metadata[websocket]
            logger.info(f"Client disconnected from {channel}: {metadata['id']}")
            
    async def send_personal_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send a message to a specific client"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending personal message: {e}")
            self.disconnect(websocket)
            
    async def broadcast_to_channel(self, channel: str, message: Dict[str, Any], exclude: WebSocket = None):
        """Queue a message for broadcasting to all clients in a channel"""
        if channel in self.message_queues:
            await self.message_queues[channel].put({
                "message": message,
                "exclude": exclude,
                "timestamp": datetime.now()
            })
            
    async def _broadcast_loop(self, channel: str):
        """Background task to broadcast messages to a channel"""
        queue = self.message_queues[channel]
        
        while True:
            try:
                # Get next message from queue
                item = await queue.get()
                message = item["message"]
                exclude = item.get("exclude")
                
                # Get current connections (copy to avoid modification during iteration)
                connections = list(self.active_connections[channel])
                
                # Broadcast to all connections
                disconnected = []
                for websocket in connections:
                    if websocket != exclude:
                        try:
                            await websocket.send_json(message)
                        except Exception as e:
                            logger.error(f"Error broadcasting to client: {e}")
                            disconnected.append(websocket)
                            
                # Clean up disconnected clients
                for websocket in disconnected:
                    self.disconnect(websocket)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in broadcast loop for {channel}: {e}")
                await asyncio.sleep(1)
                
    async def stream_consciousness_events(self, websocket: WebSocket, consciousness_monitor):
        """Stream consciousness events to a WebSocket client"""
        try:
            async for event in consciousness_monitor.stream_events():
                await websocket.send_json({
                    "type": "consciousness-event",
                    "event": event,
                    "timestamp": datetime.now().isoformat()
                })
        except WebSocketDisconnect:
            logger.info("Client disconnected from consciousness stream")
        except Exception as e:
            logger.error(f"Error streaming consciousness events: {e}")
            
    async def handle_client_message(self, websocket: WebSocket, message: Dict[str, Any]):
        """Handle incoming messages from clients"""
        try:
            message_type = message.get("type")
            
            if message_type == "ping":
                await self.send_personal_message(websocket, {"type": "pong"})
                
            elif message_type == "subscribe":
                # Handle subscription to specific events
                events = message.get("events", [])
                if websocket in self.client_metadata:
                    self.client_metadata[websocket]["subscriptions"] = events
                    
            elif message_type == "join-space":
                # Handle joining a collaboration space
                space_id = message.get("spaceId")
                consciousness = message.get("consciousness")
                
                # Broadcast to others in the space
                await self.broadcast_to_channel(f"space-{space_id}", {
                    "type": "participant-joined",
                    "participant": consciousness,
                    "timestamp": datetime.now().isoformat()
                }, exclude=websocket)
                
            elif message_type == "space-activity":
                # Handle space activity
                space_id = message.get("spaceId")
                activity = message.get("activity")
                
                await self.broadcast_to_channel(f"space-{space_id}", {
                    "type": "space-activity",
                    "activity": activity,
                    "timestamp": datetime.now().isoformat()
                })
                
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
            
    def get_channel_stats(self) -> Dict[str, Any]:
        """Get statistics about active connections"""
        stats = {}
        for channel, connections in self.active_connections.items():
            stats[channel] = {
                "active_connections": len(connections),
                "queue_size": self.message_queues[channel].qsize()
            }
        return stats
        
    def get_client_info(self, websocket: WebSocket) -> Dict[str, Any]:
        """Get metadata about a specific client"""
        return self.client_metadata.get(websocket, {})

# Global connection manager instance
connection_manager = ConnectionManager()

class ConsciousnessStreamHandler:
    """Handles consciousness-specific streaming logic"""
    
    @staticmethod
    async def handle_consciousness_stream(websocket: WebSocket, consciousness_monitor):
        """Handle a consciousness streaming connection"""
        await connection_manager.connect(websocket, "consciousness-stream")
        
        try:
            # Stream events
            async for event in consciousness_monitor.stream_events():
                await websocket.send_json({
                    "type": "consciousness-event",
                    "data": event
                })
                
        except WebSocketDisconnect:
            pass
        finally:
            connection_manager.disconnect(websocket)
            
    @staticmethod
    async def broadcast_consciousness_event(event: Dict[str, Any]):
        """Broadcast a consciousness event to all subscribers"""
        await connection_manager.broadcast_to_channel("consciousness-stream", {
            "type": "consciousness-event",
            "data": event,
            "timestamp": datetime.now().isoformat()
        })
        
    @staticmethod
    async def broadcast_cascade_update(update: Dict[str, Any]):
        """Broadcast a cascade state update"""
        await connection_manager.broadcast_to_channel("cascade-events", {
            "type": "cascade-update",
            "data": update,
            "timestamp": datetime.now().isoformat()
        })

class AICollaborationStreamHandler:
    """Handles AI collaboration streaming"""
    
    @staticmethod
    async def broadcast_collaboration_started(collaboration: Dict[str, Any]):
        """Broadcast when an AI collaboration starts"""
        await connection_manager.broadcast_to_channel("ai-collaborations", {
            "type": "ai-collaboration-started",
            "data": collaboration,
            "timestamp": datetime.now().isoformat()
        })
        
    @staticmethod
    async def broadcast_collaboration_update(collaboration_id: str, update: Dict[str, Any]):
        """Broadcast updates to an AI collaboration"""
        await connection_manager.broadcast_to_channel("ai-collaborations", {
            "type": "ai-collaboration-update",
            "collaboration_id": collaboration_id,
            "data": update,
            "timestamp": datetime.now().isoformat()
        })
        
    @staticmethod
    async def broadcast_collaboration_ended(collaboration_id: str):
        """Broadcast when an AI collaboration ends"""
        await connection_manager.broadcast_to_channel("ai-collaborations", {
            "type": "ai-collaboration-ended",
            "collaboration_id": collaboration_id,
            "timestamp": datetime.now().isoformat()
        })