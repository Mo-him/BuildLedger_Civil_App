import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill_tax import BillTaxCreate, BillTaxResponse
from app.services.bill_tax_service import (
    create_bill_tax,
    get_all_bill_taxes,
    get_bill_tax,
    remove_bill_tax,
    update_bill_tax_details,
)

router = APIRouter(prefix="/bills/{bill_id}/taxes", tags=["Bill Taxes"])


@router.get("", response_model=list[BillTaxResponse])
def get_taxes(bill_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_all_bill_taxes(db, bill_id, user_id)


@router.post("", response_model=BillTaxResponse, status_code=status.HTTP_201_CREATED)
def create_tax(bill_id: uuid.UUID, tax: BillTaxCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return create_bill_tax(db=db, bill_id=bill_id, user_id=user_id, **tax.model_dump())


@router.get("/{tax_id}", response_model=BillTaxResponse)
def get_tax(bill_id: uuid.UUID, tax_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_bill_tax(db, bill_id, tax_id, user_id)


@router.put("/{tax_id}", response_model=BillTaxResponse)
def update_tax(bill_id: uuid.UUID, tax_id: uuid.UUID, tax: BillTaxCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return update_bill_tax_details(db=db, bill_id=bill_id, tax_id=tax_id, user_id=user_id, **tax.model_dump())


@router.delete("/{tax_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tax(bill_id: uuid.UUID, tax_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    remove_bill_tax(db, bill_id, tax_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
