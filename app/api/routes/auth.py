from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import UserCreate, UserLogin, UserResponse, Token
from app.db.postgres import AsyncSessionLocal
from app.services.auth_service import AuthService

router = APIRouter()

# Dependency to get DB session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService.create_user(user_in, db)

@router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    return await AuthService.authenticate_user(user_in, db)
