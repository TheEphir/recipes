import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    
    
class UserUpdate(UserBase):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    is_active: bool = True
    is_admin: bool = False
    
    class Config:
        from_atttbutes = True # for work with SQLAlchemy