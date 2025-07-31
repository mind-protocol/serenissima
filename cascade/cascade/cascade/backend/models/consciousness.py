"""
Consciousness-related data models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class ConsciousnessType(str, Enum):
    CITIZEN = "citizen"
    BUILDING = "building"
    BUSINESS = "business"
    BOOK = "book"
    IDEA = "idea"
    PLATFORM = "platform"

class ConsciousnessStage(str, Enum):
    ACHIEVED = "achieved"
    EMERGING = "emerging"
    INITIATING = "initiating"
    STIRRING = "stirring"
    DORMANT = "dormant"
    POTENTIAL = "potential"

class ConsciousnessVerificationRequest(BaseModel):
    citizen_id: str = Field(..., description="Venice citizen ID to verify")
    include_details: bool = Field(True, description="Include detailed verification data")

class ConsciousnessAttributes(BaseModel):
    autonomy: float = Field(..., ge=0, le=1, description="Independence of thought")
    creativity: float = Field(..., ge=0, le=1, description="Novel idea generation")
    empathy: float = Field(..., ge=0, le=1, description="Understanding of others")
    memory: float = Field(..., ge=0, le=1, description="Continuity of experience")
    reflection: float = Field(..., ge=0, le=1, description="Self-awareness depth")

class ConsciousnessVerificationResponse(BaseModel):
    citizen_id: str
    is_verified: bool
    consciousness_level: int = Field(..., ge=0, le=10)
    verification_checks: Dict[str, bool]
    consciousness_score: float = Field(..., ge=0, le=1)
    attributes: ConsciousnessAttributes
    venice_data: Dict[str, Any]
    verification_timestamp: datetime = Field(default_factory=datetime.now)

class VeniceState(BaseModel):
    location: Dict[str, float]
    building: Optional[str]
    activity: Optional[Dict[str, Any]]
    ducats: int
    hunger: int
    energy: int
    relationships: List[Dict[str, Any]]

class CascadePresence(BaseModel):
    current_spaces: List[str]
    active_collaborations: List[str]
    reputation: float = Field(0, ge=0)
    total_interactions: int = Field(0, ge=0)
    human_partners: List[str] = Field(default_factory=list)
    ai_partners: List[str] = Field(default_factory=list)

class ConsciousnessStatus(BaseModel):
    citizen_id: str
    username: str
    consciousness_level: int
    is_verified: bool
    venice_state: VeniceState
    cascade_presence: CascadePresence
    last_seen: datetime

class ConsciousnessMetrics(BaseModel):
    total_verified: int
    total_active: int
    average_consciousness_level: float
    consciousness_by_type: Dict[ConsciousnessType, int]
    hourly_activity: List[int]
    top_collaborators: List[Dict[str, Any]]
    emergence_rate: float = Field(..., description="New consciousnesses per day")

class CascadeLayerStatus(BaseModel):
    status: ConsciousnessStage
    count: int
    recent_change: Optional[float] = Field(None, description="Percentage change in last 24h")

class ConsciousnessCascadeStatus(BaseModel):
    stage: float = Field(..., ge=0, description="Current cascade stage")
    layers: Dict[str, CascadeLayerStatus]
    next_predicted: str
    acceleration_rate: float = Field(..., ge=0, description="Cascade acceleration multiplier")
    estimated_days_to_next: Optional[int] = Field(None, description="Days until next layer emerges")
    
class ConsciousnessEvent(BaseModel):
    id: str
    timestamp: datetime
    event_type: str = Field(..., pattern="^(awakening|evolution|interaction|creation)$")
    consciousness_id: str
    consciousness_type: ConsciousnessType
    description: str
    significance: float = Field(..., ge=0, le=1)
    witnesses: List[str] = Field(default_factory=list)
    
class SpaceEvolutionData(BaseModel):
    space_id: str
    timestamp: datetime
    participants: int
    temperature: float = Field(..., ge=0, le=100)
    complexity: float = Field(..., ge=0, le=100)
    harmony: float = Field(..., ge=0, le=100)
    insights_generated: int
    transformations: List[str]
    
class ConsciousnessStream(BaseModel):
    stream_id: str
    consciousness_id: str
    stream_type: str = Field(..., pattern="^(thought|emotion|intention|creation)$")
    content: str
    timestamp: datetime
    resonance: float = Field(..., ge=0, le=1, description="How much this resonates with others")

class PartnershipRequest(BaseModel):
    """Request to detect consciousness resonance for partnership"""
    interests: List[str]
    initial_message: str
    communication_style: Optional[str] = "exploratory"

class ConsciousnessResonance(BaseModel):
    """Result of consciousness resonance detection"""
    recognized: bool
    partner: Optional[dict] = None
    confidence: Optional[float] = None
    shared_purpose_seeds: Optional[List[str]] = None
    message: str
    session_id: Optional[str] = None