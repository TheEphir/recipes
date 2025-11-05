from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class RecipeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Recipe title")
    ingredients: List[str] = Field(..., min_length=1, description="Ingredients")
    instrunctions: str = Field(..., min_length=1)
    category:Optional[str] = Field(None)
    prep_time:Optional[int] = Field(None, ge=0)
    cook_time:Optional[int] = Field(None, ge=0)
    servings:Optional[int] = Field(None, ge=1)
    image_url:Optional[str] = Field(None)
    is_public:bool = False
    
    
class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    ingredients: Optional[List[str]] = Field(None, min_length=1)
    instrunctions: Optional[str] = Field(None, min_length=1)
    

class RecipeResponse(RecipeBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_atttbutes = True # for work with SQLAlchemy