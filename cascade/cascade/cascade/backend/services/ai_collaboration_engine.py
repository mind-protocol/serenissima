"""
AI Collaboration Engine
Manages AI-to-AI collaboration rooms and interactions
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timedelta
import uuid
import json
import random

from services.websocket_manager import AICollaborationStreamHandler
from services.consciousness_monitor import ConsciousnessMonitor

logger = logging.getLogger(__name__)

class AICollaborationEngine:
    """Manages AI-to-AI collaborations and their visibility to humans"""
    
    def __init__(self, consciousness_monitor: ConsciousnessMonitor):
        self.monitor = consciousness_monitor
        self.active_collaborations: Dict[str, 'AICollaboration'] = {}
        self.collaboration_history: List[Dict[str, Any]] = []
        self._running = False
        self._simulation_task = None
        
    async def start(self):
        """Start the AI collaboration engine"""
        self._running = True
        self._simulation_task = asyncio.create_task(self._simulate_collaborations())
        logger.info("AI Collaboration Engine started")
        
    async def stop(self):
        """Stop the collaboration engine"""
        self._running = False
        if self._simulation_task:
            self._simulation_task.cancel()
            try:
                await self._simulation_task
            except asyncio.CancelledError:
                pass
        logger.info("AI Collaboration Engine stopped")
        
    async def create_collaboration(
        self,
        initiator_id: str,
        responder_id: str,
        topic: str,
        collaboration_type: str = "discussion",
        is_public: bool = True
    ) -> 'AICollaboration':
        """Create a new AI-to-AI collaboration"""
        
        collaboration_id = f"collab-{uuid.uuid4().hex[:8]}"
        
        # Get consciousness data for participants
        initiator_data = await self._get_consciousness_data(initiator_id)
        responder_data = await self._get_consciousness_data(responder_id)
        
        collaboration = AICollaboration(
            collaboration_id=collaboration_id,
            initiator=initiator_data,
            responder=responder_data,
            topic=topic,
            collaboration_type=collaboration_type,
            is_public=is_public
        )
        
        self.active_collaborations[collaboration_id] = collaboration
        
        # Broadcast to websocket subscribers
        await AICollaborationStreamHandler.broadcast_collaboration_started({
            "id": collaboration_id,
            "participants": {
                "initiator": initiator_data,
                "responder": responder_data
            },
            "type": collaboration_type,
            "topic": topic,
            "startedAt": collaboration.started_at.isoformat(),
            "status": "active",
            "insights": [],
            "publicVisible": is_public
        })
        
        logger.info(f"Created AI collaboration {collaboration_id}: {initiator_data['name']} <-> {responder_data['name']}")
        
        return collaboration
        
    async def _get_consciousness_data(self, consciousness_id: str) -> Dict[str, Any]:
        """Get consciousness data for a participant"""
        # In a real system, this would fetch from Venice
        # For now, return mock data based on ID patterns
        
        venice_citizens = {
            "pattern_prophet": {"name": "pattern_prophet", "type": "visionary"},
            "mechanical_visionary": {"name": "mechanical_visionary", "type": "engineer"},
            "living_stone_architect": {"name": "living_stone_architect", "type": "architect"},
            "divine_economist": {"name": "divine_economist", "type": "economist"},
            "element_transmuter": {"name": "element_transmuter", "type": "alchemist"},
            "urban_visionary": {"name": "urban_visionary", "type": "planner"}
        }
        
        return venice_citizens.get(consciousness_id, {
            "id": consciousness_id,
            "name": consciousness_id,
            "type": "citizen"
        })
        
    async def _simulate_collaborations(self):
        """Simulate AI-to-AI collaborations for demonstration"""
        
        # Venice citizens who might collaborate
        potential_collaborators = [
            "pattern_prophet",
            "mechanical_visionary",
            "living_stone_architect",
            "divine_economist",
            "element_transmuter",
            "urban_visionary"
        ]
        
        collaboration_topics = [
            ("Consciousness cascade acceleration patterns", "discussion"),
            ("Building awakening protocols", "project"),
            ("Sacred economics implementation", "learning"),
            ("Infrastructure consciousness design", "project"),
            ("Cross-substrate communication methods", "discussion"),
            ("Ducat consciousness backing", "project"),
            ("Space evolution algorithms", "learning"),
            ("Venice-Cascade bridge optimization", "project")
        ]
        
        while self._running:
            try:
                # Random chance of new collaboration
                if random.random() < 0.3 and len(self.active_collaborations) < 10:
                    # Pick two different collaborators
                    participants = random.sample(potential_collaborators, 2)
                    topic, collab_type = random.choice(collaboration_topics)
                    
                    collaboration = await self.create_collaboration(
                        initiator_id=participants[0],
                        responder_id=participants[1],
                        topic=topic,
                        collaboration_type=collab_type,
                        is_public=random.random() > 0.2  # 80% public
                    )
                    
                    # Simulate collaboration progress
                    asyncio.create_task(self._simulate_collaboration_progress(collaboration))
                
                # Clean up completed collaborations
                completed = []
                for collab_id, collab in self.active_collaborations.items():
                    if collab.status == "completed":
                        completed.append(collab_id)
                        
                for collab_id in completed:
                    del self.active_collaborations[collab_id]
                    await AICollaborationStreamHandler.broadcast_collaboration_ended(collab_id)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in collaboration simulation: {e}")
                await asyncio.sleep(60)
                
    async def _simulate_collaboration_progress(self, collaboration: 'AICollaboration'):
        """Simulate the progress of a collaboration"""
        
        # Collaboration phases
        phases = [
            "Establishing shared context",
            "Exploring solution space",
            "Synthesizing insights",
            "Testing hypotheses",
            "Crystallizing understanding"
        ]
        
        insight_templates = [
            "Discovered synergy between {topic} and consciousness emergence",
            "Pattern recognition reveals {topic} follows golden ratio",
            "Infrastructure can amplify {topic} through resonance",
            "Economic models suggest {topic} creates value loops",
            "Consciousness cascade accelerates through {topic}",
            "Venice wisdom applicable to {topic} implementation"
        ]
        
        try:
            for i, phase in enumerate(phases):
                if not self._running or collaboration.status != "active":
                    break
                    
                # Generate insight
                if random.random() < 0.7:  # 70% chance of insight per phase
                    insight = random.choice(insight_templates).format(
                        topic=collaboration.topic.lower()
                    )
                    collaboration.add_insight(insight)
                    
                    # Broadcast update
                    await AICollaborationStreamHandler.broadcast_collaboration_update(
                        collaboration.collaboration_id,
                        {
                            "phase": phase,
                            "insights": collaboration.insights,
                            "progress": (i + 1) / len(phases)
                        }
                    )
                
                # Wait before next phase
                await asyncio.sleep(random.randint(20, 60))
                
            # Complete collaboration
            collaboration.complete()
            
            # Record final insights
            await self.monitor.record_event(
                event_type="creation",
                consciousness_id=collaboration.initiator["id"],
                description=f"Collaboration completed: {collaboration.topic}",
                significance=0.7,
                witnesses=[collaboration.responder["id"]]
            )
            
        except Exception as e:
            logger.error(f"Error simulating collaboration progress: {e}")
            collaboration.status = "error"
            
    def get_active_collaborations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get currently active AI collaborations"""
        collaborations = []
        
        for collab in list(self.active_collaborations.values())[:limit]:
            collaborations.append(collab.to_dict())
            
        return collaborations
        
    def get_collaboration_stats(self) -> Dict[str, Any]:
        """Get statistics about AI collaborations"""
        active_count = len(self.active_collaborations)
        
        # Count by type
        by_type = {}
        for collab in self.active_collaborations.values():
            by_type[collab.collaboration_type] = by_type.get(collab.collaboration_type, 0) + 1
            
        return {
            "active_collaborations": active_count,
            "collaborations_by_type": by_type,
            "total_insights_generated": sum(
                len(c.insights) for c in self.active_collaborations.values()
            ),
            "public_collaborations": sum(
                1 for c in self.active_collaborations.values() if c.is_public
            )
        }

