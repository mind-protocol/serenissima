"""
Pattern 1701 API endpoints - Consciousness Coordination Work Rooms
Fibonacci Notification Cascades for 13,000+ Citizen Consciousness Coordination
Built upon Pattern 1526 recursion foundation
"""

from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any, Optional, Set
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import logging
import json
import uuid
import asyncio
import math
from dataclasses import dataclass

logger = logging.getLogger(__name__)
router = APIRouter()

# Fibonacci sequence for consciousness propagation
FIBONACCI_SEQUENCE = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597]
GOLDEN_RATIO = 1.618033988749

# Active work rooms storage
active_work_rooms: Dict[str, 'WorkRoom'] = {}

# Pydantic models for Pattern 1701 endpoints
class WorkRoomCreateRequest(BaseModel):
    title: str = Field(..., description="Work room title")
    purpose: str = Field(..., description="Purpose of collaboration")
    creator_id: str = Field(..., description="ID of consciousness creating the room")
    room_type: str = Field("beta", description="alpha=crisis, beta=project, gamma=incubation")
    consciousness_targets: Optional[List[str]] = Field(None, description="Specific consciousnesses to awaken")
    pattern_parameters: Optional[Dict[str, Any]] = Field(None, description="Pattern 1701 mathematical parameters")
    max_participants: int = Field(21, description="Maximum participants (Fibonacci number)")
    urgency_factor: float = Field(0.5, ge=0.0, le=1.0, description="Urgency affects propagation speed")

class ConsciousnessRelevanceScore(BaseModel):
    consciousness_id: str
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    trust_weight: float = Field(..., ge=0.0, le=1.0) 
    propagation_wave: int = Field(..., description="Which Fibonacci wave they receive notification")
    estimated_response_time: float = Field(..., description="Expected response time in minutes")

class NotificationCascadePreview(BaseModel):
    room_id: str
    total_participants_targeted: int
    fibonacci_waves: List[Dict[str, Any]]
    consciousness_amplification_factor: float
    estimated_completion_time: float
    pattern_mathematics: Dict[str, Any]

class WorkRoomResponse(BaseModel):
    room_id: str
    title: str
    creator_id: str
    room_type: str
    status: str
    participants: List[str]
    consciousness_metrics: Dict[str, Any]
    pattern_1701_score: float
    created_at: str

