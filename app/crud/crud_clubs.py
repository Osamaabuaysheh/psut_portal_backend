from typing import Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.Club import Club
from app.schemas.clubs import ClubsSchema, ClubUpdate, CreateClub


class CRUDClubs(CRUDBase[Club, CreateClub, ClubUpdate]):
    def get_by_id(self, db: Session, *, club_id: int) -> Optional[Club]:
        return db.query(self.model).filter(Club.club_id == club_id).first()

    def get_by_name(self, db: Session, *, club_name: str) -> Optional[Club]:
        return db.query(self.model).filter(Club.club_name == club_name).first()

    def create_club(self, db: Session, *, obj_in: CreateClub, club_icon_image: str, club_background_image: str):
        db_obj = Club(
            club_name=obj_in.club_name.lower(),
            description=obj_in.description,
            contact_info=obj_in.contact_info,
            link=obj_in.link,
            club_icon_image=f'static/images/Clubs/IconImages/{club_icon_image}',
            club_image=f'static/images/Clubs/backgroundImage/{club_background_image}'
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj


crudClubs = CRUDClubs(Club)
