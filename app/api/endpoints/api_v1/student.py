from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any, List
from datetime import timedelta
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.StudentSchema import StudentSchema, StudentOut, StudentIn
from app.models.Student import Student
from app.schemas import token
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security

from app.core.config import settings

router = APIRouter()


@router.post('/login_Student', response_model=token.Token, status_code=status.HTTP_200_OK)
def login_access_token(
        db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    student = db.query(Student).filter(
        Student.id == form_data.username).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not security.verify_password(form_data.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials PASSWORD")

    access_token = security.create_access_token(student.id,
                                                expires_delta=timedelta(minutes=settings.access_token_expire_minutes))

    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/get_students', response_model=List[StudentOut], response_model_exclude={'hashed_password'})
def get_students(db: Session = Depends(get_db)):
    users = db.query(Student).all()
    return users


# @router.get('/get_studentsbyID', response_model=List[StudentOut], response_model_exclude={'hashed_password'})
# def get_students(db: Session = Depends(get_db), student_in=StudentIn):
#     users = db.query(Student).filter(Student.id == student_in.id).first()
#     return users


@router.post("/create_Student")
def create_student(
        *,
        db: Session = Depends(get_db),
        user_in: StudentSchema
) -> Any:
    """
    Create new user.
    """
    user = db.query(Student).filter(Student.email == user_in.email).first()
    if user:
        raise HTTPException(  # handling errors, exception with additional data relevant for APIs.
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    db_obj = Student(
        id=user_in.id,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.hashed_password),
        full_name=user_in.full_name,
        colleage=user_in.colleage
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)

    return db_obj
