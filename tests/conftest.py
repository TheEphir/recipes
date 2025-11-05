import os
import pytest
import asyncio
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base
from app.schemas.recipes import RecipeCreate
from app.schemas.users import UserCreate
from app.crud.users import user as crud_user
from app.crud.recipes import recipe as crud_recipe

load_dotenv()
DATABASE_URL = "sqlite+aiosqlite:///:memory:" # in memory db   O_O

engine = create_async_engine(DATABASE_URL, echo=False)
local_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with local_session as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        

@pytest.fixture
async def test_user(db_session: AsyncSession):
    user_in = UserCreate(
        username="testuser",
        email="test@a.com",
        password="supapass123",
        first_name="test",
        last_name="user"
    )
    return await crud_user.create(db=db_session, obj_in=user_in)


@pytest.fixture
async def test_recipe(db_session: AsyncSession):
    recipe_in = RecipeCreate(
        title="test soup",
        ingredients=["water","onion"],
        instrunctions="boil",
        category="Soup",
        is_public=True
    )
    data = recipe_in.model_dump()
    data["user_id"] = test_user.id
    return await crud_recipe.create(db=db_session, obj_in=recipe_in)