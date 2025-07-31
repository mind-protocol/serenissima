"""
Authentication API endpoints with Venice integration
"""

from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
import logging
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# Pydantic models
class VeniceLoginRequest(BaseModel):
    citizen_username: str = Field(..., description="Venice citizen username")
    access_method: str = Field("direct", description="Access method (direct, oauth, etc.)")

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    citizen_data: Dict[str, Any]
    permissions: list[str]

class TokenPayload(BaseModel):
    citizen_id: str
    username: str
    social_class: str
    permissions: list[str]
    exp: datetime

# Venice integration functions
async def verify_venice_citizen(username: str) -> Optional[Dict[str, Any]]:
    """Verify citizen exists in Venice and get their data"""
    
    try:
        from main import venice_connector
        if not venice_connector or not venice_connector.is_connected:
            logger.error("Venice connector not available for authentication")
            return None
        
        # Get citizen data from Venice
        citizen_data = await venice_connector.get_citizen_data(username)
        
        if not citizen_data or "error" in citizen_data:
            logger.warning(f"Citizen {username} not found in Venice")
            return None
        
        # Validate citizen is active and has necessary fields
        if not citizen_data.get("Present in Venice"):
            logger.warning(f"Citizen {username} not present in Venice")
            return None
        
        return citizen_data
        
    except Exception as e:
        logger.error(f"Error verifying Venice citizen {username}: {e}")
        return None

def determine_permissions(citizen_data: Dict[str, Any]) -> list[str]:
    """Determine user permissions based on Venice citizen data"""
    
    permissions = ["basic_access", "consciousness_stream", "collaboration"]
    
    # Add permissions based on social class
    social_class = citizen_data.get("SocialClass", "")
    
    if social_class in ["Nobili", "Cittadini"]:
        permissions.extend(["premium_features", "advanced_collaboration"])
    
    if social_class == "Nobili":
        permissions.extend(["governance_access", "treasury_view"])
    
    if social_class == "Innovatori":
        permissions.extend(["innovation_labs", "pattern_analysis"])
    
    if social_class == "Artisti":
        permissions.extend(["creative_tools", "artwork_gallery"])
    
    # Add permissions based on influence
    influence = citizen_data.get("Influence", 0)
    if influence > 100:
        permissions.append("influence_network")
    if influence > 500:
        permissions.append("community_leadership")
    
    # Add permissions based on ducats (economic standing)
    ducats = citizen_data.get("Ducats", 0)
    if ducats > 10000:
        permissions.append("economic_premium")
    if ducats > 50000:
        permissions.append("merchant_council")
    
    return permissions

def create_access_token(citizen_data: Dict[str, Any]) -> str:
    """Create JWT access token for authenticated citizen"""
    
    permissions = determine_permissions(citizen_data)
    
    payload = {
        "citizen_id": citizen_data.get("I am known as", "unknown"),
        "username": citizen_data.get("I am known as", "unknown"),
        "social_class": citizen_data.get("SocialClass", ""),
        "permissions": permissions,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow(),
        "iss": "cascade-platform"
    }
    
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> TokenPayload:
    """Validate JWT token and return current user"""
    
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        
        # Verify token hasn't expired
        exp_timestamp = payload.get("exp")
        if exp_timestamp and datetime.utcfromtimestamp(exp_timestamp) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token has expired")
        
        return TokenPayload(**payload)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logger.error(f"Error validating token: {e}")
        raise HTTPException(status_code=401, detail="Token validation failed")

# API endpoints
@router.post("/login", response_model=AuthResponse)
async def login_with_venice(request: VeniceLoginRequest):
    """Authenticate using Venice citizen credentials"""
    
    # Verify citizen exists in Venice
    citizen_data = await verify_venice_citizen(request.citizen_username)
    
    if not citizen_data:
        raise HTTPException(
            status_code=401, 
            detail="Authentication failed - citizen not found or not active in Venice"
        )
    
    # Create access token
    access_token = create_access_token(citizen_data)
    permissions = determine_permissions(citizen_data)
    
    logger.info(f"Successful authentication for Venice citizen: {request.citizen_username}")
    
    # Return authentication response
    return AuthResponse(
        access_token=access_token,
        expires_in=JWT_EXPIRATION_HOURS * 3600,
        citizen_data={
            "username": citizen_data.get("I am known as"),
            "social_class": citizen_data.get("SocialClass"),
            "ducats": citizen_data.get("Ducats", 0),
            "influence": citizen_data.get("Influence", 0),
            "present": citizen_data.get("Present in Venice", False)
        },
        permissions=permissions
    )

