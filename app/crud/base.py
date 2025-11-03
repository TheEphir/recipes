from typing import Any, Generic, TypeVar, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, update
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateShemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model:type[ModelType]):
        self.model = model

    
    async def get(self, db:AsyncSession, id:UUID):
        result = await db.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()
    
    
    async def get_multi(self, db:AsyncSession, *, skip:int=0, limit:int=100):
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalar().all()
    
    
    async def create(self, db:AsyncSession, *, obj_in: CreateSchemaType):
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    
    async def update(self, db:AsyncSession, *, db_obj:ModelType, obj_in: UpdateSchemaType):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)        
            
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
        
    
    async def remove(self, db:AsyncSession, *, id:UUID):
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.commit()
        
        return obj
    
    
    