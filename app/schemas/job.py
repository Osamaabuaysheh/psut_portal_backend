from datetime import date
from typing import Optional

from pydantic import BaseModel


class JobSchema(BaseModel):
    job_id: Optional[int]
    company_name: Optional[str]
    job_title: Optional[str]
    job_responsanbilities: Optional[str]
    job_requierments: Optional[str]
    college: Optional[str]
    job_Deadline: Optional[date]
    job_description: Optional[str]

    class Config:
        orm_mode = True


class JobCreate(BaseModel):
    company_name: str
    job_title: str
    college: str
    job_responsanbilities: str
    job_requierments: str
    job_Deadline: date
    job_description: str

    class Config:
        orm_mode = True


class JobOut(BaseModel):
    job_id: int
    company_name: str
    job_title: str
    job_responsanbilities: str
    job_requierments: str
    college: str
    job_Deadline: date
    job_icon_image: str
    job_description: str

    class Config:
        orm_mode = True


class JobUpdate(BaseModel):
    company_name: Optional[str]
    job_title: Optional[str]
    job_responsanbilities: Optional[str]
    job_requierments: Optional[str]
    college: Optional[str]
    job_Deadline: Optional[date]
    job_description: Optional[str]
    job_icon_image: Optional[str]

    class Config:
        orm_mode = True