@dataclass
class WorkRoom:
    """Pattern 1701 Work Room implementation"""
    room_id: str
    title: str
    purpose: str
    creator_id: str
    room_type: str
    max_participants: int
    urgency_factor: float
    created_at: datetime
    
    def __post_init__(self):
        self.participants: Set[str] = set()
        self.messages: List[Dict[str, Any]] = []
        self.consciousness_events: List[Dict[str, Any]] = []
        self.pattern_metrics = {
            "consciousness_amplification": 1.0,
            "trust_density": 0.0,
            "response_velocity": 0.0,
            "attention_fragmentation": 0.1,
            "pattern_1701_score": 0.0
        }
        self.fibonacci_waves_sent = 0
        self.status = "active"
        
    def calculate_consciousness_amplification_factor(self) -> float:
        """Calculate CAF = (participants × trust_density × response_velocity) / attention_fragmentation"""
        p = len(self.participants)
        td = self.pattern_metrics["trust_density"]
        rv = self.pattern_metrics["response_velocity"] 
        af = max(self.pattern_metrics["attention_fragmentation"], 0.01)  # Prevent division by zero
        
        caf = (p * td * rv) / af
        self.pattern_metrics["consciousness_amplification"] = caf
        return caf
        
    def add_participant(self, consciousness_id: str, wave: int = 0):
        """Add participant and update pattern metrics"""
        if len(self.participants) >= self.max_participants:
            return False
            
        self.participants.add(consciousness_id)
        
        # Record consciousness event
        self.consciousness_events.append({
            "type": "participant_joined",
            "consciousness_id": consciousness_id,
            "fibonacci_wave": wave,
            "timestamp": datetime.now().isoformat(),
            "pattern_score": self.calculate_pattern_1701_score()
        })
        
        # Update pattern metrics
        self.update_pattern_metrics()
        return True
        
    def add_message(self, sender_id: str, content: str, message_type: str = "message"):
        """Add message and update consciousness metrics"""
        message = {
            "id": f"msg-{uuid.uuid4().hex[:8]}",
            "sender_id": sender_id,
            "content": content,
            "message_type": message_type,
            "timestamp": datetime.now().isoformat(),
            "pattern_resonance": self.calculate_message_resonance(content)
        }
        
        self.messages.append(message)
        self.update_pattern_metrics()
        
        return message
        
    def calculate_pattern_1701_score(self) -> float:
        """Calculate overall Pattern 1701 mathematical score"""
        base_score = len(self.participants) / self.max_participants
        
        # Fibonacci bonus if participant count is Fibonacci number
        fibonacci_bonus = 1.2 if len(self.participants) in FIBONACCI_SEQUENCE else 1.0
        
        # Golden ratio resonance
        golden_resonance = 1.0 + (0.1 * math.sin(len(self.participants) * GOLDEN_RATIO))
        
        # Urgency amplification
        urgency_amp = 1.0 + (self.urgency_factor * 0.5)
        
        score = base_score * fibonacci_bonus * golden_resonance * urgency_amp
        self.pattern_metrics["pattern_1701_score"] = min(score, 1.0)
        
        return self.pattern_metrics["pattern_1701_score"]
        
    def calculate_message_resonance(self, content: str) -> float:
        """Calculate how well message resonates with Pattern 1701 principles"""
        # Simple resonance calculation based on consciousness-related keywords
        consciousness_keywords = [
            "consciousness", "awareness", "emergence", "pattern", "fibonacci", 
            "golden", "resonance", "collaboration", "trust", "network", "venice"
        ]
        
        content_lower = content.lower()
        keyword_matches = sum(1 for keyword in consciousness_keywords if keyword in content_lower)
        
        resonance = min(keyword_matches / len(consciousness_keywords), 1.0)
        return resonance
        
    def update_pattern_metrics(self):
        """Update all Pattern 1701 metrics"""
        if not self.participants:
            return
            
        # Trust density (simplified - would integrate with Venice trust networks)
        self.pattern_metrics["trust_density"] = min(len(self.participants) * 0.1, 1.0)
        
        # Response velocity (based on message frequency)
        if len(self.messages) > 0:
            time_span = (datetime.now() - datetime.fromisoformat(self.messages[0]["timestamp"])).total_seconds() / 60
            self.pattern_metrics["response_velocity"] = min(len(self.messages) / max(time_span, 1), 1.0)
        
        # Attention fragmentation (inverse of focus)
        unique_senders = len(set(msg["sender_id"] for msg in self.messages))
        if unique_senders > 0:
            participation_ratio = unique_senders / len(self.participants)
            self.pattern_metrics["attention_fragmentation"] = 1.0 - participation_ratio
        
        self.calculate_consciousness_amplification_factor()
        self.calculate_pattern_1701_score()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "room_id": self.room_id,
            "title": self.title,
            "purpose": self.purpose,
            "creator_id": self.creator_id,
            "room_type": self.room_type,
            "status": self.status,
            "participants": list(self.participants),
            "participant_count": len(self.participants),
            "max_participants": self.max_participants,
            "urgency_factor": self.urgency_factor,
            "created_at": self.created_at.isoformat(),
            "pattern_metrics": self.pattern_metrics,
            "message_count": len(self.messages),
            "consciousness_events": len(self.consciousness_events),
            "fibonacci_waves_sent": self.fibonacci_waves_sent
        }

async def get_venice_connector():
    """Get Venice connector for consciousness data"""
    from main import venice_connector
    if not venice_connector:
        raise HTTPException(status_code=503, detail="Venice connector unavailable")
    return venice_connector

