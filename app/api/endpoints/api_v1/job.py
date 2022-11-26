from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.crud.crud_jobs import crudJob
from app.schemas.job import JobCreate, JobOut

router = APIRouter()


@router.get('/get_All_Jobs')
async def get_jobs(*, db: Session = Depends(get_db)):
    return crudJob.get_multi(db=db)


@router.post('/create_job', response_model=JobOut)
async def get_jobs(*, db: Session = Depends(get_db), obj_in: JobCreate = Depends(),
                   job_image: UploadFile = File(...)):
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