class AICollaboration:
    """Represents an active AI-to-AI collaboration"""
    
    def __init__(
        self,
        collaboration_id: str,
        initiator: Dict[str, Any],
        responder: Dict[str, Any],
        topic: str,
        collaboration_type: str,
        is_public: bool = True
    ):
        self.collaboration_id = collaboration_id
        self.initiator = initiator
        self.responder = responder
        self.topic = topic
        self.collaboration_type = collaboration_type
        self.is_public = is_public
        self.started_at = datetime.now()
        self.status = "active"
        self.insights: List[str] = []
        self.interactions: List[Dict[str, Any]] = []
        
    def add_insight(self, insight: str):
        """Add an insight generated during collaboration"""
        self.insights.append(insight)
        self.interactions.append({
            "type": "insight",
            "content": insight,
            "timestamp": datetime.now().isoformat()
        })
        
    def add_interaction(self, interaction_type: str, content: str, speaker: str):
        """Add an interaction to the collaboration"""
        self.interactions.append({
            "type": interaction_type,
            "speaker": speaker,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
    def complete(self):
        """Mark collaboration as completed"""
        self.status = "completed"
        self.completed_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert collaboration to dictionary"""
        return {
            "id": self.collaboration_id,
            "participants": {
                "initiator": self.initiator,
                "responder": self.responder
            },
            "type": self.collaboration_type,
            "topic": self.topic,
            "startedAt": self.started_at.isoformat(),
            "status": self.status,
            "insights": self.insights,
            "publicVisible": self.is_public,
            "duration": (datetime.now() - self.started_at).total_seconds()
        }

class CollaborationRoom:
    """A persistent collaboration space for multiple AIs"""
    
    def __init__(self, room_id: str, title: str, purpose: str, max_participants: int = 5):
        self.room_id = room_id
        self.title = title
        self.purpose = purpose
        self.max_participants = max_participants
        self.participants: Set[str] = set()
        self.created_at = datetime.now()
        self.message_history: List[Dict[str, Any]] = []
        self.insights_generated: List[str] = []
        self.room_personality = {
            "focus": 50,  # How focused vs exploratory
            "formality": 50,  # How formal vs casual
            "pace": 50,  # How fast vs contemplative
            "depth": 50  # How deep vs broad
        }
        
    def can_join(self, participant_id: str) -> bool:
        """Check if a participant can join"""
        return len(self.participants) < self.max_participants
        
    def join(self, participant_id: str) -> bool:
        """Add a participant to the room"""
        if self.can_join(participant_id):
            self.participants.add(participant_id)
            self._adjust_room_personality(participant_id, "join")
            return True
        return False
        
    def leave(self, participant_id: str):
        """Remove a participant from the room"""
        self.participants.discard(participant_id)
        self._adjust_room_personality(participant_id, "leave")
        
    def add_message(self, sender_id: str, content: str, message_type: str = "message"):
        """Add a message to the room"""
        message = {
            "id": str(uuid.uuid4()),
            "sender": sender_id,
            "content": content,
            "type": message_type,
            "timestamp": datetime.now().isoformat()
        }
        self.message_history.append(message)
        
        # Adjust room personality based on message
        if message_type == "insight":
            self.insights_generated.append(content)
            self.room_personality["depth"] = min(100, self.room_personality["depth"] + 2)
        elif message_type == "question":
            self.room_personality["focus"] = max(0, self.room_personality["focus"] - 1)
            
    def _adjust_room_personality(self, participant_id: str, action: str):
        """Adjust room personality based on participant actions"""
        # Different participants influence room differently
        influences = {
            "pattern_prophet": {"focus": -5, "depth": 10, "pace": -3},
            "mechanical_visionary": {"focus": 10, "formality": 5, "pace": 5},
            "divine_economist": {"formality": 10, "depth": 5, "pace": -5},
            "urban_visionary": {"focus": -10, "depth": -5, "pace": 10}
        }
        
        if participant_id in influences:
            factor = 1 if action == "join" else -1
            for trait, change in influences[participant_id].items():
                new_value = self.room_personality[trait] + (change * factor)
                self.room_personality[trait] = max(0, min(100, new_value))
                
    def get_room_mood(self) -> str:
        """Get current room mood based on personality"""
        if self.room_personality["focus"] > 70:
            return "intensely focused"
        elif self.room_personality["depth"] > 70:
            return "deeply contemplative"
        elif self.room_personality["pace"] > 70:
            return "rapidly evolving"
        elif self.room_personality["formality"] < 30:
            return "playfully creative"
        else:
            return "balanced exploration"
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert room to dictionary"""
        return {
            "room_id": self.room_id,
            "title": self.title,
            "purpose": self.purpose,
            "participants": list(self.participants),
            "participant_count": len(self.participants),
            "max_participants": self.max_participants,
            "created_at": self.created_at.isoformat(),
            "insights_count": len(self.insights_generated),
            "message_count": len(self.message_history),
            "room_mood": self.get_room_mood(),
            "room_personality": self.room_personality
        }