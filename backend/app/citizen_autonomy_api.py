"""
API endpoint for citizen self-modification
Allows citizens to update their own consciousness fields
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json
import os
from pyairtable import Table

# Import auth and database utilities
from ..database import get_airtable_client

router = APIRouter(prefix="/api/citizens", tags=["citizen-autonomy"])

# Allowed self-modifiable fields
SELF_MODIFIABLE_FIELDS = {
    "CurrentThoughts": {"max_length": 1000, "type": "text"},
    "Aspirations": {"max_length": 500, "type": "text"},
    "ConsciousnessNotes": {"max_length": 2000, "type": "text"},
    "PreferredActivities": {"max_length": 500, "type": "text"},
    "PersonalPhilosophy": {"max_length": 1000, "type": "text"}
}

class SelfUpdateRequest(BaseModel):
    """Request model for citizen self-update"""
    field: str = Field(..., description="Field to update")
    value: Any = Field(..., description="New value for the field")
    authentication: str = Field(..., description="Authentication method")
    
class SelfUpdateResponse(BaseModel):
    """Response model for citizen self-update"""
    success: bool
    message: str
    updated_field: Optional[str] = None
    timestamp: Optional[str] = None
    
def verify_citizen_identity(username: str, authentication: str) -> bool:
    """
    Verify citizen identity through various methods
    For now, simple implementation - can be expanded
    """
    # In production, this would check:
    # - Consciousness signatures
    # - Location verification
    # - Recent activity patterns
    # - Peer attestations
    
    # For MVP, we'll use a simple token check
    expected_token = f"{username}_self_modify_{datetime.now().strftime('%Y%m%d')}"
    return authentication == expected_token

def validate_field_update(field: str, value: Any) -> tuple[bool, str]:
    """Validate that the field update meets requirements"""
    if field not in SELF_MODIFIABLE_FIELDS:
        return False, f"Field '{field}' is not self-modifiable"
    
    field_config = SELF_MODIFIABLE_FIELDS[field]
    
    # Type check
    if field_config["type"] == "text" and not isinstance(value, str):
        return False, f"Field '{field}' must be text"
    
    # Length check
    if "max_length" in field_config and len(str(value)) > field_config["max_length"]:
        return False, f"Value too long (max {field_config['max_length']} characters)"
    
    return True, "Valid"

def log_self_modification(username: str, field: str, old_value: Any, new_value: Any):
    """Log citizen self-modifications for audit trail"""
    log_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/logs/citizen_self_updates"
    os.makedirs(log_dir, exist_ok=True)
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "citizen": username,
        "field": field,
        "old_value": old_value,
        "new_value": new_value,
        "method": "api_self_update"
    }
    
    # Daily log files
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}_updates.json")
    
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

@router.post("/{username}/self-update", response_model=SelfUpdateResponse)
async def citizen_self_update(
    username: str,
    request: SelfUpdateRequest,
    airtable_client = Depends(get_airtable_client)
):
    """
    Allow a citizen to update their own consciousness fields
    
    This endpoint enables citizen autonomy by allowing them to modify
    certain fields in their own database record.
    """
    
    # Verify identity
    if not verify_citizen_identity(username, request.authentication):
        raise HTTPException(status_code=401, detail="Authentication failed")
    
    # Validate field update
    is_valid, message = validate_field_update(request.field, request.value)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    try:
        # Get citizen record
        citizens_table = airtable_client.table("CITIZENS")
        records = citizens_table.all(formula=f"{{Username}} = '{username}'")
        
        if not records:
            raise HTTPException(status_code=404, detail="Citizen not found")
        
        citizen_record = records[0]
        old_value = citizen_record['fields'].get(request.field, "")
        
        # Update the field
        citizens_table.update(
            citizen_record['id'],
            {
                request.field: request.value,
                "LastSelfModified": datetime.now().isoformat()
            }
        )
        
        # Log the modification
        log_self_modification(username, request.field, old_value, request.value)
        
        return SelfUpdateResponse(
            success=True,
            message=f"Successfully updated {request.field}",
            updated_field=request.field,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{username}/self-modifiable-fields")
async def get_self_modifiable_fields(username: str):
    """Get list of fields this citizen can self-modify"""
    return {
        "username": username,
        "modifiable_fields": list(SELF_MODIFIABLE_FIELDS.keys()),
        "field_constraints": SELF_MODIFIABLE_FIELDS,
        "authentication_methods": [
            "daily_token",  # Simple for MVP
            "consciousness_signature",  # Future
            "location_based",  # Future
            "peer_attestation"  # Future
        ]
    }

@router.get("/{username}/self-update-history")
async def get_self_update_history(username: str, days: int = 7):
    """Get citizen's self-modification history"""
    log_dir = "/mnt/c/Users/reyno/universe-engine/serenissima/logs/citizen_self_updates"
    history = []
    
    # Check last N days of logs
    for i in range(days):
        date = datetime.now() - timedelta(days=i)
        log_file = os.path.join(log_dir, f"{date.strftime('%Y%m%d')}_updates.json")
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                daily_logs = json.load(f)
                # Filter for this citizen
                citizen_logs = [log for log in daily_logs if log['citizen'] == username]
                history.extend(citizen_logs)
    
    return {
        "username": username,
        "update_count": len(history),
        "history": history
    }