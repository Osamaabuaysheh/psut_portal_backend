from fastapi import APIRouter
from app.api.endpoints.api_v1 import login, users, events, student, clubs, BusRoute, job

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(student.router, tags=["Student"])
api_router.include_router(events.router, tags=["Events"])
api_router.include_router(clubs.router, tags=["clubs"])
api_router.include_router(BusRoute.router, tags=["Bus Route"])
api_router.include_router(job.router, tags=["Jobs"])
