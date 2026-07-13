from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.api.schemas import UserCreate, UserLogin, Token
from app.db.models import User
from app.core.security import get_password_hash, verify_password, create_access_token


class AuthService:
    @staticmethod
    async def create_user(user_in: UserCreate, db: AsyncSession) -> User:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == user_in.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists."
            )

        # Create new user
        hashed_password = get_password_hash(user_in.password)
        new_user = User(
            email=user_in.email,
            firstname=user_in.firstname,
            hashed_password=hashed_password
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def authenticate_user(user_in: UserLogin, db: AsyncSession) -> dict:
        # Find user by email
        result = await db.execute(select(User).where(User.email == user_in.email))
        user = result.scalars().first()
        
        if not user or not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

        # Generate JWT
        access_token = create_access_token(subject=user.email)
        
        return {"access_token": access_token, "token_type": "bearer"}
