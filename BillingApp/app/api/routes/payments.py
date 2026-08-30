import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill_payment import BillPaymentCreate, BillPaymentResponse, BillPaymentUpdate
from app.services.payment_service import (
    add_payment,
    get_all_payments,
    get_payment,
    remove_payment,
    update_payment,
)

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/bills/{bill_id}", response_model=BillPaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    bill_id: uuid.UUID,
    payment: BillPaymentCreate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return add_payment(db=db, bill_id=bill_id, user_id=user_id, **payment.model_dump())


@router.get("/bills/{bill_id}", response_model=list[BillPaymentResponse])
def get_payments(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_all_payments(db, bill_id, user_id)


@router.get("/bills/{bill_id}/{payment_id}", response_model=BillPaymentResponse)
def get_payment_by_id(
    bill_id: uuid.UUID,
    payment_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_payment(db, bill_id, payment_id, user_id)


@router.put("/bills/{bill_id}/{payment_id}", response_model=BillPaymentResponse)
def edit_payment(
    bill_id: uuid.UUID,
    payment_id: uuid.UUID,
    payment: BillPaymentUpdate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_payment(
        db=db, bill_id=bill_id, payment_id=payment_id, user_id=user_id,
        **payment.model_dump(exclude_unset=True),
    )


@router.delete("/bills/{bill_id}/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
    bill_id: uuid.UUID,
    payment_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    remove_payment(db, bill_id, payment_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
