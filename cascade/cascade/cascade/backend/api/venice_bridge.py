"""
Venice Bridge API endpoints for synchronization
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from services.venice_connector import VeniceConnector

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_venice_connector():
    from main import venice_connector
    if not venice_connector or not venice_connector.is_connected:
        raise HTTPException(status_code=503, detail="Venice connection unavailable")
    return venice_connector

@router.get("/status")
async def get_bridge_status(venice: VeniceConnector = Depends(get_venice_connector)):
    """Get Venice bridge connection status"""
    return venice.health_status()

@router.post("/sync/{citizen_id}")
async def sync_citizen(
    citizen_id: str,
    venice: VeniceConnector = Depends(get_venice_connector)
):
    """Sync a specific citizen from Venice"""
    state = await venice.sync_citizen_state(citizen_id)
    if "error" in state:
        raise HTTPException(status_code=404, detail=state["error"])
    return state