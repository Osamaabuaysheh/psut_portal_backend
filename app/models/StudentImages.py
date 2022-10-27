from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class StudentImages(Base):
    __tablename__ = "studentImages"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    imagePath = Column(String, nullable=False)
