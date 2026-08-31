
import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BillItem(Base):
    __tablename__ = "BILL_ITEMS"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    bill_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("BILLS.id"),
        nullable=False,
    )

    item_number: Mapped[int] = mapped_column(
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    unit_id: Mapped[int] = mapped_column(
        ForeignKey("UNITS.id"),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(18, 3),
        nullable=False,
    )

    rate: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    remark: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
