from typing import Optional

from pydantic import BaseModel


class CourseRequestsSchema(BaseModel):
    course_id: Optional[int] = None
    student_id: Optional[int] = None

    class Config:
        orm_mode = True


class CreateCourseRequest(CourseRequestsSchema):
    course_id: int
    student_id: int

    class Config:
        orm_mode = True


class UpdateCourseRequest(CourseRequestsSchema):
    pass

    class Config:
        orm_mode = True
