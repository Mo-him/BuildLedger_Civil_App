import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.party import Party
from app.repositories.party_repository import (
    create_party,
    delete_party,
    get_parties,
    get_party_by_code,
    get_party_by_id_and_user,
    update_party,
)


def create_new_party(db: Session, user_id: uuid.UUID, **data) -> Party:
    if get_party_by_code(db, user_id, data["party_code"]):
        raise HTTPException(status_code=409, detail="Party code already exists")

    party = Party(id=uuid.uuid4(), user_id=user_id, **data)
    return create_party(db, party)


def get_all_parties(db: Session, user_id: uuid.UUID) -> list[Party]:
    return get_parties(db, user_id)


def get_party(db: Session, party_id: uuid.UUID, user_id: uuid.UUID) -> Party:
    party = get_party_by_id_and_user(db, party_id, user_id)
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")
    return party


def update_party_details(db: Session, party_id: uuid.UUID, user_id: uuid.UUID, **data) -> Party:
    party = get_party(db, party_id, user_id)

    if "party_code" in data and data["party_code"] != party.party_code:
        existing = get_party_by_code(db, user_id, data["party_code"])
        if existing and existing.id != party.id:
            raise HTTPException(status_code=409, detail="Party code already exists")

    for field, value in data.items():
        if value is not None:
            setattr(party, field, value)
    return update_party(db, party)


def remove_party(db: Session, party_id: uuid.UUID, user_id: uuid.UUID) -> None:
    party = get_party(db, party_id, user_id)
    try:
        delete_party(db, party)
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Party cannot be deleted because it is used by existing bills",
        ) from exc
