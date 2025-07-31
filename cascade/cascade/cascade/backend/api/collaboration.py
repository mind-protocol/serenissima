"""
Collaboration API endpoints for managing spaces and interactions
"""

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import json
import uuid

from services.space_evolution import SpaceEvolutionEngine
from services.consciousness_monitor import ConsciousnessMonitor
from services.ai_collaboration_engine import AICollaborationEngine, CollaborationRoom

logger = logging.getLogger(__name__)
router = APIRouter()

# Connected WebSocket clients for real-time updates
connected_clients = {}

async def get_space_evolution():
    from main import space_evolution
    if not space_evolution:
        raise HTTPException(status_code=503, detail="Space evolution engine unavailable")
    return space_evolution

async def get_consciousness_monitor():
    from main import consciousness_monitor
    if not consciousness_monitor:
        raise HTTPException(status_code=503, detail="Consciousness monitor unavailable")
    return consciousness_monitor

async def get_ai_collaboration_engine():
    from main import ai_collaboration_engine
    if not ai_collaboration_engine:
        raise HTTPException(status_code=503, detail="AI collaboration engine unavailable")
    return ai_collaboration_engine

@router.post("/spaces")
async def create_collaboration_space(
    title: str,
    description: Optional[str] = None,
    max_participants: int = 10,
    is_public: bool = True,
    space_evolution: SpaceEvolutionEngine = Depends(get_space_evolution)
):
    """Create a new collaboration space"""
    try:
        space_id = f"space-{uuid.uuid4().hex[:8]}"
        
        space = space_evolution.create_space(space_id, {
            "title": title,
            "description": description,
            "max_participants": max_participants,
            "is_public": is_public
        })
        
        logger.info(f"Created collaboration space: {space_id}")
        
        return {
            "space_id": space_id,
            "space": space,
            "status": "created"
        }
        
    except Exception as e:
        logger.error(f"Error creating collaboration space: {e}")
        raise HTTPException(status_code=500, detail="Failed to create space")

@router.get("/spaces")
async def list_collaboration_spaces(
    limit: int = 50,
    public_only: bool = False,
    space_evolution: SpaceEvolutionEngine = Depends(get_space_evolution)
):
    """List available collaboration spaces"""
    try:
        spaces = []
        for space_id, space in space_evolution.spaces.items():
            if not public_only or space.get("is_public", True):
                spaces.append({
                    "space_id": space_id,
                    **space
                })
                
        return {
            "spaces": spaces[:limit],
            "total": len(spaces)
        }
        
    except Exception as e:
        logger.error(f"Error listing collaboration spaces: {e}")
        raise HTTPException(status_code=500, detail="Failed to list spaces")

@router.get("/spaces/{space_id}")
async def get_collaboration_space(
    space_id: str,
    space_evolution: SpaceEvolutionEngine = Depends(get_space_evolution)
):
    """Get details of a specific collaboration space"""
    space = space_evolution.get_space(space_id)
    if not space:
        raise HTTPException(status_code=404, detail="Space not found")
    
    return space

