from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_TutorRequest import crudTutorRequest
from app.crud.crud_tutor import crudTutor
from app.db.database import get_db
from app.models import TutorRequests
from app.models.Course import Course
from app.models.Student import Student
from app.models.Tutor import Tutor
from app.models.User import User
from app.models.course_tutor import CourseTutor
from app.schemas.TutorRequest import TutorRequestCreate

router = APIRouter()


@router.get('/get_All_Tutor_Requests')
async def get_Requests(*, db: Session = Depends(get_db), user_in: User = Depends(get_current_user)):
    requests = db.query(TutorRequests.TutorRequests).all()
    for req in requests:
        req = req.__dict__
        req['Student_Name'] = db.query(Student).filter(req['student_id'] == Student.student_id).first().full_name
        req['course_name'] = db.query(Course).filter(req['course_id'] == Course.course_id).first().course_name
    return requests


@router.post('/Create_Request')
async def create_request(*, db: Session = Depends(get_db), obj_in: TutorRequestCreate = Depends()):
    db_obj = crudTutorRequest.create_request(db=db, obj_in=obj_in)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return db_obj


@router.post('/delete_tutor_request/{tutor_request_id}')
async def delete_request_session(*, db: Session = Depends(get_db),
                                 tutor_request_id: int):
    db_obj = crudTutorRequest.get_by_id(db=db, tutorRequest_id=tutor_request_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    crudTutorRequest.delete_course_request_id(db=db, tutor_request_id=tutor_request_id)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Request Deleted")


@router.post('/accept_tutor_request/{tutor_request_id}')
async def accept_tutor_request(*, db: Session = Depends(get_db),
                               tutor_request_id: int, current_user: User = Depends(get_current_user)):
    db_obj = crudTutorRequest.get_by_id(db=db, tutorRequest_id=tutor_request_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not Found")
    is_tutor = db.query(Tutor).filter(Tutor.student_id == db_obj.student_id).first()
    if is_tutor is None:
        crudTutor.create_tutor(db=db, std_id=db_obj.student_id, owner=current_user.id)
    is_tutor = db.query(Tutor).filter(Tutor.student_id == db_obj.student_id).first()

    is_exist = db.query(CourseTutor).filter(CourseTutor.course_id == db_obj.course_id).filter(
        CourseTutor.tutor_id == is_tutor.tutor_id).first()
    if is_exist is not None:
        crudTutorRequest.delete_course_request_id(db=db, tutor_request_id=tutor_request_id)
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="Course Tutor Already Exist")

    add_course_tutor = CourseTutor(tutor_id=is_tutor.tutor_id, course_id=db_obj.course_id)
    db.add(add_course_tutor)
    db.commit()
    db.refresh(add_course_tutor)
    crudTutorRequest.delete_course_request_id(db=db, tutor_request_id=tutor_request_id)
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Request Deleted")
