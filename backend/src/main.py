from fastapi import FastAPI

from src.core.config import settings
from src.modules.auth.router import router as auth_router
from src.modules.health.router import router as health_router
from src.modules.users.models import User

app = FastAPI(title=settings.app_name)

app.include_router(health_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "FitVision API is running"}