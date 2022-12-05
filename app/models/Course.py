from sqlalchemy import Column, Integer, String
from app.db.base_class import Base


class Course(Base):
    __tablename__ = "courses"
    course_id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, nullable=False)
    college = Column(String, nullable=False)
