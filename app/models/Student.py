from sqlalchemy import Column, Integer, String, Float

from app.db.base_class import Base


class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    full_name_arabic = Column(String, index=True)
    student_image_id = Column(Integer, nullable=True, unique=True)
    colleage = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hours_completed = Column(Integer, nullable=False)
    hashed_password = Column(String, nullable=False)
    gpa = Column(Float, nullable=False, server_default="0")
