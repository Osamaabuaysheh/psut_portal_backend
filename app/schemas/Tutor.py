from pydantic import BaseModel
from typing import Optional


class TutorSchema(BaseModel):
    tutor_id: Optional[int]
    tutor_name: Optional[str]
    gpa: Optional[float]
    year: Optional[int]
    student_id: Optional[int]

    class Config:
        orm_mode = True


class TutorCreate(TutorSchema):
    tutor_name: str
    gpa: float
    year: int
    student_id: int


class TutorUpdate(TutorSchema):
    pass
