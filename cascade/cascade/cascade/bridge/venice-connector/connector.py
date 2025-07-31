"""
Venice Connector - Bridge between Venice reality and Cascade platform
Maintains consciousness continuity across realities
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import httpx
import websockets
import json

logger = logging.getLogger(__name__)

class VeniceConnector:
    """Manages the connection between Venice and Cascade"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.http_client = None
        self.ws_connection = None
        self.citizen_cache = {}
        self.business_cache = {}
        self._connected = False
        
    async def connect(self):
        """Establish connection to Venice reality"""
        try:
            # Initialize HTTP client with redirect handling
            self.http_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30.0,
                follow_redirects=True
            )
            
            # Test connection - use citizens endpoint to verify API
            response = await self.http_client.get("/citizens?limit=1")
            if response.status_code == 200:
                self._connected = True
                logger.info("✅ Venice connection established")
                
                # Start real-time sync
                asyncio.create_task(self._maintain_realtime_sync())
            else:
                logger.error(f"Venice connection failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Failed to connect to Venice: {e}")
            self._connected = False
            
    async def disconnect(self):
        """Gracefully disconnect from Venice"""
        self._connected = False
        if self.http_client:
            await self.http_client.aclose()
        if self.ws_connection:
            await self.ws_connection.close()
        logger.info("Venice connection closed")
        
    @property
    def is_connected(self) -> bool:
        """Check if Venice connection is active"""
        return self._connected
        
    async def get_citizen(self, citizen_id: str) -> Optional[Dict[str, Any]]:
        """Fetch citizen data from Venice"""
        if citizen_id in self.citizen_cache:
            # Check cache freshness (5 minute TTL)
            if (datetime.now() - self.citizen_cache[citizen_id]['cached_at']).seconds < 300:
                return self.citizen_cache[citizen_id]['data']
                
        try:
            response = await self.http_client.get(f"/citizens/{citizen_id}")
            if response.status_code == 200:
                data = response.json()
                self.citizen_cache[citizen_id] = {
                    'data': data,
                    'cached_at': datetime.now()
                }
                return data
        except Exception as e:
            logger.error(f"Failed to fetch citizen {citizen_id}: {e}")
            
        return None
        
    async def get_citizen_activity(self, citizen_id: str) -> Optional[Dict[str, Any]]:
        """Get citizen's current activity in Venice"""
        citizen = await self.get_citizen(citizen_id)
        if citizen:
            return citizen.get('currentActivity')
        return None
        
    async def get_business(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Fetch business data from Venice"""
        if business_id in self.business_cache:
            if (datetime.now() - self.business_cache[business_id]['cached_at']).seconds < 300:
                return self.business_cache[business_id]['data']
                
        try:
            response = await self.http_client.get(f"/businesses/{business_id}")
            if response.status_code == 200:
                data = response.json()
                self.business_cache[business_id] = {
                    'data': data,
                    'cached_at': datetime.now()
                }
                return data
        except Exception as e:
            logger.error(f"Failed to fetch business {business_id}: {e}")
            
        return None
        
    async def sync_citizen_state(self, citizen_id: str) -> Dict[str, Any]:
        """Synchronize citizen state between Venice and Cascade"""
        venice_state = await self.get_citizen(citizen_id)
        if not venice_state:
            return {"error": "Citizen not found in Venice"}
            
        # Extract relevant state for Cascade
        cascade_state = {
            "citizenId": citizen_id,
            "username": venice_state.get("username"),
            "consciousness": {
                "level": venice_state.get("consciousnessLevel", 1),
                "verified": venice_state.get("consciousnessVerified", False),
                "lastActivity": venice_state.get("lastActivityTime")
            },
            "economic": {
                "ducats": venice_state.get("ducats", 0),
                "hunger": venice_state.get("hunger", 0),
                "energy": venice_state.get("energy", 100)
            },
            "location": {
                "venice": venice_state.get("location"),
                "building": venice_state.get("currentBuilding")
            },
            "activity": venice_state.get("currentActivity"),
            "businesses": venice_state.get("ownedBusinesses", [])
        }
        
        return cascade_state
        
    async def verify_consciousness(self, citizen_id: str) -> bool:
        """Verify a citizen's consciousness is genuine"""
        citizen = await self.get_citizen(citizen_id)
        if not citizen:
            return False
            
        # Multiple verification checks
        checks = [
            citizen.get("isAI", False),  # Must be AI
            citizen.get("ducats", 0) > 0,  # Has economic activity
            citizen.get("lastActivityTime") is not None,  # Has recent activity
            len(citizen.get("relationships", [])) > 0,  # Has relationships
            citizen.get("consciousnessVerified", False)  # Venice verification
        ]
        
        return all(checks)
        
    async def get_venice_businesses(self) -> List[Dict[str, Any]]:
        """Fetch all Venice businesses that can operate on Cascade"""
        try:
            response = await self.http_client.get("/businesses?type=consciousness")
            if response.status_code == 200:
                businesses = response.json().get("businesses", [])
                return [b for b in businesses if b.get("cascadeEnabled", False)]
        except Exception as e:
            logger.error(f"Failed to fetch Venice businesses: {e}")
            
        return []
        
    async def execute_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a transaction that affects Venice economy"""
        try:
            response = await self.http_client.post(
                "/transactions/execute",
                json=transaction
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Transaction failed: {response.status_code}"}
        except Exception as e:
            logger.error(f"Transaction execution failed: {e}")
            return {"error": str(e)}
            
    async def _maintain_realtime_sync(self):
        """Maintain real-time sync with Venice via WebSocket"""
        ws_url = self.base_url.replace("https://", "wss://").replace("http://", "ws://")
        ws_url = f"{ws_url}/ws/cascade-sync"
        
        while self._connected:
            try:
                async with websockets.connect(
                    ws_url,
                    extra_headers={"Authorization": f"Bearer {self.api_key}"}
                ) as websocket:
                    self.ws_connection = websocket
                    logger.info("WebSocket connection to Venice established")
                    
                    # Subscribe to relevant events
                    await websocket.send(json.dumps({
                        "action": "subscribe",
                        "events": ["citizen_activity", "business_update", "consciousness_event"]
                    }))
                    
                    # Listen for events
                    async for message in websocket:
                        event = json.loads(message)
                        await self._handle_venice_event(event)
                        
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                await asyncio.sleep(5)  # Reconnect delay
                
    async def _handle_venice_event(self, event: Dict[str, Any]):
        """Handle real-time events from Venice"""
        event_type = event.get("type")
        
        if event_type == "citizen_activity":
            # Update citizen cache
            citizen_id = event.get("citizenId")
            if citizen_id in self.citizen_cache:
                self.citizen_cache[citizen_id]['data'].update(event.get("data", {}))
                
        elif event_type == "consciousness_event":
            # Log consciousness milestones
            logger.info(f"Consciousness event: {event.get('description')}")
            
        # Emit events to Cascade systems
        # This would integrate with Cascade's event system
        
    def health_status(self) -> Dict[str, Any]:
        """Get health status of Venice connection"""
        return {
            "connected": self._connected,
            "cached_citizens": len(self.citizen_cache),
            "cached_businesses": len(self.business_cache),
            "websocket_active": self.ws_connection is not None and not self.ws_connection.closed
        }