import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.company_profile import CompanyProfile
from app.repositories.company_profile_repository import (
    create_company_profile,
    get_company_profile,
    update_company_profile,
)


def get_my_company_profile(
    db: Session,
    user_id: uuid.UUID,
) -> CompanyProfile | None:

    return get_company_profile(db, user_id)


def create_my_company_profile(
    db: Session,
    user_id: uuid.UUID,
    **data,
) -> CompanyProfile:

    existing = get_company_profile(db, user_id)

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Company profile already exists",
        )

    profile = CompanyProfile(
        id=uuid.uuid4(),
        user_id=user_id,
        **data,
    )

    return create_company_profile(db, profile)


def update_my_company_profile(
    db: Session,
    user_id: uuid.UUID,
    **data,
) -> CompanyProfile:

    profile = get_company_profile(db, user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found",
        )

    for field, value in data.items():
        if value is not None:
            setattr(profile, field, value)

    return update_company_profile(db, profile)