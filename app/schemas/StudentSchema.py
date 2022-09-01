from pydantic import BaseModel, EmailStr
from typing import Optional


class StudentSchema(BaseModel):
    id: Optional[int] = None
    full_name: Optional[str] = ""
    email: EmailStr = ""
    hashed_password: Optional[str] = None
    colleage: Optional[str] = None

    class Config:
        orm_mode = True


class StudentOut(StudentSchema):
    id: int
    pass


class StudentIn(StudentSchema):
    id: int
