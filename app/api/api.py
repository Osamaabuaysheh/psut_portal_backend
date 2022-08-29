from fastapi import APIRouter
from app.api.endpoints.api_v1 import login

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
