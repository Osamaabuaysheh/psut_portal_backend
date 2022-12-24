from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student
from app.crud.crud_session_enrolled import crudSessionEnrolled
from app.db.database import get_db
from app.models.SessionEnrolled import SessionEnrolled
from app.models.Student import Student
from app.schemas.session_enrolled import IncrementSession

router = APIRouter()


@router.get('/get_All_Session_Students')
async def get_courses(*, db: Session = Depends(get_db)):
    return crudSessionEnrolled.get_all_session_std(db=db)


@router.post('/get_session_total/{session_id}')
async def get_session_total(*, db: Session = Depends(get_db), session_id: int,
                            current_user: Student = Depends(get_current_student)):
    return db.query(SessionEnrolled).filter(SessionEnrolled.sessionId == session_id).count()


@router.post('/increment_Session_Student')
async def get_courses(*, db: Session = Depends(get_db), obj_in: IncrementSession = Depends(),
                      current_user: Student = Depends(get_current_student)):
    std = db.query(Student).filter(Student.student_id == obj_in.std_id).first()
    if std is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student Doesn't Exist")
    if std:
        db_obj = db.query(SessionEnrolled).filter(SessionEnrolled.sessionId == obj_in.session_id).first()
        if db_obj:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student Already Enrolled")

    return crudSessionEnrolled.increment_one_session(db=db, obj_in=obj_in)
