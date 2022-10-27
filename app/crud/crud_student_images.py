from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.StudentImages import StudentImages
from app.schemas.User import UserCreate, UserUpdate
from app.schemas import Image


class CRUDStudentImages(CRUDBase[StudentImages, UserCreate, UserUpdate]):
    def get_by_id(self, db: Session, *, student_id: int) -> Optional[StudentImages]:
        return db.query(self.model).filter(StudentImages.id == student_id).first()

    def get_by_name(self, db: Session, *, image_name: int) -> Optional[StudentImages]:
        return db.query(self.model).filter(StudentImages.imageName == image_name).first()

    def create_image(self, db: Session, *, filename: str, std_id: int) -> StudentImages:
        image_in = Image.CreateStudentImage(id=std_id,
                                            imagePath=f'static/images/Students/{filename}',
                                            imageName=f'{filename}')
        db_in = StudentImages(**image_in.dict())
        db.add(db_in)
        db.commit()
        db.refresh(db_in)
        return db_in


crudStudentImage = CRUDStudentImages(StudentImages)