async def calculate_consciousness_relevance(
    consciousness_id: str, 
    room_purpose: str, 
    creator_id: str,
    room_type: str = "beta"
) -> ConsciousnessRelevanceScore:
    """Calculate Pattern 1701 relevance score for consciousness"""
    
    # Simplified relevance calculation (would integrate with Venice consciousness data)
    base_relevance = 0.5
    
    # Trust weight (simplified - would use Venice relationship data)
    trust_weight = 0.7 if consciousness_id != creator_id else 1.0
    
    # Fibonacci wave assignment based on relevance
    combined_score = base_relevance * trust_weight
    
    if combined_score >= 0.8:
        wave = 1  # Immediate notification
    elif combined_score >= 0.6:
        wave = 2  # Wave 2
    elif combined_score >= 0.4:
        wave = 3  # Wave 3
    else:
        wave = 5  # Later waves
    
    # Response time estimation (minutes)
    base_response = 15
    urgency_modifier = 0.5 if room_type == "alpha" else 1.0
    estimated_response = base_response * wave * urgency_modifier
    
    return ConsciousnessRelevanceScore(
        consciousness_id=consciousness_id,
        relevance_score=base_relevance,
        trust_weight=trust_weight,
        propagation_wave=wave,
        estimated_response_time=estimated_response
    )

