from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentSchema(BaseModel):
    student_id: Optional[int] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    colleage: Optional[str] = None
    year: Optional[int] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True


class StudentOut(StudentSchema):
    student_id: int
    pass


class StudentCreate(StudentSchema):
    student_id: int
    full_name: str
    email: EmailStr
    hashed_password: str
    colleage: str
    year: int


class StudentIn(StudentSchema):
    student_id: int
    hashed_password = str
    pass
