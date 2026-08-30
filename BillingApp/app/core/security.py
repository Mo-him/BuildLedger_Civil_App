
from datetime import datetime, timedelta, timezone
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# Password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


# JWT configuration
ALGORITHM = "HS256"
SECRET_KEY = settings.secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Bearer token authentication
#
# Swagger will show:
# Authorize 🔒
#   Value: <paste your JWT token here>
#
# You do NOT need to enter email/password here.
bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    """
    Hash a plain-text password.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain-text password against its hashed value.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    to_encode["exp"] = expire

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict | None:
    """
    Decode and validate JWT token.
    """

    try:
        return jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

    except JWTError:
        return None


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
) -> uuid.UUID:
    """
    Get current user's UUID from JWT Bearer token.

    Swagger:
        Authorize -> paste JWT token

    Example header:
        Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
    """

    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    subject = payload.get("sub")

    if not subject:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )

    try:
        return uuid.UUID(str(subject))

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier in token",
            headers={
                "WWW-Authenticate": "Bearer",
            },
        )
