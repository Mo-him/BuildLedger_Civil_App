import uuid

from sqlalchemy import String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from app.core.database import Base


class CompanyProfile(Base):
    __tablename__ = "COMPANY_PROFILES"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
    UNIQUEIDENTIFIER,
    ForeignKey("USERS.id"),
    nullable=False,
    unique=True
)

    company_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    company_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    pincode: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    gst_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    pan_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    bank_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    account_number: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    ifsc_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    account_holder_name: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )