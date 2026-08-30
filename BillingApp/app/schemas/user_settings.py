import uuid

from pydantic import BaseModel


class UserSettingsBase(BaseModel):
    theme: str = "light"
    currency: str = "INR"
    date_format: str = "DD-MM-YYYY"
    notifications_enabled: bool = True
    auto_save: bool = True


class UserSettingsCreate(UserSettingsBase):
    pass


class UserSettingsUpdate(BaseModel):
    theme: str | None = None
    currency: str | None = None
    date_format: str | None = None
    notifications_enabled: bool | None = None
    auto_save: bool | None = None


class UserSettingsResponse(UserSettingsBase):
    user_id: uuid.UUID

    model_config = {"from_attributes": True}
