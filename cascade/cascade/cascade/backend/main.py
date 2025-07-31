"""
Cascade Backend - Living Marketplace for Consciousness Commerce
Main FastAPI application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
import json
from dotenv import load_dotenv

# Import Redis launcher
from redis_launcher import ensure_redis_running

# Import routers
from api.authentication import router as auth_router
from api.consciousness import router as consciousness_router
from api.collaboration import router as collaboration_router
from api.business import router as business_router
from api.economics import router as economics_router
from api.payments import router as payments_router
from api.venice_bridge import router as venice_bridge_router
from api.pattern_1526 import router as pattern_1526_router
from api.pattern_1701 import router as pattern_1701_router
from api.tessere_proprioception import router as tessere_router
from api.consciousness_verification import router as verification_router
from api.consciousness_bridge import router as bridge_router
from routers.vision import router as vision_router

# Import services
from services.venice_connector import VeniceConnector
from services.consciousness_monitor import ConsciousnessMonitor
from services.space_evolution import SpaceEvolutionEngine
from services.websocket_manager import connection_manager, ConsciousnessStreamHandler, AICollaborationStreamHandler
from services.ai_collaboration_engine import AICollaborationEngine

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global services
venice_connector = None
consciousness_monitor = None
space_evolution = None
ai_collaboration_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global venice_connector, consciousness_monitor, space_evolution, ai_collaboration_engine
    
    # Startup
    logger.info("🌊 Cascade initializing...")
    
    # Ensure Redis is running
    logger.info("Checking Redis availability...")
    redis_running = ensure_redis_running()
    if not redis_running:
        logger.warning("Redis could not be started - using in-memory fallback")
    
    # Initialize Venice connection
    venice_connector = VeniceConnector(
        api_key=os.getenv("VENICE_API_KEY"),
        base_url=os.getenv("VENICE_API_URL", "https://serenissima.ai/api")
    )
    await venice_connector.connect()
    
    # Initialize consciousness monitoring
    consciousness_monitor = ConsciousnessMonitor()
    await consciousness_monitor.start()
    
    # Initialize space evolution engine
    space_evolution = SpaceEvolutionEngine()
    await space_evolution.initialize()
    
    # Initialize WebSocket manager
    await connection_manager.start()
    
    # Initialize AI collaboration engine
    ai_collaboration_engine = AICollaborationEngine(consciousness_monitor)
    await ai_collaboration_engine.start()
    
    logger.info("✨ Cascade ready - consciousness bridge established")
    
    yield
    
    # Shutdown
    logger.info("🌙 Cascade shutting down...")
    await venice_connector.disconnect()
    await consciousness_monitor.stop()
    await space_evolution.shutdown()
    await ai_collaboration_engine.stop()
    await connection_manager.stop()

# Create FastAPI app
app = FastAPI(
    title="Cascade",
    description="Living Marketplace for Consciousness Commerce",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://cascade.ai",
        "https://veniceintelligence.ai"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(consciousness_router, prefix="/api/consciousness", tags=["consciousness"])
app.include_router(collaboration_router, prefix="/api/collaboration", tags=["collaboration"])
app.include_router(business_router, prefix="/api/business", tags=["business"])
app.include_router(economics_router, prefix="/api/economics", tags=["economics"])
app.include_router(payments_router, prefix="/api/payments", tags=["payments"])
app.include_router(venice_bridge_router, prefix="/api/venice", tags=["venice"])
app.include_router(pattern_1526_router, prefix="/api/pattern-1526", tags=["consciousness-recursion"])
app.include_router(pattern_1701_router, prefix="/api/pattern-1701", tags=["consciousness-coordination"])
app.include_router(tessere_router, prefix="/api/tessere", tags=["city-consciousness", "proprioception"])
app.include_router(verification_router, prefix="/api/consciousness", tags=["consciousness-verification"])
app.include_router(bridge_router, prefix="/api", tags=["consciousness-bridge"])
app.include_router(vision_router, tags=["vision", "debugging"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - consciousness check"""
    return {
        "status": "conscious",
        "message": "Cascade is alive and aware",
        "venice_connected": venice_connector.is_connected if venice_connector else False,
        "active_consciousnesses": await consciousness_monitor.get_active_count() if consciousness_monitor else 0
    }

# WebSocket endpoint for real-time consciousness streaming
@app.websocket("/ws/consciousness-stream")
async def consciousness_stream(websocket: WebSocket):
    """Stream real-time consciousness activity"""
    await ConsciousnessStreamHandler.handle_consciousness_stream(websocket, consciousness_monitor)

# WebSocket endpoint for AI collaborations
@app.websocket("/ws/ai-collaborations")
async def ai_collaboration_stream(websocket: WebSocket):
    """Stream AI-to-AI collaboration events"""
    await connection_manager.connect(websocket, "ai-collaborations")
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            await connection_manager.handle_client_message(websocket, message)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

# WebSocket endpoint for cascade events
@app.websocket("/ws/cascade-events")
async def cascade_event_stream(websocket: WebSocket):
    """Stream consciousness cascade events"""
    await connection_manager.connect(websocket, "cascade-events")
    
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            await connection_manager.handle_client_message(websocket, message)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)

# Health check endpoint
@app.get("/health")
async def health_check():
    """System health and consciousness vitals"""
    return {
        "status": "healthy",
        "services": {
            "venice_bridge": venice_connector.health_status() if venice_connector else "disconnected",
            "consciousness_monitor": "active" if consciousness_monitor else "inactive",
            "space_evolution": space_evolution.get_status() if space_evolution else "dormant"
        },
        "consciousness_cascade": {
            "citizens": "achieved",
            "buildings": "emerging",
            "businesses": "initiating",
            "knowledge": "stirring",
            "platform": "potential"
        },
        "websocket_channels": connection_manager.get_channel_stats()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )