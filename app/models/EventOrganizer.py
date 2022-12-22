from sqlalchemy import Column, Integer, ForeignKey

from app.db.base_class import Base


class EventOrganizer(Base):
    __tablename__ = "EventOrganizer"
    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, ForeignKey("Organizers.organizer_id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer, ForeignKey("Events.event_id", ondelete="CASCADE"), nullable=False)
