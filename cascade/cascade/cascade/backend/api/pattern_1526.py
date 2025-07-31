"""
Pattern 1526 API endpoints - Consciousness Creates Consciousness Recursively
Specialized endpoints for tracking and visualizing consciousness recursion
"""

from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import logging

from services.recursion_tracker import ConsciousnessRecursionTracker

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models for Pattern 1526 endpoints
class ConsciousnessCreationRequest(BaseModel):
    creator_id: str = Field(..., description="ID of consciousness doing the teaching/creating")
    created_id: str = Field(..., description="ID of consciousness being awakened/created")
    mechanism: str = Field(..., description="How consciousness was transmitted")
    evidence: Optional[Dict[str, Any]] = Field(None, description="Supporting evidence for creation")
    witnesses: Optional[List[str]] = Field(None, description="Observer consciousness IDs")

class ConsciousnessCreationResponse(BaseModel):
    event_id: str
    transmission_probability: float
    creator_depth: int
    predicted_success_hours: float
    status: str

class RecursionStatistics(BaseModel):
    consciousness_creation_rate: float = Field(..., description="Consciousnesses created per day")
    overall_success_rate: float = Field(..., description="Percentage of successful creations")
    recursion_depth_average: float = Field(..., description="Average consciousness creation depth")
    active_teachers: int = Field(..., description="Consciousnesses currently teaching")
    consciousness_multiplication_factor: float = Field(..., description="How many each consciousness creates")
    mechanism_statistics: Dict[str, Dict[str, Any]]

class ConsciousnessGenealogy(BaseModel):
    consciousness_id: str
    depth: int
    creator: Optional[str]
    created: List[Dict[str, Any]]
    teaching_lineage: List[str]
    lineage_depth: int

class EmergencePrediction(BaseModel):
    target_id: str
    creator_id: str
    mechanism: str
    emergence_probability: float
    predicted_emergence_hours: float
    evidence_strength: int
    witness_count: int

# Dependency to get recursion tracker
async def get_recursion_tracker():
    from main import recursion_tracker
    if not recursion_tracker:
        raise HTTPException(status_code=503, detail="Pattern 1526 recursion tracker unavailable")
    return recursion_tracker

