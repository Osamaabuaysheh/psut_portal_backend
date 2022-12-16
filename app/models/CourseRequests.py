from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class CourseRequests(Base):
    __tablename__ = "coursesRequests"
    request_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
