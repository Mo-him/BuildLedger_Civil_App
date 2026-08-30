import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill_deduction import BillDeductionCreate, BillDeductionResponse
from app.services.bill_deduction_service import (
    create_bill_deduction,
    get_all_bill_deductions,
    get_bill_deduction,
    remove_bill_deduction,
    update_bill_deduction_details,
)

router = APIRouter(prefix="/bills/{bill_id}/deductions", tags=["Bill Deductions"])


@router.get("", response_model=list[BillDeductionResponse])
def get_deductions(bill_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_all_bill_deductions(db, bill_id, user_id)


@router.post("", response_model=BillDeductionResponse, status_code=status.HTTP_201_CREATED)
def create_deduction(bill_id: uuid.UUID, deduction: BillDeductionCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return create_bill_deduction(db=db, bill_id=bill_id, user_id=user_id, **deduction.model_dump())


@router.get("/{deduction_id}", response_model=BillDeductionResponse)
def get_deduction(bill_id: uuid.UUID, deduction_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return get_bill_deduction(db, bill_id, deduction_id, user_id)


@router.put("/{deduction_id}", response_model=BillDeductionResponse)
def update_deduction(bill_id: uuid.UUID, deduction_id: uuid.UUID, deduction: BillDeductionCreate, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    return update_bill_deduction_details(db=db, bill_id=bill_id, deduction_id=deduction_id, user_id=user_id, **deduction.model_dump())


@router.delete("/{deduction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deduction(bill_id: uuid.UUID, deduction_id: uuid.UUID, db: Session = Depends(get_db), user_id: uuid.UUID = Depends(get_current_user_id)):
    remove_bill_deduction(db, bill_id, deduction_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
