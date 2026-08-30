import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Bill(Base):
    __tablename__ = "BILLS"

    id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("USERS.id"),
        nullable=False
    )

    bill_number: Mapped[str] = mapped_column(
        String(80),
        nullable=False
    )

    bill_type_id: Mapped[int] = mapped_column(
        ForeignKey("BILL_TYPES.id"),
        nullable=False
    )

    party_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("PARTIES.id"),
        nullable=False
    )

    project_id: Mapped[uuid.UUID] = mapped_column(
        UNIQUEIDENTIFIER,
        ForeignKey("PROJECTS.id"),
        nullable=False
    )

    bill_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    work_period_from: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    work_period_to: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    reference_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    work_order_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Draft"
    )

    total_items_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    other_charges: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    gross_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    total_deductions: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    total_tax: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    previous_bill_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    previous_payment_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    balance_carried_forward: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    current_bill_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    net_payable_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    paid_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    balance_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True)

    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="INR")