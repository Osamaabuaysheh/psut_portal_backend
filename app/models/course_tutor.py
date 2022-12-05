from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base


class CourseTutor(Base):
    __tablename__ = "coursesTutors"
    ct_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tutor_id = Column(Integer, ForeignKey("tutors.tutor_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
