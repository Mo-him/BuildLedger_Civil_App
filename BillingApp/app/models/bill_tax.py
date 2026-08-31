
import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class BillTax(Base):
    __tablename__ = "BILL_TAXES"

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

    tax_type_id: Mapped[int] = mapped_column(
        ForeignKey("TAX_TYPES.id"),
        nullable=False,
    )

    percentage: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    taxable_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    tax_amount: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )