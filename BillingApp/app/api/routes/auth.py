from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
)
from app.schemas.user import UserResponse
from app.services.auth_service import (
    authenticate_user,
    register_user,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    return register_user(
        db=db,
        full_name=data.full_name,
        email=data.email,
        mobile=data.mobile,
        password=data.password,
    )


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db=db,
        email=data.email,
        password=data.password,
    )

    token = create_access_token(
        {
            "sub": str(user.id),
            "name": user.full_name,
            "email": user.email,
            "mobile": user.mobile,
        }
    )

    return LoginResponse(
        access_token=token,
        token_type="bearer",
    )
