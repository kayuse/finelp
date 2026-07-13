from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.dependencies import get_db
from app.db.redis import get_redis
from app.agents.workflows import run_agent
from pydantic import BaseModel
from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/db-test")
async def db_test(db: AsyncSession = Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"db_status": "connected", "result": result.scalar()}

@router.get("/redis-test")
async def redis_test():
    redis = await get_redis()
    await redis.set("test_key", "test_value")
    val = await redis.get("test_key")
    return {"redis_status": "connected", "test_value": val}

@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    response = await run_agent(request.message)
    return {"response": response}

@router.post("/trigger-task")
async def trigger_task(message: str):
    redis_settings = RedisSettings(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    redis_pool = await create_pool(redis_settings)
    await redis_pool.enqueue_job('sample_background_task', message)
    return {"status": "Task triggered"}
