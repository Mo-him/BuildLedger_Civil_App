import uuid

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.bill_item import BillItemCreate, BillItemResponse, BillItemUpdate
from app.services.bill_item_service import (
    create_bill_item,
    get_all_bill_items,
    get_bill_item,
    remove_bill_item,
    update_bill_item_details,
)

router = APIRouter(prefix="/bills/{bill_id}/items", tags=["Bill Items"])


@router.get("", response_model=list[BillItemResponse])
def get_items(
    bill_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_all_bill_items(db, bill_id, user_id)


@router.post("", response_model=BillItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    bill_id: uuid.UUID,
    item: BillItemCreate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return create_bill_item(
        db=db, bill_id=bill_id, user_id=user_id,
        item_number=item.item_number, description=item.description,
        unit_id=item.unit_id, quantity=item.quantity, rate=item.rate,
        remark=item.remark,
    )


@router.get("/{item_id}", response_model=BillItemResponse)
def get_item(
    bill_id: uuid.UUID,
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_bill_item(db, bill_id, item_id, user_id)


@router.put("/{item_id}", response_model=BillItemResponse)
def update_item(
    bill_id: uuid.UUID,
    item_id: uuid.UUID,
    item: BillItemUpdate,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return update_bill_item_details(
        db=db, bill_id=bill_id, item_id=item_id, user_id=user_id,
        **item.model_dump(exclude_unset=True),
    )


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    bill_id: uuid.UUID,
    item_id: uuid.UUID,
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    remove_bill_item(db, bill_id, item_id, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
