from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ClubEvent(Base):
    __tablename__ = "clubevents"
    club_event_id = Column(Integer, primary_key=True, index=True)
    club_id = Column(Integer, ForeignKey("Clubs.club_id", ondelete="CASCADE"), nullable=True)
    event_id = Column(Integer, ForeignKey("Events.event_id", ondelete="CASCADE"), nullable=False)

    event_owner = relationship("Event")
