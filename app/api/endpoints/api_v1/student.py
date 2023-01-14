from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_current_student
from app.core import security
from app.core.config import settings
from app.crud import crudStudent, crudStudentImage
from app.db.database import get_db
from app.models.Student import Student
from app.models.User import User
from app.schemas import token
from app.schemas.Student import StudentOut, StudentIn

router = APIRouter()


@router.post("/create_Student", response_model=StudentOut, response_model_exclude={'url'})
def create_student(
        *,
        db: Session = Depends(get_db),
        file: UploadFile = File(...),
        user_in: StudentIn = Depends(),
        current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new user.
    """
    extension = file.filename.split(".")[1]
    if extension not in ["png", "jpg", "jpeg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="File extension not allowed")

    try:
        with open(f'static/images/Students/{file.filename}', 'wb') as f:
            while contents := file.file.read():
                f.write(contents)

                image = crudStudentImage.get_by_name(db=db, image_name=file.filename)
                if image:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="The Image with this Name already exists in the system.")

                if not image:
                    crudStudentImage.create_image(db=db, std_id=user_in.student_id,
                                                  filename=file.filename)
                    # Check Users
                    user = crudStudent.get_by_id(db=db, student_id=user_in.student_id)
                    if user:
                        raise HTTPException(
                            status_code=400,
                            detail="The user with this username already exists in the system.",
                        )
                return crudStudent.create_student(db=db, obj_in=user_in)

    finally:
        file.file.close()


@router.post('/login_Student/access-token', response_model=token.Token, status_code=status.HTTP_200_OK)
def login_access_token(
        db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    student = db.query(Student).filter(
        Student.student_id == form_data.username).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials Username")

    if not security.verify_password(form_data.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials PASSWORD")

    access_token = security.create_access_token(student.student_id,
                                                expires_delta=timedelta(minutes=settings.access_token_expire_minutes))

    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/get_students', response_model=List[StudentOut], response_model_exclude={'hashed_password'})
def get_students(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    users = crudStudent.get_multi(db=db)
    for user in users:
        user.url = crudStudentImage.get_by_id(db=db, student_id=user.student_id).imagePath
    return users


@router.get("/get_studentsById/{user_id}", response_model=StudentOut, response_model_exclude={'hashed_password'})
def get_students(db: Session = Depends(get_db), user_id: int = None,
                 current_user: User = Depends(get_current_user)):
    user = crudStudent.get_by_id(db=db, student_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Student With This ID")
    user.url = crudStudentImage.get_by_id(db=db, student_id=user_id).imagePath

    return user


@router.get("/get_studentsById_student/{user_id}", response_model=StudentOut,
            response_model_exclude={'hashed_password'})
def get_students(db: Session = Depends(get_db), user_id: int = None,
                 current_user: User = Depends(get_current_student)):
    user = crudStudent.get_by_id(db=db, student_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No Student With This ID")
    user.url = crudStudentImage.get_by_id(db=db, student_id=user_id).imagePath

    return user


@router.post("/login_student")
def login_student(
        *,
        db: Session = Depends(get_db),
        current_user: Student = Depends(get_current_student),
) -> Any:
    return current_user
