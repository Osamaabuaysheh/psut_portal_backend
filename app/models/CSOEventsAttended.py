from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from app.db.base_class import Base


class CSOEventsAttended(Base):
    __tablename__ = "csoeventsattended"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("Events.event_id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
