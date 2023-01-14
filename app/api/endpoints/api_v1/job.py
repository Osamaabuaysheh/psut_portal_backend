from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.crud.crud_jobs import crudJob
from app.db.database import get_db
from app.models import User
from app.models.Job import Job
from app.models.Student import Student
from app.schemas.job import JobCreate, JobOut, JobUpdate

router = APIRouter()


@router.get('/get_All_Jobs')
async def get_jobs(*, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    return crudJob.get_multi(db=db)


@router.get('/get_all_jobs_students')
async def get_jobs_students(*, db: Session = Depends(get_db),
                            current_user: Student = Depends(get_current_student)):
    return crudJob.get_multi(db=db)


@router.post('/create_job', response_model=JobOut)
async def get_jobs(*, db: Session = Depends(get_db), obj_in: JobCreate = Depends(),
                   job_image: UploadFile = File(...),
                   current_user: User = Depends(get_current_user), ):
    extension = job_image.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed For Backgound")

    try:
        with open(f'static/images/Jobs/{job_image.filename}', 'wb') as f:
            while contents := job_image.file.read():
                f.write(contents)
        return crudJob.create_job(db=db, obj_in=obj_in, job_image=job_image.filename)
    finally:
        job_image.file.close()


@router.post('/delete_job/{job_id}')
async def get_jobs(*, db: Session = Depends(get_db), job_id: int,
                   current_user: User = Depends(get_current_user), ):
    job = db.query(Job).filter(Job.job_id == job_id)
    if job.first() is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job Doesn't Exist")
    else:
        crudJob.delete_job_by_id(db=db, job_id=job_id)
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Job Deleted Successfully")


@router.post('/job_id/{job_id}')
async def update_job(*, db: Session = Depends(get_db), job_id: int,
                     current_user: User = Depends(get_current_user), job_in: JobUpdate = Depends(),
                     job_image: UploadFile = None):
    if job_image is None:
        db_obj = db.query(Job).filter(Job.job_id == job_id).update(values=job_in.dict(exclude_none=True))
        db.commit()
        return db_obj
    else:
        extension = job_image.filename.split(".")[1]
        if extension not in ["png", "jpg", "jpeg"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="File extension not allowed For Backgound")

        try:
            with open(f'static/images/Jobs/{job_image.filename}', 'wb') as f:
                while contents := job_image.file.read():
                    f.write(contents)
            job_in.job_icon_image = f'static/images/Jobs/{job_image.filename}'
            db_obj = db.query(Job).filter(Job.job_id == job_id).update(values=job_in.dict(exclude_none=True))
            db.commit()
            return db_obj
        finally:
            job_image.file.close()
