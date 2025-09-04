"""
FastAPI Backend for Computer Use Agent
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import asyncio
import base64
import json
import logging
from datetime import datetime
from pathlib import Path

from core import ComputerUseAgent
from core.base import Action, ActionType
from providers import ProviderFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Computer Use Agent API",
    description="AI-powered computer automation API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent instance
agent = None

# Request/Response models
class ActionRequest(BaseModel):
    type: str
    parameters: Dict[str, Any]
    timeout: Optional[float] = 30.0

class TaskRequest(BaseModel):
    description: str
    provider: Optional[str] = "anthropic"
    model: Optional[str] = "claude-3-opus"

class ActionResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    duration: float = 0.0

class ScreenshotResponse(BaseModel):
    image: str  # Base64 encoded
    timestamp: str
    resolution: tuple

class HealthResponse(BaseModel):
    status: str
    agent_ready: bool
    providers_available: List[str]

# Initialize agent on startup
@app.on_event("startup")
async def startup_event():
    """Initialize the agent on startup"""
    global agent
    try:
        config = {
            'enable_vision': True,
            'failsafe': True,
            'action_delay': 0.1
        }
        agent = ComputerUseAgent(config)
        logger.info("Computer Use Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}")

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health status"""
    return HealthResponse(
        status="healthy",
        agent_ready=agent is not None,
        providers_available=["anthropic", "openai", "bedrock", "vertex"]
    )

# Screenshot endpoint
@app.get("/screenshot", response_model=ScreenshotResponse)
async def capture_screenshot():
    """Capture current screenshot"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        screenshot = agent.capture_screenshot()
        if screenshot:
            # Convert PIL Image to base64
            import io
            buffer = io.BytesIO()
            screenshot.save(buffer, format="PNG")
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return ScreenshotResponse(
                image=image_base64,
                timestamp=datetime.now().isoformat(),
                resolution=screenshot.size
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to capture screenshot")
            
    except Exception as e:
        logger.error(f"Screenshot capture failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Execute action endpoint
@app.post("/execute", response_model=ActionResponse)
async def execute_action(request: ActionRequest):
    """Execute a single action"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        # Create action
        action = Action(
            type=ActionType(request.type),
            parameters=request.parameters,
            timeout=request.timeout
        )
        
        # Execute action
        result = agent.execute_action(action)
        
        return ActionResponse(
            success=result.success,
            data=result.data,
            error=result.error,
            duration=result.duration
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid action type: {e}")
    except Exception as e:
        logger.error(f"Action execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Execute task endpoint
@app.post("/task")
async def execute_task(request: TaskRequest, background_tasks: BackgroundTasks):
    """Execute a complex task"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        # Set provider if specified
        if request.provider:
            provider = ProviderFactory.create(request.provider)
            agent.set_provider(provider)
        
        # Execute task
        results = agent.execute_task(request.description)
        
        # Format results
        actions = []
        for action, result in zip(agent.get_history()[-len(results):], results):
            actions.append({
                "type": action[0].type.value,
                "parameters": action[0].parameters,
                "success": result.success,
                "error": result.error,
                "duration": result.duration
            })
        
        return {
            "success": all(r.success for r in results),
            "task": request.description,
            "actions": actions,
            "total_duration": sum(r.duration for r in results)
        }
        
    except Exception as e:
        logger.error(f"Task execution failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analyze screen endpoint
@app.post("/analyze")
async def analyze_screen(instruction: Optional[str] = None):
    """Analyze current screen"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        analysis = agent.analyze_screen(instruction)
        
        # Convert screenshot to base64 if present
        if analysis.get("screenshot"):
            import io
            buffer = io.BytesIO()
            analysis["screenshot"].save(buffer, format="PNG")
            analysis["screenshot"] = base64.b64encode(buffer.getvalue()).decode()
        
        return analysis
        
    except Exception as e:
        logger.error(f"Screen analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Session management endpoints
@app.get("/session/history")
async def get_session_history():
    """Get action history for current session"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        history = []
        for action, result in agent.get_history():
            history.append({
                "action": action.to_dict(),
                "result": result.to_dict()
            })
        
        return {"history": history, "count": len(history)}
        
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/save")
async def save_session(name: Optional[str] = None):
    """Save current session"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        if not name:
            name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        path = agent.record_session(f"sessions/{name}.json")
        
        return {"success": True, "path": path, "name": name}
        
    except Exception as e:
        logger.error(f"Failed to save session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/session/load/{name}")
async def load_session(name: str):
    """Load and replay a session"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        session_path = f"sessions/{name}.json"
        if not Path(session_path).exists():
            raise HTTPException(status_code=404, detail="Session not found")
        
        results = agent.replay_session(session_path)
        
        return {
            "success": all(r.success for r in results),
            "actions_replayed": len(results),
            "name": name
        }
        
    except Exception as e:
        logger.error(f"Failed to load session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/clear")
async def clear_session():
    """Clear current session history"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        agent.clear_history()
        
        return {"success": True, "message": "Session history cleared"}
        
    except Exception as e:
        logger.error(f"Failed to clear session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Provider management
@app.get("/providers")
async def list_providers():
    """List available providers"""
    return {
        "providers": [
            {"name": "anthropic", "models": ["claude-3-opus", "claude-3-sonnet"]},
            {"name": "openai", "models": ["gpt-4", "gpt-4-vision"]},
            {"name": "bedrock", "models": ["claude-v2", "claude-instant"]},
            {"name": "vertex", "models": ["claude-3-opus", "claude-3-sonnet"]}
        ]
    }

@app.post("/providers/set")
async def set_provider(provider: str, model: Optional[str] = None):
    """Set active provider"""
    try:
        if not agent:
            raise HTTPException(status_code=503, detail="Agent not initialized")
        
        provider_instance = ProviderFactory.create(provider, model=model)
        agent.set_provider(provider_instance)
        
        return {"success": True, "provider": provider, "model": model}
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to set provider: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket support for real-time updates
from fastapi import WebSocket
from typing import Set

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates"""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Handle incoming messages
            message = json.loads(data)
            
            if message.get("type") == "execute":
                # Execute action and broadcast result
                result = await execute_action(ActionRequest(**message["data"]))
                await manager.broadcast({
                    "type": "action_result",
                    "data": result.dict()
                })
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)