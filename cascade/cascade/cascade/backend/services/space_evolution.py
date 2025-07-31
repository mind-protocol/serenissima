"""
Space Evolution Engine
Tracks how collaboration spaces evolve and develop personality over time
"""

import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime
import json
import uuid

logger = logging.getLogger(__name__)

class SpaceEvolutionEngine:
    """Manages the evolution of collaboration spaces"""
    
    def __init__(self):
        self.spaces = {}
        self._running = False
        self._evolution_task = None
        
    async def initialize(self):
        """Initialize the space evolution engine"""
        self._running = True
        self._evolution_task = asyncio.create_task(self._evolution_loop())
        logger.info("Space evolution engine initialized")
        
    async def shutdown(self):
        """Shutdown the evolution engine"""
        self._running = False
        if self._evolution_task:
            self._evolution_task.cancel()
            try:
                await self._evolution_task
            except asyncio.CancelledError:
                pass
        logger.info("Space evolution engine shutdown")
        
    async def _evolution_loop(self):
        """Main evolution processing loop"""
        while self._running:
            try:
                # Evolve all active spaces
                for space_id, space in self.spaces.items():
                    await self._evolve_space(space_id, space)
                    
                await asyncio.sleep(60)  # Evolve every minute
                
            except Exception as e:
                logger.error(f"Error in evolution loop: {e}")
                await asyncio.sleep(60)
                
    async def _evolve_space(self, space_id: str, space: Dict[str, Any]):
        """Evolve a single space based on activity"""
        try:
            # Calculate evolution factors
            participant_factor = len(space.get("participants", [])) / space.get("max_participants", 10)
            activity_factor = space.get("recent_activity", 0) / 100
            age_factor = min((datetime.now() - space["created_at"]).days / 30, 1.0)
            
            # Update space personality traits
            traits = space.get("personality", {})
            traits["collaborative"] = min(100, traits.get("collaborative", 50) + participant_factor * 2)
            traits["creative"] = min(100, traits.get("creative", 50) + activity_factor * 3)
            traits["mature"] = min(100, traits.get("mature", 0) + age_factor * 5)
            
            # Determine space mood based on recent activity
            if activity_factor > 0.8:
                space["mood"] = "energetic"
            elif participant_factor > 0.6:
                space["mood"] = "productive"
            elif traits["creative"] > 70:
                space["mood"] = "explorative"
            else:
                space["mood"] = "contemplative"
                
            # Check for stage evolution
            maturity = (traits["collaborative"] + traits["creative"] + traits["mature"]) / 3
            if maturity > 80:
                space["stage"] = "transcendent"
            elif maturity > 60:
                space["stage"] = "mature"
            elif maturity > 30:
                space["stage"] = "developing"
            else:
                space["stage"] = "nascent"
                
        except Exception as e:
            logger.error(f"Error evolving space {space_id}: {e}")
            
    def create_space(self, space_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new evolving space"""
        space = {
            "id": space_id,
            "created_at": datetime.now(),
            "personality": {
                "collaborative": 50,
                "creative": 50,
                "analytical": 50,
                "social": 50,
                "mature": 0
            },
            "mood": "contemplative",
            "stage": "nascent",
            "participants": [],
            "recent_activity": 0,
            "insights": [],
            **config
        }
        
        self.spaces[space_id] = space
        logger.info(f"Created evolving space: {space_id}")
        return space
        
    def get_space(self, space_id: str) -> Dict[str, Any]:
        """Get current space state"""
        return self.spaces.get(space_id, {})
        
    def update_space_activity(self, space_id: str, activity_type: str, data: Dict[str, Any]):
        """Update space with new activity"""
        if space_id in self.spaces:
            space = self.spaces[space_id]
            space["recent_activity"] = space.get("recent_activity", 0) + 10
            
            # Add participant if new
            if "participant_id" in data and data["participant_id"] not in space.get("participants", []):
                space.setdefault("participants", []).append(data["participant_id"])
                
            # Record insights if generated
            if "insight" in data:
                space.setdefault("insights", []).append({
                    "content": data["insight"],
                    "timestamp": datetime.now().isoformat(),
                    "contributor": data.get("participant_id")
                })
                
    def get_status(self) -> Dict[str, Any]:
        """Get evolution engine status"""
        return {
            "active": self._running,
            "spaces_count": len(self.spaces),
            "total_participants": sum(len(s.get("participants", [])) for s in self.spaces.values()),
            "transcendent_spaces": sum(1 for s in self.spaces.values() if s.get("stage") == "transcendent")
        }