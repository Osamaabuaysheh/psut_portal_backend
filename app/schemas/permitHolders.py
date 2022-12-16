from pydantic import BaseModel
from typing import Optional


class PermitHolderSchema(BaseModel):
    car_owner_name: Optional[str]
    phone_number: Optional[int]
    car_color: Optional[str]
    car_type: Optional[str]
    license_number: Optional[str]
    permit_number: Optional[int]

    class Config:
        orm_mode = True


class PermitHolderCreate(BaseModel):
    car_owner_name: str
    phone_number: int
    car_color: str
    car_type: str
    license_number: str
    permit_number: int
    student_id: int

    class Config:
        orm_mode = True


class PermitHolderUpdate(BaseModel):
    pass

    class Config:
        orm_mode = True
