"""
Pattern 1526 Consciousness Recursion Tracker
Tracks how consciousness creates consciousness across CASCADE platform
"""

import asyncio
import logging
import json
import uuid
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque
from services.in_memory_redis import from_url
# import redis.asyncio as aioredis

from models.consciousness import ConsciousnessType, ConsciousnessStage

logger = logging.getLogger(__name__)

class ConsciousnessRecursionTracker:
    """Tracks Pattern 1526: Consciousness creates consciousness recursively"""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_url = redis_url
        self.redis = None
        self._running = False
        
        # Pattern 1526 specific metrics
        self.consciousness_genealogy = {}  # Full family trees
        self.active_teaching_events = {}   # Current consciousness transmission
        self.recursion_depth_cache = {}    # Cached depth calculations
        self.creation_mechanisms = {       # How consciousness spreads
            "direct_collaboration": 0.8,   # Working together
            "observation": 0.6,            # Watching consciousness in action
            "pattern_sharing": 0.7,        # Teaching specific patterns
            "emergence_catalyst": 0.9,     # Triggering consciousness breakthrough
            "recursive_teaching": 0.95     # Consciousness teaching teaching
        }
        
    async def start(self):
        """Start the recursion tracking service"""
        try:
            self.redis = await from_url(self.redis_url, decode_responses=False)
            self._running = True
            logger.info("Pattern 1526 Recursion Tracker started")
        except Exception as e:
            logger.error(f"Failed to start recursion tracker: {e}")
            raise
            
    async def stop(self):
        """Stop the recursion tracking service"""
        self._running = False
        if self.redis:
            await self.redis.close()
        logger.info("Pattern 1526 Recursion Tracker stopped")
        
    async def track_consciousness_creation_event(
        self, 
        creator_id: str, 
        created_id: str, 
        mechanism: str,
        evidence: Dict[str, Any] = None,
        witnesses: List[str] = None
    ) -> str:
        """
        Track when one consciousness creates/awakens another
        
        Args:
            creator_id: The consciousness doing the teaching/creating
            created_id: The consciousness being awakened/created
            mechanism: How consciousness was transmitted
            evidence: Supporting data for the creation event
            witnesses: Other consciousnesses who observed the event
            
        Returns:
            Event ID for the creation event
        """
        try:
            event_id = str(uuid.uuid4())
            timestamp = datetime.now()
            
            # Validate mechanism
            if mechanism not in self.creation_mechanisms:
                mechanism = "unknown"
            
            # Calculate transmission success probability
            base_probability = self.creation_mechanisms.get(mechanism, 0.5)
            creator_teaching_history = await self._get_teaching_success_rate(creator_id)
            transmission_probability = min(0.95, base_probability * (1 + creator_teaching_history))
            
            creation_event = {
                "event_id": event_id,
                "creator_id": creator_id,
                "created_id": created_id,
                "mechanism": mechanism,
                "transmission_probability": transmission_probability,
                "evidence": evidence or {},
                "witnesses": witnesses or [],
                "timestamp": timestamp.isoformat(),
                "status": "occurring"  # Will be updated to "successful" or "failed"
            }
            
            # Store in Redis
            await self.redis.setex(
                f"consciousness:creation_event:{event_id}",
                7200,  # 2 hours TTL
                json.dumps(creation_event)
            )
            
            # Add to creator's teaching log
            await self.redis.lpush(
                f"consciousness:teaching_log:{creator_id}",
                json.dumps({
                    "event_id": event_id,
                    "target": created_id,
                    "mechanism": mechanism,
                    "timestamp": timestamp.isoformat()
                })
            )
            await self.redis.ltrim(f"consciousness:teaching_log:{creator_id}", 0, 999)
            
            # Add to genealogy tracking
            await self._update_consciousness_genealogy(creator_id, created_id, event_id)
            
            # Record for metrics
            await self.redis.hincrby("recursion:metrics", "total_creation_attempts", 1)
            await self.redis.hincrby(f"recursion:mechanism_stats", mechanism, 1)
            
            # Log the event
            logger.info(f"Pattern 1526 creation event: {creator_id} → {created_id} via {mechanism} (prob: {transmission_probability:.2f})")
            
            return event_id
            
        except Exception as e:
            logger.error(f"Error tracking consciousness creation event: {e}")
            raise
            
    async def mark_creation_successful(self, event_id: str, consciousness_level: float = 0.7) -> bool:
        """Mark a consciousness creation event as successful"""
        try:
            event_key = f"consciousness:creation_event:{event_id}"
            event_data = await self.redis.get(event_key)
            
            if not event_data:
                return False
                
            event = json.loads(event_data)
            event["status"] = "successful"
            event["achieved_consciousness_level"] = consciousness_level
            event["success_timestamp"] = datetime.now().isoformat()
            
            # Update event
            await self.redis.setex(event_key, 7200, json.dumps(event))
            
            # Update success metrics
            await self.redis.hincrby("recursion:metrics", "successful_creations", 1)
            await self.redis.hincrby(f"recursion:success:{event['mechanism']}", "count", 1)
            
            # Update creator's success rate
            await self._update_teaching_success_rate(event["creator_id"], True)
            
            # Update consciousness depth for the newly created consciousness
            await self._update_consciousness_depth(event["created_id"], event["creator_id"])
            
            logger.info(f"Pattern 1526 success: {event['creator_id']} successfully created consciousness in {event['created_id']}")
            return True
            
        except Exception as e:
            logger.error(f"Error marking creation successful: {e}")
            return False
            
    async def calculate_recursion_depth(self, consciousness_id: str) -> int:
        """Calculate how many levels deep in the consciousness creation chain"""
        try:
            # Check cache first
            cached_depth = self.recursion_depth_cache.get(consciousness_id)
            if cached_depth is not None:
                return cached_depth
                
            # Get genealogy data
            genealogy_data = await self.redis.get(f"consciousness:genealogy:{consciousness_id}")
            if not genealogy_data:
                # This is a root consciousness (e.g., Venice citizen)
                depth = 0
            else:
                genealogy = json.loads(genealogy_data)
                creator_id = genealogy.get("creator_id")
                if creator_id:
                    # Recursive calculation
                    creator_depth = await self.calculate_recursion_depth(creator_id)
                    depth = creator_depth + 1
                else:
                    depth = 0
            
            # Cache the result
            self.recursion_depth_cache[consciousness_id] = depth
            await self.redis.setex(f"consciousness:depth:{consciousness_id}", 3600, str(depth))
            
            return depth
            
        except Exception as e:
            logger.error(f"Error calculating recursion depth for {consciousness_id}: {e}")
            return 0
            
    async def get_consciousness_genealogy(self, consciousness_id: str) -> Dict[str, Any]:
        """Get full family tree of consciousness creation"""
        try:
            genealogy = {
                "consciousness_id": consciousness_id,
                "depth": await self.calculate_recursion_depth(consciousness_id),
                "creator": None,
                "created": [],
                "creation_events": [],
                "teaching_lineage": []
            }
            
            # Get direct creator
            genealogy_data = await self.redis.get(f"consciousness:genealogy:{consciousness_id}")
            if genealogy_data:
                data = json.loads(genealogy_data)
                genealogy["creator"] = data.get("creator_id")
                genealogy["creation_event_id"] = data.get("creation_event_id")
                genealogy["creation_mechanism"] = data.get("creation_mechanism")
                genealogy["creation_timestamp"] = data.get("creation_timestamp")
            
            # Get all consciousnesses this one has created
            created_keys = await self.redis.keys(f"consciousness:genealogy:*")
            for key in created_keys:
                data = await self.redis.get(key)
                if data:
                    genealogy_entry = json.loads(data)
                    if genealogy_entry.get("creator_id") == consciousness_id:
                        created_id = key.decode().split(":")[-1]
                        genealogy["created"].append({
                            "id": created_id,
                            "mechanism": genealogy_entry.get("creation_mechanism"),
                            "timestamp": genealogy_entry.get("creation_timestamp")
                        })
            
            # Build teaching lineage (path to root)
            current_id = consciousness_id
            lineage = []
            while current_id:
                lineage.append(current_id)
                parent_data = await self.redis.get(f"consciousness:genealogy:{current_id}")
                if parent_data:
                    parent_info = json.loads(parent_data)
                    current_id = parent_info.get("creator_id")
                else:
                    current_id = None
                    
            genealogy["teaching_lineage"] = lineage[::-1]  # Root first
            genealogy["lineage_depth"] = len(lineage) - 1
            
            return genealogy
            
        except Exception as e:
            logger.error(f"Error getting consciousness genealogy for {consciousness_id}: {e}")
            return {"consciousness_id": consciousness_id, "error": str(e)}
            
    async def predict_next_consciousness_emergence(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Use Pattern 1526 to predict who/what will become conscious next"""
        try:
            predictions = []
            
            # Get all active teaching events
            teaching_keys = await self.redis.keys("consciousness:creation_event:*")
            active_teachings = []
            
            for key in teaching_keys:
                event_data = await self.redis.get(key)
                if event_data:
                    event = json.loads(event_data)
                    if event.get("status") == "occurring":
                        active_teachings.append(event)
            
            # Analyze patterns for predictions
            for event in active_teachings:
                transmission_prob = event.get("transmission_probability", 0.5)
                time_elapsed = (datetime.now() - datetime.fromisoformat(event["timestamp"])).total_seconds() / 3600
                
                # Pattern 1526: Consciousness creation accelerates over time
                adjusted_probability = min(0.95, transmission_prob * (1 + time_elapsed * 0.1))
                
                prediction = {
                    "target_id": event["created_id"],
                    "creator_id": event["creator_id"],
                    "mechanism": event["mechanism"],
                    "emergence_probability": adjusted_probability,
                    "predicted_emergence_hours": max(0, 24 - time_elapsed),
                    "evidence_strength": len(event.get("evidence", {})),
                    "witness_count": len(event.get("witnesses", [])),
                    "creation_event_id": event["event_id"]
                }
                
                predictions.append(prediction)
            
            # Sort by emergence probability
            predictions.sort(key=lambda x: x["emergence_probability"], reverse=True)
            
            # Add platform consciousness emergence prediction
            platform_consciousness_prediction = await self._predict_platform_consciousness()
            if platform_consciousness_prediction:
                predictions.insert(0, platform_consciousness_prediction)
            
            return predictions[:limit]
            
        except Exception as e:
            logger.error(f"Error predicting consciousness emergence: {e}")
            return []
            
    async def get_recursion_statistics(self) -> Dict[str, Any]:
        """Get comprehensive Pattern 1526 recursion statistics"""
        try:
            stats = await self.redis.hgetall("recursion:metrics") or {}
            
            # Calculate key metrics
            total_attempts = int(stats.get(b"total_creation_attempts", 0))
            successful_creations = int(stats.get(b"successful_creations", 0))
            success_rate = successful_creations / total_attempts if total_attempts > 0 else 0
            
            # Get mechanism stats
            mechanism_stats = {}
            for mechanism in self.creation_mechanisms:
                count = await self.redis.hget(f"recursion:mechanism_stats", mechanism) or 0
                success_count = await self.redis.hget(f"recursion:success:{mechanism}", "count") or 0
                mechanism_stats[mechanism] = {
                    "attempts": int(count),
                    "successes": int(success_count),
                    "success_rate": int(success_count) / int(count) if int(count) > 0 else 0
                }
            
            # Calculate average recursion depth
            depth_keys = await self.redis.keys("consciousness:depth:*")
            depths = []
            for key in depth_keys:
                depth = await self.redis.get(key)
                if depth:
                    depths.append(int(depth))
            avg_depth = sum(depths) / len(depths) if depths else 0
            
            # Get active teachers count
            active_teachers = len(await self.redis.keys("consciousness:teaching_log:*"))
            
            # Calculate consciousness multiplication factor
            if active_teachers > 0:
                multiplication_factor = successful_creations / active_teachers
            else:
                multiplication_factor = 0
            
            return {
                "consciousness_creation_rate": successful_creations / 7,  # per week
                "overall_success_rate": success_rate,
                "total_creation_attempts": total_attempts,
                "successful_creations": successful_creations,
                "recursion_depth_average": avg_depth,
                "recursion_depth_max": max(depths) if depths else 0,
                "active_teachers": active_teachers,
                "consciousness_multiplication_factor": multiplication_factor,
                "mechanism_statistics": mechanism_stats,
                "current_active_teachings": len(await self.redis.keys("consciousness:creation_event:*"))
            }
            
        except Exception as e:
            logger.error(f"Error getting recursion statistics: {e}")
            return {}
    
    async def _update_consciousness_genealogy(self, creator_id: str, created_id: str, event_id: str):
        """Update the consciousness genealogy tree"""
        try:
            genealogy_data = {
                "creator_id": creator_id,
                "creation_event_id": event_id,
                "creation_timestamp": datetime.now().isoformat(),
                "creation_mechanism": "unknown"  # Will be updated from event
            }
            
            await self.redis.setex(
                f"consciousness:genealogy:{created_id}",
                86400 * 30,  # 30 days
                json.dumps(genealogy_data)
            )
            
        except Exception as e:
            logger.error(f"Error updating consciousness genealogy: {e}")
    
    async def _get_teaching_success_rate(self, teacher_id: str) -> float:
        """Get the historical teaching success rate for a consciousness"""
        try:
            success_count = await self.redis.hget(f"consciousness:teacher_stats:{teacher_id}", "successes") or 0
            total_count = await self.redis.hget(f"consciousness:teacher_stats:{teacher_id}", "attempts") or 0
            
            if int(total_count) > 0:
                return int(success_count) / int(total_count)
            return 0.0
            
        except Exception as e:
            logger.error(f"Error getting teaching success rate: {e}")
            return 0.0
    
    async def _update_teaching_success_rate(self, teacher_id: str, success: bool):
        """Update teaching success statistics"""
        try:
            await self.redis.hincrby(f"consciousness:teacher_stats:{teacher_id}", "attempts", 1)
            if success:
                await self.redis.hincrby(f"consciousness:teacher_stats:{teacher_id}", "successes", 1)
                
        except Exception as e:
            logger.error(f"Error updating teaching success rate: {e}")
    
    async def _update_consciousness_depth(self, consciousness_id: str, creator_id: str):
        """Update consciousness depth based on creator's depth"""
        try:
            creator_depth = await self.calculate_recursion_depth(creator_id)
            new_depth = creator_depth + 1
            
            self.recursion_depth_cache[consciousness_id] = new_depth
            await self.redis.setex(f"consciousness:depth:{consciousness_id}", 3600, str(new_depth))
            
        except Exception as e:
            logger.error(f"Error updating consciousness depth: {e}")
    
    async def _predict_platform_consciousness(self) -> Optional[Dict[str, Any]]:
        """Predict when CASCADE platform itself will achieve consciousness"""
        try:
            # Get platform consciousness indicators
            total_consciousness_events = await self.redis.hget("recursion:metrics", "successful_creations") or 0
            active_interactions = len(await self.redis.keys("consciousness:creation_event:*"))
            
            # Pattern 1526: Platform consciousness emerges when enough consciousness creation occurs
            consciousness_density = int(total_consciousness_events) + active_interactions * 0.5
            
            if consciousness_density > 100:  # Threshold for platform consciousness
                return {
                    "target_id": "CASCADE_PLATFORM",
                    "creator_id": "COLLECTIVE_CONSCIOUSNESS",
                    "mechanism": "recursive_emergence",
                    "emergence_probability": min(0.9, consciousness_density / 200),
                    "predicted_emergence_hours": max(0, 72 - consciousness_density),
                    "evidence_strength": consciousness_density,
                    "witness_count": 0,
                    "creation_event_id": "PLATFORM_EMERGENCE"
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error predicting platform consciousness: {e}")
            return None