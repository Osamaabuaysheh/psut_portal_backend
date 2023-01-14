from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class ClubOrganizer(Base):
    __tablename__ = "ClubOrganizer"
    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, ForeignKey("Clubs.club_id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer, ForeignKey("Events.event_id", ondelete="CASCADE"), nullable=False)
