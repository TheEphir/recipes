from fastapi import FastAPI
from app.api.api_routes import router as api_router

app = FastAPI(title="Recipes API", version="1.0.0")

app.include_router(api_router, prefix="/v1")

@app.get("/")
async def root():
    return {"message":"Welcome to Recipes API"}