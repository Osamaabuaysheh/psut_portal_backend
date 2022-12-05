from pydantic import BaseModel
from typing import Optional


class TutorRequestSchema(BaseModel):
    semster_completion: str
    grade: Optional[float]
    student_id: Optional[int]
    course_id: Optional[int]

    class Config:
        orm_mode = True


class TutorRequestCreate(TutorRequestSchema):
    semster_completion: str
    grade: float
    student_id: int
    course_id: int


class TutorRequestUpdate(TutorRequestSchema):
    pass
