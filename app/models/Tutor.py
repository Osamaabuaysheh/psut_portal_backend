from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.db.base_class import Base


class Tutor(Base):
    __tablename__ = "tutors"
    tutor_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete="CASCADE"), nullable=False)
