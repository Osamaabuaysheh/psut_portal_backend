from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.db.base_class import Base


class TutorRequests(Base):
    __tablename__ = "tutorsRequests"
    tutor_request_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    semester_completion = Column(String, nullable=False)
    grade = Column(Float, nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
