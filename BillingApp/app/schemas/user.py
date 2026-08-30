import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    mobile: str
    profile_image: str | None = None
    is_active: bool
    last_login_at: datetime | None = None

    model_config = {"from_attributes": True}
