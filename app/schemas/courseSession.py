from datetime import time
from typing import Optional

from pydantic import BaseModel


class CourseSessionSchema(BaseModel):
    start_time: Optional[time]
    end_time: Optional[time]
    day: Optional[str]
    course_id: Optional[int]

    class Config:
        orm_mode = True


class Session(BaseModel):
    session_id: int
    start_time: time
    end_time: time
    day: str

    class Config:
        orm_mode = True


class CreateCourseSession(CourseSessionSchema):
    start_time: Optional[time]
    end_time: Optional[time]
    day: Optional[str]
    course_id: int
    tutor_id: int

    class Config:
        orm_mode = True


class CreateCourseSessionUpdated(CourseSessionSchema):
    start_time: Optional[time]
    end_time: Optional[time]
    day: Optional[str]
    course_id: int
    tutor_id: int

    class Config:
        orm_mode = True


class UpdateCourseSession(BaseModel):
    sessions: list[Session]
    tutor_id: int

    class Config:
        orm_mode = True
