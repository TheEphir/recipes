from typing import List, Optional
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID
from app.crud.base import CRUDBase
from app.models.recipes import Recipe
from app.schemas.recipes import RecipeCreate, RecipeUpdate


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    async def get_multi_by_owner(self, db:AsyncSession, *, user_id:UUID, skip:int=0, limit:int=100) -> List[Recipe]:
        res = await db.execute(select(Recipe).where(Recipe.user_id == user_id).offset(skip).limit(limit))
        return res.scalars().all()
    
    
    async def get_public_recipes(self, db:AsyncSession, *, skip:int=0, limit:int=100) -> List[Recipe]:
        res = await db.execute(select(Recipe).where(Recipe.is_public==True).offset(skip).limit(limit))
        return res.scalars().all()
    
    
    async def search_by_title(self, db:AsyncSession, *, title:str, user_id:Optional[UUID] = None, skip:int=0, limit:int=100):
        filters = [Recipe.title.ilike(f"%{title}")]
        if user_id:
            filters.append(Recipe.user_id == user_id)
        
        res = await db.execute(select(Recipe).where(and_(*filters)).offset(skip).limit(limit))
        return res.scalars().all()
    

recipe = CRUDRecipe(Recipe)