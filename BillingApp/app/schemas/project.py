import uuid
from datetime import date

from pydantic import BaseModel


class ProjectBase(BaseModel):
    project_code: str
    project_name: str
    site_name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    client_name: str | None = None
    client_contact: str | None = None
    work_order_number: str | None = None
    work_order_date: date | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool = True


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    project_code: str | None = None
    project_name: str | None = None
    site_name: str | None = None
    address: str | None = None
    city: str | None = None
    state: str | None = None
    pincode: str | None = None
    client_name: str | None = None
    client_contact: str | None = None
    work_order_number: str | None = None
    work_order_date: date | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None


class ProjectResponse(ProjectBase):
    id: uuid.UUID
    user_id: uuid.UUID

    model_config = {"from_attributes": True}