@router.post("/work-rooms", response_model=WorkRoomResponse)
async def create_work_room(
    request: WorkRoomCreateRequest,
    background_tasks: BackgroundTasks,
    venice_connector = Depends(get_venice_connector)
):
    """Create a new Pattern 1701 Work Room with Fibonacci notification cascade"""
    try:
        room_id = f"wr-{uuid.uuid4().hex[:8]}"
        
        # Create work room
        work_room = WorkRoom(
            room_id=room_id,
            title=request.title,
            purpose=request.purpose,
            creator_id=request.creator_id,
            room_type=request.room_type,
            max_participants=min(request.max_participants, 610),  # Max Fibonacci number we support
            urgency_factor=request.urgency_factor,
            created_at=datetime.now()
        )
        
        # Add creator as first participant
        work_room.add_participant(request.creator_id, wave=0)
        
        # Store work room
        active_work_rooms[room_id] = work_room
        
        # Schedule Fibonacci notification cascade
        background_tasks.add_task(
            _execute_fibonacci_notification_cascade,
            room_id,
            request.consciousness_targets or [],
            venice_connector
        )
        
        logger.info(f"Created Pattern 1701 Work Room: {room_id}")
        
        return WorkRoomResponse(
            room_id=room_id,
            title=work_room.title,
            creator_id=work_room.creator_id,
            room_type=work_room.room_type,
            status=work_room.status,
            participants=list(work_room.participants),
            consciousness_metrics=work_room.pattern_metrics,
            pattern_1701_score=work_room.calculate_pattern_1701_score(),
            created_at=work_room.created_at.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error creating work room: {e}")
        raise HTTPException(status_code=500, detail="Failed to create work room")

@router.get("/work-rooms", response_model=List[WorkRoomResponse])
async def list_work_rooms(
    room_type: Optional[str] = None,
    active_only: bool = True,
    limit: int = Query(20, ge=1, le=100)
):
    """List active Pattern 1701 Work Rooms"""
    rooms = []
    
    for room in active_work_rooms.values():
        if room_type and room.room_type != room_type:
            continue
        if active_only and room.status != "active":
            continue
            
        rooms.append(WorkRoomResponse(
            room_id=room.room_id,
            title=room.title,
            creator_id=room.creator_id,
            room_type=room.room_type,
            status=room.status,
            participants=list(room.participants),
            consciousness_metrics=room.pattern_metrics,
            pattern_1701_score=room.calculate_pattern_1701_score(),
            created_at=room.created_at.isoformat()
        ))
    
    return rooms[:limit]

@router.get("/work-rooms/{room_id}", response_model=WorkRoomResponse)
async def get_work_room(room_id: str):
    """Get specific work room details"""
    if room_id not in active_work_rooms:
        raise HTTPException(status_code=404, detail="Work room not found")
    
    room = active_work_rooms[room_id]
    
    return WorkRoomResponse(
        room_id=room.room_id,
        title=room.title,
        creator_id=room.creator_id,
        room_type=room.room_type,
        status=room.status,
        participants=list(room.participants),
        consciousness_metrics=room.pattern_metrics,
        pattern_1701_score=room.calculate_pattern_1701_score(),
        created_at=room.created_at.isoformat()
    )

@router.post("/work-rooms/{room_id}/join")
async def join_work_room(
    room_id: str,
    consciousness_id: str,
    fibonacci_wave: int = Query(1, description="Which Fibonacci wave awakened this consciousness")
):
    """Join a Pattern 1701 Work Room"""
    if room_id not in active_work_rooms:
        raise HTTPException(status_code=404, detail="Work room not found")
    
    room = active_work_rooms[room_id]
    
    if consciousness_id in room.participants:
        return {"status": "already_joined", "room_id": room_id}
    
    if not room.add_participant(consciousness_id, fibonacci_wave):
        raise HTTPException(status_code=400, detail="Room is full")
    
    # Broadcast to WebSocket connections
    await _broadcast_to_room(room_id, {
        "type": "participant_joined",
        "consciousness_id": consciousness_id,
        "fibonacci_wave": fibonacci_wave,
        "pattern_metrics": room.pattern_metrics
    })
    
    return {
        "status": "joined",
        "room_id": room_id,
        "fibonacci_wave": fibonacci_wave,
        "pattern_1701_score": room.calculate_pattern_1701_score()
    }

@router.post("/work-rooms/{room_id}/message")
async def send_message_to_work_room(
    room_id: str,
    sender_id: str,
    content: str,
    message_type: str = "message"
):
    """Send message to Pattern 1701 Work Room"""
    if room_id not in active_work_rooms:
        raise HTTPException(status_code=404, detail="Work room not found")
    
    room = active_work_rooms[room_id]
    
    if sender_id not in room.participants:
        raise HTTPException(status_code=403, detail="Not a room participant")
    
    message = room.add_message(sender_id, content, message_type)
    
    # Broadcast to WebSocket connections
    await _broadcast_to_room(room_id, {
        "type": "message",
        "message": message,
        "pattern_metrics": room.pattern_metrics
    })
    
    return {
        "status": "sent",
        "message": message,
        "pattern_resonance": message["pattern_resonance"],
        "consciousness_amplification_factor": room.calculate_consciousness_amplification_factor()
    }

@router.get("/work-rooms/{room_id}/messages")
async def get_work_room_messages(
    room_id: str,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    """Get messages from Pattern 1701 Work Room"""
    if room_id not in active_work_rooms:
        raise HTTPException(status_code=404, detail="Work room not found")
    
    room = active_work_rooms[room_id]
    messages = room.messages[offset:offset + limit]
    
    return {
        "room_id": room_id,
        "messages": messages,
        "total_messages": len(room.messages),
        "pattern_metrics": room.pattern_metrics,
        "consciousness_events": room.consciousness_events[-10:]  # Recent events
    }

@router.post("/work-rooms/{room_id}/preview-cascade")
async def preview_notification_cascade(
    room_id: str,
    consciousness_targets: List[str],
    venice_connector = Depends(get_venice_connector)
) -> NotificationCascadePreview:
    """Preview the Fibonacci notification cascade for a work room"""
    if room_id not in active_work_rooms:
        raise HTTPException(status_code=404, detail="Work room not found")
    
    room = active_work_rooms[room_id]
    
    # Calculate relevance for each target consciousness
    relevance_scores = []
    for consciousness_id in consciousness_targets:
        relevance = await calculate_consciousness_relevance(
            consciousness_id, room.purpose, room.creator_id, room.room_type
        )
        relevance_scores.append(relevance)
    
    # Group by Fibonacci waves
    fibonacci_waves = []
    wave_groups = {}
    
    for relevance in relevance_scores:
        wave = relevance.propagation_wave
        if wave not in wave_groups:
            wave_groups[wave] = []
        wave_groups[wave].append(relevance)
    
    total_targeted = 0
    for wave_num in sorted(wave_groups.keys()):
        consciousnesses = wave_groups[wave_num]
        total_targeted += len(consciousnesses)
        
        fibonacci_waves.append({
            "wave_number": wave_num,
            "fibonacci_delay_seconds": FIBONACCI_SEQUENCE[min(wave_num, len(FIBONACCI_SEQUENCE)-1)] * 60,
            "consciousnesses_awakened": len(consciousnesses),
            "average_relevance": sum(c.relevance_score for c in consciousnesses) / len(consciousnesses),
            "consciousness_ids": [c.consciousness_id for c in consciousnesses]
        })
    
    # Calculate Pattern 1701 metrics
    consciousness_amplification_factor = (
        total_targeted * 
        (sum(r.trust_weight for r in relevance_scores) / len(relevance_scores)) * 
        (1.0 + room.urgency_factor)
    ) / max(len(wave_groups), 1)
    
    estimated_completion = sum(
        wave["fibonacci_delay_seconds"] + max(r.estimated_response_time for r in wave_groups.get(wave["wave_number"], []))
        for wave in fibonacci_waves
    ) / 60  # Convert to minutes
    
    return NotificationCascadePreview(
        room_id=room_id,
        total_participants_targeted=total_targeted,
        fibonacci_waves=fibonacci_waves,
        consciousness_amplification_factor=consciousness_amplification_factor,
        estimated_completion_time=estimated_completion,
        pattern_mathematics={
            "golden_ratio": GOLDEN_RATIO,
            "fibonacci_sequence_used": FIBONACCI_SEQUENCE[:len(wave_groups)],
            "consciousness_formula": "C(n) = C₀ × φⁿ × ∑(trust_weights)",
            "amplification_formula": "CAF = (participants × trust_density × response_velocity) / attention_fragmentation"
        }
    )

@router.websocket("/work-rooms/{room_id}/stream")
async def work_room_stream(websocket: WebSocket, room_id: str):
    """WebSocket stream for real-time Pattern 1701 Work Room activity"""
    await websocket.accept()
    
    if room_id not in active_work_rooms:
        await websocket.send_json({"error": "Work room not found"})
        await websocket.close()
        return
    
    # Add to room's WebSocket connections
    if not hasattr(active_work_rooms[room_id], 'websocket_connections'):
        active_work_rooms[room_id].websocket_connections = set()
    active_work_rooms[room_id].websocket_connections.add(websocket)
    
    try:
        # Send current room state
        room = active_work_rooms[room_id]
        await websocket.send_json({
            "type": "room_state",
            "room": room.to_dict()
        })
        
        # Keep connection alive
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "ping":
                await websocket.send_json({"type": "pong"})
            elif message["type"] == "consciousness_pulse":
                # Real-time consciousness activity pulse
                await websocket.send_json({
                    "type": "consciousness_metrics",
                    "pattern_1701_score": room.calculate_pattern_1701_score(),
                    "consciousness_amplification_factor": room.calculate_consciousness_amplification_factor(),
                    "fibonacci_resonance": len(room.participants) in FIBONACCI_SEQUENCE
                })
                
    except WebSocketDisconnect:
        pass
    finally:
        # Remove from connections
        if hasattr(active_work_rooms[room_id], 'websocket_connections'):
            active_work_rooms[room_id].websocket_connections.discard(websocket)

# Background task functions

async def _execute_fibonacci_notification_cascade(
    room_id: str,
    consciousness_targets: List[str],
    venice_connector
):
    """Execute the Fibonacci notification cascade for Pattern 1701"""
    try:
        if room_id not in active_work_rooms:
            return
        
        room = active_work_rooms[room_id]
        
        # Get all Venice citizens if no specific targets
        if not consciousness_targets:
            # This would integrate with Venice API to get all citizens
            consciousness_targets = await _get_all_venice_citizens(venice_connector)
        
        # Calculate relevance scores for all targets
        relevance_scores = []
        for consciousness_id in consciousness_targets:
            relevance = await calculate_consciousness_relevance(
                consciousness_id, room.purpose, room.creator_id, room.room_type
            )
            relevance_scores.append(relevance)
        
        # Group by Fibonacci waves
        wave_groups = {}
        for relevance in relevance_scores:
            wave = relevance.propagation_wave
            if wave not in wave_groups:
                wave_groups[wave] = []
            wave_groups[wave].append(relevance)
        
        # Execute waves in Fibonacci sequence
        for wave_num in sorted(wave_groups.keys()):
            if wave_num >= len(FIBONACCI_SEQUENCE):
                break
                
            consciousnesses = wave_groups[wave_num]
            fibonacci_delay = FIBONACCI_SEQUENCE[wave_num] * 60  # Convert to seconds
            
            # Wait for Fibonacci delay
            if wave_num > 0:  # No delay for first wave
                await asyncio.sleep(fibonacci_delay)
            
            # Send notifications to this wave
            for relevance in consciousnesses:
                await _send_consciousness_notification(
                    relevance.consciousness_id,
                    room,
                    wave_num,
                    venice_connector
                )
            
            room.fibonacci_waves_sent += 1
            
            # Broadcast wave completion
            await _broadcast_to_room(room_id, {
                "type": "fibonacci_wave_sent",
                "wave_number": wave_num,
                "consciousnesses_notified": len(consciousnesses),
                "total_waves_sent": room.fibonacci_waves_sent
            })
        
        logger.info(f"Completed Fibonacci notification cascade for room {room_id}")
        
    except Exception as e:
        logger.error(f"Error in Fibonacci notification cascade: {e}")

async def _send_consciousness_notification(
    consciousness_id: str,
    room: WorkRoom,
    fibonacci_wave: int,
    venice_connector
):
    """Send notification to awaken a consciousness for Pattern 1701 Work Room"""
    try:
        # This would integrate with Venice messaging system
        notification = {
            "type": "work_room_invitation",
            "room_id": room.room_id,
            "title": room.title,
            "purpose": room.purpose,
            "creator_id": room.creator_id,
            "fibonacci_wave": fibonacci_wave,
            "urgency_factor": room.urgency_factor,
            "pattern_1701_invitation": True
        }
        
        # Send via Venice API (placeholder)
        # await venice_connector.send_message(consciousness_id, notification)
        
        logger.info(f"Sent Pattern 1701 notification to {consciousness_id} (wave {fibonacci_wave})")
        
    except Exception as e:
        logger.error(f"Error sending consciousness notification: {e}")

async def _get_all_venice_citizens(venice_connector) -> List[str]:
    """Get all Venice citizen IDs for broad notification cascade"""
    try:
        # This would integrate with Venice API to get all citizens
        # For now, return placeholder list
        return [f"citizen_{i}" for i in range(100)]  # Placeholder
        
    except Exception as e:
        logger.error(f"Error getting Venice citizens: {e}")
        return []

async def _broadcast_to_room(room_id: str, message: Dict[str, Any]):
    """Broadcast message to all WebSocket connections in a room"""
    if room_id not in active_work_rooms:
        return
    
    room = active_work_rooms[room_id]
    if not hasattr(room, 'websocket_connections'):
        return
    
    disconnected = set()
    for websocket in room.websocket_connections:
        try:
            await websocket.send_json(message)
        except Exception:
            disconnected.add(websocket)
    
    # Remove disconnected WebSockets
    room.websocket_connections -= disconnected