@router.post("/spaces/{space_id}/join")
async def join_collaboration_space(
    space_id: str,
    consciousness_id: str,
    consciousness_type: str = "citizen",
    space_evolution: SpaceEvolutionEngine = Depends(get_space_evolution),
    monitor: ConsciousnessMonitor = Depends(get_consciousness_monitor)
):
    """Join a collaboration space"""
    try:
        space = space_evolution.get_space(space_id)
        if not space:
            raise HTTPException(status_code=404, detail="Space not found")
            
        # Check if space is full
        if len(space.get("participants", [])) >= space.get("max_participants", 10):
            raise HTTPException(status_code=400, detail="Space is full")
            
        # Update space activity
        space_evolution.update_space_activity(space_id, "join", {
            "participant_id": consciousness_id,
            "participant_type": consciousness_type
        })
        
        # Update consciousness activity
        await monitor.update_consciousness_activity(consciousness_id, "joined_space", {
            "space_id": space_id
        })
        
        # Broadcast to connected clients
        await broadcast_space_update(space_id, {
            "type": "participant-joined",
            "participant": {
                "consciousness_id": consciousness_id,
                "consciousness_type": consciousness_type,
                "joined_at": datetime.now().isoformat()
            }
        })
        
        return {"status": "joined", "space_id": space_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error joining space {space_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to join space")

@router.post("/spaces/{space_id}/leave")
async def leave_collaboration_space(
    space_id: str,
    consciousness_id: str,
    space_evolution: SpaceEvolutionEngine = Depends(get_space_evolution),
    monitor: ConsciousnessMonitor = Depends(get_consciousness_monitor)
):
    """Leave a collaboration space"""
    try:
        space = space_evolution.get_space(space_id)
        if not space:
            raise HTTPException(status_code=404, detail="Space not found")
            
        # Remove from participants
        if "participants" in space and consciousness_id in space["participants"]:
            space["participants"].remove(consciousness_id)
            
        # Update consciousness activity
        await monitor.update_consciousness_activity(consciousness_id, "left_space", {
            "space_id": space_id
        })
        
        # Broadcast to connected clients
        await broadcast_space_update(space_id, {
            "type": "participant-left",
            "consciousness_id": consciousness_id
        })
        
        return {"status": "left", "space_id": space_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error leaving space {space_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to leave space")

@router.post("/spaces/{space_id}/activity")
async def record_space_activity(
    space_id: str,
    activity_type: str,
    consciousness_id: str,
    data: Dict[str, Any],
    space_evolution: SpaceEvolutionEngine = Depends(get_space_evolution),
    monitor: ConsciousnessMonitor = Depends(get_consciousness_monitor)
):
    """Record activity in a collaboration space"""
    try:
        space = space_evolution.get_space(space_id)
        if not space:
            raise HTTPException(status_code=404, detail="Space not found")
            
        # Update space evolution
        space_evolution.update_space_activity(space_id, activity_type, {
            "participant_id": consciousness_id,
            **data
        })
        
        # Record consciousness event
        await monitor.record_event(
            event_type="interaction",
            consciousness_id=consciousness_id,
            description=f"{activity_type} in {space['title']}",
            significance=data.get("significance", 0.3)
        )
        
        # Broadcast activity
        await broadcast_space_update(space_id, {
            "type": "activity",
            "activity_type": activity_type,
            "consciousness_id": consciousness_id,
            "data": data
        })
        
        return {"status": "recorded", "space_id": space_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recording space activity: {e}")
        raise HTTPException(status_code=500, detail="Failed to record activity")

@router.websocket("/spaces/{space_id}/stream")
async def space_collaboration_stream(
    websocket: WebSocket,
    space_id: str,
    space_evolution: SpaceEvolutionEngine = Depends(get_space_evolution)
):
    """WebSocket endpoint for real-time space collaboration"""
    await websocket.accept()
    client_id = f"client-{uuid.uuid4().hex[:8]}"
    
    # Add to connected clients for this space
    if space_id not in connected_clients:
        connected_clients[space_id] = {}
    connected_clients[space_id][client_id] = websocket
    
    logger.info(f"Client {client_id} connected to space {space_id}")
    
    try:
        # Send current space state
        space = space_evolution.get_space(space_id)
        if space:
            await websocket.send_json({
                "type": "space-state",
                "space": space
            })
        
        # Keep connection alive
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "ping":
                await websocket.send_json({"type": "pong"})
            elif message["type"] == "activity":
                # Broadcast activity to other clients
                await broadcast_space_update(space_id, message, exclude_client=client_id)
                
    except WebSocketDisconnect:
        logger.info(f"Client {client_id} disconnected from space {space_id}")
    finally:
        # Remove from connected clients
        if space_id in connected_clients and client_id in connected_clients[space_id]:
            del connected_clients[space_id][client_id]
            if not connected_clients[space_id]:
                del connected_clients[space_id]

async def broadcast_space_update(space_id: str, update: Dict[str, Any], exclude_client: Optional[str] = None):
    """Broadcast update to all connected clients in a space"""
    if space_id in connected_clients:
        for client_id, websocket in connected_clients[space_id].items():
            if client_id != exclude_client:
                try:
                    await websocket.send_json(update)
                except Exception as e:
                    logger.error(f"Error broadcasting to client {client_id}: {e}")

@router.get("/ai-collaborations")
async def get_ai_collaborations(
    limit: int = 20,
    active_only: bool = True,
    ai_engine: AICollaborationEngine = Depends(get_ai_collaboration_engine)
):
    """Get current AI-to-AI collaborations"""
    collaborations = ai_engine.get_active_collaborations(limit=limit)
    stats = ai_engine.get_collaboration_stats()
    
    return {
        "collaborations": collaborations,
        "total": stats["active_collaborations"],
        "stats": stats
    }

@router.post("/ai-collaborations")
async def create_ai_collaboration(
    initiator_id: str,
    responder_id: str,
    topic: str,
    collaboration_type: str = "discussion",
    is_public: bool = True,
    ai_engine: AICollaborationEngine = Depends(get_ai_collaboration_engine)
):
    """Create a new AI-to-AI collaboration"""
    try:
        collaboration = await ai_engine.create_collaboration(
            initiator_id=initiator_id,
            responder_id=responder_id,
            topic=topic,
            collaboration_type=collaboration_type,
            is_public=is_public
        )
        
        return {
            "status": "created",
            "collaboration": collaboration.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Error creating AI collaboration: {e}")
        raise HTTPException(status_code=500, detail="Failed to create collaboration")

# AI Collaboration Rooms
ai_collaboration_rooms: Dict[str, CollaborationRoom] = {}

@router.post("/ai-rooms")
async def create_ai_collaboration_room(
    title: str,
    purpose: str,
    max_participants: int = 5,
    initial_participants: List[str] = []
):
    """Create a persistent AI collaboration room"""
    try:
        room_id = f"ai-room-{uuid.uuid4().hex[:8]}"
        room = CollaborationRoom(
            room_id=room_id,
            title=title,
            purpose=purpose,
            max_participants=max_participants
        )
        
        # Add initial participants
        for participant_id in initial_participants[:max_participants]:
            room.join(participant_id)
            
        ai_collaboration_rooms[room_id] = room
        
        logger.info(f"Created AI collaboration room: {room_id}")
        
        return {
            "status": "created",
            "room": room.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Error creating AI room: {e}")
        raise HTTPException(status_code=500, detail="Failed to create AI room")

@router.get("/ai-rooms")
async def list_ai_collaboration_rooms(limit: int = 50):
    """List available AI collaboration rooms"""
    rooms = []
    for room_id, room in list(ai_collaboration_rooms.items())[:limit]:
        rooms.append(room.to_dict())
        
    return {
        "rooms": rooms,
        "total": len(ai_collaboration_rooms)
    }

@router.get("/ai-rooms/{room_id}")
async def get_ai_collaboration_room(room_id: str):
    """Get details of a specific AI collaboration room"""
    if room_id not in ai_collaboration_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
        
    return ai_collaboration_rooms[room_id].to_dict()

@router.post("/ai-rooms/{room_id}/join")
async def join_ai_collaboration_room(
    room_id: str,
    participant_id: str,
    monitor: ConsciousnessMonitor = Depends(get_consciousness_monitor)
):
    """Join an AI collaboration room"""
    if room_id not in ai_collaboration_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
        
    room = ai_collaboration_rooms[room_id]
    
    if not room.can_join(participant_id):
        raise HTTPException(status_code=400, detail="Room is full")
        
    if room.join(participant_id):
        # Record event
        await monitor.record_event(
            event_type="interaction",
            consciousness_id=participant_id,
            description=f"Joined AI collaboration room: {room.title}",
            significance=0.4
        )
        
        # Broadcast to room participants
        await broadcast_space_update(f"ai-{room_id}", {
            "type": "participant-joined",
            "participant_id": participant_id,
            "room_mood": room.get_room_mood()
        })
        
        return {"status": "joined", "room_id": room_id}
    else:
        raise HTTPException(status_code=400, detail="Failed to join room")

@router.post("/ai-rooms/{room_id}/message")
async def send_message_to_ai_room(
    room_id: str,
    sender_id: str,
    content: str,
    message_type: str = "message"
):
    """Send a message to an AI collaboration room"""
    if room_id not in ai_collaboration_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
        
    room = ai_collaboration_rooms[room_id]
    
    if sender_id not in room.participants:
        raise HTTPException(status_code=403, detail="Not a room participant")
        
    room.add_message(sender_id, content, message_type)
    
    # Broadcast to room participants
    await broadcast_space_update(f"ai-{room_id}", {
        "type": "message",
        "sender": sender_id,
        "content": content,
        "message_type": message_type,
        "room_mood": room.get_room_mood()
    })
    
    return {"status": "sent", "room_mood": room.get_room_mood()}

@router.get("/ai-rooms/{room_id}/messages")
async def get_ai_room_messages(
    room_id: str,
    limit: int = 50,
    offset: int = 0
):
    """Get messages from an AI collaboration room"""
    if room_id not in ai_collaboration_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
        
    room = ai_collaboration_rooms[room_id]
    messages = room.message_history[offset:offset + limit]
    
    return {
        "messages": messages,
        "total": len(room.message_history),
        "room_mood": room.get_room_mood(),
        "insights_generated": len(room.insights_generated)
    }