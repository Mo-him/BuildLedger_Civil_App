import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.user_settings import UserSettingsCreate, UserSettingsResponse, UserSettingsUpdate
from app.services.user_settings_service import (
    create_my_user_settings,
    get_my_user_settings,
    update_my_user_settings,
)

router = APIRouter(prefix="/user-settings", tags=["User Settings"])


@router.get("", response_model=UserSettingsResponse | None)
def get_settings(db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_my_user_settings(db, user_id)


@router.post("", response_model=UserSettingsResponse, status_code=status.HTTP_201_CREATED)
def create_settings(settings: UserSettingsCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return create_my_user_settings(db=db, user_id=user_id, **settings.model_dump())


@router.put("", response_model=UserSettingsResponse)
def update_settings(settings: UserSettingsUpdate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return update_my_user_settings(db=db, user_id=user_id, **settings.model_dump(exclude_unset=True))
