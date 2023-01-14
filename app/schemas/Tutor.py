from typing import Optional

from pydantic import BaseModel


class TutorSchema(BaseModel):
    tutor_id: Optional[int]
    tutor_name: Optional[str]
    gpa: Optional[float]
    student_id: Optional[int]

    class Config:
        orm_mode = True


class TutorCreate(TutorSchema):
    student_id: int


class TutorUpdate(TutorSchema):
    pass
