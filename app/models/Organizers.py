from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base


class Organizer(Base):
    __tablename__ = "Organizers"
    organizer_id = Column(Integer, primary_key=True, index=True)
    organizer_name = Column(String, nullable=False)
    organizer_image = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("Events.event_id", ondelete="CASCADE"), nullable=False)



