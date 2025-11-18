from fastapi import APIRouter
from app.api.routes import auth_routes, users, recipes

router = APIRouter()

router.include_router(auth_routes.router, prefix="/auth")
router.include_router(users.router, prefix="/users")
router.include_router(recipes.router, prefix="/recipes")

