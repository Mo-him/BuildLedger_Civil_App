from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.services.master_service import master_service
from app.schemas.master import (
    PartyTypeResponse,
    BillTypeResponse,
    UnitResponse,
    DeductionTypeResponse,
    TaxTypeResponse,
)

router = APIRouter(prefix="/masters", tags=["Masters"])


@router.get("/party-types", response_model=list[PartyTypeResponse])
def get_party_types(db: Session = Depends(get_db), _: object = Depends(get_current_user_id)):
    return master_service.get_party_types(db)


@router.get("/bill-types", response_model=list[BillTypeResponse])
def get_bill_types(db: Session = Depends(get_db), _: object = Depends(get_current_user_id)):
    return master_service.get_bill_types(db)


@router.get("/units", response_model=list[UnitResponse])
def get_units(db: Session = Depends(get_db), _: object = Depends(get_current_user_id)):
    return master_service.get_units(db)


@router.get("/deduction-types", response_model=list[DeductionTypeResponse])
def get_deduction_types(db: Session = Depends(get_db), _: object = Depends(get_current_user_id)):
    return master_service.get_deduction_types(db)


@router.get("/tax-types", response_model=list[TaxTypeResponse])
def get_tax_types(db: Session = Depends(get_db), _: object = Depends(get_current_user_id)):
    return master_service.get_tax_types(db)
