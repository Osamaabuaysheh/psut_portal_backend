from typing import Optional

from pydantic import BaseModel


class SessionEnrolledSchema(BaseModel):
    enroll_id: Optional[int]
    session_id: Optional[int]
    std_id: Optional[int]

    class Config:
        orm_mode = True


class IncrementSession(SessionEnrolledSchema):
    session_id: int
    std_id: int

    class Config:
        orm_mode = True


class SessionEnrolledCreate(BaseModel):
    pass

    class Config:
        orm_mode = True


class SessionEnrolledUpdate(BaseModel):
    pass

    class Config:
        orm_mode = True
