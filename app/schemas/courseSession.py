from pydantic import BaseModel
from typing import Optional
from datetime import time


class CourseSessionSchema(BaseModel):
    start_time: Optional[time]
    end_time: Optional[time]
    day: Optional[str]
    course_id: Optional[int]

    class Config:
        orm_mode = True


class CreateCourseSession(CourseSessionSchema):
    start_time: time
    end_time: time
    day: str
    course_id: int
    student_id: int

    class Config:
        orm_mode = True


class UpdateCourseSession(CourseSessionSchema):
    pass
