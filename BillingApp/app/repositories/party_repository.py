import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.party import Party


def get_party_by_id(db: Session, party_id: uuid.UUID) -> Party | None:
    return db.scalar(select(Party).where(Party.id == party_id))


def get_party_by_id_and_user(
    db: Session,
    party_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Party | None:
    return db.scalar(
        select(Party).where(
            Party.id == party_id,
            Party.user_id == user_id,
        )
    )


def get_parties(db: Session, user_id: uuid.UUID) -> list[Party]:
    return list(
        db.scalars(
            select(Party)
            .where(Party.user_id == user_id)
            .order_by(Party.name)
        ).all()
    )


def get_party_by_code(
    db: Session,
    user_id: uuid.UUID,
    party_code: str,
) -> Party | None:
    return db.scalar(
        select(Party).where(
            Party.user_id == user_id,
            Party.party_code == party_code,
        )
    )


def create_party(db: Session, party: Party) -> Party:
    db.add(party)
    db.commit()
    db.refresh(party)
    return party


def update_party(db: Session, party: Party) -> Party:
    db.commit()
    db.refresh(party)
    return party


def delete_party(db: Session, party: Party) -> None:
    db.delete(party)
    db.commit()
