from sqlalchemy import Column, Integer, String, Time, ForeignKey

from app.db.base_class import Base


class CourseSession(Base):
    __tablename__ = "courseSessions"
    session_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    day = Column(String, nullable=True)
    tutor_id = Column(Integer, ForeignKey("tutors.tutor_id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.course_id", ondelete="CASCADE"), nullable=False)
