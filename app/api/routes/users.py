from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserResponse
from crud.users import user as crud_user
from db.session import get_db
from core.secutiry import get_current_user
from models.users import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_users_me(current_user: User = Depends(get_db)):
    return current_user


@router.get("/", response_model=list[UserResponse]) # for admin usage
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Don't have permission for this")
    return await crud_user.get_multi(db=db, skip=skip, limit=limit)

