from typing import Optional
from uuid import UUID
from warnings import deprecated

from fastapi import dependencies
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.users import User
from app.schemas.users import UserCreate


class CRUDUser(CRUDBase[User, UserCreate, UserCreate]):
    async def get_by_email(self, db: AsyncSession, *, email:str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email==email))
        return result.scalar_one_or_none()
    
    
    async def get_by_username(self, db: AsyncSession, *, username:str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username==username))
        return result.scalar_one_or_none()
    
    async def create(self, db:AsyncSession, *, obj_in:UserCreate) -> User:
        from passlib.context import CryptContext
        pwd_context= CryptContext(schemes=["bcrypt"], deprecated="auto") 
        hashed_password = pwd_context.hash(obj_in.password)

        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            password_hash=hashed_password,
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
        )

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
user = CRUDUser(User)