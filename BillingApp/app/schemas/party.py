import uuid

from pydantic import BaseModel, EmailStr


class PartyBase(BaseModel):
    party_type_id: int
    party_code: str
    name: str
    company_name: str | None = None
    mobile: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    gst_number: str | None = None
    pan_number: str | None = None
    is_active: bool = True


class PartyCreate(PartyBase):
    pass


class PartyUpdate(BaseModel):
    party_type_id: int | None = None
    party_code: str | None = None
    name: str | None = None
    company_name: str | None = None
    mobile: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    gst_number: str | None = None
    pan_number: str | None = None
    is_active: bool | None = None


class PartyResponse(PartyBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}
