import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
)


def register_user(
    db: Session,
    full_name: str,
    email: str,
    mobile: str,
    password: str,
) -> User:

    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        id=uuid.uuid4(),
        full_name=full_name,
        email=email,
        mobile=mobile,
        password_hash=hash_password(password),
        is_active=True,
    )

    return create_user(db, user)


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User:

    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    user.last_login_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)

    return user