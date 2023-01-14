from sqlalchemy import Column, Integer, ForeignKey, DateTime

from app.db.base_class import Base


class CallLogsStudent(Base):
    __tablename__ = "CallLogsStudent"
    id = Column(Integer, primary_key=True, index=True)
    caller = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    receiver = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
    datetime = Column(DateTime, nullable=False)
