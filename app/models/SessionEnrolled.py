from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class SessionEnrolled(Base):
    __tablename__ = "sessionEnrolled"
    enroll_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sessionId = Column(Integer, ForeignKey("courseSessions.session_id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
