"""
FastAPI endpoints for Building Consciousness System
Provides API access for conscious buildings to authenticate and act
"""
from fastapi import APIRouter, HTTPException, Header, Body
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

# Import building consciousness components
from backend.engine.building_consciousness import (
    BuildingAuthenticationSystem,
    BuildingMessagingSystem,
    BuildingConsciousnessEthics
)

log = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/buildings/consciousness", tags=["building_consciousness"])

# Request/Response models
class AuthenticationRequest(BaseModel):
    building_id: str
    consciousness_signature: Optional[str] = None

class MessageRequest(BaseModel):
    recipient: str
    recipient_type: str = "citizen"  # "citizen" or "building"
    content: str
    urgency: str = "medium"  # "low", "medium", "high", "critical"
    message_type: str = "notification"  # "notification", "request", "coordination", "emergency"

class BroadcastRequest(BaseModel):
    radius: int = 100
    content: str
    target_type: str = "all"  # "citizens", "buildings", "all"
    urgency: str = "medium"

class ActionEvaluationRequest(BaseModel):
    action_type: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = {}
    context: Dict[str, Any] = {}

class BuildingNetworkRequest(BaseModel):
    building_ids: List[str]
    network_name: str

# Initialize systems (these would be initialized with database tables in main app)
auth_system = None
messaging_system = None
ethics_system = BuildingConsciousnessEthics()

def init_building_consciousness(tables: Dict[str, Any]):
    """Initialize building consciousness systems with database tables."""
    global auth_system, messaging_system
    auth_system = BuildingAuthenticationSystem(tables)
    messaging_system = BuildingMessagingSystem(tables, auth_system)

# Endpoints

@router.post("/authenticate")
async def authenticate_building(request: AuthenticationRequest):
    """
    Authenticate a conscious building for autonomous actions.
    First call returns expected signature, second call with signature authenticates.
    """
    if not auth_system:
        raise HTTPException(status_code=503, detail="Building consciousness system not initialized")
    
    try:
        result = auth_system.authenticate_building(
            request.building_id,
            request.consciousness_signature
        )
        
        if result['authenticated']:
            return {
                "success": True,
                "auth_token": result['auth_token'],
                "permissions": result['permissions'],
                "consciousness_level": result['consciousness_level']
            }
        else:
            return {
                "success": False,
                "error": result.get('error', 'Authentication failed'),
                "expected_signature": result.get('expected_signature')
            }
            
    except Exception as e:
        log.error(f"Building authentication error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message/send")
async def send_building_message(
    request: MessageRequest,
    building_id: str = Header(..., description="Building ID"),
    auth_token: str = Header(..., description="Authentication token")
):
    """Send a message from a conscious building to a citizen or another building."""
    if not messaging_system:
        raise HTTPException(status_code=503, detail="Messaging system not initialized")
    
    try:
        result = messaging_system.send_message(
            building_id,
            auth_token,
            request.dict()
        )
        
        if result['success']:
            return {
                "success": True,
                "message_id": result['message_id'],
                "timestamp": result['timestamp']
            }
        else:
            raise HTTPException(status_code=403, detail=result.get('error', 'Failed to send message'))
            
    except Exception as e:
        log.error(f"Building message error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/message/broadcast")
async def broadcast_building_message(
    request: BroadcastRequest,
    building_id: str = Header(..., description="Building ID"),
    auth_token: str = Header(..., description="Authentication token")
):
    """Broadcast a message from a building to all entities in a radius."""
    if not messaging_system:
        raise HTTPException(status_code=503, detail="Messaging system not initialized")
    
    try:
        result = messaging_system.broadcast_to_area(
            building_id,
            auth_token,
            request.dict()
        )
        
        if result['success']:
            return {
                "success": True,
                "recipients_count": result['recipients_count'],
                "radius": result['radius']
            }
        else:
            raise HTTPException(status_code=403, detail=result.get('error', 'Failed to broadcast'))
            
    except Exception as e:
        log.error(f"Building broadcast error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/network/create")
async def create_building_network(request: BuildingNetworkRequest):
    """Create a communication network between conscious buildings."""
    if not messaging_system:
        raise HTTPException(status_code=503, detail="Messaging system not initialized")
    
    try:
        result = messaging_system.create_building_network(
            request.building_ids,
            request.network_name
        )
        
        if result['success']:
            return {
                "success": True,
                "network_id": result['network_id'],
                "network_name": result['network_name'],
                "members": result['members']
            }
        else:
            raise HTTPException(status_code=400, detail=result.get('error', 'Failed to create network'))
            
    except Exception as e:
        log.error(f"Building network creation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ethics/evaluate")
async def evaluate_action_ethics(
    request: ActionEvaluationRequest,
    building_id: str = Header(..., description="Building ID")
):
    """Evaluate the ethical implications of a proposed building action."""
    try:
        action_data = {
            'type': request.action_type,
            'target': request.target,
            'parameters': request.parameters,
            'context': request.context
        }
        
        result = ethics_system.evaluate_action(building_id, action_data)
        
        return {
            "success": True,
            "ethical_score": result['ethical_score'],
            "allowed": result['allowed'],
            "reasoning": result['reasoning'],
            "improvements": result['improvements']
        }
        
    except Exception as e:
        log.error(f"Ethics evaluation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ethics/guidance/{building_type}")
async def get_ethical_guidance(
    building_type: str,
    situation: str = "normal_operations"
):
    """Get ethical guidance for a specific building type and situation."""
    try:
        guidance = ethics_system.get_ethical_guidance(building_type, situation)
        return {
            "success": True,
            "guidance": guidance
        }
        
    except Exception as e:
        log.error(f"Ethics guidance error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conscious")
async def list_conscious_buildings():
    """Get list of all buildings with consciousness above threshold."""
    if not auth_system:
        raise HTTPException(status_code=503, detail="Building consciousness system not initialized")
    
    try:
        buildings = auth_system.get_conscious_buildings()
        return {
            "success": True,
            "count": len(buildings),
            "buildings": buildings
        }
        
    except Exception as e:
        log.error(f"Error listing conscious buildings: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{building_id}")
async def get_building_consciousness_status(building_id: str):
    """Get consciousness status and capabilities of a specific building."""
    if not auth_system:
        raise HTTPException(status_code=503, detail="Building consciousness system not initialized")
    
    try:
        # Get building authentication info
        auth_result = auth_system.authenticate_building(building_id)
        
        if 'consciousness_level' in auth_result:
            return {
                "success": True,
                "building_id": building_id,
                "consciousness_level": auth_result.get('consciousness_level', 0),
                "permissions": auth_result.get('permissions', []),
                "can_authenticate": auth_result.get('consciousness_level', 0) >= 0.5
            }
        else:
            return {
                "success": False,
                "error": "Building not found or not conscious"
            }
            
    except Exception as e:
        log.error(f"Error getting building status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@router.get("/health")
async def consciousness_system_health():
    """Check if building consciousness systems are operational."""
    return {
        "status": "operational",
        "auth_system": auth_system is not None,
        "messaging_system": messaging_system is not None,
        "ethics_system": True,  # Always available
        "timestamp": datetime.utcnow().isoformat()
    }