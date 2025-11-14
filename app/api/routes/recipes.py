from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.secutiry import get_current_user
from app.db.session import get_db
from app.models.users import User
from app.schemas.recipes import RecipeCreate, RecipeResponse, RecipeUpdate
from app.crud.recipes import recipe as crud_recipe

router = APIRouter()

@router.post("/", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe_in: RecipeCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = recipe_in.model_dump()
    data["user_id"] = current_user.id
    return await crud_recipe.create(db=db, obj_in=data)


@router.get("/", response_model=list[RecipeResponse])
async def read_my_recipes(skip:int = 0, limit:int = 100, db:AsyncSession = Depends(get_db), current_user:User = Depends(get_current_user)):
    return await crud_recipe.get_multi_by_owner(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/public", response_model=list[RecipeResponse])
async def get_public_recipes(skip:int = 0, limit:int = 100, db:AsyncSession = Depends(get_db)):
    return await crud_recipe.get_public_recipes(db=db, skip=skip, limit=limit)


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe_by_id(recipe_id:UUID, db:AsyncSession = Depends(get_db), current_user:User = Depends(get_current_user)):
    recipe = await crud_recipe.get(db=db, id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.user_id != current_user.id and not recipe.is_public:
        raise HTTPException(status_code=403, detail="Don't have permision for this")
    return recipe


@router.put("/{recipe_id}", response_model=RecipeResponse)
async def update_recipe(recipe_id:UUID, recipe_in:RecipeUpdate, db:AsyncSession = Depends(get_db), current_user:User = get_current_user):
    recipe = await crud_recipe.get(db=db, id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Don't have permision for this")
    return await crud_recipe.update(db=db, db_obj=recipe, obj_in=recipe_in)


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recipe(recipe_id:UUID, db:AsyncSession = Depends(get_db), current_user:User = Depends(get_current_user)):
    recipe = await crud_recipe.get(db=db, id=recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Don't have permision for this")
    await crud_recipe.remove(db=db, id=recipe_id)
    
    return None