from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from crud.users import user as crud_user
from db.session import get_db

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str=Depends(oauth_scheme), db:AsyncSession=Depends(get_db)):
    user = await crud_user.get_by_email(db, email="test@user.com")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentification credentials"
        )
    
    return user

