import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user_id
from app.schemas.user import UserResponse
from app.services.user_service import get_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def current_user(
    db: Session = Depends(get_db),
    user_id: uuid.UUID = Depends(get_current_user_id),
):
    return get_user(db, user_id)


@router.get("/{user_id}", response_model=UserResponse)
def user_by_id(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id),
):
    if user_id != current_user_id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="You can only access your own user profile")
    return get_user(db, user_id)
