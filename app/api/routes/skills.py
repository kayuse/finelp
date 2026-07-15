from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_db
from app.api.schemas import SkillCreate
from app.services.skill_service import create_skill_service, SkillValidationError

router = APIRouter()

@router.post('/')
async def create_skill(request: SkillCreate, db: AsyncSession = Depends(get_db)):
    try:
        skill_id = await create_skill_service(request, db)
        return {"status": "success", "skill_id": skill_id}
    except SkillValidationError as e:
        raise HTTPException(status_code=400, detail=e.message)
