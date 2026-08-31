"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


engine = (
    create_engine(
        settings.database_url
    )
    if settings.database_url
    else None
)


SessionLocal = (
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    if engine
    else None
)


class Base(DeclarativeBase):
    pass


def get_db():

    if SessionLocal is None:
        raise RuntimeError(
            "DATABASE_URL is not configured"
        )

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

        """


from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


if not settings.database_url:
    raise RuntimeError("DATABASE_URL is not configured")


engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()