from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import redis
import json
import time

from .config import settings
from .logger import logger
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget
from utils.mock_llm import ask

# --- Models ---
class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)

class AskResponse(BaseModel):
    user_id: str
    question: str
    answer: str
    history_count: int
    timestamp: str

# --- Global Stats ---
START_TIME = time.time()
stats = {"requests": 0, "errors": 0}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Agent starting up...")
    try:
        app.state.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        app.state.redis.ping()
        logger.info("Successfully connected to Redis!")
    except Exception as e:
        logger.error(f"FATAL: Could not connect to Redis at {settings.REDIS_URL}. Error: {str(e)}")
    yield
    logger.info("Agent shutting down gracefully...")
    if hasattr(app.state, 'redis'):
        app.state.redis.close()


app = FastAPI(
    title="Ultimate AI Agent",
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.LOG_LEVEL == "DEBUG" else None
)

# ✅ Security & Analytics Middleware
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    stats["requests"] += 1
    try:
        response: Response = await call_next(request)
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        
        duration = round((time.time() - start_time) * 1000, 2)
        logger.info(json.dumps({
            "event": "http_request",
            "method": request.method,
            "path": request.url.path,
            "duration_ms": duration,
            "status": response.status_code
        }))
        return response
    except Exception as e:
        stats["errors"] += 1
        logger.error(f"Request failed: {str(e)}")
        raise

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "uptime": round(time.time() - START_TIME, 1)}

@app.get("/ready")
def ready():
    try:
        app.state.redis.ping()
        return {"status": "ready"}
    except Exception:
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/metrics")
def get_metrics(_: str = Depends(verify_api_key)):
    return {
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "total_requests": stats["requests"],
        "total_errors": stats["errors"],
        "version": "3.0.0"
    }

@app.post("/ask", response_model=AskResponse)
async def ask_agent(
    body: AskRequest,
    user_id: str = Depends(verify_api_key),
    _rate_limit = Depends(check_rate_limit),
    _budget = Depends(check_budget)
):
    question = body.question
    history_key = f"history:{user_id}"
    history = app.state.redis.lrange(history_key, 0, 5)
    
    answer = ask(question)
    
    app.state.redis.lpush(history_key, f"User: {question}", f"AI: {answer}")
    app.state.redis.ltrim(history_key, 0, 10)
    
    return AskResponse(
        user_id=user_id,
        question=question,
        answer=answer,
        history_count=len(history) // 2,
        timestamp=datetime.now(timezone.utc).isoformat()
    )



