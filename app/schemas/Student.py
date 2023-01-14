from typing import Optional

from pydantic import BaseModel, EmailStr


class StudentSchema(BaseModel):
    student_id: Optional[int] = None
    full_name: Optional[str] = None
    full_name_arabic: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    colleage: Optional[str] = None
    year: Optional[int] = None
    url: Optional[str] = ""
    hours_completed: Optional[int] = None

    class Config:
        orm_mode = True


class StudentOut(StudentSchema):
    student_id: int
    pass


class StudentCreate(StudentSchema):
    student_id: int
    full_name: str
    full_name_arabic: str
    email: EmailStr
    hashed_password: str
    colleage: str
    year: int
    hours_completed: int


class StudentIn(StudentSchema):
    student_id: int
    hashed_password = str
