from pydantic import BaseModel
from typing import Optional


class CourseSchema(BaseModel):
    course_id: Optional[int]
    course_name: Optional[str]
    college: Optional[str]

    class Config:
        orm_mode = True


class CreateCourse(CourseSchema):
    course_id: int
    course_name: str
    college: str

    class Config:
        orm_mode = True


class UpdateCourse(CourseSchema):
    course_id: int
    course_name: str
    student_id: Optional[int]

    class Config:
        orm_mode = True
