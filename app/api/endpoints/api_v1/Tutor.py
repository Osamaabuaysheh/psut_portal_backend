from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.crud.crud_tutor import crudTutor
from app.db.database import get_db
from app.models import Tutor, User
from app.models.Course import Course
from app.models.Student import Student
from app.models.course_tutor import CourseTutor
from app.schemas.Tutor import TutorCreate

router = APIRouter()


@router.get('/get_All_Tutors')
async def get_tutors(*, db: Session = Depends(get_db)):
    tutors = db.query(Tutor.Tutor).all()
    for tutor in tutors:
        tutor_name = db.query(Student).filter(Student.student_id == tutor.student_id).first().full_name
        tutor = tutor.__dict__
        tutor['tutor_name'] = tutor_name
    return tutors


@router.post('/Create_Tutor')
async def create_tutor(*, db: Session = Depends(get_db), obj_in: TutorCreate = Depends(),
                       current_user: User.User = Depends(get_current_user)):
    return crudTutor.create_tutor(db=db, obj_in=obj_in, owner=current_user.id)


@router.get('/get_all_course_tutors')
async def get_all_course_tutors(*, db: Session = Depends(get_db)):
    all = db.query(CourseTutor.course_id).group_by(CourseTutor.course_id).all()
    re = []
    for course in all:
        obj = db.query(CourseTutor).filter(course.course_id == CourseTutor.course_id).all()
        ar = []
        for tutor in obj:
            tutor = db.query(Tutor.Tutor).filter(Tutor.Tutor.tutor_id == tutor.tutor_id).first()
            student_name = db.query(Student).filter(Student.student_id == tutor.student_id).first().full_name
            tutor = tutor.__dict__
            tutor['student_name'] = student_name
            ar.append(tutor)
        in_obj = {'course_id': course.course_id, 'tutors': ar,
                  'course_name': db.query(Course).filter(Course.course_id == course.course_id).first().course_name}
        re.append(in_obj)
    return re
