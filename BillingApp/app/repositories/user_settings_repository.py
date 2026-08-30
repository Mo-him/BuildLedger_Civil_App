import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_settings import UserSettings


def get_user_settings(
    db: Session,
    user_id: uuid.UUID
) -> UserSettings | None:

    return db.scalar(
        select(UserSettings)
        .where(UserSettings.user_id == user_id)
    )


def create_user_settings(
    db: Session,
    settings: UserSettings
) -> UserSettings:

    db.add(settings)
    db.commit()
    db.refresh(settings)

    return settings


def update_user_settings(
    db: Session,
    settings: UserSettings
) -> UserSettings:

    db.commit()
    db.refresh(settings)

    return settings