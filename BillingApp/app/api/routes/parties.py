import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.party import PartyCreate, PartyResponse, PartyUpdate
from app.services.party_service import (
    create_new_party,
    get_all_parties,
    get_party,
    remove_party,
    update_party_details,
)

router = APIRouter(prefix="/parties", tags=["Parties"])


@router.get("/", response_model=list[PartyResponse])
def parties(db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_all_parties(db, user_id)


@router.get("/{party_id}", response_model=PartyResponse)
def party_by_id(party_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_party(db, party_id, user_id)


@router.post("/", response_model=PartyResponse, status_code=status.HTTP_201_CREATED)
def create(data: PartyCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return create_new_party(db, user_id, **data.model_dump())


@router.put("/{party_id}", response_model=PartyResponse)
def update(party_id: uuid.UUID, data: PartyUpdate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return update_party_details(db, party_id, user_id, **data.model_dump(exclude_unset=True))


@router.delete("/{party_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(party_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    remove_party(db, party_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
