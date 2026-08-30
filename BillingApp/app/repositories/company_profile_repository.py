import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company_profile import CompanyProfile


def get_company_profile(
    db: Session,
    user_id: uuid.UUID
) -> CompanyProfile | None:

    return db.scalar(
        select(CompanyProfile)
        .where(CompanyProfile.user_id == user_id)
    )


def get_company_profile_by_id(
    db: Session,
    profile_id: uuid.UUID
) -> CompanyProfile | None:

    return db.scalar(
        select(CompanyProfile)
        .where(CompanyProfile.id == profile_id)
    )


def create_company_profile(
    db: Session,
    profile: CompanyProfile
) -> CompanyProfile:

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


def update_company_profile(
    db: Session,
    profile: CompanyProfile
) -> CompanyProfile:

    db.commit()
    db.refresh(profile)

    return profile


def delete_company_profile(
    db: Session,
    profile: CompanyProfile
) -> None:

    db.delete(profile)
    db.commit()