from turtle import title
import pytest

from app.schemas.recipes import RecipeCreate, RecipeUpdate
from app.crud.recipes import recipe as crud_recipe

pytestmark = pytest.mark.asyncio


async def test_create_recipe(db_session, test_user):
    recipe_in = RecipeCreate(
        title="test recipe",
        ingredients=["ing1","ing2","ing2","ing5","ing4","ing3"],
        instrunctions="cut, cake it boil",
        category="soup",
        prep_time=30,
        is_public=True
        )
    data = recipe_in.model_dump()
    data["user_id"] = test_user.id
    
    db_recipe = await crud_recipe.create(db=db_session, obj_in=RecipeCreate(**data))
    
    assert db_recipe.title == data["title"]
    assert db_recipe.user_id == data["user_id"]
    assert db_recipe.ingredients == ["ing1","ing2","ing2","ing5","ing4","ing3"]
    assert not db_recipe.is_public
    

async def test_get_recipe(db_session, test_recipe):
    fetch = await crud_recipe.get(db=db_session, id=test_recipe.id)
    assert fetch.id == test_recipe.id
    assert fetch.title == test_recipe.title
    

async def test_get_multi_by_owner(db_session, test_user, test_recipe):
    second_recipe = RecipeCreate(title="second", ingredients=["only","one"], instrunctions="be")
    second_data = second_recipe.model_dump()
    second_data["user_id"] = test_user.id
    
    await crud_recipe.create(db=db_session, obj_in=second_data)
    
    recipes = crud_recipe.get_multi_by_owner(db=db_session, user_id=test_user.id)
    
    assert len(recipes) >= 2
    assert any(r.title == "test soup" for r in recipes)
    

async def test_get_public_recipes(db_session, test_recipe):
    test_recipe.is_public = True
    await db_session.commit()
    
    public = await crud_recipe.get_public_recipes(db_session)
    assert len(public) >= 1
    assert public[0].title == "test soup"
    
    
async def test_update_recipe(db_session, test_recipe):
    update_data = RecipeUpdate(title="updated title")
    updated = await crud_recipe.update(db=db_session, db_obj=test_recipe, obj_in=update_data)
    
    assert updated.title == "updated title"
    assert updated.is_public is True
    assert updated.ingredients == test_recipe.ingredients
    

async def test_remove_recipe(db_session, test_recipe):
    deleted = await crud_recipe.remove(db=db_session, id=test_recipe.id)
    assert deleted.id == test_recipe.id
    
    fetch = await crud_recipe.get(db=db_session, id=test_recipe.id)
    assert fetch is None
    