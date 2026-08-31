import uuid
from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Project(Base):
    __tablename__ = "PROJECTS"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("USERS.id"),
        nullable=False,
    )

    project_code: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    project_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    site_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    client_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    client_contact: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    work_order_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    work_order_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
