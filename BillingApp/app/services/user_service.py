import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import (
    get_user_by_id,
    get_users,
    update_user,
)


def get_all_users(
    db: Session,
) -> list[User]:

    return get_users(db)


def get_user(
    db: Session,
    user_id: uuid.UUID,
) -> User:

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


def update_user_details(
    db: Session,
    user_id: uuid.UUID,
    full_name: str | None = None,
    mobile: str | None = None,
    is_active: bool | None = None,
) -> User:

    user = get_user(db, user_id)

    if full_name is not None:
        user.full_name = full_name

    if mobile is not None:
        user.mobile = mobile

    if is_active is not None:
        user.is_active = is_active

    return update_user(db, user)