from typing import Optional
from uuid import UUID

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
        # should hash password
        hashed_password = "supasecredpass" # should change it!!!
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