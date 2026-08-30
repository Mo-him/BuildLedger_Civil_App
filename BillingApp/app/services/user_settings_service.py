import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_settings import UserSettings
from app.repositories.user_settings_repository import (
    create_user_settings,
    get_user_settings,
    update_user_settings,
)


def get_my_user_settings(
    db: Session,
    user_id: uuid.UUID,
) -> UserSettings | None:

    return get_user_settings(db, user_id)


def create_my_user_settings(
    db: Session,
    user_id: uuid.UUID,
    **data,
) -> UserSettings:

    existing = get_user_settings(db, user_id)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User settings already exist",
        )

    settings = UserSettings(
        user_id=user_id,
        **data,
    )

    return create_user_settings(db, settings)


def update_my_user_settings(
    db: Session,
    user_id: uuid.UUID,
    **data,
) -> UserSettings:

    settings = get_user_settings(db, user_id)

    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User settings not found",
        )

    for field, value in data.items():
        if value is not None:
            setattr(settings, field, value)

    return update_user_settings(db, settings)