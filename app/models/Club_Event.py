from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class ClubEvent(Base):
    __tablename__ = "clubevents"
    club_event_id = Column(Integer, primary_key=True, index=True)
    club_name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("Events.event_id", ondelete="CASCADE"), nullable=False)

    event_owner = relationship("Event")
