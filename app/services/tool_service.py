from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.db.models import Tool
from app.api.schemas import APIToolCreate

async def create_tool_service(request: APIToolCreate, db: AsyncSession) -> str:
    tool_id = request.id or str(uuid.uuid4())
    
    new_tool = Tool(
        id=tool_id,
        name=request.name,
        description=request.description,
        type=request.type,
        method=request.method,
        url=request.url,
        cache_ttl_minutes=request.cache_ttl_minutes,
        auth_tool_id=request.auth_tool_id,
        headers=request.headers,
        request_params=request.request_params,
        response_params=request.response_params,
        body_schema=request.body_schema,
        timeout_seconds=request.timeout_seconds,
        retries=request.retries
    )
    db.add(new_tool)
    await db.commit()
    await db.refresh(new_tool)
    
    return new_tool.id
