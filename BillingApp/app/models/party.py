import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Party(Base):
    __tablename__ = "PARTIES"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER, ForeignKey("USERS.id"), nullable=False
    )
    party_type_id: Mapped[int] = mapped_column(
        ForeignKey("PARTY_TYPES.id"), nullable=False
    )
    party_code: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pincode: Mapped[str | None] = mapped_column(String(10), nullable=True)
    gst_number: Mapped[str | None] = mapped_column(String(30), nullable=True)
    pan_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