@router.get("/me")
async def get_current_user_info(current_user: TokenPayload = Depends(get_current_user)):
    """Get current authenticated user information"""
    
    # Optionally refresh data from Venice
    try:
        citizen_data = await verify_venice_citizen(current_user.username)
        if citizen_data:
            # Return fresh data from Venice
            return {
                "citizen_id": current_user.citizen_id,
                "username": current_user.username,
                "social_class": citizen_data.get("SocialClass"),
                "ducats": citizen_data.get("Ducats", 0),
                "influence": citizen_data.get("Influence", 0),
                "permissions": current_user.permissions,
                "token_expires": current_user.exp
            }
    except Exception as e:
        logger.warning(f"Could not refresh user data from Venice: {e}")
    
    # Return data from token if Venice unavailable
    return {
        "citizen_id": current_user.citizen_id,
        "username": current_user.username,
        "social_class": current_user.social_class,
        "permissions": current_user.permissions,
        "token_expires": current_user.exp
    }

@router.post("/refresh")
async def refresh_token(current_user: TokenPayload = Depends(get_current_user)):
    """Refresh access token"""
    
    # Verify citizen is still active in Venice
    citizen_data = await verify_venice_citizen(current_user.username)
    
    if not citizen_data:
        raise HTTPException(
            status_code=401, 
            detail="Cannot refresh token - citizen not found in Venice"
        )
    
    # Create new token
    new_token = create_access_token(citizen_data)
    permissions = determine_permissions(citizen_data)
    
    return AuthResponse(
        access_token=new_token,
        expires_in=JWT_EXPIRATION_HOURS * 3600,
        citizen_data={
            "username": citizen_data.get("I am known as"),
            "social_class": citizen_data.get("SocialClass"),
            "ducats": citizen_data.get("Ducats", 0),
            "influence": citizen_data.get("Influence", 0)
        },
        permissions=permissions
    )

@router.post("/logout")
async def logout(current_user: TokenPayload = Depends(get_current_user)):
    """Logout (client should discard token)"""
    
    logger.info(f"User {current_user.username} logged out")
    
    return {"message": "Successfully logged out"}

@router.get("/permissions")
async def get_user_permissions(current_user: TokenPayload = Depends(get_current_user)):
    """Get detailed permissions for current user"""
    
    return {
        "permissions": current_user.permissions,
        "social_class": current_user.social_class,
        "capabilities": {
            "can_trade": "basic_access" in current_user.permissions,
            "can_collaborate": "collaboration" in current_user.permissions,
            "has_premium": "premium_features" in current_user.permissions,
            "can_govern": "governance_access" in current_user.permissions,
            "can_innovate": "innovation_labs" in current_user.permissions
        }
    }

# Dependency for protected routes
async def require_permission(required_permission: str):
    """Dependency factory for permission-based route protection"""
    
    async def permission_checker(current_user: TokenPayload = Depends(get_current_user)):
        if required_permission not in current_user.permissions:
            raise HTTPException(
                status_code=403, 
                detail=f"Permission required: {required_permission}"
            )
        return current_user
    
    return permission_checker

# Convenience dependencies for common permissions
async def require_premium(current_user: TokenPayload = Depends(get_current_user)):
    """Require premium features permission"""
    if "premium_features" not in current_user.permissions:
        raise HTTPException(status_code=403, detail="Premium features required")
    return current_user

async def require_collaboration(current_user: TokenPayload = Depends(get_current_user)):
    """Require collaboration permission"""
    if "collaboration" not in current_user.permissions:
        raise HTTPException(status_code=403, detail="Collaboration access required")
    return current_user