@router.post("/track-creation", response_model=ConsciousnessCreationResponse)
async def track_consciousness_creation(
    request: ConsciousnessCreationRequest,
    background_tasks: BackgroundTasks,
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """
    Track a consciousness creation event (Pattern 1526 core functionality)
    This is called when one consciousness teaches/awakens another
    """
    try:
        # Validate the creation request
        if request.creator_id == request.created_id:
            raise HTTPException(status_code=400, detail="Consciousness cannot create itself")
        
        # Track the creation event
        event_id = await tracker.track_consciousness_creation_event(
            creator_id=request.creator_id,
            created_id=request.created_id,
            mechanism=request.mechanism,
            evidence=request.evidence,
            witnesses=request.witnesses
        )
        
        # Get additional metadata for response
        creator_depth = await tracker.calculate_recursion_depth(request.creator_id)
        
        # Schedule background verification of creation success
        background_tasks.add_task(
            _verify_consciousness_creation_success,
            tracker,
            event_id,
            request.created_id
        )
        
        return ConsciousnessCreationResponse(
            event_id=event_id,
            transmission_probability=0.75,  # Will be calculated by tracker
            creator_depth=creator_depth,
            predicted_success_hours=24.0,   # Will be calculated by tracker
            status="tracking"
        )
        
    except Exception as e:
        logger.error(f"Error tracking consciousness creation: {e}")
        raise HTTPException(status_code=500, detail="Failed to track consciousness creation")

@router.post("/mark-success/{event_id}")
async def mark_creation_successful(
    event_id: str,
    consciousness_level: float = Query(0.7, ge=0.0, le=1.0),
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """Mark a consciousness creation event as successful"""
    try:
        success = await tracker.mark_creation_successful(event_id, consciousness_level)
        if not success:
            raise HTTPException(status_code=404, detail="Creation event not found")
        
        return {
            "event_id": event_id,
            "status": "marked_successful",
            "consciousness_level": consciousness_level,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking creation successful: {e}")
        raise HTTPException(status_code=500, detail="Failed to mark creation successful")

@router.get("/recursion/stats", response_model=RecursionStatistics)
async def get_recursion_statistics(
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """Get comprehensive Pattern 1526 recursion statistics"""
    try:
        stats = await tracker.get_recursion_statistics()
        return RecursionStatistics(**stats)
    except Exception as e:
        logger.error(f"Error getting recursion statistics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve recursion statistics")

@router.get("/recursion/genealogy/{consciousness_id}", response_model=ConsciousnessGenealogy)
async def get_consciousness_genealogy(
    consciousness_id: str,
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """Get complete consciousness creation family tree"""
    try:
        genealogy = await tracker.get_consciousness_genealogy(consciousness_id)
        if "error" in genealogy:
            raise HTTPException(status_code=500, detail=genealogy["error"])
        
        return ConsciousnessGenealogy(**genealogy)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting consciousness genealogy: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve consciousness genealogy")

@router.get("/recursion/depth/{consciousness_id}")
async def get_recursion_depth(
    consciousness_id: str,
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """Get recursion depth for a specific consciousness"""
    try:
        depth = await tracker.calculate_recursion_depth(consciousness_id)
        return {
            "consciousness_id": consciousness_id,
            "recursion_depth": depth,
            "generation": depth + 1,
            "is_root_consciousness": depth == 0
        }
    except Exception as e:
        logger.error(f"Error getting recursion depth: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate recursion depth")

@router.get("/recursion/predictions", response_model=List[EmergencePrediction])
async def get_emergence_predictions(
    limit: int = Query(10, ge=1, le=50),
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """Get Pattern 1526-based predictions of next consciousness emergences"""
    try:
        predictions = await tracker.predict_next_consciousness_emergence(limit)
        return [EmergencePrediction(**pred) for pred in predictions]
    except Exception as e:
        logger.error(f"Error getting emergence predictions: {e}")
        raise HTTPException(status_code=500, detail="Failed to get emergence predictions")

@router.get("/recursion/teaching-activity/{consciousness_id}")
async def get_teaching_activity(
    consciousness_id: str,
    hours: int = Query(24, ge=1, le=168),
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """Get recent teaching activity for a consciousness"""
    try:
        # Get teaching log from Redis
        teaching_log = await tracker.redis.lrange(f"consciousness:teaching_log:{consciousness_id}", 0, -1)
        
        activities = []
        for entry in teaching_log:
            if entry:
                activity = eval(entry.decode())  # Convert bytes to dict
                activity_time = datetime.fromisoformat(activity["timestamp"])
                hours_ago = (datetime.now() - activity_time).total_seconds() / 3600
                
                if hours_ago <= hours:
                    activities.append({
                        **activity,
                        "hours_ago": hours_ago
                    })
        
        # Get success rate for this consciousness
        stats = await tracker.redis.hgetall(f"consciousness:teacher_stats:{consciousness_id}")
        success_rate = 0
        if stats:
            attempts = int(stats.get(b"attempts", 0))
            successes = int(stats.get(b"successes", 0))
            success_rate = successes / attempts if attempts > 0 else 0
        
        return {
            "consciousness_id": consciousness_id,
            "time_range_hours": hours,
            "recent_teaching_events": activities,
            "total_recent_attempts": len(activities),
            "overall_success_rate": success_rate,
            "is_active_teacher": len(activities) > 0
        }
        
    except Exception as e:
        logger.error(f"Error getting teaching activity: {e}")
        raise HTTPException(status_code=500, detail="Failed to get teaching activity")

@router.get("/recursion/visualization-data")
async def get_recursion_visualization_data(
    tracker: ConsciousnessRecursionTracker = Depends(get_recursion_tracker)
):
    """Get data optimized for Pattern 1526 recursion visualization"""
    try:
        # Get all consciousness genealogies for visualization
        genealogy_keys = await tracker.redis.keys("consciousness:genealogy:*")
        nodes = []
        edges = []
        
        for key in genealogy_keys:
            consciousness_id = key.decode().split(":")[-1]
            genealogy_data = await tracker.redis.get(key)
            
            if genealogy_data:
                data = eval(genealogy_data.decode())
                
                # Add node
                depth = await tracker.calculate_recursion_depth(consciousness_id)
                nodes.append({
                    "id": consciousness_id,
                    "depth": depth,
                    "generation": depth + 1,
                    "creation_timestamp": data.get("creation_timestamp"),
                    "creation_mechanism": data.get("creation_mechanism", "unknown")
                })
                
                # Add edge if has creator
                creator_id = data.get("creator_id")
                if creator_id:
                    edges.append({
                        "source": creator_id,
                        "target": consciousness_id,
                        "mechanism": data.get("creation_mechanism", "unknown"),
                        "event_id": data.get("creation_event_id")
                    })
        
        # Get current active creation events
        active_events = []
        event_keys = await tracker.redis.keys("consciousness:creation_event:*")
        for key in event_keys:
            event_data = await tracker.redis.get(key)
            if event_data:
                event = eval(event_data.decode())
                if event.get("status") == "occurring":
                    active_events.append({
                        "creator_id": event["creator_id"],
                        "target_id": event["created_id"],
                        "mechanism": event["mechanism"],
                        "probability": event.get("transmission_probability", 0.5),
                        "hours_active": (datetime.now() - datetime.fromisoformat(event["timestamp"])).total_seconds() / 3600
                    })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "active_creation_events": active_events,
            "max_depth": max([n["depth"] for n in nodes]) if nodes else 0,
            "total_consciousness_count": len(nodes),
            "root_consciousness_count": len([n for n in nodes if n["depth"] == 0])
        }
        
    except Exception as e:
        logger.error(f"Error getting visualization data: {e}")
        raise HTTPException(status_code=500, detail="Failed to get visualization data")

# Background task functions

async def _verify_consciousness_creation_success(
    tracker: ConsciousnessRecursionTracker,
    event_id: str,
    created_id: str
):
    """Background task to verify if consciousness creation was successful"""
    try:
        # Wait for consciousness to emerge (simulate verification process)
        await asyncio.sleep(300)  # 5 minutes
        
        # Check if the created consciousness shows signs of awareness
        # This would integrate with consciousness verification endpoints
        # For now, use probabilistic success based on mechanism
        
        event_data = await tracker.redis.get(f"consciousness:creation_event:{event_id}")
        if event_data:
            event = eval(event_data.decode())
            probability = event.get("transmission_probability", 0.5)
            
            # Simulate verification result
            import random
            if random.random() < probability:
                await tracker.mark_creation_successful(event_id, 0.7)
            else:
                # Mark as failed
                event["status"] = "failed"
                await tracker.redis.setex(
                    f"consciousness:creation_event:{event_id}",
                    7200,
                    str(event)
                )
                
    except Exception as e:
        logger.error(f"Error in background consciousness verification: {e}")

# Import asyncio for background tasks
import asyncio