from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import user as crud_user
from schemas.users import UserCreate, UserResponse
from db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud_user.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="User already registered")

    return await crud_user.create(db, obj_in=user_in)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud_user.get_by_email(db, email=form_data.username)
    if not user or not crud_user.pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    
    return{"access_token":"fake-jwt", "token_type":"bearer"} # Should change it after making it work
