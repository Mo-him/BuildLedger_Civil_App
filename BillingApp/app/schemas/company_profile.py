import uuid

from pydantic import BaseModel, EmailStr


class CompanyProfileBase(BaseModel):
    company_name: str
    company_address: str
    city: str
    state: str
    pincode: str
    gst_number: str | None = None
    pan_number: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    bank_name: str | None = None
    account_number: str | None = None
    ifsc_code: str | None = None
    account_holder_name: str | None = None


class CompanyProfileCreate(CompanyProfileBase):
    pass


class CompanyProfileResponse(CompanyProfileBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = {
        "from_attributes": True
    }