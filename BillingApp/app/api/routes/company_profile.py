import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.company_profile import CompanyProfileCreate, CompanyProfileResponse
from app.services.company_profile_service import (
    create_my_company_profile,
    get_my_company_profile,
    update_my_company_profile,
)

router = APIRouter(prefix="/company-profile", tags=["Company Profile"])


@router.get("", response_model=CompanyProfileResponse | None)
def get_company_profile(
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_my_company_profile(db, user_id)


@router.post("", response_model=CompanyProfileResponse, status_code=status.HTTP_201_CREATED)
def create_company_profile(
    profile: CompanyProfileCreate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return create_my_company_profile(db=db, user_id=user_id, **profile.model_dump())


@router.put("", response_model=CompanyProfileResponse)
def update_company_profile(
    profile: CompanyProfileCreate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_my_company_profile(db=db, user_id=user_id, **profile.model_dump())
