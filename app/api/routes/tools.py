from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.api.dependencies import get_db
from app.db.redis import get_redis
from app.agents.workflows import run_agent
from pydantic import BaseModel
from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings
import uuid
from app.api.schemas import APIToolCreate
from app.db.models import Tool
from app.services.tool_service import create_tool_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ToolRequest(BaseModel):
    tool_name: str
    tool_description: str

@router.post('/tools')
async def create_tool(request: APIToolCreate, db: AsyncSession = Depends(get_db)):
    try:
        tool_id = await create_tool_service(request, db)
        return {"status": "success", "tool_id": tool_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))