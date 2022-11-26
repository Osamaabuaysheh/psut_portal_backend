from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.Job import Job
from app.schemas.job import JobCreate, JobUpdate


class CRUDJobs(CRUDBase[Job, JobCreate, JobUpdate]):
    def get_by_id(self, db: Session, *, job_id: int) -> Optional[Job]:
        return db.query(self.model).filter(Job.job_id == job_id).first()

    def get_by_company_name(self, db: Session, *, company_name: str) -> Optional[Job]:
        return db.query(self.model).filter(Job.company_name == company_name).first()

    def create_job(self, db: Session, *, obj_in: JobCreate, job_image: str):
        db_obj = Job(
            job_Deadline=obj_in.job_Deadline,
            job_description=obj_in.job_description,
            job_title=obj_in.job_title,
            college=obj_in.college.upper(),
            job_requierments=obj_in.job_requierments,
            job_icon_image=f'static/images/Jobs/{job_image}',
            job_responsanbilities=obj_in.job_responsanbilities,
            company_name=obj_in.company_name
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudJob = CRUDJobs(Job)
