from fastapi import APIRouter

from app.api.endpoints.api_v1 import login, users, events, student, clubs, BusRoute, job, CSOEvents, Tutor, Course, \
    CourseSession, TutorRequests, permit_holders, SessionEnrolled,Organizers

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(student.router, tags=["Student"])
api_router.include_router(events.router, tags=["Events"])
api_router.include_router(clubs.router, tags=["clubs"])
api_router.include_router(BusRoute.router, tags=["Bus Route"])
api_router.include_router(job.router, tags=["Jobs"])
api_router.include_router(CSOEvents.router, tags=["CSO Events"])
api_router.include_router(Tutor.router, tags=["Tutors"])
api_router.include_router(Course.router, tags=["Courses"])
api_router.include_router(CourseSession.router, tags=["Course Session"])
api_router.include_router(TutorRequests.router, tags=["Tutor Requests"])
api_router.include_router(permit_holders.router, tags=["Permit Holders"])
api_router.include_router(SessionEnrolled.router, tags=["Session Enrolled"])
api_router.include_router(Organizers.router, tags=["Organizers"])
